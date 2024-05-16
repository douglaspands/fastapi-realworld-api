from typing import Any, Sequence

from sqlmodel import select

from server.core import utils
from server.core.database import SessionIO
from server.models.people_model import People


async def create(session: SessionIO, people: People) -> People:
    session.add(people)
    return people


async def get(session: SessionIO, pk: int) -> People:
    statement = select(People).where(People.id == pk)
    result = await session.exec(statement)
    return result.one()


async def get_all(
    session: SessionIO, limit: int = 250, **values: Any
) -> Sequence[People]:
    statement = select(People).filter_by(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update(session: SessionIO, pk: int, **values: Any) -> People:
    utils.repository_columns_can_update(values)
    people = await get(session=session, pk=pk)
    people.sqlmodel_update(values)
    session.add(people)
    return people


async def delete(session: SessionIO, pk: int):
    people = await get(session=session, pk=pk)
    await session.delete(people)


async def get_or_create(session: SessionIO, people: People) -> People:
    people_ = await get_all(
        session=session,
        limit=1,
        first_name=people.first_name,
        last_name=people.last_name,
    )
    if people_:
        return people_[0]
    return await create(session=session, people=people)


__all__ = (
    "get",
    "get_all",
    "create",
    "update",
    "delete",
    "get_or_create",
)
