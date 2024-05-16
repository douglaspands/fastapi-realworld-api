from typing import Sequence

from server.core.context import Context
from server.core.exceptions import BusinessError
from server.models.people_model import People
from server.models.user_model import User
from server.repositories import people_repository, user_repository
from server.resources.user_resource import (
    CreateUserAndPeople,
    UpdateUser,
    UpdateUserOptional,
    UpdateUserPassword,
)
from server.services import auth_service


async def create_user_people(
    ctx: Context, user_people_create: CreateUserAndPeople
) -> User:
    people = await people_repository.get_or_create(
        session=ctx.session,
        people=People(
            first_name=user_people_create.first_name,
            last_name=user_people_create.last_name,
        ),
    )
    password_hash = auth_service.get_password_hash(user_people_create.password)
    user = await user_repository.create(
        session=ctx.session,
        user=User(
            username=user_people_create.username,
            password=password_hash,
            people_id=people.id,
        ),
    )
    return user


async def change_password(
    ctx: Context, user_id: int, update_password: UpdateUserPassword
) -> User:
    user = await user_repository.get(session=ctx.session, pk=user_id)
    if not auth_service.verify_password(
        update_password.current_password, user.password
    ):
        raise BusinessError("current password invalid")
    res = await user_repository.update(
        session=ctx.session, pk=user_id, password=update_password.new_password
    )
    return res


async def all_user(ctx: Context) -> Sequence[User]:
    user = await user_repository.get_all(ctx.session)
    return user


async def get_user(ctx: Context, pk: int) -> User:
    user = await user_repository.get(ctx.session, pk=pk)
    return user


async def update_user(ctx: Context, pk: int, update_user: UpdateUser) -> User:
    async with ctx.session.begin():
        values = update_user.model_dump()
        user = await user_repository.update(ctx.session, pk=pk, **values)
    return user


async def update_user_optional(
    ctx: Context, pk: int, update_user: UpdateUserOptional
) -> User:
    async with ctx.session.begin():
        values = update_user.model_dump(exclude_none=True)
        user = await user_repository.update(ctx.session, pk=pk, **values)
    return user


async def delete_user(ctx: Context, pk: int):
    async with ctx.session.begin():
        await user_repository.delete(ctx.session, pk=pk)


__all__ = (
    "create_user_people",
    "change_password",
    "all_user",
    "get_user",
    "update_user",
    "update_user_optional",
    "delete_user",
)
