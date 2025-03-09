import io
import logging
import os
import time
from typing import Optional

import humanize
from clients.minio import client
from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteObject
from minio.error import S3Error
from models.file import File

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Logs endpoint processing time

    Args:
        call_next: the endpoint to be called
        request (Request): params for the endpoint

    Returns:
        response (the relavant endpoint's response)
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"{request.client.host}:{request.client.port} - "
        f'"{request.method} {request.url.path} HTTP/{request.scope.get("http_version", "unknown")}" '
        f"took {humanize.naturaldelta(process_time, minimum_unit='milliseconds')}"
    )
    return response

@app.get("/workspaces/{workspace_id}/stat")
@app.get("/workspaces/{workspace_id}/stat/{path:path}")
async def stat(workspace_id: str, path: Optional[str] = "") -> list[File]:
    """
    Asynchronously retrieves the status of files in a specified workspace.

    Args:
      workspace_id (str): The ID of the workspace.
      path (Optional[str], optional): The path within the workspace. Defaults to "".

    Returns:
      list[File]: A list of File objects representing the files in the workspace.

    Raises:
      HTTPException: If the specified path is not found in the workspace.
    """

    try:
        objects = list(client.list_objects(workspace_id, prefix=path))
        return [File.from_minio_object(obj) for obj in objects]
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )

    # -- for a later date --
    # TODO: as well a listing of the files in the directory, we should also list
    #       the folders within the directory
    # TODO: Return a union list when listing i.e list[File|Folder] to tell the
    #       client what folders exist in the current path
    # TODO: Use the path option to filter files in a specific path of the bucket

    # TODO: Check user has read permission for workspace

@app.get("/workspaces/{workspace_id}/download/{path:path}")
async def download_file(workspace_id: str, path: str):
    """
    Asynchronously downloads a file from a specified workspace.

    Args:
      workspace_id (str): The ID of the workspace containing the file.
      path (str): The path of the file within the workspace.

    Returns:
      Response: A response containing the file content and appropriate headers.

    Raises:
      HTTPException: If the file is not found in the specified workspace.
    """
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    try:
        file_object = client.stat_object(workspace_id, path)
        response = client.get_object(workspace_id, path)
        file_content = b"".join(
            chunk for chunk in response.stream()
        )  # retrieves all chunks and combines them.
        filename = os.path.basename(path)  # gets the filename from the path.

        return Response(
            content=file_content,
            media_type=file_object.content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )


@app.post("/workspaces/{workspace_id}/upload")
@app.post("/workspaces/{workspace_id}/upload/{path:path}")
async def upload_file(
    workspace_id: str, files: list[UploadFile], path: Optional[str] = ""
):
    """
    Asynchronously uploads files to a specified workspace.

    Args:
      workspace_id (str): The ID of the workspace where the files will be uploaded.
      files (list[UploadFile]): A list of files to be uploaded.
      path (Optional[str], optional): The path within the workspace where the files will be uploaded. Defaults to "".

    Logs:
      Info: Logs the filename, size, and upload path for each uploaded file.
    """
    for file in files:
        upload_path = os.path.join(path, file.filename) if path else file.filename

        file_stream = io.BytesIO(await file.read())

        client.put_object(
            workspace_id,
            upload_path,
            file_stream,
            length=file.size,
            content_type=file.content_type,
        )

        logging.info(
            f"UPLOADED {file.filename} ({humanize.naturalsize(file.size)}) to {workspace_id}/{upload_path}"
        )


@app.delete(
    "/workspaces/{workspace_id}/remove/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_file(workspace_id: str, path: str):
    """
    Asynchronously deletes a file from a workspace.

    Args:
      workspace_id (str): The ID of the workspace containing the file.
      path (str): The path of the file within the workspace.

    Raises:
      HTTPException: If the file is not found in the specified workspace.

    Logs:
      Info: Logs the path of the file deleted from the specified workspace.
    """
    try:
        # Check if the file exists
        client.stat_object(workspace_id, path)
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )

    # Perform the deletion
    client.remove_object(workspace_id, path)
    logger.info(f"DELETED {path} from {workspace_id}")

    # -- for a later date --
    # TODO: Check user has write permission for workspace
    # see @stat()


