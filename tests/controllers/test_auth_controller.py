from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from faker import Faker

from server.core.context import get_context_with_request
from server.resources.token_resource import Token
from server.services.auth_service import credentials_error
from tests.mocks.context_mock import ContextMock
from tests.utils.http_client import HttpClient

fake = Faker("pt_BR")
Faker.seed(0)


@patch("server.controllers.auth_controller.auth_service", new_callable=AsyncMock)
def test_get_token_ok(
    auth_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    username = fake.user_name()
    password = fake.password(8)

    # MOCK
    httpclient.current_app.dependency_overrides[get_context_with_request] = (
        lambda: ContextMock.context_session_mock()
    )
    token_mock = Token(access_token=fake.password(20))
    auth_service_mock.authenticate_user.return_value = token_mock

    # WHEN
    url = "/auth/v1/token"
    response = httpclient.post(url, data={"username": username, "password": password})

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert response.json() == token_mock.model_dump(mode="json")


@patch("server.controllers.auth_controller.auth_service", new_callable=AsyncMock)
def test_get_token_error(
    auth_service_mock: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    username = fake.user_name()
    password = fake.password(8)

    # MOCK
    httpclient.current_app.dependency_overrides[get_context_with_request] = (
        lambda: ContextMock.context_session_mock()
    )
    auth_service_mock.authenticate_user.side_effect = credentials_error

    # WHEN
    url = "/auth/v1/token"
    response = httpclient.post(url, data={"username": username, "password": password})

    # THEN
    assert response.status_code == HTTPStatus.UNAUTHORIZED
