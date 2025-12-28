from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

from app.enums.openapi_enum import OpenApiTagEnum
from app.infra.database import ping_database

router = APIRouter(
    prefix="/health",
    tags=[OpenApiTagEnum.HEALTH],
)


@router.get(
    "/v1/readness",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
)
async def health_readness():
    return "OK"


@router.get(
    "/v1/liveness",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
)
async def health_liveness():
    await ping_database()
    return "OK"


__all__ = ("router",)
