from fastapi import FastAPI

from app.controllers import auth_controller, person_controller, user_controller


def init_app(app: FastAPI):
    app.include_router(auth_controller.router)
    app.include_router(person_controller.router)
    app.include_router(user_controller.router)


__all__ = ("init_app",)
