from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response, status

from server.core.context import Context, get_context_with_request
from server.core.exceptions import NoContentError
from server.core.openapi import response_generator
from server.core.schema import ResponseOK
from server.enums.openapi_enum import OpenApiTagEnum
from server.resources.user_resource import (
    CreateUserPerson,
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
    "/v1/user-person",
    response_model=ResponseOK[User],
    status_code=status.HTTP_201_CREATED,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def create_user_and_person(
    ctx: Annotated[Context, Depends(get_context_with_request)],
    user_person_create: CreateUserPerson,
):
    data = await user_service.create_user_person(
        ctx=ctx, user_person_create=user_person_create
    )
    return ResponseOK(data=data)


@router.post(
    "/v1/users/{user_id}/change-password",
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
    user_id: int,
    update_password: UpdateUserPassword,
):
    data = await user_service.change_password(
        ctx=ctx, user_id=user_id, update_password=update_password
    )
    return ResponseOK(data=data)


@router.get(
    "/v1/users/{user_id}",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def get_user(ctx: Annotated[Context, Depends(check_access_token)], user_id: int):
    data = await user_service.get_user(ctx, user_id=user_id)
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
    data = await user_service.get_all_users(ctx)
    if not data:
        raise NoContentError()
    return ResponseOK(data=data)


@router.put(
    "/v1/users/{user_id}",
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
    user_id: int,
    update_user: UpdateUser,
):
    data = await user_service.update_user(ctx, user_id=user_id, update_user=update_user)
    return ResponseOK(data=data)


@router.patch(
    "/v1/users/{user_id}",
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
    user_id: int,
    update_user: UpdateUserOptional,
):
    data = await user_service.update_user_optional(
        ctx, user_id=user_id, update_user=update_user
    )
    return ResponseOK(data=data)


@router.delete(
    "/v1/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses=response_generator(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def delete_user(
    ctx: Annotated[Context, Depends(check_access_token)], user_id: int
):
    await user_service.delete_user(ctx, user_id=user_id)
    return


__all__ = ("router",)
