from typing import Sequence

from fastapi import APIRouter, Depends, Response, status

from server.core.db import SessionIO, get_sessionio
from server.core.exceptions import NoContentError
from server.core.openapi import response_generator
from server.core.schema import ResponseOK
from server.resources.people_resources import (
    CreatePeople,
    People,
    UpdatePeople,
    UpdatePeopleOptional,
)
from server.services import people_service

router = APIRouter(
    prefix="/people",
    tags=["people"],
)


@router.get(
    "/v1/people/{pk}",
    response_model=ResponseOK[People],
    status_code=status.HTTP_200_OK,
    responses=response_generator(404, 500),
)
async def get_people(pk: int, session: SessionIO = Depends(get_sessionio)):
    data = await people_service.get_people(session=session, pk=pk)
    return ResponseOK(data=data)


@router.get(
    "/v1/people",
    response_model=ResponseOK[Sequence[People]],
    status_code=status.HTTP_200_OK,
    responses=response_generator(204, 500),
)
async def all_people(session: SessionIO = Depends(get_sessionio)):
    data = await people_service.all_people(session=session)
    if not data:
        raise NoContentError()
    return ResponseOK(data=data)


@router.post(
    "/v1/people",
    response_model=ResponseOK[People],
    status_code=status.HTTP_201_CREATED,
    responses=response_generator(400, 422, 500),
)
async def create_people(
    create_people: CreatePeople, session: SessionIO = Depends(get_sessionio)
):
    data = await people_service.create_people(
        session=session, create_people=create_people
    )
    return ResponseOK(data=data)


@router.put(
    "/v1/people/{pk}",
    response_model=ResponseOK[People],
    status_code=status.HTTP_200_OK,
    responses=response_generator(400, 422, 500),
)
async def update_people(
    pk: int, update_people: UpdatePeople, session: SessionIO = Depends(get_sessionio)
):
    data = await people_service.update_people(
        session=session, pk=pk, update_people=update_people
    )
    return ResponseOK(data=data)


@router.patch(
    "/v1/people/{pk}",
    response_model=ResponseOK[People],
    status_code=status.HTTP_200_OK,
    responses=response_generator(400, 422, 500),
)
async def update_people_optional(
    pk: int,
    update_people: UpdatePeopleOptional,
    session: SessionIO = Depends(get_sessionio),
):
    data = await people_service.update_people_optional(
        session=session, pk=pk, update_people=update_people
    )
    return ResponseOK(data=data)


@router.delete(
    "/v1/people/{pk}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses=response_generator(404, 500),
)
async def delete_people(pk: int, session: SessionIO = Depends(get_sessionio)):
    await people_service.delete_people(session=session, pk=pk)
    return


__all__ = ("router",)
