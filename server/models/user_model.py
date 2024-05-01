# from typing import TYPE_CHECKING, Optional

# from sqlmodel import Field, Relationship, SQLModel

# if TYPE_CHECKING:
#     from .people_model import People


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str
#     password: str

#     people_id: int | None = Field(default=None, foreign_key="people.id")
#     people: People | None = Relationship()


# __all__ = ("User",)
