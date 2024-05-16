from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response, status

from server.core.context import Context
from server.core.exceptions import NoContentError
from server.core.openapi import response_generator
from server.core.schema import ResponseOK
from server.enums.openapi_enum import OpenApiTagEnum
from server.resources.people_resources import (
    CreatePeople,
    People,
    UpdatePeople,
    UpdatePeopleOptional,
)
from server.services import people_service
from server.services.auth_service import check_access_token

router = APIRouter(
    prefix="/people",
    tags=[OpenApiTagEnum.PEOPLE],
)


@router.get(
    "/v1/people/{pk}",
    response_model=ResponseOK[People],
    status_code=status.HTTP_200_OK,
    responses=response_generator(401, 404, 500),
)
async def get_people(ctx: Annotated[Context, Depends(check_access_token)], pk: int):
    data = await people_service.get_people(ctx, pk=pk)
    return ResponseOK(data=data)


@router.get(
    "/v1/people",
    response_model=ResponseOK[Sequence[People]],
    status_code=status.HTTP_200_OK,
    responses=response_generator(204, 401, 500),
)
async def get_all_people(ctx: Annotated[Context, Depends(check_access_token)]):
    data = await people_service.all_people(ctx)
    if not data:
        raise NoContentError()
    return ResponseOK(data=data)


@router.post(
    "/v1/people",
    response_model=ResponseOK[People],
    status_code=status.HTTP_201_CREATED,
    responses=response_generator(400, 401, 422, 500),
)
async def create_people(
    ctx: Annotated[Context, Depends(check_access_token)], create_people: CreatePeople
):
    data = await people_service.create_people(ctx, create_people=create_people)
    return ResponseOK(data=data)


@router.put(
    "/v1/people/{pk}",
    response_model=ResponseOK[People],
    status_code=status.HTTP_200_OK,
    responses=response_generator(400, 401, 422, 500),
)
async def update_people(
    ctx: Annotated[Context, Depends(check_access_token)],
    pk: int,
    update_people: UpdatePeople,
):
    data = await people_service.update_people(ctx, pk=pk, update_people=update_people)
    return ResponseOK(data=data)


@router.patch(
    "/v1/people/{pk}",
    response_model=ResponseOK[People],
    status_code=status.HTTP_200_OK,
    responses=response_generator(400, 401, 422, 500),
)
async def update_people_optional(
    ctx: Annotated[Context, Depends(check_access_token)],
    pk: int,
    update_people: UpdatePeopleOptional,
):
    data = await people_service.update_people_optional(
        ctx, pk=pk, update_people=update_people
    )
    return ResponseOK(data=data)


@router.delete(
    "/v1/people/{pk}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses=response_generator(401, 404, 500),
)
async def delete_people(ctx: Annotated[Context, Depends(check_access_token)], pk: int):
    await people_service.delete_people(ctx, pk=pk)
    return


__all__ = ("router",)
