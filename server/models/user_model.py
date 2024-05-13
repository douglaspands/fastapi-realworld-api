from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from server.models.base_model import BaseModel

if TYPE_CHECKING:
    from server.models.people_model import People


class User(BaseModel, table=True):
    username: str = Field(index=True, nullable=False)
    password: str
    active: bool = True

    # Relationship
    people_id: int = Field(foreign_key="people.id", nullable=False)
    people: People = Relationship(back_populates="people")


__all__ = ("User",)
