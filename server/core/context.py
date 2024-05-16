from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Self

from pydantic import BaseModel, ConfigDict

from server.core.database import SessionIO, get_sessionio
from server.core.exceptions import NotFoundError

if TYPE_CHECKING:
    from server.models.user_model import User


class Context(BaseModel):
    _user: User | None = None
    session: SessionIO

    # config
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self: Self, session: SessionIO, user: User | None = None):
        super().__init__(session=session)
        if user:
            self._user = user

    @property
    def user(self: Self) -> User:
        if not self._user:
            raise NotFoundError("user not found")
        return self._user


async def get_context() -> AsyncGenerator[Context, Any]:
    async for session in get_sessionio():
        yield Context(session=session)


__all__ = ("Context", "get_context")
