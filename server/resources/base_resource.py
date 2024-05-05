from pydantic import AliasGenerator as PydanticAliasGenerator
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict
from pydash import camel_case as PydashCamelCase


class BaseResource(PydanticBaseModel):
    model_config = PydanticConfigDict(
        alias_generator=PydanticAliasGenerator(
            validation_alias=PydashCamelCase, serialization_alias=PydashCamelCase
        ),
        populate_by_name=True,
    )


__all__ = ("BaseResource",)
