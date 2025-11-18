from typing import Any, Dict, Generic, Optional, Sequence, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ValidationError(BaseModel):
    type: str
    loc: Sequence[str]
    msg: str
    input: Optional[Dict[str, Any]]


class MessageError(BaseModel):
    message: str


class ResponseOK(BaseModel, Generic[T]):
    data: T


class ResponseBadRequest(BaseModel):
    errors: Sequence[ValidationError]


class ResponseErrors(BaseModel):
    errors: Sequence[MessageError]


__all__ = ("ResponseOK", "ResponseBadRequest", "ResponseErrors")
