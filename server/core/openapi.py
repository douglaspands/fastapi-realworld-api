from http import HTTPStatus
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydash import unset

from server.core.schema import ResponseBadRequest, ResponseErrors

HTTP_422 = {
    "description": "Unprocessable Entity",
    "content": {
        "application/json": {"schema": {"$ref": "#/components/schemas/ResponseErrors"}}
    },
}


def response_generator(*args: int) -> dict[int | str, dict[str, Any]]:
    responses: dict[int | str, dict[str, Any]] = {}
    for status in set(args):
        if status in HTTPStatus:
            if status in (204, 404):
                responses[status] = {"model": None}
            elif status in (400,):
                responses[status] = {"model": ResponseBadRequest}
            elif status not in (200, 201):
                responses[status] = {"model": ResponseErrors}
    return responses


def init_app(app: FastAPI):
    app.router.responses = response_generator(500)
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        summary=app.summary,
        description=app.description,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,
        webhooks=app.webhooks.routes,
        tags=app.openapi_tags,
        servers=app.servers,
        separate_input_output_schemas=app.separate_input_output_schemas,
    )
    unset(openapi_schema, "components.schemas.HTTPValidationError")
    for path_value in dict(openapi_schema["paths"]).values():
        for method_value in dict(path_value).values():
            if dict(method_value["responses"]).get("422"):
                method_value["responses"]["422"] = HTTP_422
    app.openapi_schema = openapi_schema


__all__ = ("init_app", "response_generator")
