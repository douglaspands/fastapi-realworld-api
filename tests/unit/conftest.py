import os
from typing import Generator

import pytest

from tests.unit.utils.http_client import HttpClient

os.environ["db_url"] = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def httpclient() -> Generator[HttpClient, None, None]:
    from app.infra.api import create_app

    app = create_app()
    yield HttpClient(app)
