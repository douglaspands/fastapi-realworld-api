from datetime import datetime
from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock, patch

from faker import Faker

from server.controllers.user_controller import UpdateUser, UpdateUserOptional
from server.models.user_model import User as UserModel
from server.services.auth_service import check_access_token
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
    pk = fake.pyint(1, 999)

    # MOCK
    user_mock = UserModel(
        id=pk,
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
    url = f"/users/v1/users/{pk}"
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
    user_service_mock.all_users.return_value = user_mock

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
    user_service_mock.all_users.return_value = user_mock

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
    pk = fake.pyint(1, 999)
    update_user = UpdateUser(  # type: ignore
        username=fake.user_name(),
        person_id=fake.pyint(1, 999),
        active=fake.pybool(),
    )

    # MOCK
    user_mock = UserModel(
        id=pk,
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
    url = f"/users/v1/users/{pk}"
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
    pk = fake.pyint(1, 999)
    update_user = UpdateUserOptional(  # type: ignore
        username=fake.user_name(),
    )

    # MOCK
    user_mock = UserModel(
        id=pk,
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
    url = f"/users/v1/users/{pk}"
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
    pk = fake.pyint(1, 999)

    # MOCK
    httpclient.current_app.dependency_overrides[check_access_token] = (
        lambda: ContextMock.context_session_mock()
    )
    user_service_mock.delete_user.return_value = True

    # WHEN
    url = f"/users/v1/users/{pk}"
    response = httpclient.delete(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
