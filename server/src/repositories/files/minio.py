from typing import Optional

from clients.minio import client
from fastapi import UploadFile  # TODO: Remove FastAPI dependency
from models.file import DirectoryListing, directory_listing_from_object
from repositories.files.base import FileRepository


class MinioFileRepository(FileRepository):

    async def download_file(self, workspace_id: str, path: str) -> bytes:
        pass

    async def stat(
        self, workspace_id: str, path: Optional[str] = None
    ) -> list[DirectoryListing]:
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

        objects = list(
            client.list_objects(
                workspace_id, prefix=f"{path}/" if path is not None else None
            )
        )
        return [
            directory_listing_from_object(obj)
            for obj in objects
            if obj.object_name != f"{path}/"
        ]

        # -- for a later date --
        # TODO: as well a listing of the files in the directory, we should also list
        #       the folders within the directory
        # TODO: Return a union list when listing i.e list[File|Folder] to tell the
        #       client what folders exist in the current path
        # TODO: Use the path option to filter files in a specific path of the bucket

        # TODO: Check user has read permission for workspace

    async def upload_file(
        self, workspace_id: str, files: list[UploadFile], path: Optional[str] = ""
    ) -> None:
        pass

    async def create_directory(self, workspace_id: str, path: str) -> None:
        pass

    async def delete_directory(self, workspace_id: str, path: str) -> None:
        pass

    async def delete_file(self, workspace_id: str, path: str) -> None:
        pass

    async def copy_file(
        self,
        workspace_id: str,
        path: str,
        target_path: str,
        target_workspace_id: Optional[str] = None,
    ) -> None:
        pass

    async def move_file(
        self,
        workspace_id: str,
        path: str,
        target_path: str,
        target_workspace_id: Optional[str] = None,
    ) -> None:
        pass
