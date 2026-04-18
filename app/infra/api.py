from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.infra import handler, logging, middleware, openapi, router
from app.infra.logging import set_logging_webapp
from app.infra.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.get_logger(__name__)
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")


def create_app(is_test: bool = False) -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        with_google_fonts=True,
        lifespan=lifespan,
        root_path=settings.root_path,
    )
    middleware.init_app(app)
    handler.init_app(app)
    router.init_app(app)
    app.get("/", include_in_schema=False)(
        lambda: RedirectResponse(url=f"{settings.root_path}/docs")
    )
    openapi.init_app(app)
    if not is_test:
        set_logging_webapp(app)
    return app


__all__ = ("create_app",)
