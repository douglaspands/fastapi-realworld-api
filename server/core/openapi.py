from http import HTTPStatus
from typing import Any, Dict, Union

from server.core.schema import ResponseBadRequest, ResponseErrors


def get_config() -> dict[str, Any]:
    return {
        "responses": response_generator(500),
        "with_google_fonts": True,
    }


def response_generator(*args: int) -> Dict[Union[int, str], Dict[str, Any]]:
    responses: Dict[Union[int, str], Dict[str, Any]] = {}
    for status in set(args):
        if status in HTTPStatus:
            if status in (204, 404):
                responses[status] = {"model": None}
            elif status in (400,):
                responses[status] = {"model": ResponseBadRequest}
            elif status not in (200, 201):
                responses[status] = {"model": ResponseErrors}
    return responses


__all__ = ("get_config", "response_generator")
