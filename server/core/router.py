from fastapi import FastAPI

from server.controllers.people_controller import router as people_router


def init_app(app: FastAPI):
    app.include_router(people_router)


__all__ = ("init_app",)
