import http
import logging
import time
from typing import Optional

import humanize
from clients.minio import client
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from minio.commonconfig import CopySource
from minio.error import S3Error

from src.clients.minio import client
from src.models.file import DirectoryListing

app = FastAPI()
logger = logging.getLogger("uvicorn.error")


def get_logger():
    return logger


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
        response (the relavant endpoint's response time in ms)
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


@app.get(
    "/ready",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Readiness Probe",
)
async def ready():
    """
    This endpoint returns a 204 No Content response to indicate that the service
    is running and ready to accept traffic.

    Example usage:
        GET /ready

    Response:
        204 No Content

    Typically used for Kubernetes or load balancer health checks.
    """
    pass


@app.get(
    "/workspaces/{workspace_id}/stat",
    summary="List workspace root",
    description="Returns a list of files and directories in the root of the workspace.",
)
@app.get(
    "/workspaces/{workspace_id}/stat/{path:path}",
    summary="List directory",
    description="Returns a list of files and directories in the specified directory.",
)
async def stat(
    file_repository: FileRepositoryDependency,
    workspace_id: str,
    path: Optional[str] = None,
) -> list[DirectoryListing]:
    try:
        return await file_repository.stat(workspace_id, path)
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )


@app.get(
    "/workspaces/{workspace_id}/download/{path:path}",
    summary="Download file",
    description="Downloads the specified file from the specified workspace.",
)
async def download_file(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    try:
        filename, file_content, content_type = await file_repository.download_file(
            workspace_id, path
        )

        return Response(
            content=file_content,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )


@app.post(
    "/workspaces/{workspace_id}/upload",
    summary="",
    description="",
)
@app.post(
    "/workspaces/{workspace_id}/upload/{path:path}",
    summary="Upload a file",
    description="Upload a file (BLOB) to the specified workspace and path.",
)
async def upload_file(
    file_repository: FileRepositoryDependency,
    workspace_id: str,
    files: list[UploadFile],
    path: Optional[str] = "",
):
    await file_repository.upload_file(
        workspace_id,
        files,
        path,
    )
    logger.info(f"Uploaded {len(files)} file(s) to {workspace_id}/{path}")
    return http.HTTPStatus.OK


@app.post(
    "/workspaces/{workspace_id}/directory/{path:path}",
    summary="Create a directory",
    description="Creates a directory in the specified workspace.",
)
async def create_directory(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    return {"message": f"CREATED {path} in {workspace_id}"}


@app.delete(
    "/workspaces/{workspace_id}/directory/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete directory",
    description="DESTRUCTIVE ACTION - Remove a directory and all of its contents - DESTRUCTIVE ACTION",
)
async def delete_directory(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    await file_repository.delete_directory(workspace_id, path)

@app.delete(
    "/workspaces/{workspace_id}/remove/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a file",
    description="DESTRUCTIVE ACTION - Deletes the specified file, in the specified workspace - DESTRUCTIVE ACTION",
)
async def delete_file(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
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


@app.put(
    "/workspaces/{workspace_id}/cp/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Copy a file",
    description="Copies a file from to another path, in the specified workspace.",
)
async def copy_file(
    file_repository: FileRepositoryDependency,
    workspace_id: str,
    path: str,
    target_path: str,
    target_workspace_id: Optional[str] = None,
):
    """
    Asynchronously copies a file from one location to another within the same workspace, or to another workspace.

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
    summary="Move file",
    description="Move a file to another path, in the specified workspace.",
)
async def move_file(
    file_repository: FileRepositoryDependency,
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
