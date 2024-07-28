from datetime import datetime, timezone

from sqlmodel import Column, DateTime, Field, SQLModel


class Person(SQLModel, table=True):
    # pk
    id: int | None = Field(default=None, primary_key=True)
    # columns
    first_name: str
    last_name: str
    # timestamp
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
    )


__all__ = ("Person",)
