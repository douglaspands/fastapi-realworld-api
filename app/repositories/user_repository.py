from typing import Any

from sqlmodel import select

from app.infra import utils
from app.infra.context import IContext
from app.models.user_model import User


async def create(ctx: IContext, *, user: User) -> User:
    ctx.session.add(user)
    return user


async def get(ctx: IContext, *, pk: int) -> User:
    statement = select(User).where(User.id == pk)
    result = await ctx.session.exec(statement)
    return result.one()


async def get_all(ctx: IContext, *, limit: int = 250, **values: Any) -> list[User]:
    statement = select(User).filter_by(**values).limit(limit)
    result = await ctx.session.exec(statement)
    return list(result.all())


async def update(ctx: IContext, *, pk: int, **values: Any) -> User:
    utils.repository_columns_can_update(values)
    user = await get(ctx, pk=pk)
    user.sqlmodel_update(values)
    ctx.session.add(user)
    return user


async def delete(ctx: IContext, *, pk: int):
    user = await get(ctx, pk=pk)
    await ctx.session.delete(user)


__all__ = (
    "get",
    "get_all",
    "create",
    "update",
    "delete",
)
