from typing import Any, Self

from fastapi import FastAPI
from fastapi.testclient import TestClient


class HttpClient(TestClient):
    current_app: FastAPI

    def __init__(self: Self, *args: Any, **kwargs: Any):
        for arg in args:
            if isinstance(arg, FastAPI):
                self.current_app: FastAPI = arg
        if not self.current_app:
            self.current_app = kwargs["app"]
        super().__init__(*args, **kwargs)


__all__ = ("HttpClient",)
