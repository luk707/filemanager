from typing import Annotated

from fastapi import Depends
from repositories.files.base import FileRepository
from repositories.files.minio import MinioFileRepository


def get_file_repository():
    return MinioFileRepository()


FileRepositoryDependency = Annotated[FileRepository, Depends(get_file_repository)]
