from pydantic import AliasGenerator as PydanticAliasGenerator
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict
from pydash import camel_case as PydashCamelCase


class Base(PydanticBaseModel):
    model_config = PydanticConfigDict(
        alias_generator=PydanticAliasGenerator(serialization_alias=PydashCamelCase)
    )
