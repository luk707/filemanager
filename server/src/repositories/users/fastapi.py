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
        case LDAPIdentityBackendConfiguration() as ldap_configuration:
            return LDAPUserRepository(
                ldap_configuration,
                logger,
            )


UserRepositoryDependency = Annotated[
    UserRepository,
    Depends(get_user_repository),
]
