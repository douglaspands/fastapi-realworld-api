from typer import Typer

from app.command import user_command
from app.infra import logging
from app.infra.settings import get_settings


def create_app(is_test: bool = False) -> Typer:
    logging.set_logging_nonwebapp()
    settings = get_settings()

    app = Typer(
        name=f"{settings.app_name} ({settings.app_version})",
        help=settings.app_description,
        add_completion=False,
        no_args_is_help=True,
    )
    app.add_typer(user_command.app, name="user")
    return app


__all__ = ("create_app",)
