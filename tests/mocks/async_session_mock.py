from __future__ import annotations

from random import randint
from typing import Any, Self, Sequence, TypeVar

T = TypeVar("T")


class AsyncSessionMock:
    def __init__(
        self: Self, return_value: Any = None, side_effect: BaseException | None = None
    ):
        self._return_value = return_value
        self._side_effect = side_effect

    def __enter__(self: Self, *args: Any, **kwargs: Any) -> Self:
        self._enter_count = getattr(self, "_enter_count", 0) + 1
        self._enter_args = args
        self._enter_kwargs = kwargs
        if self._side_effect:
            raise self._side_effect
        return self

    def __exit__(self: Self, exc_type, exc_value, exc_tb) -> Self:
        self._exit_count = getattr(self, "_exit_count", 0) + 1
        if exc_value:
            raise exc_value
        return self

    async def __aenter__(self: Self, *args: Any, **kwargs: Any) -> Self:
        self._aenter_count = getattr(self, "_aenter_count", 0) + 1
        self._aenter_args = args
        self._aenter_kwargs = kwargs
        if self._side_effect:
            raise self._side_effect
        return self

    async def __aexit__(self: Self, exc_type, exc_value, exc_tb) -> Self:
        self._aexit_count = getattr(self, "_aexit_count", 0) + 1
        if exc_value:
            raise exc_value
        return self

    async def exec(self: Self, *args: Any, **kwargs: Any) -> Self:
        print(args, kwargs)
        self._exec_count = getattr(self, "_exec_count", 0) + 1
        self._exec_args = args
        self._exec_kwargs = kwargs
        return self

    def one(self: Self) -> Any:
        self._one_count = getattr(self, "_one_count", 0) + 1
        if self._side_effect:
            raise self._side_effect
        return self._return_value

    def all(self: Self) -> Sequence[Any]:
        self._all_count = getattr(self, "_all_count", 0) + 1
        if self._side_effect:
            raise self._side_effect
        return self._return_value

    def add(self: Self, model: T):
        self._add_count = getattr(self, "_add_count", 0) + 1
        setattr(model, "id", randint(1, 1000))
        if self._side_effect:
            raise self._side_effect

    async def refresh(self: Self, model: T) -> Self:
        self._refresh_count = getattr(self, "_refresh_count", 0) + 1
        return self

    def begin(self: Self) -> Self:
        self._begin_count = getattr(self, "_begin_count", 0) + 1
        return self

    async def commit(self: Self) -> Self:
        self._commit_count = getattr(self, "_commit_count", 0) + 1
        return self

    async def rollback(self: Self) -> Self:
        self._rollback_count = getattr(self, "_rollback_count", 0) + 1
        return self
