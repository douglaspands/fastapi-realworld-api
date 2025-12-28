from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from tests.unit.utils.http_client import HttpClient


def test_get_health_readness_ok(httpclient: HttpClient):
    # GIVEN
    url = "/health/v1/readness"

    # WHEN
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert "OK" in response.text


@patch("app.controllers.health_controller.ping_database", new_callable=AsyncMock)
def test_get_health_liveness_ok_01(
    mock_ping_database: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    url = "/health/v1/liveness"

    # MOCK
    mock_ping_database.return_value = True

    # WHEN
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert "OK" in response.text


def test_get_health_liveness_ok_02(
    httpclient: HttpClient,
):
    # GIVEN
    url = "/health/v1/liveness"

    # WHEN
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.OK
    assert "OK" in response.text


@patch("app.controllers.health_controller.ping_database", new_callable=AsyncMock)
def test_get_health_liveness_error(
    mock_ping_database: AsyncMock,
    httpclient: HttpClient,
):
    # GIVEN
    url = "/health/v1/liveness"

    # MOCK
    mock_ping_database.side_effect = Exception("Database is not available")

    # WHEN
    response = httpclient.get(url)

    # THEN
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Database is not available" in response.text
