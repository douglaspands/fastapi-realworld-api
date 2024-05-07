from __future__ import annotations

from typing import Any, Optional, Type

from pydantic import AliasGenerator as PydanticAliasGenerator
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict
from pydantic._internal._model_construction import (
    ModelMetaclass as PydanticModelMetaclass,
)
from pydash import camel_case as PydashCamelCase


class BaseResource(PydanticBaseModel):
    model_config = PydanticConfigDict(
        alias_generator=PydanticAliasGenerator(
            validation_alias=PydashCamelCase, serialization_alias=PydashCamelCase
        ),
        populate_by_name=True,
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


__all__ = ("BaseResource", "AllOptionalMetaclass")
