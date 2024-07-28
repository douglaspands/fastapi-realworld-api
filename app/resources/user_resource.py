from typing import Self

from pydantic import model_validator

from app.resources.base_resource import BaseResource
from app.resources.metaclasses.all_optional_metaclass import AllOptionalMetaclass
from app.resources.mixins.timestamp_mixin import TimestampMixin
from app.resources.person_resource import CreatePerson


class CreateUserPerson(CreatePerson):
    username: str
    password: str
    password_check: str

    @model_validator(mode="after")
    def check_passwords_match(self: Self) -> Self:
        pw1 = self.password
        pw2 = self.password_check
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


class UpdateUserPassword(BaseResource):
    current_password: str
    new_password: str
    new_password_check: str

    @model_validator(mode="after")
    def check_passwords_match(self: Self) -> Self:
        pw1 = self.new_password
        pw2 = self.new_password_check
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


class UpdateUser(BaseResource):
    username: str
    active: bool
    person_id: int


class UpdateUserOptional(UpdateUser, metaclass=AllOptionalMetaclass):
    pass


class User(TimestampMixin, UpdateUser):
    id: int


__all__ = (
    "CreateUserPerson",
    "User",
    "UpdateUserPassword",
    "UpdateUser",
    "UpdateUserOptional",
)
