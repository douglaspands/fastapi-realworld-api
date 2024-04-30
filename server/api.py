from server.core import api

app = api.create_app()

__all__ = ("app",)
