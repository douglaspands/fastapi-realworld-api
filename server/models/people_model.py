from typing import Optional

from sqlmodel import Field, SQLModel


class People(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str


__all__ = ("People",)
