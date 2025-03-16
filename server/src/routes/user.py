import mimetypes

from fastapi import APIRouter, Response, HTTPException, status

from src.dependencies.user import UserDependency
from src.models.user import User
from src.repositories.users.fastapi import UserRepositoryDependency

router = APIRouter()


@router.get("/users")
async def get_users(
    user: UserDependency,
    user_repository: UserRepositoryDependency,
) -> list[User]:
    # TODO: Check user has permission to list all users
    return await user_repository.get_users()


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_repository: UserRepositoryDependency,
    user_id: str,
) -> User:
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


@router.get("/users/{user_id}/avatar")
async def get_user_avatar(
    user_repository: UserRepositoryDependency,
    user_id: str,
):
    data, content_type = await user_repository.get_user_avatar(user_id)
    ext = mimetypes.guess_extension(content_type)
    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={user_id}{ext}"},
    )
