from fastapi import FastAPI

from app.infra import handler, middleware, openapi, router
from app.infra.settings import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.openapi_description,
        with_google_fonts=True,
    )
    middleware.init_app(app)
    handler.init_app(app)
    router.init_app(app)
    openapi.init_app(app)
    return app


__all__ = ("create_app",)
