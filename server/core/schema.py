from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")
# E = TypeVar("E")


class ResponseOK(BaseModel, Generic[T]):
    data: T


# class ResponseError(BaseModel, Generic[E]):
#     errors: list[E] = Field(..., title="Envelope", description="Errors envelope")


__all__ = ("ResponseOK",)
