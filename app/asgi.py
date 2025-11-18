from app.infra import api

app = api.create_app()

__all__ = ("app",)
