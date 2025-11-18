from functools import cache
from typing import Protocol, Self

from pwdlib import PasswordHash


class CryptInterface(Protocol):
    def check_password(self: Self, password: str, hashed_password: str) -> bool: ...
    def hash_password(self: Self, password: str) -> str: ...


class CryptCore(CryptInterface):
    def __init__(self: Self):
        self._pw_context = PasswordHash.recommended()

    def check_password(self: Self, password: str, hashed_password: str) -> bool:
        return self._pw_context.verify(password, hashed_password)

    def hash_password(self: Self, password: str) -> str:
        return self._pw_context.hash(password)


@cache
def get_crypt() -> CryptInterface:
    return CryptCore()


__all__ = (
    "CryptInterface",
    "get_crypt",
)
