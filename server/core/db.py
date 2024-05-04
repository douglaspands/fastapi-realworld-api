from functools import cache
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from server.core.settings import get_settings


class SessionIO(AsyncSession):
    pass


@cache
def _make_session() -> async_sessionmaker[SessionIO]:
    config = get_settings()
    async_session = async_sessionmaker(
        bind=create_async_engine(
            url=str(config.db_url),
            echo=config.db_debug,
        ),
        class_=SessionIO,
        expire_on_commit=False,
    )
    return async_session


async def get_sessionio() -> AsyncGenerator[SessionIO, Any]:
    async_session = _make_session()
    async with async_session() as session:
        yield session


__all__ = ("get_sessionio", "SessionIO")
