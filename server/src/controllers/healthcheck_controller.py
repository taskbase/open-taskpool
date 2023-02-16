from fastapi import APIRouter
from models.api_models import HealthStatus

router = APIRouter()


@router.get(
    "/healthcheck",
    tags=["Metadata"],
    response_model=HealthStatus
)
async def healthcheck() -> HealthStatus:
    return HealthStatus(
        healthy=True,
        status="Up and running!"
    )
