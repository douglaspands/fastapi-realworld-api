import pytest
from sqlalchemy.exc import OperationalError

from server.core.database import get_sessionio
from server.core.settings import DatabaseDsn, Settings
from server.repositories import person_repository


@pytest.mark.asyncio
async def test_get_sessionio_ok(settings: Settings):
    settings.db_url = DatabaseDsn(r"sqlite+aiosqlite://")
    async for session in get_sessionio():
        assert callable(session.begin)


@pytest.mark.asyncio
async def test_get_sessionio_error(settings: Settings):
    settings.db_url = DatabaseDsn(r"sqlite+aiosqlite://")
    with pytest.raises(OperationalError) as exc_info:
        async for session in get_sessionio():
            await person_repository.get(pk=99999, session=session)
    assert "no such table: person" in str(exc_info.value)
