from fastapi import FastAPI

from server.core import handler, middleware, openapi, router


def create_app() -> FastAPI:
    app = FastAPI(**openapi.get_config())
    middleware.init_app(app)
    handler.init_app(app)
    router.init_app(app)
    return app


__all__ = ("create_app",)
