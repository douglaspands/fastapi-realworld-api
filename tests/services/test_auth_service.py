from typing import cast
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from fastapi import HTTPException, Request

from server.core.context import Context
from server.models.user_model import User
from server.resources.token_resource import Token
from server.services.auth_service import authenticate_user, check_access_token, crypt
from tests.mocks.context_mock import ContextMock

fake = Faker("pt_BR")
Faker.seed(0)


class RequestMock:
    pass


@pytest.fixture
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def token_mock(user_repository_mock: AsyncMock) -> Token:
    username = "abc.xyz"
    password = "asdfgh123456"
    users_mock = [
        User(
            id=1,
            username=username,
            password=crypt.hash_password(password),
            people_id=fake.pyint(1, 999),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
    ]
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = users_mock
    token = await authenticate_user(
        ctx=context_mock, username=username, password=password
    )
    return token


@pytest.mark.asyncio
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def test_authenticate_user_ok(user_repository_mock: AsyncMock):
    # GIVEN
    username = fake.user_name()
    password = fake.password(8)

    # MOCK
    users_mock = [
        User(
            id=fake.pyint(1, 999),
            username=username,
            password=crypt.hash_password(password),
            people_id=fake.pyint(1, 999),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
    ]
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = users_mock

    # WHEN
    token = await authenticate_user(
        ctx=context_mock, username=username, password=password
    )

    # THEN
    assert token.access_token
    assert token.token_type == "Bearer"


@pytest.mark.asyncio
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def test_authenticate_user_not_found(user_repository_mock: AsyncMock):
    # GIVEN
    username = fake.user_name()
    password = fake.password(8)

    # MOCK
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = []

    # WHEN
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(ctx=context_mock, username=username, password=password)

    # THEN
    assert "Could not validate credentials" in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def test_authenticate_user_error_password_invalid(
    user_repository_mock: AsyncMock,
):
    # GIVEN
    username = fake.user_name()
    password = fake.password(8)

    # MOCK
    users_mock = [
        User(
            id=fake.pyint(1, 999),
            username=username,
            password=crypt.hash_password(fake.password(8)),
            people_id=fake.pyint(1, 999),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
    ]
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = users_mock

    # WHEN
    with pytest.raises(HTTPException) as exc_info:
        await authenticate_user(ctx=context_mock, username=username, password=password)

    # THEN
    assert "Could not validate credentials" in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def test_check_access_token_ok(
    user_repository_mock: AsyncMock, token_mock: Token
):
    # GIVEN
    username = "abc.xyz"
    password = "asdfgh123456"

    # MOCK
    request_mock = cast(Request, RequestMock())
    users_mock = [
        User(
            id=1,
            username=username,
            password=crypt.hash_password(password),
            people_id=fake.pyint(1, 999),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
    ]
    user_repository_mock.get_all.return_value = users_mock

    # WHEN
    async for context in check_access_token(
        request=request_mock, token=token_mock.access_token
    ):
        # THEN
        assert isinstance(context, Context)


@pytest.mark.asyncio
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def test_check_access_token_not_found(
    user_repository_mock: AsyncMock, token_mock: Token
):
    # MOCK
    request_mock = cast(Request, RequestMock())
    user_repository_mock.get_all.return_value = []

    # WHEN
    with pytest.raises(HTTPException) as exc_info:
        async for context in check_access_token(
            request=request_mock, token=token_mock.access_token
        ):
            # THEN
            assert isinstance(context, Context)

    # THEN
    assert "Could not validate credentials" in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.auth_service.user_repository", new_callable=AsyncMock)
async def test_check_access_token_invalid(user_repository_mock: AsyncMock):
    # MOCK
    request_mock = cast(Request, RequestMock())
    user_repository_mock.get_all.return_value = []

    # WHEN
    with pytest.raises(HTTPException) as exc_info:
        async for context in check_access_token(
            request=request_mock, token=fake.password(20)
        ):
            # THEN
            assert isinstance(context, Context)

    # THEN
    assert "Could not validate credentials" in str(exc_info.value)
