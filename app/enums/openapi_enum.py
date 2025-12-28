from enum import StrEnum


class OpenApiTagEnum(StrEnum):
    AUTH = "Auth"
    HEALTH = "Health"
    PERSON = "Person"
    USER = "User"


__all__ = ("OpenApiTagEnum",)
