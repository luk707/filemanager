from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt

from src.repositories.users.fastapi import UserRepositoryDependency
from src.configuration import ConfigurationDependency


router = APIRouter()


@router.get(
    "/auth/token",
    status_code=status.HTTP_200_OK,
    summary="Get an authentication token",
    description="Creates a new signed JWT from the users credentials.",
)
async def get_auth_token(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    configuration: ConfigurationDependency,
    user_repository: UserRepositoryDependency,
) -> str:
    user = await user_repository.verify_basic_credentials(
        credentials.username,
        credentials.password,
    )
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
        )

    return jwt.encode(
        {"iat": datetime.now(tz=timezone.utc), "sub": user.id},
        configuration.identity.jwt_secret.get_secret_value(),
        algorithm="HS256",
    )
