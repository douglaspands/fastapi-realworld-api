from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response, status

from server.core.context import Context, get_context
from server.core.exceptions import NoContentError
from server.core.openapi import response_generator
from server.core.schema import ResponseOK
from server.resources.user_resource import (
    CreateUserAndPeople,
    UpdateUser,
    UpdateUserOptional,
    UpdateUserPassword,
    User,
)
from server.services import user_service
from server.services.auth_service import check_access_token

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post(
    "/v1/users",
    response_model=ResponseOK[User],
    status_code=status.HTTP_201_CREATED,
    responses=response_generator(400, 422),
)
async def create_user_and_people(
    ctx: Annotated[Context, Depends(get_context)],
    user_people_create: CreateUserAndPeople,
):
    data = await user_service.create_user_people(
        ctx=ctx, user_people_create=user_people_create
    )
    return ResponseOK(data=data)


@router.post(
    "/v1/users/{pk}/change-password",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(400, 401, 422),
)
async def update_password(
    ctx: Annotated[Context, Depends(check_access_token)],
    pk: int,
    update_password: UpdateUserPassword,
):
    data = await user_service.change_password(
        ctx=ctx, user_id=pk, update_password=update_password
    )
    return ResponseOK(data=data)


@router.get(
    "/v1/users/{pk}",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(404, 500),
)
async def get_user(ctx: Annotated[Context, Depends(check_access_token)], pk: int):
    data = await user_service.get_user(ctx, pk=pk)
    return ResponseOK(data=data)


@router.get(
    "/v1/users",
    response_model=ResponseOK[Sequence[User]],
    status_code=status.HTTP_200_OK,
    responses=response_generator(204, 500),
)
async def all_users(ctx: Annotated[Context, Depends(check_access_token)]):
    data = await user_service.all_user(ctx)
    if not data:
        raise NoContentError()
    return ResponseOK(data=data)


@router.put(
    "/v1/users/{pk}",
    response_model=ResponseOK[User],
    status_code=status.HTTP_200_OK,
    responses=response_generator(400, 422, 500),
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
    responses=response_generator(400, 422, 500),
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
    responses=response_generator(404, 500),
)
async def delete_user(ctx: Annotated[Context, Depends(check_access_token)], pk: int):
    await user_service.delete_user(ctx, pk=pk)
    return


__all__ = ("router",)
