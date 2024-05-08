from __future__ import annotations

from typing import Any, AsyncGenerator

from pydantic import BaseModel, ConfigDict

from server.core.db import SessionIO, get_sessionio


class Context(BaseModel):
    session: SessionIO

    # config
    model_config = ConfigDict(arbitrary_types_allowed=True)


async def get_context() -> AsyncGenerator[Context, Any]:
    async for session in get_sessionio():
        yield Context(session=session)


__all__ = ("Context", "get_context")
