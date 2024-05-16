from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from server.core.context import Context, get_context
from server.core.openapi import response_generator
from server.resources.token_resource import Token
from server.services import auth_service

router = APIRouter(
    prefix="/token",
    tags=["token"],
)


@router.post(
    "/v1/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses=response_generator(401),
    # include_in_schema=False,
)
async def get_token(
    ctx: Annotated[Context, Depends(get_context)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    data = await auth_service.authenticate_user(
        ctx, username=form_data.username, password=form_data.password
    )
    return data


__all__ = ("router",)
