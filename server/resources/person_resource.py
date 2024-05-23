from server.resources.base_resource import BaseResource
from server.resources.metaclasses.all_optional_metaclass import AllOptionalMetaclass
from server.resources.mixins.timestamp_mixin import TimestampMixin


class CreatePerson(BaseResource):
    first_name: str
    last_name: str


class UpdatePerson(CreatePerson):
    pass


class UpdatePersonOptional(CreatePerson, metaclass=AllOptionalMetaclass):
    pass


class Person(TimestampMixin, CreatePerson):
    id: int


__all__ = ("CreatePerson", "Person", "UpdatePerson", "UpdatePersonOptional")
