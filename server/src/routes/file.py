import http
from typing import Optional

from fastapi import (
    APIRouter,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from minio.error import S3Error
from src.models.file import DirectoryListing
from src.repositories.files.fastapi import FileRepositoryDependency

from server.src.repositories.logger import LoggerDependency

router = APIRouter()


@router.get(
    "/workspaces/{workspace_id}/stat",
    summary="List workspace root",
    description="Returns a list of files and directories in the root of the workspace.",
)
@router.get(
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


@router.get(
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


@router.post(
    "/workspaces/{workspace_id}/upload",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="",
    description="",
)
@router.post(
    "/workspaces/{workspace_id}/upload/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Upload a file",
    description="Upload a file (BLOB) to the specified workspace and path.",
)
async def upload_file(
    file_repository: FileRepositoryDependency,
    logger: LoggerDependency,
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


@router.post(
    "/workspaces/{workspace_id}/directory/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Create a directory",
    description="Creates a directory in the specified workspace.",
)
async def create_directory(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    await file_repository.create_directory(workspace_id, path)


@router.delete(
    "/workspaces/{workspace_id}/directory/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete directory",
    description="DESTRUCTIVE ACTION - Remove a directory and all of its contents - DESTRUCTIVE ACTION",
)
async def delete_directory(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    await file_repository.delete_directory(workspace_id, path)


@router.delete(
    "/workspaces/{workspace_id}/remove/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a file",
    description="DESTRUCTIVE ACTION - Deletes the specified file, in the specified workspace - DESTRUCTIVE ACTION",
)
async def delete_file(
    file_repository: FileRepositoryDependency, workspace_id: str, path: str
):
    await file_repository.delete_file(workspace_id, path)


@router.put(
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


@router.put(
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
