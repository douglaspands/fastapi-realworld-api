from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")
# E = TypeVar("E")


class ResponseOK(BaseModel, Generic[T]):
    data: T | Sequence[T] = Field(..., title="Envelope", description="Data envelope")


# class ResponseError(BaseModel, Generic[E]):
#     errors: list[E] = Field(..., title="Envelope", description="Errors envelope")


__all__ = ("ResponseOK",)
