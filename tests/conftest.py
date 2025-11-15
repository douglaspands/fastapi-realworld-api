from typing import Any, Generator

import pytest

from app.asgi import app
from app.infra.settings import Settings, get_settings
from tests.utils.http_client import HttpClient


@pytest.fixture
def httpclient() -> HttpClient:
    return HttpClient(app)


@pytest.fixture
def settings() -> Generator[Settings, Any, Any]:
    settings = get_settings()
    yield settings
    get_settings.cache_clear()
