from functools import cache
from typing import Annotated

from pydantic import Field, UrlConstraints
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

DatabaseDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=True,
        allowed_schemes=[
            "sqlite+aiosqlite",
        ],
    ),
]


class Settings(BaseSettings):
    # app
    app_name: str = "fastapi-realworld-api"

    # database
    db_debug: bool = False
    db_url: DatabaseDsn = Field(default=None)

    # token
    token_secret_key: str = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    token_algorithm: str = "HS256"
    token_expire_minutes: int = 30

    # config
    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    return Settings()


__all__ = ("Settings", "get_settings")
