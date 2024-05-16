from __future__ import annotations

from typing import Any, Optional, Type

from pydantic._internal._model_construction import (
    ModelMetaclass as PydanticModelMetaclass,
)


class AllOptionalMetaclass(PydanticModelMetaclass):
    def __new__(
        cls: Type[AllOptionalMetaclass],
        name: str,
        bases: tuple[type[Any], ...],
        namespaces: dict[str, Any],
        **kwargs: Any,
    ):
        annotations: dict[str, Any] = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
                namespaces[field] = None
        namespaces["__annotations__"] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)


__all__ = ("AllOptionalMetaclass",)
