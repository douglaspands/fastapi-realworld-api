from typing import Sequence

from server.core.db import SessionIO
from server.models.people_model import People
from server.repositories import people_repository
from server.resources.people_resources import CreatePeople


async def all_people(session: SessionIO) -> Sequence[People]:
    people = await people_repository.get_all(session=session)
    return people


async def get_people(session: SessionIO, pk: int) -> People:
    people = await people_repository.get(session=session, pk=pk)
    return people


async def create_people(session: SessionIO, create_people: CreatePeople) -> People:
    async with session.begin():
        people = People(
            first_name=create_people.first_name, last_name=create_people.last_name
        )
        await people_repository.create(session=session, people=people)
    return people
