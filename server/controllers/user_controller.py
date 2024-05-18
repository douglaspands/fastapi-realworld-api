from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response, status

from server.core.context import Context, get_context_with_request
from server.core.exceptions import NoContentError
from server.core.openapi import response_generator
from server.core.schema import ResponseOK
from server.enums.openapi_enum import OpenApiTagEnum
from server.resources.user_resource import (
    CreateUserPeople,
    UpdateUser,
    UpdateUserOptional,
    UpdateUserPassword,
    User,
)
from server.services import user_service
from server.services.auth_service import check_access_token

router = APIRouter(
    prefix="/users",
    tags=[OpenApiTagEnum.USER],
)


@router.post(
    "/v1/user-people",
    response_model=ResponseOK[User],
    status_code=status.HTTP_201_CREATED,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def create_user_and_people(
    ctx: Annotated[Context, Depends(get_context_with_request)],
    user_people_create: CreateUserPeople,
):
    data = await user_service.create_user_people(
        ctx=ctx, user_people_create=user_people_create
    )
    return ResponseOK(data=data)


@router.post(
    "/v1/users/{pk}/change-password",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def update_user_password(
    ctx: Annotated[Context, Depends(check_access_token)],
    pk: int,
    update_password: UpdateUserPassword,
):
    data = await user_service.change_password(
        ctx=ctx, pk=pk, update_password=update_password
    )
    return ResponseOK(data=data)


@router.get(
    "/v1/users/{pk}",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def get_user(ctx: Annotated[Context, Depends(check_access_token)], pk: int):
    data = await user_service.get_user(ctx, pk=pk)
    return ResponseOK(data=data)


@router.get(
    "/v1/users",
    response_model=ResponseOK[Sequence[User]],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_204_NO_CONTENT,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def get_all_users(ctx: Annotated[Context, Depends(check_access_token)]):
    data = await user_service.all_users(ctx)
    if not data:
        raise NoContentError()
    return ResponseOK(data=data)


@router.put(
    "/v1/users/{pk}",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def update_user(
    ctx: Annotated[Context, Depends(check_access_token)],
    pk: int,
    update_user: UpdateUser,
):
    data = await user_service.update_user(ctx, pk=pk, update_user=update_user)
    return ResponseOK(data=data)


@router.patch(
    "/v1/users/{pk}",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def update_user_optional(
    ctx: Annotated[Context, Depends(check_access_token)],
    pk: int,
    update_user: UpdateUserOptional,
):
    data = await user_service.update_user_optional(ctx, pk=pk, update_user=update_user)
    return ResponseOK(data=data)


@router.delete(
    "/v1/users/{pk}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses=response_generator(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def delete_user(ctx: Annotated[Context, Depends(check_access_token)], pk: int):
    await user_service.delete_user(ctx, pk=pk)
    return


__all__ = ("router",)
