from copy import copy
from typing import cast

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.models.people_model import People
from server.repositories import people_repository
from tests.mocks.async_session_mock import SessionIO, SessionIOMock

fake = Faker("pt_BR")
Faker.seed(0)


@pytest.mark.asyncio
async def test_people_get_by_pk_ok():
    # GIVEN
    people_id = 1

    # MOCK
    people_mock = People(
        id=people_id, first_name=fake.first_name(), last_name=fake.last_name()
    )
    session_mock = SessionIOMock.cast(return_value=people_mock)

    # WHEN
    res = await people_repository.get(session=session_mock, pk=people_id)

    # THEN
    assert res.id == people_id
    assert res.first_name and isinstance(res.first_name, str)
    assert res.last_name and isinstance(res.last_name, str)


@pytest.mark.asyncio
async def test_people_get_by_pk_not_found():
    # GIVEN
    people_id = 9999

    # MOCK
    error_message = "No row was found when one was required"
    session_mock = SessionIOMock.cast(side_effect=NoResultFound(error_message))

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await people_repository.get(session=session_mock, pk=people_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_people_get_all_ok():
    # MOCK
    people_mock = [
        People(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
        for idx in range(10)
    ]
    session_mock = SessionIOMock.cast(return_value=people_mock)

    # WHEN
    res = await people_repository.get_all(session=session_mock)

    # THEN
    assert len(res) == len(people_mock)
    for idx in range(len(people_mock)):
        assert res[idx].id == people_mock[idx].id
        assert res[idx].first_name == people_mock[idx].first_name
        assert res[idx].last_name == people_mock[idx].last_name


@pytest.mark.asyncio
async def test_people_save_ok():
    # GIVEN
    create_people = People(first_name=fake.first_name(), last_name=fake.last_name())

    # MOCK
    session_mock = SessionIOMock.cast()

    # WHEN
    await people_repository.create(session=session_mock, people=create_people)

    # THEN
    assert create_people.id and isinstance(create_people.id, int)
    assert create_people.id > 0


@pytest.mark.asyncio
async def test_people_save_error():
    # GIVEN
    create_people = People(first_name=fake.first_name(), last_name=fake.last_name())

    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    session_mock = SessionIOMock.cast(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_repository.create(session=session_mock, people=create_people)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_people_update_ok():
    # MOCK
    mock_people = People(
        id=fake.random_int(min=1, max=10),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    session_mock = SessionIOMock.cast(return_value=copy(mock_people))

    # GIVEN
    people_id = mock_people.id
    first_name = fake.first_name()

    # WHEN
    people_updated = await people_repository.update(
        session=session_mock, pk=people_id, first_name=first_name
    )

    # THEN
    assert people_updated.id == people_id
    assert people_updated.first_name == first_name


@pytest.mark.asyncio
async def test_people_update_error():
    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    session_mock = SessionIOMock.cast(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # GIVEN
    people_id = fake.random_int(min=10000, max=999999)
    first_name = fake.first_name()

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_repository.update(
            session=session_mock, pk=people_id, first_name=first_name
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_people_delete_ok():
    # MOCK
    mock_people = People(
        id=fake.random_int(min=1, max=10),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    session_mock = SessionIOMock(return_value=mock_people)

    # GIVEN
    people_id = mock_people.id

    # WHEN
    await people_repository.delete(session=cast(SessionIO, session_mock), pk=people_id)

    # THEN
    assert session_mock._delete_count == 1


@pytest.mark.asyncio
async def test_people_delete_error():
    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    session_mock = SessionIOMock.cast(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # GIVEN
    people_id = fake.random_int(min=10000, max=999999)

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_repository.delete(session=session_mock, pk=people_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_people_get_or_create_ok_01():
    # MOCK
    people_mock = People(
        id=fake.random_int(min=1, max=999),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    session_mock = SessionIOMock.cast(return_value=[people_mock])

    # GIVEN
    people = People(
        first_name=people_mock.first_name,
        last_name=people_mock.last_name,
    )

    # WHEN
    res = await people_repository.get_or_create(session=session_mock, people=people)

    # THEN
    assert res.id == people_mock.id
    assert res.first_name == people_mock.first_name
    assert res.last_name == people_mock.last_name


@pytest.mark.asyncio
async def test_people_get_or_create_ok_02():
    # MOCK
    session_mock = SessionIOMock.cast(return_value=[])

    # GIVEN
    people = People(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )

    # WHEN
    res = await people_repository.get_or_create(session=session_mock, people=people)

    # THEN
    assert isinstance(res.id, int)
    assert res.first_name == people.first_name
    assert res.last_name == people.last_name