@app.post("/workspaces/{workspace_id}/directory/{path:path}")
async def create_directory(workspace_id: str, path: str):
    """
    Asynchronously creates a directory in the specified workspace.

    Args:
      workspace_id (str): The ID of the workspace where the directory will be created.
      path (str): The path of the directory to be created within the workspace.

    Returns:
      dict: A message indicating the directory creation status.
    """
    empty_data = bytes()
    data_stream = io.BytesIO(empty_data)
    client.put_object(
        workspace_id,
        path + "/",
        data=data_stream,
        length=0,
    )
    return {"message": f"CREATED {path} in {workspace_id}"}


@app.delete(
    "/workspaces/{workspace_id}/directory/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_directory(workspace_id: str, path: str):
    """
    Asynchronously deletes an object from a workspace

    Args:
      workspace_id (str): The ID of the workspace containing the source file.
      path (str): The path of the source file within the workspace.

    Logs:
      Info: Logs the number of objects deleted from the specified workspace, and the total objects to delete
    """
    errors_count: int = 0

    objects = list((client.list_objects(workspace_id, prefix=path + "/")))

    errors = client.remove_objects(
        workspace_id,
        [DeleteObject(object.object_name) for object in objects],
    )

    logger.info(f"Added {len(objects)} objects to be removed")

    for error in errors:
        errors_count += 1
        logger.warning(
            f"Failed to delete object '{error.name}' with error code '{error.code}'."
        )

    if errors_count != 0:
        logger.warning(
            f"FAILED to delete {errors_count} object(s) from {path} in {workspace_id}"
        )

    logger.info(
        f"DELETED {len(objects) - errors_count} of {len(objects)} object(s) from {path} in {workspace_id}."
    )


@app.put(
    "/workspaces/{workspace_id}/cp/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def copy_file(
    workspace_id: str,
    path: str,
    target_path: str,
    target_workspace_id: Optional[str] = None,
):
    """
    Asynchronously copies a file from one workspace to another.

    Args:
      workspace_id (str): The ID of the workspace containing the source file.
      path (str): The path of the source file within the workspace.
      target_path (str): The path where the file should be copied to in the target workspace.
      target_workspace_id (Optional[str], optional): The ID of the target workspace. If not provided, defaults to the source workspace ID.

    Raises:
      HTTPException: If the source file is not found in the specified workspace.

    Logs:
      Info: Logs the source and target paths along with their respective workspace IDs after a successful copy operation.
    """
    target_workspace_id = (
        workspace_id if target_workspace_id is None else target_workspace_id
    )
    try:
        source = CopySource(workspace_id, path)
        client.copy_object(target_workspace_id, target_path, source)

    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    logger.info(
        f"Copied {path} in {workspace_id} TO {target_path} in {target_workspace_id}"
    )


@app.put(
    "/workspaces/{workspace_id}/mv/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def move_file(
    workspace_id: str,
    path: str,
    target_path: str,
    target_workspace_id: Optional[str] = None,
):
    """
    Asynchronously moves a file from one workspace to another - by cp then rm

    Args:
      workspace_id (str): The ID of the workspace containing the source file.
      path (str): The path of the source file within the workspace.
      target_path (str): The path where the file should be moved to in the target workspace.
      target_workspace_id (Optional[str], optional): The ID of the target workspace. If not provided, defaults to the source workspace ID.

    Raises:
      HTTPException: If the source file is not found in the specified workspace.

    Logs:
      Info: Logs the source and target paths along with their respective workspace IDs after a successful move operation.
    """
    target_workspace_id = (
        workspace_id if target_workspace_id is None else target_workspace_id
    )

    await copy_file(workspace_id, path, target_path, target_workspace_id)
    await delete_file(workspace_id, path)
    logger.info(
        f"Moved {path} in {workspace_id} TO {target_path} in {target_workspace_id}"
    )
