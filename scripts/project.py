import os
import sys
from pathlib import Path
from shlex import quote

from art import text2art
from rich.console import Console
from rich.prompt import Prompt

console = Console()

ROOT_FOLDER = Path(__file__).parent.parent
SERVER_FOLDER = ROOT_FOLDER / "app"
MIGRATION_FOLDER = ROOT_FOLDER / "migrations"
TEST_FOLDER = ROOT_FOLDER / "tests"

API_APP = "main:app"
API_PORT = 8000
API_WORKERS = 3


def _shell(cmd: str) -> int:
    console.print(f"[yellow]%[/yellow] {cmd}")
    return os.system(cmd)


def _print(msg: str, is_error: bool = False):
    if is_error is True:
        console.print(f"\n[red]{msg}[/red]\n")
    else:
        console.print(f"\n[green]{msg}[/green]\n")


def unit_test():
    cmd = "pytest -vv -ra -q --cov=app --cov-report html --cov-fail-under=85 tests/unit"
    _shell(cmd)


def integration_test():
    cmd = "pytest -vv -ra -q tests/integration"
    _shell(cmd)


def lint():
    results = []
    cmd_tools = ("ty check {folder}", "ruff check {folder}")
    folders = " ".join((str(SERVER_FOLDER), str(TEST_FOLDER)))
    for cmd in cmd_tools:
        results.append(_shell(cmd.format(folder=folders)))
    if not all(sc == 0 for sc in results):
        _print(text2art("LINT ERROR"), is_error=True)
        sys.exit(1)
    _print(text2art("LINT SUCCESSFUL"))


def format():
    cmd = "ruff format {folder}"
    folders = " ".join((str(SERVER_FOLDER), str(TEST_FOLDER), str(MIGRATION_FOLDER)))
    _shell(cmd.format(folder=folders))


def build():
    results = []
    cmd_tools = ("ty check {folder}", "ruff check {folder}")
    folders = " ".join((str(SERVER_FOLDER), str(TEST_FOLDER)))
    for cmd in cmd_tools:
        results.append(_shell(cmd.format(folder=folders)))
    results.append(_shell("pytest -v tests"))
    if not all(sc == 0 for sc in results):
        _print(text2art("BUILD ERROR"), is_error=True)
        sys.exit(1)
    _print(text2art("BUILD SUCCESSFUL"))


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
        f"uvicorn --reload --reload-dir {SERVER_FOLDER!s} --port {API_PORT!s} {API_APP}"
    )
    _shell(cmd)


def prodution_server():
    cmd = (
        "gunicorn "
        f"--workers {API_WORKERS} "
        "--worker-class uvicorn.workers.UvicornWorker "
        f"--bind 0.0.0.0:{API_PORT!s} "
        f"{API_APP}"
    )
    _shell(cmd)


def make_requirements():
    cmd = "uv pip compile pyproject.toml --output-file requirements.txt"
    _shell(cmd)


def docker_build():
    cmd = "docker compose -f scripts/docker-compose.yaml build"
    _shell(cmd)


def compose_up():
    cmd = "docker compose -f scripts/docker-compose.yaml up"
    _shell(cmd)


def deployment_apply():
    cmd = "kubectl deployment apply scripts/deployment.yaml"
    _shell(cmd)
