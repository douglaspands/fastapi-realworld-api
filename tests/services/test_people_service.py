import pytest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.models.people_model import People
from server.resources.people_resources import CreatePeople
from server.services import people_service
from tests.mocks.async_session_mock import AsyncSessionMock

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
    session_mock = AsyncSessionMock(return_value=people_mock)

    # WHEN
    res = await people_service.get_people(session=session_mock, pk=people_id)

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
    session_mock = AsyncSessionMock(side_effect=NoResultFound(error_message))

    # WHEN
    with pytest.raises(NoResultFound) as exc_info:
        await people_service.get_people(session=session_mock, pk=people_id)

    # THEN
    assert error_message in str(exc_info.value)


@pytest.mark.asyncio
async def test_people_get_all_ok():
    # MOCK
    people_mock = [
        People(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
        for idx in range(10)
    ]
    session_mock = AsyncSessionMock(return_value=people_mock)

    # WHEN
    res = await people_service.all_people(session=session_mock)

    # THEN
    assert len(res) == len(people_mock)
    for idx in range(len(people_mock)):
        assert res[idx].id == people_mock[idx].id
        assert res[idx].first_name == people_mock[idx].first_name
        assert res[idx].last_name == people_mock[idx].last_name


@pytest.mark.asyncio
async def test_people_save_ok():
    # GIVEN
    create_people = CreatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    people_mock = People(
        first_name=create_people.first_name, last_name=create_people.last_name
    )
    session_mock = AsyncSessionMock(return_value=people_mock)

    # WHEN
    people = await people_service.create_people(
        session=session_mock, create_people=create_people
    )

    # THEN
    assert people.id and people.id > 0
    assert people.first_name == create_people.first_name
    assert people.last_name == create_people.last_name


@pytest.mark.asyncio
async def test_people_save_error():
    # GIVEN
    create_people = CreatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    error_message = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    session_mock = AsyncSessionMock(
        side_effect=IntegrityError(
            orig=Exception(error_message), params={}, statement=""
        )
    )

    # WHEN
    with pytest.raises(IntegrityError) as exc_info:
        await people_service.create_people(
            session=session_mock, create_people=create_people
        )

    # THEN
    assert error_message in str(exc_info.value)
