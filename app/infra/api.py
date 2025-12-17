from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infra import handler, middleware, openapi, router
from app.infra.database import ping_database
from app.infra.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_ready = await ping_database()
    if not db_ready:
        raise Exception("Database is not available")
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        with_google_fonts=True,
        lifespan=lifespan,
    )
    middleware.init_app(app)
    handler.init_app(app)
    router.init_app(app)
    openapi.init_app(app)
    return app


__all__ = ("create_app",)
