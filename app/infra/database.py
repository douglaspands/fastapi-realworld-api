from contextlib import asynccontextmanager
from functools import cache
from typing import Any, AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infra.settings import get_settings


class SessionIO(AsyncSession):
    pass


@cache
def sessionio_maker() -> async_sessionmaker[SessionIO]:
    config = get_settings()
    session_local = async_sessionmaker(
        bind=create_async_engine(
            url=config.db_url, echo=config.db_debug, pool_recycle=3600
        ),
        class_=SessionIO,
        expire_on_commit=False,
    )
    return session_local


@asynccontextmanager
async def get_sessionio() -> AsyncGenerator[SessionIO, Any]:
    session_local = sessionio_maker()
    async with session_local() as session:
        yield session


async def ping_database() -> bool:
    async with get_sessionio() as session:
        cursor = await session.exec(text("SELECT 1"))
        result = cursor.fetchone()
        return result[0] == 1


__all__ = ("sessionio_maker", "get_sessionio", "SessionIO", "ping_database")
