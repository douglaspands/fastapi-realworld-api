from copy import copy
from typing import cast

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.models.user_model import User
from app.repositories import user_repository
from app.services.auth_service import crypt
from tests.unit.mocks.context_mock import ContextMock, SessionIOMock

fake = Faker("pt_BR")
Faker.seed(0)


@pytest.mark.asyncio
async def test_user_get_by_pk_ok():
    # GIVEN
    user_id = fake.random_int(min=1, max=999)

    # MOCK
    user_mock = User(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(length=8)),
        person_id=fake.random_int(min=1, max=999),
    )
    context_mock = ContextMock.context_session_mock(return_value=user_mock)

    # WHEN
    res = await user_repository.get(context_mock, pk=user_id)

    # THEN
    assert res.id == user_id
    assert res.username and isinstance(res.username, str)
    assert res.password and isinstance(res.password, str)


@pytest.mark.asyncio
async def test_user_get_by_pk_not_found():
    # GIVEN
    user_id = fake.random_int(min=1000, max=9999)

    # MOCK
    error_message = "No row was found when one was required"
    context_mock = ContextMock.context_session_mock(
        side_effect=NoResultFound(error_message)
    )

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await user_repository.get(context_mock, pk=user_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_user_get_all_ok():
    # MOCK
    user_mock = [
        User(
            id=idx + 1,
            username=fake.user_name(),
            password=crypt.hash_password(fake.password(length=8)),
            person_id=fake.random_int(min=1, max=999),
        )
        for idx in range(10)
    ]
    context_mock = ContextMock.context_session_mock(return_value=user_mock)

    # WHEN
    res = await user_repository.get_all(context_mock)

    # THEN
    assert len(res) == len(user_mock)
    for idx in range(len(user_mock)):
        assert res[idx].id == user_mock[idx].id
        assert res[idx].username == user_mock[idx].username
        assert res[idx].password == user_mock[idx].password


@pytest.mark.asyncio
async def test_user_save_ok():
    # GIVEN
    create_user = User(
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(length=8)),
        person_id=fake.random_int(min=1, max=999),
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()

    # WHEN
    await user_repository.create(context_mock, user=create_user)

    # THEN
    assert create_user.id and isinstance(create_user.id, int)
    assert create_user.id > 0


@pytest.mark.asyncio
async def test_user_save_error():
    # GIVEN
    create_user = User(
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(length=8)),
        person_id=fake.random_int(min=1, max=999),
    )

    # MOCK
    error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
    context_mock = ContextMock.context_session_mock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await user_repository.create(context_mock, user=create_user)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_user_update_ok():
    # GIVEN
    user_id = fake.random_int(min=1, max=10)
    username = fake.user_name()

    # MOCK
    mock_user = User(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(length=8)),
        person_id=fake.random_int(min=1, max=999),
    )
    context_mock = ContextMock.context_session_mock(return_value=copy(mock_user))

    # WHEN
    user_updated = await user_repository.update(
        context_mock, pk=user_id, username=username
    )

    # THEN
    assert user_updated.id == user_id
    assert user_updated.username == username


@pytest.mark.asyncio
async def test_user_update_error():
    # MOCK
    error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
    context_mock = ContextMock.context_session_mock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # GIVEN
    user_id = fake.random_int(min=10000, max=999999)
    username = fake.user_name()

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await user_repository.update(context_mock, pk=user_id, username=username)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_user_delete_ok():
    # GIVEN
    user_id = fake.random_int(min=1, max=10)

    # MOCK
    mock_user = User(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(fake.password(length=8)),
        person_id=fake.random_int(min=1, max=999),
    )
    context_mock = ContextMock.context_session_mock(return_value=mock_user)

    # WHEN
    await user_repository.delete(context_mock, pk=user_id)

    # THEN
    session: SessionIOMock = cast(SessionIOMock, context_mock.session)
    assert session._delete_count == 1


@pytest.mark.asyncio
async def test_user_delete_error():
    # MOCK
    error_message = 'insert or update on table "user" violates foreign key constraint "user_some_column_fkey"'
    context_mock = ContextMock.context_session_mock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # GIVEN
    user_id = fake.random_int(min=10000, max=999999)

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await user_repository.delete(context_mock, pk=user_id)

    # THEN
    assert error_message in str(exc_info.value)
