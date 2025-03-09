import io
import logging
import os
import time
from typing import Optional

import humanize
from clients.minio import client
from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/workspaces/{workspace_id}/stat")
@app.get("/workspaces/{workspace_id}/stat/{path:path}")
async def stat(workspace_id: str, path: Optional[str] = "") -> list[File]:

    if path:
        try:
            response = [
                File.from_minio_object(obj)
                for obj in client.list_objects(workspace_id)
                if obj.object_name == path
            ]
            if response == []:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
                )
            return [
                File.from_minio_object(obj)
                for obj in client.list_objects(workspace_id)
                if obj.object_name == path
            ]
        except S3Error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
            )

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

    # is this not moot? it'll be handled by whatever access keygiven to the  client; no? @see clients/minio.py


@app.get("/workspaces/{workspace_id}/download/{path:path}")
async def download_file(workspace_id: str, path: str):
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    try:
        object = client.stat_object(workspace_id, path)
        response = client.get_object(workspace_id, path)
        file_content = b"".join(
            chunk for chunk in response.stream()
        )  # retrieves all chunks and combines them.
        filename = os.path.basename(path)  # gets the filename from the path.

        return Response(
            content=file_content,
            media_type=object.content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )

@app.post("/workspaces/{workspace_id}/upload")
@app.post("/workspaces/{workspace_id}/upload/{directory_path:path}")
async def upload_file(workspace_id: str, files: list[UploadFile], directory_path: Optional[str] = ""):
    # Loop through each file in the list of files
    for file in files:
        path = (
            os.path.join(directory_path, file.filename)
            if directory_path
            else file.filename
        )

        file_stream = io.BytesIO(await file.read())

        client.put_object(
            workspace_id,
            path,
            file_stream,
            length=file.size,
            content_type=file.content_type,
        )

        logging.info(
            f"UPLOADED {file.filename} ({humanize.naturalsize(file.size)}) to {workspace_id}/{path}"
        )


# delete file
@app.delete("/workspaces/{workspace_id}/remove/{path:path}")
async def delete_file(workspace_id: str, path: str):
    # TODO: Implement logic to delete files from a workspace
    # 1. check that the file path is a valid path to a file or folder
    try:
        client.stat_object(workspace_id, path)
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    # 2. perform the deletion logic

    client.remove_object(workspace_id, path)
    return {"message": f"DELETED {path} from {workspace_id}"}

    # -- for a later date --
    # TODO: Check user has write permission for workspace
    # see @stat()


@app.post("/workspaces/{workspace_id}/directory/{directory_path}")
async def create_directory(workspace_id: str, directory_path: str):
    empty_data = bytes()
    data_stream = io.BytesIO(empty_data)
    client.put_object(
        workspace_id,
        directory_path + "/",
        data=data_stream,
        length=0,
    )
    return {"message": f"CREATED {directory_path} in {workspace_id}"}


@app.delete(
    "/workspaces/{workspace_id}/directory/{directory_path}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_directory(workspace_id: str, directory_path: str):
    errors_count: int = 0
    del_list: list[str] = []

    objects = list((client.list_objects(workspace_id, prefix=directory_path + "/")))

    for i in objects:
        logger.debug(f"Adding {i.object_name} to delete list")
        del_list.append(DeleteObject(i.object_name))
    errors = client.remove_objects(
        workspace_id,
        del_list,
    )

    logger.info(f"Added {len(del_list)} objects to be removed")

    for error in errors:
        errors_count += 1
        logger.warning(
            f"Failed to delete object '{error.name}' with error code '{error.code}'."
        )

    if errors_count != 0:
        logger.warning(
            f"FAILED to delete {errors_count} object(s) from {directory_path} in {workspace_id}"
        )

    logger.info(
        f"DELETED {len(del_list) - errors_count} of {len(del_list)} object(s) from {directory_path} in {workspace_id}."
    )
