import logging
from typing import Annotated

from fastapi import Depends
from src.repositories.files.base import FileRepository
from src.repositories.files.minio import MinioFileRepository
from src.configuration import (
    ConfigurationDependency,
    MinioStorageBackendConfiguration,
)

logger = logging.getLogger("uvicorn.error")


def get_file_repository(
    configuration: ConfigurationDependency,
):
    match configuration.storage_backend:
        case MinioStorageBackendConfiguration() as config:
            return MinioFileRepository(config, logger)
        case _:
            raise Exception("Unsupported storage backend type")


FileRepositoryDependency = Annotated[
    FileRepository,
    Depends(get_file_repository),
]
