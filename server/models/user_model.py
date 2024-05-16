from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from server.models.people_model import People


class User(SQLModel, table=True):
    # pk
    id: int | None = Field(default=None, primary_key=True)
    # columns
    username: str = Field(index=True, unique=True, nullable=False)
    password: str
    active: bool = True
    # relationship
    people_id: int = Field(foreign_key="people.id", nullable=False)
    people: People = Relationship()
    # timestamp
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=datetime.now,
            nullable=False,
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=datetime.now,
            onupdate=datetime.now,
            nullable=False,
        )
    )


__all__ = ("User",)
