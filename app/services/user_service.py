from typing import cast

from app.infra.context import IContext
from app.infra.crypt import get_crypt
from app.infra.exceptions import BusinessError
from app.models.person_model import Person as PersonModel
from app.models.user_model import User as UserModel
from app.repositories import person_repository, user_repository
from app.resources.user_resource import (
    CreateUserPerson,
    UpdateUser,
    UpdateUserOptional,
    UpdateUserPassword,
    User,
)

crypt = get_crypt()


async def create_user_person(
    ctx: IContext, *, user_person_create: CreateUserPerson
) -> User:
    person = await person_repository.get_or_create(
        ctx,
        person=PersonModel(
            first_name=user_person_create.first_name,
            last_name=user_person_create.last_name,
        ),
    )
    password_hash = crypt.hash_password(user_person_create.password)
    user = await user_repository.create(
        ctx,
        user=UserModel(
            username=user_person_create.username,
            password=password_hash,
            person_id=cast(int, person.id),
        ),
    )
    return User(**user.__dict__)


async def change_password(
    ctx: IContext, *, user_id: int, update_password: UpdateUserPassword
) -> User:
    user = await user_repository.get(ctx, pk=user_id)
    if not crypt.check_password(update_password.current_password, user.password):
        raise BusinessError("current password invalid")
    password_hash = crypt.hash_password(update_password.new_password)
    user = await user_repository.update(
        ctx,
        pk=user_id,
        password=password_hash,
    )
    return User(**user.__dict__)


async def get_all_users(ctx: IContext) -> list[User]:
    users = await user_repository.get_all(ctx)
    return [User(**user.__dict__) for user in users]


async def get_user(ctx: IContext, *, user_id: int) -> User:
    user = await user_repository.get(ctx, pk=user_id)
    return User(**user.__dict__)


async def update_user(ctx: IContext, *, user_id: int, update_user: UpdateUser) -> User:
    values = update_user.model_dump()
    user = await user_repository.update(ctx, pk=user_id, **values)
    return User(**user.__dict__)


async def update_user_optional(
    ctx: IContext, *, user_id: int, update_user: UpdateUserOptional
) -> User:
    values = update_user.model_dump(exclude_none=True)
    user = await user_repository.update(ctx, pk=user_id, **values)
    return User(**user.__dict__)


async def delete_user(ctx: IContext, *, user_id: int):
    await user_repository.delete(ctx, pk=user_id)


__all__ = (
    "create_user_person",
    "change_password",
    "get_all_users",
    "get_user",
    "update_user",
    "update_user_optional",
    "delete_user",
)
