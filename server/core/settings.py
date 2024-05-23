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
    app_name: str = "FastAPI RealWorld API"
    app_version: str = "0.3.0"

    # openapi_doc
    openapi_description: str = (
        "Exemplo de projeto com <b>FastAPI</b> e <b>SQLModel</b> usando <b>async/await</b> utilizado no mundo real.<br>"
        "Meu desejo é apresentar um motor de API REST utilizando o que considero que tem de melhor no universo Python. <b>[MINHA OPINIÃO]</b>"
    )

    # database
    db_debug: bool = False
    db_url: DatabaseDsn = Field(default=None)

    # token
    token_secret_key: str = Field(default=None)
    token_algorithm: str = "HS256"
    token_expire_minutes: int = 30

    # config
    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    return Settings()


__all__ = ("Settings", "get_settings")
