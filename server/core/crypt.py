from functools import cache
from typing import Protocol, Self

from passlib.context import CryptContext


class CryptInterface(Protocol):
    def check_password(self: Self, password: str, hashed_password: str) -> bool: ...
    def hash_password(self: Self, password: str) -> str: ...


class PasslibCore(CryptInterface):
    def __init__(self: Self):
        self._pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def check_password(self: Self, password: str, hashed_password: str) -> bool:
        return self._pw_context.verify(password, hashed_password)

    def hash_password(self: Self, password: str) -> str:
        return self._pw_context.hash(password)


@cache
def get_crypt() -> CryptInterface:
    return PasslibCore()


__all__ = (
    "CryptInterface",
    "get_crypt",
)
