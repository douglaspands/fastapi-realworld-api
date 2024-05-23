from copy import copy
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.core.database import SessionIO
from server.models.person_model import Person
from server.resources.person_resource import (
    CreatePerson,
    UpdatePerson,
    UpdatePersonOptional,
)
from server.services import person_service
from tests.mocks.context_mock import ContextMock

fake = Faker("pt_BR")
Faker.seed(0)


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_get_person_ok(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 1

    # MOCK
    person_mock = Person(
        id=person_id, first_name=fake.first_name(), last_name=fake.last_name()
    )
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.get.return_value = person_mock

    # WHEN
    res = await person_service.get_person(context_mock, person_id=person_id)

    # THEN
    assert res.id == person_id
    assert res.first_name and isinstance(res.first_name, str)
    assert res.last_name and isinstance(res.last_name, str)


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_get_person_not_found(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 9999

    # MOCK
    error_message = "No row was found when one was required"
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.get.side_effect = NoResultFound(error_message)

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await person_service.get_person(context_mock, person_id=person_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_get_all_persons_ok(person_repository_mock: AsyncMock):
    # MOCK
    person_mock = [
        Person(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
        for idx in range(10)
    ]
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.get_all.return_value = person_mock

    # WHEN
    res = await person_service.get_all_persons(context_mock)

    # THEN
    assert len(res) == len(person_mock)
    for idx in range(len(person_mock)):
        assert res[idx].id == person_mock[idx].id
        assert res[idx].first_name == person_mock[idx].first_name
        assert res[idx].last_name == person_mock[idx].last_name


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_create_person_ok(person_repository_mock: AsyncMock):
    # GIVEN
    create_person = CreatePerson(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()

    async def create_mock(session: SessionIO, person: Person):
        person.id = 1

    person_repository_mock.create = create_mock

    # WHEN
    person = await person_service.create_person(
        context_mock, create_person=create_person
    )

    # THEN
    assert person.id and person.id == 1
    assert person.first_name == create_person.first_name
    assert person.last_name == create_person.last_name


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_create_person_error(person_repository_mock: AsyncMock):
    # GIVEN
    create_person = CreatePerson(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.create.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_service.create_person(context_mock, create_person=create_person)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_update_person_ok(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 1
    update_person = UpdatePerson(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()

    async def update_mock(session: SessionIO, pk: int, **values):
        return Person(id=pk, **values)

    person_repository_mock.update = update_mock

    # WHEN
    person = await person_service.update_person(
        context_mock, person_id=person_id, update_person=update_person
    )

    # THEN
    assert person.id == person_id
    assert person.first_name == update_person.first_name
    assert person.last_name == update_person.last_name


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_update_person_error(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 1
    update_person = UpdatePerson(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.update.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_service.update_person(
            context_mock, person_id=person_id, update_person=update_person
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_update_person_optional_ok(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 1
    update_person = UpdatePersonOptional(first_name=fake.first_name())  # type: ignore

    # MOCK
    context_mock = ContextMock.context_session_mock()
    person_mock = Person(
        id=person_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )

    async def update_mock(session: SessionIO, pk: int, **values):
        person = copy(person_mock)
        for k, v in values.items():
            setattr(person, k, v)
        return person

    person_repository_mock.update = update_mock

    # WHEN
    person = await person_service.update_person_optional(
        context_mock, person_id=person_id, update_person=update_person
    )

    # THEN
    assert person.id == person_id
    assert person.first_name != person_mock.first_name
    assert person.first_name == update_person.first_name
    assert person.last_name == person_mock.last_name


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_update_person_optional_error(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 999999
    update_person = UpdatePersonOptional(first_name=fake.first_name())  # type: ignore

    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.update.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_service.update_person_optional(
            context_mock, person_id=person_id, update_person=update_person
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_delete_person_ok(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 1

    # MOCK
    context_mock = ContextMock.context_session_mock()

    # WHEN
    await person_service.delete_person(context_mock, person_id=person_id)

    # THEN
    assert True


@pytest.mark.asyncio
@patch("server.services.person_service.person_repository", new_callable=AsyncMock)
async def test_delete_person_error(person_repository_mock: AsyncMock):
    # GIVEN
    person_id = 999999

    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    person_repository_mock.delete.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_service.delete_person(context_mock, person_id=person_id)

    # THEN
    assert error_message in str(exc_info.value)
