from datetime import datetime

from sqlmodel import Column, DateTime, Field, SQLModel

from server.core.utils import datetime_now


class People(SQLModel, table=True):
    # pk
    id: int | None = Field(default=None, primary_key=True)
    # columns
    first_name: str
    last_name: str
    # timestamp
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=datetime_now,
            nullable=False,
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime,
            default=datetime_now,
            onupdate=datetime_now,
            nullable=False,
        )
    )


__all__ = ("People",)
