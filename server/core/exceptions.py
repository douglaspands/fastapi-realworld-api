from typing import Self

from fastapi import status
from fastapi.exceptions import HTTPException


class BaseError(HTTPException):
    def __init__(self: Self, http_status: int, message: str):
        super().__init__(status_code=http_status, detail=message)


class NoContentError(BaseError):
    def __init__(self: Self):
        super().__init__(http_status=status.HTTP_204_NO_CONTENT, message="")


class NotFoundError(BaseError):
    def __init__(self: Self, message: str):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND, message=message)


class BusinessError(BaseError):
    def __init__(self: Self, message: str):
        super().__init__(
            http_status=status.HTTP_422_UNPROCESSABLE_ENTITY, message=message
        )
