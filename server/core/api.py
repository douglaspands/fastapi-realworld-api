from fastapi import FastAPI

from server.core import handler, router


def create_app() -> FastAPI:
    app = FastAPI()
    handler.init_app(app)
    router.init_app(app)
    return app


__all__ = ("create_app",)
