from copy import copy
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.core.database import SessionIO
from server.models.user_model import User
from server.resources.user_resource import UpdateUser, UpdateUserOptional
from server.services import user_service
from tests.mocks.context_mock import ContextMock

fake = Faker("pt_BR")
Faker.seed(0)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_get_user_ok(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1

    # MOCK
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=fake.password(),
        people_id=fake.pyint(1, 999),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get.return_value = user_mock

    # WHEN
    user = await user_service.get_user(context_mock, pk=user_id)

    # THEN
    assert user.id == user_mock.id
    assert user.username == user_mock.username
    assert user.password == user_mock.password
    assert user.active == user_mock.active
    assert user.people_id == user_mock.people_id
    assert user.created_at == user_mock.created_at
    assert user.updated_at == user_mock.updated_at


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_get_user_not_found(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 9999

    # MOCK
    error_message = "No row was found when one was required"
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get.side_effect = NoResultFound(error_message)

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await user_service.get_user(context_mock, pk=user_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_all_users_ok(user_repository_mock: AsyncMock):
    # MOCK
    users_mock = [
        User(
            id=idx + 1,
            username=fake.user_name(),
            password=fake.password(),
            people_id=fake.pyint(1, 999),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        for idx in range(10)
    ]
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = users_mock

    # WHEN
    users = await user_service.all_users(context_mock)

    # THEN
    assert len(users) == len(users_mock)
    for idx in range(len(users_mock)):
        assert users[idx].id == users_mock[idx].id
        assert users[idx].username == users_mock[idx].username
        assert users[idx].password == users_mock[idx].password
        assert users[idx].active == users_mock[idx].active
        assert users[idx].people_id == users_mock[idx].people_id
        assert users[idx].created_at == users_mock[idx].created_at
        assert users[idx].updated_at == users_mock[idx].updated_at


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_all_users_nocontent(user_repository_mock: AsyncMock):
    # MOCK
    users_mock: list[User] = []
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = users_mock

    # WHEN
    users = await user_service.all_users(context_mock)

    # THEN
    assert len(users) == len(users_mock)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_update_user_ok(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    update_user = UpdateUser(
        username=fake.user_name(),
        active=fake.pybool(),
        people_id=fake.pyint(1, 999),
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=fake.password(),
        people_id=fake.pyint(1, 999),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )

    async def update_mock(session: SessionIO, pk: int, **values):
        user = copy(user_mock)
        for k, v in values.items():
            setattr(user, k, v)
        return user

    user_repository_mock.update = update_mock

    # WHEN
    user = await user_service.update_user(
        context_mock, pk=user_id, update_user=update_user
    )

    # THEN
    assert user.id == user_id
    assert user.username != user_mock.username
    assert user.username == update_user.username
    assert user.password == user_mock.password
    assert user.active != user_mock.active
    assert user.active == update_user.active
    assert user.people_id != user_mock.people_id
    assert user.people_id == update_user.people_id


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_update_user_error(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    update_user = UpdateUser(
        username=fake.user_name(),
        active=fake.pybool(),
        people_id=fake.pyint(1, 999),
    )

    # MOCK
    error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.update.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await user_service.update_user(
            context_mock, pk=user_id, update_user=update_user
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_update_user_optional_ok(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    update_user = UpdateUserOptional(username=fake.user_name())  # type: ignore

    # MOCK
    context_mock = ContextMock.context_session_mock()
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=fake.password(),
        people_id=fake.pyint(1, 999),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )

    async def update_mock(session: SessionIO, pk: int, **values):
        user = copy(user_mock)
        for k, v in values.items():
            setattr(user, k, v)
        return user

    user_repository_mock.update = update_mock

    # WHEN
    user = await user_service.update_user_optional(
        context_mock, pk=user_id, update_user=update_user
    )

    # THEN
    assert user.id == user_id
    assert user.username != user_mock.username
    assert user.username == update_user.username
    assert user.password == user_mock.password
    assert user.people_id == user_mock.people_id


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_update_user_optional_error(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 999999
    update_user = UpdateUserOptional(username=fake.user_name())  # type: ignore

    # MOCK
    error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.update.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await user_service.update_user_optional(
            context_mock, pk=user_id, update_user=update_user
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_delete_user_ok(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1

    # MOCK
    context_mock = ContextMock.context_session_mock()

    # WHEN
    await user_service.delete_user(context_mock, pk=user_id)

    # THEN
    assert True


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_delete_user_error(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 999999

    # MOCK
    error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.delete.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await user_service.delete_user(context_mock, pk=user_id)

    # THEN
    assert error_message in str(exc_info.value)
