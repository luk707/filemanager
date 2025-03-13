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
        case MinioStorageBackendConfiguration(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        ):
            from minio import Minio

            client = Minio(
                endpoint=endpoint,
                access_key=access_key.get_secret_value()
                if access_key is not None
                else None,
                secret_key=secret_key.get_secret_value()
                if secret_key is not None
                else None,
                secure=secure,
            )
            return MinioFileRepository(client, logger)
        case _:
            raise Exception("Unsupported storage backend type")


FileRepositoryDependency = Annotated[
    FileRepository,
    Depends(get_file_repository),
]
