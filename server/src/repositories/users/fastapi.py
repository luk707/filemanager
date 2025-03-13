import logging
from typing import Annotated
from fastapi import Depends
from src.repositories.users.base import UserRepository
from src.repositories.users.ldap import LDAPUserRepository
from src.configuration import (
    ConfigurationDependency,
    LDAPIdentityBackendConfiguration,
)

logger = logging.getLogger("uvicorn.error")


def get_user_repository(
    configuration: ConfigurationDependency,
):
    match configuration.identity_backend:
        case LDAPIdentityBackendConfiguration(
            host=host,
            port=port,
            attributes=attributes,
        ):
            from ldap3 import Server

            return LDAPUserRepository(
                Server(
                    host=host,
                    port=port,
                    get_info="ALL",
                ),
                attributes,
                logger,
            )


UserRepositoryDependency = Annotated[
    UserRepository,
    Depends(get_user_repository),
]
