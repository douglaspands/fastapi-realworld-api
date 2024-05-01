from pydantic import BaseModel


class CreatePeople(BaseModel):
    first_name: str
    last_name: str


class People(CreatePeople):
    id: int | None = None


__all__ = ("CreatePeople", "People")
