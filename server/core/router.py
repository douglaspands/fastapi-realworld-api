from fastapi import FastAPI

from server.controllers.auth_controller import router as auth_router
from server.controllers.person_controller import router as person_router
from server.controllers.user_controller import router as user_router


def init_app(app: FastAPI):
    app.include_router(router=auth_router)
    app.include_router(router=person_router)
    app.include_router(router=user_router)


__all__ = ("init_app",)
