from fastapi import FastAPI

from server.core import router


def create_app() -> FastAPI:
    app = FastAPI()
    router.init_app(app)
    return app


__all__ = ("create_app",)
