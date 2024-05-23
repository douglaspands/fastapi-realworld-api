from typing import cast

import pytest
from faker import Faker
from fastapi import Request

from server.core.context import Context, get_context_with_request
from server.core.settings import DatabaseDsn, Settings
from server.resources.user_resource import User
from tests.mocks.async_session_mock import SessionIO, SessionIOMock

fake = Faker("pt_BR")
Faker.seed(0)


class RequestMock:
    pass


@pytest.mark.asyncio
async def test_get_context_with_request_ok(settings: Settings):
    # GIVEN
    settings.db_url = DatabaseDsn(r"sqlite+aiosqlite://")
    request_mock = cast(Request, RequestMock())
    # WHEN
    async for context in get_context_with_request(request=request_mock):
        # THEN
        assert isinstance(context, Context)


def test_context_ok_request():
    # GIVEN
    request_mock = cast(Request, RequestMock())
    # WHEN
    ctx = Context(request=request_mock)
    # THEN
    assert ctx.request


def test_context_ok_session():
    # GIVEN
    session = cast(SessionIO, SessionIOMock())
    # WHEN
    ctx = Context(session=session)
    # THEN
    assert ctx.session


def test_context_ok_user():
    # GIVEN
    user = User(
        id=fake.random_int(1, 99),
        username=fake.user_name(),
        active=fake.boolean(50),
        person_id=fake.random_int(1, 99),
        updated_at=fake.date_time(),
        created_at=fake.date_time(),
    )
    # WHEN
    ctx = Context(user=user)
    # THEN
    assert ctx.user


def test_context_not_session():
    # WHEN
    with pytest.raises(ValueError) as exc_info:
        ctx = Context()
        ctx.session
    # THEN
    assert "session not found" in str(exc_info.value)


def test_context_not_user():
    # WHEN
    with pytest.raises(ValueError) as exc_info:
        ctx = Context()
        ctx.user
    # THEN
    assert "user not found" in str(exc_info.value)


def test_context_not_request():
    # WHEN
    with pytest.raises(ValueError) as exc_info:
        ctx = Context()
        ctx.request
    # THEN
    assert "request not found" in str(exc_info.value)
