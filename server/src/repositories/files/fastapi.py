import logging
from typing import Annotated

from fastapi import Depends
from src.repositories.files.base import FileRepository
from src.repositories.files.minio import MinioFileRepository

logger = logging.getLogger("uvicorn.error")


def get_file_repository():
    return MinioFileRepository(logger)


FileRepositoryDependency = Annotated[
    FileRepository,
    Depends(get_file_repository),
]
