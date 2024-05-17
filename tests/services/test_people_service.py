from copy import copy
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.core.database import SessionIO
from server.models.people_model import People
from server.resources.people_resource import (
    CreatePeople,
    UpdatePeople,
    UpdatePeopleOptional,
)
from server.services import people_service
from tests.mocks.context_mock import ContextMock

fake = Faker("pt_BR")
Faker.seed(0)


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_get_people_ok(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 1

    # MOCK
    people_mock = People(
        id=people_id, first_name=fake.first_name(), last_name=fake.last_name()
    )
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.get.return_value = people_mock

    # WHEN
    res = await people_service.get_people(context_mock, pk=people_id)

    # THEN
    assert res.id == people_id
    assert res.first_name and isinstance(res.first_name, str)
    assert res.last_name and isinstance(res.last_name, str)


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_get_people_not_found(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 9999

    # MOCK
    error_message = "No row was found when one was required"
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.get.side_effect = NoResultFound(error_message)

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await people_service.get_people(context_mock, pk=people_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_all_people_ok(people_repository_mock: AsyncMock):
    # MOCK
    people_mock = [
        People(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
        for idx in range(10)
    ]
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.get_all.return_value = people_mock

    # WHEN
    res = await people_service.all_people(context_mock)

    # THEN
    assert len(res) == len(people_mock)
    for idx in range(len(people_mock)):
        assert res[idx].id == people_mock[idx].id
        assert res[idx].first_name == people_mock[idx].first_name
        assert res[idx].last_name == people_mock[idx].last_name


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_create_people_ok(people_repository_mock: AsyncMock):
    # GIVEN
    create_people = CreatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()

    async def create_mock(session: SessionIO, people: People):
        people.id = 1

    people_repository_mock.create = create_mock

    # WHEN
    people = await people_service.create_people(
        context_mock, create_people=create_people
    )

    # THEN
    assert people.id and people.id == 1
    assert people.first_name == create_people.first_name
    assert people.last_name == create_people.last_name


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_create_people_error(people_repository_mock: AsyncMock):
    # GIVEN
    create_people = CreatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.create.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_service.create_people(context_mock, create_people=create_people)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_update_people_ok(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 1
    update_people = UpdatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()

    async def update_mock(session: SessionIO, pk: int, **values):
        return People(id=pk, **values)

    people_repository_mock.update = update_mock

    # WHEN
    people = await people_service.update_people(
        context_mock, pk=people_id, update_people=update_people
    )

    # THEN
    assert people.id == people_id
    assert people.first_name == update_people.first_name
    assert people.last_name == update_people.last_name


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_update_people_error(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 1
    update_people = UpdatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.update.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_service.update_people(
            context_mock, pk=people_id, update_people=update_people
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_update_people_optional_ok(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 1
    update_people = UpdatePeopleOptional(first_name=fake.first_name())  # type: ignore

    # MOCK
    context_mock = ContextMock.context_session_mock()
    people_mock = People(
        id=people_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )

    async def update_mock(session: SessionIO, pk: int, **values):
        people = copy(people_mock)
        for k, v in values.items():
            setattr(people, k, v)
        return people

    people_repository_mock.update = update_mock

    # WHEN
    people = await people_service.update_people_optional(
        context_mock, pk=people_id, update_people=update_people
    )

    # THEN
    assert people.id == people_id
    assert people.first_name != people_mock.first_name
    assert people.first_name == update_people.first_name
    assert people.last_name == people_mock.last_name


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_update_people_optional_error(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 999999
    update_people = UpdatePeopleOptional(first_name=fake.first_name())  # type: ignore

    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.update.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_service.update_people_optional(
            context_mock, pk=people_id, update_people=update_people
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_delete_people_ok(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 1

    # MOCK
    context_mock = ContextMock.context_session_mock()

    # WHEN
    await people_service.delete_people(context_mock, pk=people_id)

    # THEN
    assert True


@pytest.mark.asyncio
@patch("server.services.people_service.people_repository", new_callable=AsyncMock)
async def test_delete_people_error(people_repository_mock: AsyncMock):
    # GIVEN
    people_id = 999999

    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    context_mock = ContextMock.context_session_mock()
    people_repository_mock.delete.side_effect = IntegrityError(
        orig=Exception(error_message), params={}, statement=""
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_service.delete_people(context_mock, pk=people_id)

    # THEN
    assert error_message in str(exc_info.value)
