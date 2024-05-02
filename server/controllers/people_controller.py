from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter, Depends

from server.core.db import SessionIO, get_sessionio
from server.core.schemas import ResponseOK
from server.resources.people_resources import CreatePeople, People
from server.services import people_service

router = APIRouter(
    prefix="/people",
    tags=["people"],
)


@router.get("/v1/people/{pk}", response_model=ResponseOK[People])
async def get_people(pk: int, session: SessionIO = Depends(get_sessionio)):
    data = await people_service.get_people(session=session, pk=pk)
    return ResponseOK(data=data)


@router.get("/v1/people", response_model=ResponseOK[Sequence[People]])
async def all_people(session: SessionIO = Depends(get_sessionio)):
    data = await people_service.all_people(session=session)
    return ResponseOK(data=data)


@router.post(
    "/v1/people", response_model=ResponseOK[People], status_code=HTTPStatus.CREATED
)
async def create_people(
    create_people: CreatePeople, session: SessionIO = Depends(get_sessionio)
):
    data = await people_service.create_people(
        session=session, create_people=create_people
    )
    return ResponseOK(data=data)


# @router.put("/v1/users/{pk}", response_model=User)
# async def update_user(pk: int):
#     return await user_service.get_users()


# @router.delete("/v1/users/{pk}")
# async def remove_user(pk: int):
#     await user_service.get_users()


__all__ = ("router",)
