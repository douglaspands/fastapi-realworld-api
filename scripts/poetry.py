import os
from pathlib import Path
from shlex import quote

from rich.console import Console

console = Console()

SERVER_FOLDER = Path.cwd() / "server"
TEST_FOLDER = Path.cwd() / "tests"
API_APP = "server.api:app"
API_PORT = 5000
API_WORKERS = 3


def _shell(cmd: str) -> int:
    console.print(f"[yellow]$[/yellow] {cmd}")
    return os.system(cmd)


def test():
    cmd = "pytest -vv"
    _shell(cmd)


def lint():
    cmd_tools = ("mypy {folder}", "ruff check {folder}")
    folders = (str(SERVER_FOLDER), str(TEST_FOLDER))
    for cmd in cmd_tools:
        for folder in folders:
            if _shell(cmd.format(folder=folder)):
                return console.print("\n[red]LINT ERROR[/red]\n")
    console.print("\n[green]LINT SUCCESSFUL[/green]\n")


def server():
    cmd = (
        "gunicorn "
        f"--workers {API_WORKERS} "
        "--worker-class uvicorn.workers.UvicornWorker "
        f"--bind 0.0.0.0:{API_PORT} "
        f"{API_APP}"
    )
    _shell(cmd)


def server_debug():
    cmd = (
        "uvicorn "
        "--reload "
        f"--reload-dir {quote(str(SERVER_FOLDER))} "
        f"--port {API_PORT} "
        f"{API_APP}"
    )
    _shell(cmd)
