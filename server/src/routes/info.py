from fastapi import APIRouter

from src.configuration import ConfigurationDependency, ServerInfo

router = APIRouter()


@router.get("/info")
async def get_info(configuration: ConfigurationDependency) -> ServerInfo:
    return ServerInfo(
        organization_name=configuration.brand.organization_name,
    )
