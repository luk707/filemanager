import http
import logging
import time
from typing import Optional

import humanize
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from minio.error import S3Error

from src.models.file import DirectoryListing
from src.repositories.files.fastapi import FileRepositoryDependency

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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="",
    description="",
)
@app.post(
    "/workspaces/{workspace_id}/upload/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Create a directory",
    description="Creates a directory in the specified workspace.",
)
async def create_directory(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    await file_repository.create_directory(workspace_id, path)


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
    await file_repository.delete_file(workspace_id, path)


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
    await file_repository.copy_file(
        workspace_id, path, target_path, target_workspace_id
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
    await file_repository.move_file(
        workspace_id, path, target_path, target_workspace_id
    )
