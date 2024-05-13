from typing import Any, Sequence

from sqlmodel import select

from server.core.database import SessionIO
from server.models.people_model import People


async def create(session: SessionIO, people: People):
    session.add(people)


async def get(session: SessionIO, pk: int) -> People:
    statement = select(People).where(People.id == pk)
    result = await session.exec(statement)
    return result.one()


async def get_all(
    session: SessionIO, limit: int = 250, **values: Any
) -> Sequence[People]:
    statement = select(People).where(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update(session: SessionIO, pk: int, **values: Any) -> People:
    values.pop("id", None)
    people = await get(session=session, pk=pk)
    people.sqlmodel_update(values)
    session.add(people)
    return people


async def delete(session: SessionIO, pk: int):
    people = await get(session=session, pk=pk)
    await session.delete(people)


__all__ = (
    "get",
    "get_all",
    "create",
    "update",
    "delete",
)
