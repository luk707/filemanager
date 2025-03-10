from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile  # TODO: Remove FastAPI dependency
from models.file import DirectoryListing


class FileRepository(ABC):
    @abstractmethod
    async def download_file(self, workspace_id: str, path: str) -> bytes: ...

    @abstractmethod
    async def stat(
        self, workspace_id: str, path: Optional[str] = None
    ) -> list[DirectoryListing]: ...

    @abstractmethod
    async def upload_file(
        self, workspace_id: str, files: list[UploadFile], path: Optional[str] = ""
    ) -> None: ...

    @abstractmethod
    async def create_directory(self, workspace_id: str, path: str) -> None: ...

    @abstractmethod
    async def delete_directory(self, workspace_id: str, path: str) -> None: ...

    @abstractmethod
    async def delete_file(self, workspace_id: str, path: str) -> None: ...

    @abstractmethod
    async def copy_file(
        self,
        workspace_id: str,
        path: str,
        target_path: str,
        target_workspace_id: Optional[str] = None,
    ) -> None: ...

    @abstractmethod
    async def move_file(
        self,
        workspace_id: str,
        path: str,
        target_path: str,
        target_workspace_id: Optional[str] = None,
    ) -> None: ...
