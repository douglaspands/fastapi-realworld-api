from __future__ import annotations

from pydantic import AliasGenerator as PydanticAliasGenerator
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict
from pydantic.alias_generators import to_camel as PydanticToCamel


class BaseResource(PydanticBaseModel):
    model_config = PydanticConfigDict(
        alias_generator=PydanticAliasGenerator(
            validation_alias=PydanticToCamel, serialization_alias=PydanticToCamel
        ),
        populate_by_name=True,
    )


__all__ = ("BaseResource",)
