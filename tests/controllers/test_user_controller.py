from datetime import datetime
from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock, patch

from faker import Faker

from server.controllers.user_controller import UpdateUser, UpdateUserOptional
from server.models.user_model import User as UserModel
from server.services.auth_service import check_access_token, crypt
from tests.mocks.context_mock import ContextMock
from tests.utils.http_client import HttpClient
from tests.utils.utils import snake_to_camel

fake = Faker("pt_BR")
Faker.seed(0)


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_get_user_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    user_id = fake.pyint(1, 999)

    # MOCK
    user_mock = UserModel(
        id=user_id,
        username=fake.user_name(),
        person_id=fake.pyint(1, 999),
        active=fake.pybool(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )

    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.get_user.return_value = user_mock

    # WHEN
    url = f"/users/v1/users/{user_id}"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": snake_to_camel(user_mock.model_dump(mode="json"))
    }


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_get_all_users_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN

    # MOCK
    user_mock = [
        UserModel(
            id=fake.pyint(1, 999),
            username=fake.user_name(),
            person_id=fake.pyint(1, 999),
            active=fake.pybool(),
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        for _ in range(fake.pyint(1, 10))
    ]
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.get_all_users.return_value = user_mock

    # WHEN
    url = "/users/v1/users"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [snake_to_camel(u.model_dump(mode="json")) for u in user_mock]
    }


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_get_all_users_nocontent(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN

    # MOCK
    user_mock: list[Any] = []
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.get_all_users.return_value = user_mock

    # WHEN
    url = "/users/v1/users"
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.NO_CONTENT


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_update_user_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    user_id = fake.pyint(1, 999)
    update_user = UpdateUser(  # type: ignore
        username=fake.user_name(),
        person_id=fake.pyint(1, 999),
        active=fake.pybool(),
    )

    # MOCK
    user_mock = UserModel(
        id=user_id,
        username=update_user.username,
        person_id=update_user.person_id,
        active=update_user.active,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.update_user.return_value = user_mock

    # WHEN
    url = f"/users/v1/users/{user_id}"
    response = httpclient.put(url, json=update_user.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.OK
    data: dict[str, Any] = response.json()["data"]
    assert not data.get("password")
    assert data.get("username") == update_user.username
    assert data.get("personId") == update_user.person_id
    assert data.get("active") == update_user.active


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_update_user_optional_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    user_id = fake.pyint(1, 999)
    update_user = UpdateUserOptional(  # type: ignore
        username=fake.user_name(),
    )

    # MOCK
    user_mock = UserModel(
        id=user_id,
        username=update_user.username,
        person_id=fake.pyint(1, 999),
        active=fake.pybool(),
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.update_user_optional.return_value = user_mock

    # WHEN
    url = f"/users/v1/users/{user_id}"
    response = httpclient.patch(url, json=update_user.model_dump())

    # THEN
    assert response.status_code == HTTPStatus.OK
    data: dict[str, Any] = response.json()["data"]
    assert data.get("username") == update_user.username
    assert not data.get("password")


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_delete_user_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    user_id = fake.pyint(1, 999)

    # MOCK
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.delete_user.return_value = True

    # WHEN
    url = f"/users/v1/users/{user_id}"
    response = httpclient.delete(url)

    # THEN
    assert response.status_code == HTTPStatus.OK


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_user_person_create_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    password = fake.password(10)
    create_user_person = {
        "username": fake.user_name(),
        "password": password,
        "passwordCheck": password,
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
    }

    # MOCK
    datetime_now = datetime.now()
    user_mock = UserModel(
        id=fake.pyint(1, 999),
        username=create_user_person["username"],
        password=crypt.hash_password(create_user_person["password"]),
        person_id=fake.pyint(1, 999),
        active=True,
        updated_at=datetime_now,
        created_at=datetime_now,
    )
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.create_user_person.return_value = user_mock

    # WHEN
    url = "/users/v1/user-person"
    response = httpclient.post(url, json=create_user_person)

    # THEN
    assert response.status_code == HTTPStatus.CREATED
    data: dict[str, Any] = response.json()["data"]
    assert not data.get("password")
    assert data.get("username") == create_user_person["username"]
    assert data.get("personId") == user_mock.person_id
    assert data.get("active") == user_mock.active


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_user_person_create_pw_no_match(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    create_user_person = {
        "username": fake.user_name(),
        "password": fake.password(10),
        "passwordCheck": fake.password(10),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
    }

    # MOCK
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )

    # WHEN
    url = "/users/v1/user-person"
    response = httpclient.post(url, json=create_user_person)

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "passwords do not match" in response.text


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_update_user_password_ok(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    user_id = fake.pyint(1, 999)
    new_password = fake.password(10)
    update_user_password = {
        "currentPassword": fake.password(10),
        "newPassword": new_password,
        "newPasswordCheck": new_password,
    }

    # MOCK
    datetime_now = datetime.now()
    user_mock = UserModel(
        id=user_id,
        username=fake.user_name(),
        password=crypt.hash_password(update_user_password["newPassword"]),
        person_id=fake.pyint(1, 999),
        active=True,
        updated_at=datetime_now,
        created_at=datetime_now,
    )
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.change_password.return_value = user_mock

    # WHEN
    url = f"/users/v1/users/{user_id}/change-password"
    response = httpclient.post(url, json=update_user_password)

    # THEN
    assert response.status_code == HTTPStatus.OK
    data: dict[str, Any] = response.json()["data"]
    assert not data.get("password")
    assert data.get("username") == user_mock.username
    assert data.get("personId") == user_mock.person_id
    assert data.get("active") == user_mock.active


@patch("server.controllers.user_controller.user_service", new_callable=AsyncMock)
def test_update_user_password_pw_no_match(
    user_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    user_id = fake.pyint(1, 999)
    update_user_password = {
        "currentPassword": fake.password(10),
        "newPassword": fake.password(10),
        "newPasswordCheck": fake.password(10),
    }

    # MOCK
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )

    # WHEN
    url = f"/users/v1/users/{user_id}/change-password"
    response = httpclient.post(url, json=update_user_password)

    # THEN
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "passwords do not match" in response.text
