from enum import StrEnum
from functools import cache
from typing import Protocol, Self

import bcrypt
from passlib.context import CryptContext


class CryptCoreEnum(StrEnum):
    BCRYPT = "bcrypt"
    PASSLIB = "passlib"


class CryptInterface(Protocol):
    def check_password(self: Self, password: str, hashed_password: str) -> bool:
        pass

    def hash_password(self: Self, password: str) -> str:
        pass


class BcryptCore(CryptInterface):
    def __init__(self: Self):
        self._encoding = "utf-8"
        self._salt = bcrypt.gensalt()

    def check_password(self: Self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(self._encoding), hashed_password.encode(self._encoding)
        )

    def hash_password(self: Self, password: str) -> str:
        hash = bcrypt.hashpw(password.encode(self._encoding), self._salt)
        return hash.decode(self._encoding)


class PasslibCore(CryptInterface):
    def __init__(self: Self):
        self._pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def check_password(self: Self, password: str, hashed_password: str) -> bool:
        return self._pw_context.verify(password, hashed_password)

    def hash_password(self: Self, password: str) -> str:
        return self._pw_context.hash(password)


@cache
def get_crypt(core: CryptCoreEnum = CryptCoreEnum.BCRYPT) -> CryptInterface:
    match core:
        case CryptCoreEnum.PASSLIB:
            return PasslibCore()
        case CryptCoreEnum.BCRYPT:
            return BcryptCore()
        case _:
            return BcryptCore()


__all__ = ("CryptInterface", "get_crypt", "CryptCoreEnum")
