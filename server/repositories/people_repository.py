from typing import Any, Sequence

from sqlmodel import select

from server.core.db import SessionIO
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


# async def update(session: SessionIO, pk: int, **values: Any):
#     pass


# async def delete(session: SessionIO, pk: int):
#     pass


# async def count(session: SessionIO, user: User) -> int:
#     return 1


# async def get_or_create(session: SessionIO, user: User) -> User:
#     if res := await get_all(
#         session=session, name=user.name, surname=user.surname, limit=1
#     ):
#         return res[0]
#     return await create(session=session, user=user)


# async def update_and_get(session: SessionIO, pk: int, **values: Any) -> User:
#     await update(session=session, pk=pk, **values)
#     return await get(session=session, pk=pk)


__all__ = (
    "get",
    "get_all",
    "create",
    # "update",
    # "delete",
    # "count",
    # "get_or_create",
    # "update_and_get",
)
