from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import NoResultFound
from starlette.exceptions import HTTPException as StarletteHTTPException

from server.core.exceptions import BusinessError, NotFoundError


async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": exc.errors()},
    )


async def not_found_handler(request: Request, exc: Exception):
    return Response(status_code=status.HTTP_404_NOT_FOUND)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code in (status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND):
        return Response(status_code=exc.status_code)
    else:
        return JSONResponse(
            status_code=exc.status_code, content={"errors": [{"message": exc.detail}]}
        )


def init_app(app: FastAPI):
    app.exception_handler(RequestValidationError)(request_validation_error_handler)
    app.exception_handler(NoResultFound)(not_found_handler)
    app.exception_handler(NotFoundError)(not_found_handler)
    app.exception_handler(StarletteHTTPException)(http_exception_handler)
    app.exception_handler(HTTPException)(http_exception_handler)
    app.exception_handler(BusinessError)(http_exception_handler)


__all__ = ("init_app",)
