import io
import logging
import os
from typing import Optional

import humanize
from clients.minio import client
from fastapi import UploadFile  # TODO: Remove FastAPI dependency
from models.file import DirectoryListing, directory_listing_from_object
from repositories.files.base import FileRepository


class MinioFileRepository(FileRepository):

    def __init__(self, logger: logging.Logger):
        self.logger = logger

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

    async def download_file(
        self, workspace_id: str, path: str
    ) -> tuple[str, bytes, str]:
        """
        Asynchronously downloads a file from a specified workspace.

        Args:
          workspace_id (str): The ID of the workspace containing the file.
          path (str): The path of the file within the workspace.

        Returns:
          tuple: A tuple containing the filename, file content, and content type.

        Raises:
          HTTPException: If the file is not found in the specified workspace.
        """

        file_object = client.stat_object(workspace_id, path)
        response = client.get_object(workspace_id, path)
        file_content = b"".join(chunk for chunk in response.stream())
        filename = os.path.basename(path)

        return (filename, file_content, file_object.content_type)

    async def upload_file(
        self,
        workspace_id: str,
        files: list[UploadFile],
        path: Optional[str] = "",
    ) -> None:
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

            self.logger.info(
                f"UPLOADED {file.filename} ({humanize.naturalsize(file.size)}) to {workspace_id}/{upload_path}"
            )

    async def create_directory(self, workspace_id: str, path: str) -> None:
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

    async def delete_directory(self, workspace_id: str, path: str) -> None:
        """
        Asynchronously deletes a directory and all contents within it from a workspace.

        Args:
          workspace_id (str): The ID of the workspace containing the source file.
          path (str): The path of the source file within the workspace.

        Logs:
          Info: Logs the number of objects deleted from the specified workspace, and the total objects to delete
        """
        errors_count: int = 0

        objects = list(client.list_objects(workspace_id, prefix=path + "/"))

        # Fix DeleteObject undefined - comes from parent?
        errors = client.remove_objects(
            workspace_id,
            [client.remove_object(workspace_id, obj.object_name) for obj in objects],
        )

        self.logger.info(f"Added {len(objects)} objects to be removed")

        for error in errors:
            errors_count += 1
            self.logger.warning(
                f"Failed to delete object '{error.name}' with error code '{error.code}'."
            )

        if errors_count != 0:
            self.logger.warning(
                f"FAILED to delete {errors_count} object(s) from {path} in {workspace_id}"
            )

        self.logger.info(
            f"DELETED {len(objects) - errors_count} of {len(objects)} object(s) from {path} in {workspace_id}."
        )

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
