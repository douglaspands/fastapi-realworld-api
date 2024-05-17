from datetime import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from faker import Faker
from pydash import get
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.core.exceptions import BusinessError, NotFoundError
from server.models.people_model import People
from server.resources.people_resources import (
    CreatePeople,
    UpdatePeople,
    UpdatePeopleOptional,
)
from server.services.auth_service import check_access_token
from tests.mocks.context_mock import ContextMock
from tests.utils.http_client import HttpClient
from tests.utils.utils import snake_to_camel

fake = Faker("pt_BR")
Faker.seed(0)


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_get_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = 1

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_mock = People(
        id=people_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    people_service_mock.get_people.return_value = people_mock

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(people_mock.model_dump(mode="json"))
    }


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_get_people_not_found(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = 99999

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_service_mock.get_people.side_effect = NoResultFound(
        "No row was found when one was required"
    )

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NOT_FOUND


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_get_people_not_found_2(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = 99999

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_service_mock.get_people.side_effect = NotFoundError(
        "No row was found when one was required"
    )

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NOT_FOUND


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_get_people_internal_server_error(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = 500

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    message_error = 'insert or update on table "people" violates foreign key constraint "people_some_column_fkey"'
    people_service_mock.get_people.side_effect = IntegrityError(
        orig=Exception(message_error),
        params={},
        statement="",
    )

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert message_error in get(response.json(), "errors[0].message")


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_all_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_mock = [
        People(
            id=idx + 1,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        for idx in range(10)
    ]
    people_service_mock.all_people.return_value = people_mock

    # WHEN
    url = "/people/v1/people"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [snake_to_camel(p.model_dump(mode="json")) for p in people_mock]
    }


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_all_people_nocontent(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_service_mock.all_people.return_value = []

    # WHEN
    url = "/people/v1/people"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NO_CONTENT


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_create_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_mock = People(
        id=fake.pyint(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    people_service_mock.create_people.return_value = people_mock

    # GIVEN
    create_people = CreatePeople(
        first_name=people_mock.first_name, last_name=people_mock.last_name
    )

    # WHEN
    url = "/people/v1/people"
    response = httpclient.post(url, json=create_people.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "data": snake_to_camel(people_mock.model_dump(mode="json"))
    }


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_create_people_validation_error(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
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
    response = httpclient.post(url, json=create_people)

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_create_people_business_error(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_mock = People(
        id=fake.pyint(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    message_error = "Business error mock"
    people_service_mock.create_people.side_effect = BusinessError(message_error)

    # GIVEN
    create_people = CreatePeople(
        first_name=people_mock.first_name, last_name=people_mock.last_name
    )

    # WHEN
    url = "/people/v1/people"
    response = httpclient.post(url, json=create_people.model_dump(mode="json"))

    # THEN
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert message_error == get(response.json(), "errors[0].message")


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_update_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = fake.pyint()
    people_update = UpdatePeople(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_mock = People(
        id=people_id,
        first_name=people_update.first_name,
        last_name=people_update.last_name,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    people_service_mock.update_people.return_value = people_mock

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.put(url, json=people_update.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(people_mock.model_dump(mode="json"))
    }


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_update_people_optional_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = fake.pyint()
    people_update = UpdatePeopleOptional(first_name=fake.first_name())  # type: ignore

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    people_mock = People(
        id=people_id,
        first_name=people_update.first_name,
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    people_service_mock.update_people_optional.return_value = people_mock

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.patch(url, json=people_update.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(people_mock.model_dump(mode="json"))
    }


@patch("server.controllers.people_controller.people_service", new_callable=AsyncMock)
def test_delete_people_ok(
    people_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    people_id = fake.pyint()
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )

    # WHEN
    url = f"/people/v1/people/{people_id}"
    response = httpclient.delete(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
