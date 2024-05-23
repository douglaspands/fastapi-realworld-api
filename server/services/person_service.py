from typing import Sequence

from server.core.context import Context
from server.models.person_model import Person
from server.repositories import person_repository
from server.resources.person_resource import (
    CreatePerson,
    UpdatePerson,
    UpdatePersonOptional,
)


async def get_all_persons(ctx: Context) -> Sequence[Person]:
    person = await person_repository.get_all(ctx.session)
    return person


async def get_person(ctx: Context, person_id: int) -> Person:
    person = await person_repository.get(ctx.session, pk=person_id)
    return person


async def create_person(ctx: Context, create_person: CreatePerson) -> Person:
    async with ctx.session.begin():
        person = Person(
            first_name=create_person.first_name, last_name=create_person.last_name
        )
        await person_repository.create(ctx.session, person=person)
    return person


async def update_person(
    ctx: Context, person_id: int, update_person: UpdatePerson
) -> Person:
    async with ctx.session.begin():
        values = update_person.model_dump()
        person = await person_repository.update(ctx.session, pk=person_id, **values)
    return person


async def update_person_optional(
    ctx: Context, person_id: int, update_person: UpdatePersonOptional
) -> Person:
    async with ctx.session.begin():
        values = update_person.model_dump(exclude_none=True)
        person = await person_repository.update(ctx.session, pk=person_id, **values)
    return person


async def delete_person(ctx: Context, person_id: int):
    async with ctx.session.begin():
        await person_repository.delete(ctx.session, pk=person_id)


__all__ = (
    "get_person",
    "get_all_persons",
    "create_person",
    "update_person",
    "update_person_optional",
    "delete_person",
)
