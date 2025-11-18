import pytest
from sqlalchemy.exc import OperationalError

from app.infra.database import get_sessionio
from app.repositories import person_repository
from tests.unit.mocks.context_mock import ContextMock


@pytest.mark.asyncio
async def test_get_sessionio_ok():
    async with get_sessionio() as session:
        assert callable(session.begin)


@pytest.mark.asyncio
async def test_get_sessionio_error():
    with pytest.raises(OperationalError) as exc_info:
        async with get_sessionio() as session:
            await person_repository.get(ContextMock.cast(session), pk=99999)
    assert "no such table: person" in str(exc_info.value)
