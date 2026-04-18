import asyncio
import time

from typer import Typer

from app.infra import logging
from app.infra.context import get_context
from app.services import user_service

app = Typer(
    help="User related commands",
    no_args_is_help=True,
)


@app.command("check_old_password", help="Check old password")
def check_old_password():
    async def _():
        logger = logging.get_logger(f"{__name__}.check_old_password")

        time_begin = time.perf_counter()
        logger.info("check old password begin")

        async with get_context() as ctx:
            await user_service.check_old_password(ctx)

        time_end = time.perf_counter()
        logger.info(f"check old password cost {time_end - time_begin:.2f} seconds")

    asyncio.run(_())


__all__ = ("app",)
