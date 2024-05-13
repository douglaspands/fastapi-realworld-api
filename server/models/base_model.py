from datetime import datetime
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from sqlmodel import Column as SQLModelColumn
from sqlmodel import DateTime as SQLModelDatetime
from sqlmodel import Field as SQLModelField


class BaseModel(PydanticBaseModel):
    id: Optional[int] = SQLModelField(default=None, primary_key=True)

    created_at: Optional[datetime] = SQLModelField(
        sa_column=SQLModelColumn(
            SQLModelDatetime,
            default=datetime.now,
            nullable=False,
        )
    )

    updated_at: Optional[datetime] = SQLModelField(
        sa_column=SQLModelColumn(
            SQLModelDatetime,
            default=datetime.now,
            onupdate=datetime.now,
        )
    )


__all__ = ("BaseModel",)
