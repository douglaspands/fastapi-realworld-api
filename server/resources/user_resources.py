from typing import Self

from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    name: str
    surname: str

    @property
    def fullname(self: Self) -> str:
        return f"{self.name} {self.surname}"


__all__ = ("User",)
