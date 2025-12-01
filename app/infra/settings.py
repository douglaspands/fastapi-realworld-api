from __future__ import annotations

import secrets
import tomllib
from functools import cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infra.types import DatabaseDsn


class Settings(BaseSettings):
    # app
    app_name: str = ""
    app_version: str = ""
    app_description: str = ""

    # database
    db_debug: bool = False
    db_url: DatabaseDsn

    # token
    token_secret_key: str = Field(default_factory=lambda: secrets.token_hex(32))
    token_algorithm: str = "HS256"
    token_expire_minutes: int = 30

    # config
    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    root_path = Path(__file__).parent.parent.parent
    pyproject_path = root_path / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)
    settings = Settings(
        app_name=pyproject["project"]["name"],
        app_version=pyproject["project"]["version"],
        app_description=pyproject["project"]["description"],
    )
    return settings


__all__ = ("Settings", "get_settings")
