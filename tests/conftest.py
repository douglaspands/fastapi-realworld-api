from typing import Any, AsyncGenerator, Generator

import pytest

from server.api import app as api_app
from server.core.settings import Settings, get_settings
from tests.utils.http_client import HttpClientIO


@pytest.fixture
async def httpclient() -> AsyncGenerator[HttpClientIO, Any]:
    async with HttpClientIO(app=api_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def settings() -> Generator[Settings, Any, Any]:
    settings = get_settings()
    yield settings
    get_settings.cache_clear()
