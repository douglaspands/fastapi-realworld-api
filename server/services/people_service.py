from typing import Sequence

from server.core.context import Context
from server.models.people_model import People
from server.repositories import people_repository
from server.resources.people_resources import (
    CreatePeople,
    UpdatePeople,
    UpdatePeopleOptional,
)


async def all_people(ctx: Context) -> Sequence[People]:
    people = await people_repository.get_all(ctx.session)
    return people


async def get_people(ctx: Context, pk: int) -> People:
    people = await people_repository.get(ctx.session, pk=pk)
    return people


async def create_people(ctx: Context, create_people: CreatePeople) -> People:
    async with ctx.session.begin():
        people = People(
            first_name=create_people.first_name, last_name=create_people.last_name
        )
        await people_repository.create(ctx.session, people=people)
    return people


async def update_people_optional(
    ctx: Context, pk: int, update_people: UpdatePeopleOptional
) -> People:
    async with ctx.session.begin():
        values = update_people.model_dump(exclude_none=True)
        people = await people_repository.update(ctx.session, pk=pk, **values)
    return people


async def update_people(ctx: Context, pk: int, update_people: UpdatePeople) -> People:
    async with ctx.session.begin():
        values = update_people.model_dump()
        people = await people_repository.update(ctx.session, pk=pk, **values)
    return people


async def delete_people(ctx: Context, pk: int):
    async with ctx.session.begin():
        await people_repository.delete(ctx.session, pk=pk)
