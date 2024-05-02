from functools import cache
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from server.core.settings import get_settings


@cache
def get_async_engine() -> AsyncEngine:
    config = get_settings()
    engine = create_async_engine(
        url=str(config.db_url),
        echo=config.db_debug,
    )
    return engine


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async_session = async_sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


__all__ = ("get_async_session", "get_async_engine", "AsyncEngine")
