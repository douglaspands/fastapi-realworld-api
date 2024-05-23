from typing import Sequence

from server.core.context import Context
from server.core.crypt import get_crypt
from server.core.exceptions import BusinessError
from server.models.person_model import Person
from server.models.user_model import User
from server.repositories import person_repository, user_repository
from server.resources.user_resource import (
    CreateUserPerson,
    UpdateUser,
    UpdateUserOptional,
    UpdateUserPassword,
)

crypt = get_crypt()


async def create_user_person(
    ctx: Context, user_person_create: CreateUserPerson
) -> User:
    async with ctx.session.begin():
        person = await person_repository.get_or_create(
            session=ctx.session,
            person=Person(
                first_name=user_person_create.first_name,
                last_name=user_person_create.last_name,
            ),
        )
    async with ctx.session.begin():
        password_hash = crypt.hash_password(user_person_create.password)
        user = await user_repository.create(
            session=ctx.session,
            user=User(
                username=user_person_create.username,
                password=password_hash,
                person_id=person.id,
            ),
        )
    return user


async def change_password(
    ctx: Context, pk: int, update_password: UpdateUserPassword
) -> User:
    user = await user_repository.get(session=ctx.session, pk=pk)
    if not crypt.check_password(update_password.current_password, user.password):
        raise BusinessError("current password invalid")
    async with ctx.session.begin():
        password_hash = crypt.hash_password(update_password.new_password)
        res = await user_repository.update(
            session=ctx.session,
            pk=pk,
            password=password_hash,
        )
    return res


async def get_all_users(ctx: Context) -> Sequence[User]:
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
    "create_user_person",
    "change_password",
    "get_all_users",
    "get_user",
    "update_user",
    "update_user_optional",
    "delete_user",
)
