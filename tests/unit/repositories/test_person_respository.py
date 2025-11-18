from copy import copy
from typing import cast

import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.models.person_model import Person
from app.repositories import person_repository
from tests.unit.mocks.context_mock import ContextMock

fake = Faker("pt_BR")
Faker.seed(0)


@pytest.mark.asyncio
async def test_person_get_by_pk_ok():
    # GIVEN
    person_id = 1

    # MOCK
    person_mock = Person(
        id=person_id, first_name=fake.first_name(), last_name=fake.last_name()
    )
    context_mock = ContextMock.context_session_mock(return_value=person_mock)

    # WHEN
    res = await person_repository.get(context_mock, pk=person_id)

    # THEN
    assert res.id == person_id
    assert res.first_name and isinstance(res.first_name, str)
    assert res.last_name and isinstance(res.last_name, str)


@pytest.mark.asyncio
async def test_person_get_by_pk_not_found():
    # GIVEN
    person_id = 9999

    # MOCK
    error_message = "No row was found when one was required"
    context_mock = ContextMock.context_session_mock(
        side_effect=NoResultFound(error_message)
    )

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await person_repository.get(context_mock, pk=person_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_person_get_all_ok():
    # MOCK
    person_mock = [
        Person(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
        for idx in range(10)
    ]
    context_mock = ContextMock.context_session_mock(return_value=person_mock)

    # WHEN
    res = await person_repository.get_all(context_mock)

    # THEN
    assert len(res) == len(person_mock)
    for idx in range(len(person_mock)):
        assert res[idx].id == person_mock[idx].id
        assert res[idx].first_name == person_mock[idx].first_name
        assert res[idx].last_name == person_mock[idx].last_name


@pytest.mark.asyncio
async def test_person_save_ok():
    # GIVEN
    create_person = Person(first_name=fake.first_name(), last_name=fake.last_name())

    # MOCK
    context_mock = ContextMock.context_session_mock()

    # WHEN
    await person_repository.create(context_mock, person=create_person)

    # THEN
    assert create_person.id and isinstance(create_person.id, int)
    assert create_person.id > 0


@pytest.mark.asyncio
async def test_person_save_error():
    # GIVEN
    create_person = Person(first_name=fake.first_name(), last_name=fake.last_name())

    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_repository.create(context_mock, person=create_person)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_person_update_ok():
    # MOCK
    mock_person = Person(
        id=fake.random_int(min=1, max=10),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    context_mock = ContextMock.context_session_mock(return_value=copy(mock_person))
    # GIVEN
    person_id = cast(int, mock_person.id)
    first_name = fake.first_name()

    # WHEN
    person_updated = await person_repository.update(
        context_mock, pk=person_id, first_name=first_name
    )

    # THEN
    assert person_updated.id == person_id
    assert person_updated.first_name == first_name


@pytest.mark.asyncio
async def test_person_update_error():
    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # GIVEN
    person_id = fake.random_int(min=10000, max=999999)
    first_name = fake.first_name()

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_repository.update(
            context_mock, pk=person_id, first_name=first_name
        )

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_person_delete_ok():
    # MOCK
    mock_person = Person(
        id=fake.random_int(min=1, max=10),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    context_mock = ContextMock.context_session_mock(return_value=mock_person)

    # GIVEN
    person_id = cast(int, mock_person.id)

    # WHEN
    await person_repository.delete(context_mock, pk=person_id)

    # THEN
    assert getattr(context_mock.session, "_delete_count") == 1


@pytest.mark.asyncio
async def test_person_delete_error():
    # MOCK
    error_message = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    context_mock = ContextMock.context_session_mock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # GIVEN
    person_id = fake.random_int(min=10000, max=999999)

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await person_repository.delete(context_mock, pk=person_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_person_get_or_create_ok_01():
    # MOCK
    person_mock = Person(
        id=fake.random_int(min=1, max=999),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    context_mock = ContextMock.context_session_mock(return_value=[person_mock])

    # GIVEN
    person = Person(
        first_name=person_mock.first_name,
        last_name=person_mock.last_name,
    )

    # WHEN
    res = await person_repository.get_or_create(context_mock, person=person)

    # THEN
    assert res.id == person_mock.id
    assert res.first_name == person_mock.first_name
    assert res.last_name == person_mock.last_name


@pytest.mark.asyncio
async def test_person_get_or_create_ok_02():
    # MOCK
    context_mock = ContextMock.context_session_mock(return_value=[])

    # GIVEN
    person = Person(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )

    # WHEN
    res = await person_repository.get_or_create(context_mock, person=person)

    # THEN
    assert isinstance(res.id, int)
    assert res.first_name == person.first_name
    assert res.last_name == person.last_name
