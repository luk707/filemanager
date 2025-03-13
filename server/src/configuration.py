from pydantic import BaseModel, ConfigDict, Field, SecretStr
from enum import Enum
from typing import Annotated, Literal, Union
from functools import lru_cache
import toml
from fastapi import Depends


def to_kebab(snake: str) -> str:
    """Convert a snake_case string to kebab-case

    Args:
        snake: The string to convert.

    Returns:
        The converted kebab-case string.
    """
    return snake.replace("_", "-")


class StorageBackendProvider(str, Enum):
    MINIO = "minio"


class MinioStorageBackendConfiguration(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )
    provider: Literal[StorageBackendProvider.MINIO] = StorageBackendProvider.MINIO

    endpoint: str
    access_key: SecretStr | None = None
    secret_key: SecretStr | None = None
    secure: bool = True


StorageBackendConfiguration = Annotated[
    Union[MinioStorageBackendConfiguration],
    Field(discriminator="provider"),
]


class IdentityBackendProvider(str, Enum):
    LDAP = "ldap"


class LDAPIdentityBackendConfiguration(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )
    provider: Literal[IdentityBackendProvider.LDAP] = IdentityBackendProvider.LDAP
    host: str
    port: int
    base_dn: str
    user_filter: str
    bind_dn: str
    bind_password: SecretStr
    attribute_map: dict[str, str]


IdentityBackendConfiguration = Annotated[
    Union[LDAPIdentityBackendConfiguration],
    Field(discriminator="provider"),
]


class Configuration(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )

    identity_backend: IdentityBackendConfiguration
    storage_backend: StorageBackendConfiguration


@lru_cache
def get_configuration() -> Configuration:
    with open("config.toml", "r") as f:
        return Configuration(**toml.load(f))


ConfigurationDependency = Annotated[
    Configuration,
    Depends(get_configuration),
]
