from typing import Any, Sequence

from sqlmodel import select

from server.core import utils
from server.core.database import SessionIO
from server.models.person_model import Person


async def create(session: SessionIO, person: Person) -> Person:
    session.add(person)
    return person


async def get(session: SessionIO, pk: int) -> Person:
    statement = select(Person).where(Person.id == pk)
    result = await session.exec(statement)
    return result.one()


async def get_all(
    session: SessionIO, limit: int = 250, **values: Any
) -> Sequence[Person]:
    statement = select(Person).filter_by(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update(session: SessionIO, pk: int, **values: Any) -> Person:
    utils.repository_columns_can_update(values)
    person = await get(session=session, pk=pk)
    person.sqlmodel_update(values)
    session.add(person)
    return person


async def delete(session: SessionIO, pk: int):
    person = await get(session=session, pk=pk)
    await session.delete(person)


async def get_or_create(session: SessionIO, person: Person) -> Person:
    person_ = await get_all(
        session=session,
        limit=1,
        first_name=person.first_name,
        last_name=person.last_name,
    )
    if person_:
        return person_[0]
    return await create(session=session, person=person)


__all__ = (
    "get",
    "get_all",
    "create",
    "update",
    "delete",
    "get_or_create",
)
