from typing import Optional, Self

from sqlmodel import Field, SQLModel


class People(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str

    @property
    def full_name(self: Self) -> str:
        return f"{self.first_name} {self.last_name}"


__all__ = ("People",)
