from server.resources.base_resource import Base


class CreatePeople(Base):
    first_name: str
    last_name: str


class People(CreatePeople):
    id: int | None = None


__all__ = ("CreatePeople", "People")
