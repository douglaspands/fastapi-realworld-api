from functools import cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "fastapi-realworld-api"
    app_version: str = "v0.1.0"
    db_url: PostgresDsn | None = None
    db_debug: bool = False


@cache
def get_settings() -> Settings:
    return Settings()


__all__ = ("Settings", "get_settings")