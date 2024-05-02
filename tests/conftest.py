from typing import Any, AsyncGenerator

import pytest

from server.api import app as api_app
from tests.utils.http_client import HttpClientIO


@pytest.fixture
async def httpclient() -> AsyncGenerator[HttpClientIO, Any]:
    async with HttpClientIO(app=api_app, base_url="http://test") as ac:
        yield ac
