from server.resources.base_resource import AllOptionalMetaclass, BaseResource


class CreatePeople(BaseResource):
    first_name: str
    last_name: str


class UpdatePeople(CreatePeople):
    pass


class UpdatePeopleOptional(CreatePeople, metaclass=AllOptionalMetaclass):
    pass


class People(CreatePeople):
    id: int


__all__ = ("CreatePeople", "People", "UpdatePeople", "UpdatePeopleOptional")
