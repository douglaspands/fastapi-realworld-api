import os
import sys
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


def _print(msg: str, is_error: bool = False):
    if is_error is True:
        console.print(f"\n[red]{msg}[/red]\n")
    else:
        console.print(f"\n[green]{msg}[/green]\n")


def test():
    cmd = "pytest -vv"
    _shell(cmd)


def lint():
    results = []
    cmd_tools = ("mypy {folder}", "ruff check {folder}")
    folders = (str(SERVER_FOLDER), str(TEST_FOLDER))
    for cmd in cmd_tools:
        for folder in folders:
            results.append(_shell(cmd.format(folder=folder)))
    if not all(sc == 0 for sc in results):
        _print("LINT ERROR", is_error=True)
        sys.exit(1)
    _print("LINT SUCCESSFUL")


def build():
    results = []
    cmd_tools = ("mypy {folder}", "ruff check {folder}")
    folders = (str(SERVER_FOLDER), str(TEST_FOLDER))
    for cmd in cmd_tools:
        for folder in folders:
            results.append(_shell(cmd.format(folder=folder)))
    results.append(_shell("pytest -v"))
    if not all(sc == 0 for sc in results):
        _print("BUILD ERROR", is_error=True)
        sys.exit(1)
    _print("BUILD SUCCESSFUL", is_error=True)


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
