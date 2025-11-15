from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncGenerator, Protocol, Self

from fastapi import Request

from app.infra.database import SessionIO, get_sessionio

if TYPE_CHECKING:
    from app.resources.user_resource import User


class IContext(Protocol):
    session: SessionIO
    user: User
    request: Request


class Context(IContext):
    # private
    _session: SessionIO | None = None
    _user: User | None = None
    _request: Request | None = None

    def __init__(
        self: Self,
        session: SessionIO | None = None,
        user: User | None = None,
        request: Request | None = None,
    ):
        self._session = session
        self._user = user
        self._request = request

    @property
    def session(self: Self) -> SessionIO:
        if not self._session:
            raise ValueError("session not found")
        return self._session

    @property
    def user(self: Self) -> User:
        if not self._user:
            raise ValueError("user not found")
        return self._user

    @property
    def request(self: Self) -> Request:
        if not self._request:
            raise ValueError("request not found")
        return self._request


async def get_context_with_request(
    request: Request,
) -> AsyncGenerator[Context, Any]:
    async for session in get_sessionio():
        yield Context(session=session, request=request)


@asynccontextmanager
async def get_context():
    async for session in get_sessionio():
        yield Context(session=session, request=None)


__all__ = ("IContext", "Context", "get_context_with_request", "get_context")
