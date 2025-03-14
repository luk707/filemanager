import mimetypes

from fastapi import (
    Response,
    FastAPI,
    status,
)
from fastapi.middleware.cors import CORSMiddleware

from src.routes.file import router as file_router
from src.repositories.users.fastapi import UserRepositoryDependency
from src.configuration import ConfigurationDependency, ServerInfo

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(file_router)


@app.get(
    "/ready",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Readiness Probe",
)
async def ready():
    """
    This endpoint returns a 204 No Content response to indicate that the service
    is running and ready to accept traffic.

    Example usage:
        GET /ready

    Response:
        204 No Content

    Typically used for Kubernetes or load balancer health checks.
    """
    pass


@app.get("/info")
async def get_info(configuration: ConfigurationDependency) -> ServerInfo:
    return ServerInfo(
        organization_name=configuration.brand.organization_name,
    )


@app.get("/users")
async def get_users(
    user_repository: UserRepositoryDependency,
):
    return await user_repository.get_users()


@app.get("/users/{user_id}/avatar")
async def get_user_avatar(user_repository: UserRepositoryDependency, user_id: str):
    data, content_type = await user_repository.get_user_avatar(user_id)
    ext = mimetypes.guess_extension(content_type)
    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={user_id}{ext}"},
    )
