from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Response, status

from server.core.context import Context
from server.core.exceptions import NoContentError
from server.core.openapi import response_generator
from server.core.schema import ResponseOK
from server.enums.openapi_enum import OpenApiTagEnum
from server.resources.person_resource import (
    CreatePerson,
    Person,
    UpdatePerson,
    UpdatePersonOptional,
)
from server.services import person_service
from server.services.auth_service import check_access_token

router = APIRouter(
    prefix="/persons",
    tags=[OpenApiTagEnum.PERSON],
)


@router.get(
    "/v1/persons/{person_id}",
    response_model=ResponseOK[Person],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def get_person(
    ctx: Annotated[Context, Depends(check_access_token)], person_id: int
):
    data = await person_service.get_person(ctx, person_id=person_id)
    return ResponseOK(data=data)


@router.get(
    "/v1/persons",
    response_model=ResponseOK[Sequence[Person]],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_204_NO_CONTENT,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def get_all_person(ctx: Annotated[Context, Depends(check_access_token)]):
    data = await person_service.get_all_persons(ctx)
    if not len(data):
        raise NoContentError()
    return ResponseOK(data=data)


@router.post(
    "/v1/persons",
    response_model=ResponseOK[Person],
    status_code=status.HTTP_201_CREATED,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def create_person(
    ctx: Annotated[Context, Depends(check_access_token)], create_person: CreatePerson
):
    data = await person_service.create_person(ctx, create_person=create_person)
    return ResponseOK(data=data)


@router.put(
    "/v1/persons/{person_id}",
    response_model=ResponseOK[Person],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def update_person(
    ctx: Annotated[Context, Depends(check_access_token)],
    person_id: int,
    update_person: UpdatePerson,
):
    data = await person_service.update_person(
        ctx, person_id=person_id, update_person=update_person
    )
    return ResponseOK(data=data)


@router.patch(
    "/v1/persons/{person_id}",
    response_model=ResponseOK[Person],
    status_code=status.HTTP_200_OK,
    responses=response_generator(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def update_person_optional(
    ctx: Annotated[Context, Depends(check_access_token)],
    person_id: int,
    update_person: UpdatePersonOptional,
):
    data = await person_service.update_person_optional(
        ctx, person_id=person_id, update_person=update_person
    )
    return ResponseOK(data=data)


@router.delete(
    "/v1/persons/{person_id}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses=response_generator(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
)
async def delete_person(
    ctx: Annotated[Context, Depends(check_access_token)], person_id: int
):
    await person_service.delete_person(ctx, person_id=person_id)
    return


__all__ = ("router",)
