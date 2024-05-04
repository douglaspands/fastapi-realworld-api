from fastapi import FastAPI

from server.core import handler, middleware, router


def create_app() -> FastAPI:
    app = FastAPI()
    middleware.init_app(app)
    handler.init_app(app)
    router.init_app(app)
    return app


__all__ = ("create_app",)
