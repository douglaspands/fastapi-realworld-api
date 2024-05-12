from functools import cache
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from server.core.settings import get_settings


class SessionIO(AsyncSession):
    pass


@cache
def sessionio_maker() -> async_sessionmaker[SessionIO]:
    config = get_settings()
    session_local = async_sessionmaker(
        bind=create_async_engine(
            url=str(config.db_url),
            echo=config.db_debug,
        ),
        class_=SessionIO,
        expire_on_commit=False,
    )
    return session_local


async def get_sessionio() -> AsyncGenerator[SessionIO, Any]:
    session_local = await sessionio_maker()
    async with session_local() as session:
        yield session


__all__ = ("sessionio_maker", "get_sessionio", "SessionIO")
