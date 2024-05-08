import pytest

from server.core.context import get_context
from server.core.database import SessionIO
from server.core.settings import DatabaseDsn, Settings


@pytest.mark.asyncio
async def test_get_context_ok(settings: Settings):
    settings.db_url = DatabaseDsn(r"sqlite+aiosqlite://")
    async for context in get_context():
        assert isinstance(context.session, SessionIO)
