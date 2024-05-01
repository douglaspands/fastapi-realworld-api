from typing import Any

from sqlmodel import select
from server.core.db import AsyncSession
from server.models.user_model import User


async def get_all(session: AsyncSession, limit: int = 250, **values: Any) -> list[User]:
    statement = select(User).where(**values).limit(limit)
    result = await session.execute(statement)
    users = result.scalars().all()
    return users


# async def get(session: AsyncSession, pk: int) -> User:
#     return User()


# async def create(session: AsyncSession, user: User) -> User:
#     return user


# async def update(session: AsyncSession, pk: int, **values: Any):
#     pass


# async def delete(session: AsyncSession, pk: int):
#     pass


# async def count(session: AsyncSession, user: User) -> int:
#     return 1


# async def get_or_create(session: AsyncSession, user: User) -> User:
#     if res := await get_all(
#         session=session, name=user.name, surname=user.surname, limit=1
#     ):
#         return res[0]
#     return await create(session=session, user=user)


# async def update_and_get(session: AsyncSession, pk: int, **values: Any) -> User:
#     await update(session=session, pk=pk, **values)
#     return await get(session=session, pk=pk)


__all__ = (
    # "get",
    "get_all",
    # "create",
    # "update",
    # "delete",
    # "count",
    # "get_or_create",
    # "update_and_get",
)
