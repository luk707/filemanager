import mimetypes

from fastapi import APIRouter, Response

from src.repositories.users.fastapi import UserRepositoryDependency

router = APIRouter()


@router.get("/users")
async def get_users(
    user_repository: UserRepositoryDependency,
):
    return await user_repository.get_users()


@router.get("/users/{user_id}/avatar")
async def get_user_avatar(user_repository: UserRepositoryDependency, user_id: str):
    data, content_type = await user_repository.get_user_avatar(user_id)
    ext = mimetypes.guess_extension(content_type)
    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={user_id}{ext}"},
    )
