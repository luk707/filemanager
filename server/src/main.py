from fastapi import (
    FastAPI,
    status,
)
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import router as auth_router
from src.routes.file import router as file_router
from src.routes.info import router as info_router
from src.routes.user import router as user_router

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


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(info_router)
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
