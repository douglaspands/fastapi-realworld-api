from datetime import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from faker import Faker
from pydash import get
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.core.exceptions import BusinessError, NotFoundError
from server.models.person_model import Person
from server.resources.person_resource import (
    CreatePerson,
    UpdatePerson,
    UpdatePersonOptional,
)
from server.services.auth_service import check_access_token
from tests.mocks.context_mock import ContextMock
from tests.utils.http_client import HttpClient
from tests.utils.utils import snake_to_camel

fake = Faker("pt_BR")
Faker.seed(0)


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_get_person_ok(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = 1

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_mock = Person(
        id=person_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    person_service_mock.get_person.return_value = person_mock

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(person_mock.model_dump(mode="json"))
    }


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_get_person_not_found(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = 99999

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_service_mock.get_person.side_effect = NoResultFound(
        "No row was found when one was required"
    )

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NOT_FOUND


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_get_person_not_found_2(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = 99999

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_service_mock.get_person.side_effect = NotFoundError(
        "No row was found when one was required"
    )

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NOT_FOUND


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_get_person_internal_server_error(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = 500

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    message_error = 'insert or update on table "person" violates foreign key constraint "person_some_column_fkey"'
    person_service_mock.get_person.side_effect = IntegrityError(
        orig=Exception(message_error),
        params={},
        statement="",
    )

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert message_error in get(response.json(), "errors[0].message")


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_get_all_persons_ok(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_mock = [
        Person(
            id=idx + 1,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        for idx in range(10)
    ]
    person_service_mock.get_all_persons.return_value = person_mock

    # WHEN
    url = "/persons/v1/persons"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [snake_to_camel(p.model_dump(mode="json")) for p in person_mock]
    }


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_all_person_nocontent(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_service_mock.get_all_persons.return_value = []

    # WHEN
    url = "/persons/v1/persons"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NO_CONTENT


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_create_person_ok(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_mock = Person(
        id=fake.pyint(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    person_service_mock.create_person.return_value = person_mock

    # GIVEN
    create_person = CreatePerson(
        first_name=person_mock.first_name, last_name=person_mock.last_name
    )

    # WHEN
    url = "/persons/v1/persons"
    response = httpclient.post(url, json=create_person.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "data": snake_to_camel(person_mock.model_dump(mode="json"))
    }


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_create_person_validation_error(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )

    # GIVEN
    create_person = {
        "firstName": fake.first_name(),
        "lastName": None,
    }

    # WHEN
    url = "/persons/v1/persons"
    response = httpclient.post(url, json=create_person)

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_create_person_business_error(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_mock = Person(
        id=fake.pyint(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    message_error = "Business error mock"
    person_service_mock.create_person.side_effect = BusinessError(message_error)

    # GIVEN
    create_person = CreatePerson(
        first_name=person_mock.first_name, last_name=person_mock.last_name
    )

    # WHEN
    url = "/persons/v1/persons"
    response = httpclient.post(url, json=create_person.model_dump(mode="json"))

    # THEN
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert message_error == get(response.json(), "errors[0].message")


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_update_person_ok(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = fake.pyint()
    person_update = UpdatePerson(
        first_name=fake.first_name(), last_name=fake.last_name()
    )

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_mock = Person(
        id=person_id,
        first_name=person_update.first_name,
        last_name=person_update.last_name,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    person_service_mock.update_person.return_value = person_mock

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.put(url, json=person_update.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(person_mock.model_dump(mode="json"))
    }


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_update_person_optional_ok(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = fake.pyint()
    person_update = UpdatePersonOptional(first_name=fake.first_name())  # type: ignore

    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )
    person_mock = Person(
        id=person_id,
        first_name=person_update.first_name,
        last_name=fake.last_name(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    person_service_mock.update_person_optional.return_value = person_mock

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.patch(url, json=person_update.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(person_mock.model_dump(mode="json"))
    }


@patch("server.controllers.person_controller.person_service", new_callable=AsyncMock)
def test_delete_person_ok(
    person_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    person_id = fake.pyint()
    # MOCK
    context_mock = ContextMock.context_session_mock()
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: context_mock
    )

    # WHEN
    url = f"/persons/v1/persons/{person_id}"
    response = httpclient.delete(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
