import os
import sys
from pathlib import Path
from shlex import quote

from rich.console import Console
from rich.prompt import Prompt

from . import message

console = Console()

SERVER_FOLDER = Path.cwd() / "server"
TEST_FOLDER = Path.cwd() / "tests"
API_APP = "server.api:app"
API_PORT = 5000
API_WORKERS = 3


def _shell(cmd: str) -> int:
    console.print(f"[yellow]%[/yellow] {cmd}")
    return os.system(cmd)


def _print(msg: str, is_error: bool = False):
    if is_error is True:
        console.print(f"\n[red]{msg}[/red]\n")
    else:
        console.print(f"\n[green]{msg}[/green]\n")


def test():
    cmd = "pytest -vv tests"
    _shell(cmd)


def lint():
    results = []
    cmd_tools = ("mypy {folder}", "ruff check {folder}")
    folders = " ".join((str(SERVER_FOLDER), str(TEST_FOLDER)))
    for cmd in cmd_tools:
        results.append(_shell(cmd.format(folder=folders)))
    if not all(sc == 0 for sc in results):
        _print(message.LINT_ERROR, is_error=True)
        sys.exit(1)
    _print(message.LINT_SUCCESSFUL)


def format():
    cmd = "ruff format {folder}"
    folders = " ".join((str(SERVER_FOLDER), str(TEST_FOLDER)))
    _shell(cmd.format(folder=folders))


def build():
    results = []
    cmd_tools = ("mypy {folder}", "ruff check {folder}")
    folders = " ".join((str(SERVER_FOLDER), str(TEST_FOLDER)))
    for cmd in cmd_tools:
        results.append(_shell(cmd.format(folder=folders)))
    results.append(_shell("pytest -v tests"))
    if not all(sc == 0 for sc in results):
        _print(message.BUILD_ERROR, is_error=True)
        sys.exit(1)
    _print(message.BUILD_SUCCESSFUL)


def migrate():
    cmd = "alembic upgrade head"
    _shell(cmd)


def sqlmigrate():
    cmd = "alembic upgrade head --sql"
    _shell(cmd)


def make_migrations():
    message = Prompt.ask("[yellow]Enter your migration message[/yellow]").strip()
    if not message:
        _print("migration's message is required", is_error=True)
        return sys.exit(1)
    cmd = f"alembic revision --autogenerate -m {quote(message)}"
    _shell(cmd)
    _print("migration's script created")


def server():
    cmd = (
        "uvicorn "
        "--reload "
        f"--reload-dir {quote(str(SERVER_FOLDER))} "
        f"--port {API_PORT} "
        f"{API_APP}"
    )
    _shell(cmd)


def prodution_server():
    cmd = (
        "gunicorn "
        f"--workers {API_WORKERS} "
        "--worker-class uvicorn.workers.UvicornWorker "
        f"--bind 0.0.0.0:{API_PORT} "
        f"{API_APP}"
    )
    _shell(cmd)
