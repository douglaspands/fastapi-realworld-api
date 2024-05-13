from server.models.base_model import BaseModel


class People(BaseModel, table=True):
    first_name: str
    last_name: str


__all__ = ("People",)
