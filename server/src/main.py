import time

import humanize
from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware

from src.repositories.logger import LoggerDependency

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


@app.middleware("http")
async def add_process_time_header(
    request: Request,
    logger: LoggerDependency,
    call_next,
):
    """Logs endpoint processing time

    Args:
        call_next: the endpoint to be called
        request (Request): params for the endpoint

    Returns:
        response (the relavant endpoint's response time in ms)
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"{request.client.host}:{request.client.port} - "
        f'"{request.method} {request.url.path} HTTP/{request.scope.get("http_version", "unknown")}" '
        f"took {humanize.naturaldelta(process_time, minimum_unit='milliseconds')}"
    )
    return response


app.include_router()

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
