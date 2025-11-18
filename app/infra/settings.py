from __future__ import annotations

import secrets
from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infra.types import DatabaseDsn


class Settings(BaseSettings):
    # app
    app_name: str = "FastAPI RealWorld API"
    app_version: str = "0.5.1"

    # openapi_doc
    openapi_description: str = (
        "Exemplo de projeto com <b>FastAPI</b> e <b>SQLModel</b> usando <b>async/await</b> utilizado no mundo real.<br>"
        "Meu desejo é apresentar um motor de API REST utilizando o que considero que tem de melhor no universo Python. <b>[MINHA OPINIÃO]</b>"
    )

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
    return Settings()


__all__ = ("Settings", "get_settings")
