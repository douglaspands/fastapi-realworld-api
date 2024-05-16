from enum import StrEnum


class OpenApiTagEnum(StrEnum):
    AUTH = "Auth"
    PEOPLE = "People"
    USER = "User"


__all__ = ("OpenApiTagEnum",)
