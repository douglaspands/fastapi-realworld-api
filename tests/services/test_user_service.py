from copy import copy
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.core.database import SessionIO
from server.core.exceptions import BusinessError
from server.models.person_model import Person
from server.models.user_model import User
from server.resources.user_resource import (
    CreateUserPerson,
    UpdateUser,
    UpdateUserOptional,
    UpdateUserPassword,
)
from server.services import user_service
from server.services.auth_service import crypt
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
        password=crypt.hash_password(fake.password(10)),
        person_id=fake.pyint(1, 999),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get.return_value = user_mock

    # WHEN
    user = await user_service.get_user(context_mock, user_id=user_id)

    # THEN
    assert user.id == user_mock.id
    assert user.username == user_mock.username
    assert user.password == user_mock.password
    assert user.active == user_mock.active
    assert user.person_id == user_mock.person_id
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
        await user_service.get_user(context_mock, user_id=user_id)

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
            password=crypt.hash_password(fake.password(10)),
            person_id=fake.pyint(1, 999),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        for idx in range(10)
    ]
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get_all.return_value = users_mock

    # WHEN
    users = await user_service.get_all_users(context_mock)

    # THEN
    assert len(users) == len(users_mock)
    for idx in range(len(users_mock)):
        assert users[idx].id == users_mock[idx].id
        assert users[idx].username == users_mock[idx].username
        assert users[idx].password == users_mock[idx].password
        assert users[idx].active == users_mock[idx].active
        assert users[idx].person_id == users_mock[idx].person_id
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
    users = await user_service.get_all_users(context_mock)

    # THEN
    assert len(users) == len(users_mock)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_update_user_ok(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    update_user = UpdateUser(
        username=fake.user_name(),
        active=True,
        person_id=fake.pyint(1, 10),
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(10)),
        active=False,
        person_id=fake.pyint(11, 20),
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
        context_mock, user_id=user_id, update_user=update_user
    )

    # THEN
    assert user.id == user_id
    assert user.username != user_mock.username
    assert user.username == update_user.username
    assert user.password == user_mock.password
    assert user.active != user_mock.active
    assert user.active == update_user.active
    assert user.person_id != user_mock.person_id
    assert user.person_id == update_user.person_id


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_update_user_error(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    update_user = UpdateUser(
        username=fake.user_name(),
        active=fake.pybool(),
        person_id=fake.pyint(1, 999),
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
            context_mock, user_id=user_id, update_user=update_user
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
        password=crypt.hash_password(fake.password(10)),
        person_id=fake.pyint(1, 999),
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
        context_mock, user_id=user_id, update_user=update_user
    )

    # THEN
    assert user.id == user_id
    assert user.username != user_mock.username
    assert user.username == update_user.username
    assert user.password == user_mock.password
    assert user.person_id == user_mock.person_id


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
            context_mock, user_id=user_id, update_user=update_user
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
    await user_service.delete_user(context_mock, user_id=user_id)

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
        await user_service.delete_user(context_mock, user_id=user_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_change_password_ok(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    new_password = fake.password(10)
    update_password = UpdateUserPassword(
        current_password=fake.password(10),
        new_password=new_password,
        new_password_check=new_password,
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(update_password.current_password),
        person_id=fake.pyint(1, 999),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )

    async def update_mock(session: SessionIO, pk: int, **values):
        user = copy(user_mock)
        for k, v in values.items():
            setattr(user, k, v)
        return user

    user_repository_mock.get.return_value = user_mock
    user_repository_mock.update = update_mock

    # WHEN
    user = await user_service.change_password(
        ctx=context_mock, user_id=user_id, update_password=update_password
    )

    # THEN
    assert user.id == user_id
    assert user.username == user_mock.username
    assert user.password != user_mock.password
    assert crypt.check_password(update_password.new_password, user.password)
    assert user.active == user_mock.active
    assert user.person_id == user_mock.person_id
    assert user.created_at == user_mock.created_at
    assert user.updated_at == user_mock.updated_at


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_change_password_notfound(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 9999
    new_password = fake.password(10)
    update_password = UpdateUserPassword(
        current_password=fake.password(10),
        new_password=new_password,
        new_password_check=new_password,
    )

    # MOCK
    error_message = "No row was found when one was required"
    context_mock = ContextMock.context_session_mock()
    user_repository_mock.get.side_effect = NoResultFound(error_message)

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await user_service.change_password(
            ctx=context_mock, user_id=user_id, update_password=update_password
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
async def test_change_password_invalid(user_repository_mock: AsyncMock):
    # GIVEN
    user_id = 1
    new_password = fake.password(10)
    update_password = UpdateUserPassword(
        current_password=fake.password(10),
        new_password=new_password,
        new_password_check=new_password,
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(10)),
        person_id=fake.pyint(1, 999),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )
    user_repository_mock.get.return_value = user_mock

    # WHEN
    with pytest.raises(BusinessError) as exc_info:
        await user_service.change_password(
            ctx=context_mock, user_id=user_id, update_password=update_password
        )

    # THEN
    assert "current password invalid" in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.user_service.user_repository", new_callable=AsyncMock)
@patch("server.services.user_service.person_repository", new_callable=AsyncMock)
async def test_create_user_person_ok(
    person_repository_mock: AsyncMock, user_repository_mock: AsyncMock
):
    # GIVEN
    new_password = fake.password(10)
    create_user = CreateUserPerson(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        username=fake.user_name(),
        password=new_password,
        password_check=new_password,
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    person_mock = Person(
        id=fake.pyint(1, 999),
        first_name=create_user.first_name,
        last_name=create_user.last_name,
    )
    user_mock = User(
        id=fake.pyint(1, 999),
        username=create_user.username,
        password=crypt.hash_password(create_user.password),
        person_id=person_mock.id,
        active=fake.pybool(),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )

    person_repository_mock.get_or_create.return_value = person_mock
    user_repository_mock.create.return_value = user_mock

    # WHEN
    user = await user_service.create_user_person(
        ctx=context_mock, user_person_create=create_user
    )

    # THEN
    assert user.id
    assert user.username == create_user.username
    assert crypt.check_password(create_user.password, user.password)
    assert user.active == user_mock.active
    assert user.person_id == person_mock.id
