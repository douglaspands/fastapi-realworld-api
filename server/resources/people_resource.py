from server.resources.base_resource import BaseResource
from server.resources.metaclasses.all_optional_metaclass import AllOptionalMetaclass
from server.resources.mixins.timestamp_mixin import TimestampMixin


class CreatePeople(BaseResource):
    first_name: str
    last_name: str


class UpdatePeople(CreatePeople):
    pass


class UpdatePeopleOptional(CreatePeople, metaclass=AllOptionalMetaclass):
    pass


class People(TimestampMixin, CreatePeople):
    id: int


__all__ = ("CreatePeople", "People", "UpdatePeople", "UpdatePeopleOptional")
