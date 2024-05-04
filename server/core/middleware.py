from typing import Awaitable, Callable

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response


def init_app(app: FastAPI):
    @app.middleware("http")
    async def catch_exception_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as err:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"errors": [{"message": str(err)}]},
            )
