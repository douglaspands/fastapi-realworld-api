from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from pydash import camel_case
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.controllers.people_controller import get_sessionio
from server.models.people_model import People
from server.resources.people_resources import CreatePeople
from tests.mocks.async_session_mock import SessionIOMock
from tests.utils.http_client import HttpClientIO

fake = Faker("pt_BR")
Faker.seed(0)


def snake_to_camel(d: dict[str, Any]) -> dict[str, Any]:
    r: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, (list, set, tuple)):
            il = []
            for i in v:
                il.append(snake_to_camel(i) if isinstance(i, dict) else i)
            r[camel_case(k)] = il
        else:
            r[camel_case(k)] = snake_to_camel(v) if isinstance(v, dict) else v
    return r


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_get_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # GIVEN
    people_id = 1

    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_mock = People(
        id=people_id, first_name=fake.first_name(), last_name=fake.last_name()
    )
    people_service_mock.get_people.return_value = people_mock

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = await httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": snake_to_camel(people_mock.model_dump())}


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_get_people_not_found(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # GIVEN
    people_id = 99999

    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_service_mock.get_people.side_effect = NoResultFound(
        "No row was found when one was required"
    )

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = await httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_get_people_internal_server_error(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # GIVEN
    people_id = 500

    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_service_mock.get_people.side_effect = IntegrityError(
        orig=Exception(
            'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
        ),
        params={},
        statement="",
    )

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = await httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_all_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_mock = [
        People(id=idx + 1, first_name=fake.first_name(), last_name=fake.last_name())
        for idx in range(10)
    ]
    people_service_mock.all_people.return_value = people_mock

    # WHEN
    url = "/people/v1/people"
    response = await httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [snake_to_camel(p.model_dump()) for p in people_mock]
    }


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_all_people_nocontent(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_service_mock.all_people.return_value = []

    # WHEN
    url = "/people/v1/people"
    response = await httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_create_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_mock = People(
        id=fake.pyint(), first_name=fake.first_name(), last_name=fake.last_name()
    )
    people_service_mock.create_people.return_value = people_mock

    # GIVEN
    create_people = CreatePeople(
        first_name=people_mock.first_name, last_name=people_mock.last_name
    )

    # WHEN
    url = "/people/v1/people"
    response = await httpclient.post(url, json=create_people.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"data": snake_to_camel(people_mock.model_dump())}


@pytest.mark.asyncio
@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
async def test_create_people_validation_error(
    people_service_mock: AsyncMock,
    httpclient: HttpClientIO,
):
    # MOCK
    session_mock = SessionIOMock.cast()
    httpclient.app.dependency_overrides[get_sessionio] = lambda: session_mock
    people_mock = People(
        id=fake.pyint(), first_name=fake.first_name(), last_name=fake.last_name()
    )
    people_service_mock.create_people.return_value = people_mock

    # GIVEN
    create_people = {
        "firstName": people_mock.first_name,
        "lastName": None,
    }

    # WHEN
    url = "/people/v1/people"
    response = await httpclient.post(url, json=create_people)

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST
