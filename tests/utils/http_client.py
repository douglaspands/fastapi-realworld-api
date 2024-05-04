from typing import Any, Self, cast

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from httpx._transports.asgi import _ASGIApp


class HttpClientIO(AsyncClient):
    def __init__(self: Self, *args: Any, **kwargs: Any):
        self.app: FastAPI = kwargs.pop("app", None)
        kwargs["transport"] = ASGITransport(app=cast(_ASGIApp, self.app))
        super().__init__(*args, **kwargs)
