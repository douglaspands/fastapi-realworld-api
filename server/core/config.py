from functools import cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pass


@cache
def get_settings() -> Settings:
    return Settings()
