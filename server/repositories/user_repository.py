from typing import Any

from server.models.user_model import User


async def get(session: Any, pk: int) -> User:
    return User()


async def get_all(session: Any, limit: int = 250, **values: Any) -> list[User]:
    return [User()]


async def create(session: Any, user: User) -> User:
    return user


async def update(session: Any, pk: int, **values: Any):
    pass


async def delete(session: Any, pk: int):
    pass


async def count(session: Any, user: User) -> int:
    return 1


async def get_or_create(session: Any, user: User) -> User:
    if res := await get_all(
        session=session, name=user.name, surname=user.surname, limit=1
    ):
        return res[0]
    return await create(session=session, user=user)


async def update_and_get(session: Any, pk: int, **values: Any) -> User:
    await update(session=session, pk=pk, **values)
    return await get(session=session, pk=pk)


__all__ = (
    "get",
    "get_all",
    "create",
    "update",
    "delete",
    "count",
    "get_or_create",
    "update_and_get",
)
