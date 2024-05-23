from enum import StrEnum


class OpenApiTagEnum(StrEnum):
    AUTH = "Auth"
    PERSON = "Person"
    USER = "User"


__all__ = ("OpenApiTagEnum",)
