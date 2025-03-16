from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.models.user import User
from src.repositories.users.fastapi import UserRepositoryDependency

security = HTTPBearer()


async def get_user(
    user_repo: UserRepositoryDependency,
    auth: HTTPAuthorizationCredentials = Security(security),
) -> User:
    token = auth.credentials
    user = await user_repo.verify_token(token)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )
    return user


UserDependency = Annotated[
    User,
    Depends(get_user),
]
