from typing import Optional, Self

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str

    @property
    def fullname(self: Self) -> str:
        return f"{self.name} {self.surname}"


__all__ = ("User",)
