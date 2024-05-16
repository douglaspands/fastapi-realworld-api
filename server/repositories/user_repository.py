from typing import Any, Sequence

from sqlmodel import select

from server.core import utils
from server.core.database import SessionIO
from server.models.user_model import User


async def create(session: SessionIO, user: User) -> User:
    session.add(user)
    return user


async def get(session: SessionIO, pk: int) -> User:
    statement = select(User).where(User.id == pk)
    result = await session.exec(statement)
    return result.one()


async def get_all(
    session: SessionIO, limit: int = 250, **values: Any
) -> Sequence[User]:
    statement = select(User).filter_by(**values).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update(session: SessionIO, pk: int, **values: Any) -> User:
    utils.repository_columns_can_update(values)
    user = await get(session=session, pk=pk)
    user.sqlmodel_update(values)
    session.add(user)
    return user


async def delete(session: SessionIO, pk: int):
    user = await get(session=session, pk=pk)
    await session.delete(user)


__all__ = (
    "get",
    "get_all",
    "create",
    "update",
    "delete",
)
