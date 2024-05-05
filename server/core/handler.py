from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from starlette.exceptions import HTTPException as StarletteHTTPException


async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": exc.errors()},
    )


async def not_found_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"errors": [{"message": str(exc)}]},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=(
            None
            if exc.status_code
            in (status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND)
            else {"errors": [{"message": exc.detail}]}
        ),
    )


def init_app(app: FastAPI):
    app.exception_handler(RequestValidationError)(request_validation_error_handler)
    app.exception_handler(NoResultFound)(not_found_handler)
    app.exception_handler(StarletteHTTPException)(http_exception_handler)
