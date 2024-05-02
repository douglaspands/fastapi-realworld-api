from functools import cache
from typing import Any, AsyncGenerator, cast

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from server.core.settings import get_settings


class SessionIO(AsyncSession):
    pass


class EngineIO(AsyncEngine):
    pass


@cache
def get_engineio() -> EngineIO:
    config = get_settings()
    engine = cast(
        EngineIO,
        create_async_engine(
            url=str(config.db_url),
            echo=config.db_debug,
        ),
    )
    return engine


async def get_sessionio() -> AsyncGenerator[SessionIO, Any]:
    async_session = async_sessionmaker(
        bind=get_engineio(),
        class_=SessionIO,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


__all__ = ("get_sessionio", "get_engineio", "SessionIO", "EngineIO")
