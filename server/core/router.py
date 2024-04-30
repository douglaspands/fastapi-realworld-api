from fastapi import FastAPI

from server.controllers.user_controller import router as user_router


def init_app(app: FastAPI):
    app.include_router(user_router)


__all__ = ("init_app",)
