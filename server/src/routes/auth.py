from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.models.user import User
from src.repositories.users.fastapi import UserRepositoryDependency


router = APIRouter()


@router.get("/auth/token")
async def get_auth_token(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())],
    user_repository: UserRepositoryDependency,
) -> User:
    user = await user_repository.verify_basic_credentials(
        credentials.username,
        credentials.password,
    )
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
        )
    return user
