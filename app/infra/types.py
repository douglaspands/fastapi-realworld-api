from __future__ import annotations

from typing import Annotated, TypeAlias
from urllib.parse import urlparse

from pydantic import AfterValidator


def validate_specific_dsn(uri: str) -> str:
    dsn = urlparse(uri)
    if dsn.scheme not in {"sqlite+aiosqlite", "postgresql+psycopg"}:
        raise ValueError("Unsupported database scheme")
    if not dsn.path:
        raise ValueError("Unsupported database host")
    return uri


DatabaseDsn: TypeAlias = Annotated[str, AfterValidator(validate_specific_dsn)]

__all__ = ("DatabaseDsn",)
