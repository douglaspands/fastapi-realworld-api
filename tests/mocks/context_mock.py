from __future__ import annotations

from typing import Any, Self, Type, cast

from server.core.context import Context
from tests.mocks.async_session_mock import SessionIO, SessionIOMock


class ContextMock:
    session: SessionIO

    def __init__(self: Self, session: SessionIO):
        self.session = session

    @classmethod
    def context_session_mock(
        cls: Type[ContextMock],
        return_value: Any = None,
        side_effect: BaseException | None = None,
    ) -> Context:
        return cast(
            Context,
            ContextMock(
                session=SessionIOMock.cast(
                    return_value=return_value, side_effect=side_effect
                )
            ),
        )
