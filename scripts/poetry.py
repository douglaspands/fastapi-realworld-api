import os
from rich.console import Console
from pathlib import Path
from shlex import quote

console = Console()

SERVER_FOLDER = Path.cwd() / "server"
API_APP = "server.api:app"
API_PORT = 5000
API_WORKERS = 3


def _shell(cmd: str) -> int:
    console.print(f"[yellow]$[/yellow] {cmd}")
    return os.system(cmd)


def run_server():
    cmd = (
        "gunicorn "
        f"--workers {API_WORKERS} "
        "--worker-class uvicorn.workers.UvicornWorker "
        f"--bind 0.0.0.0:{API_PORT} "
        f"{API_APP}"
    )
    _shell(cmd)


def run_server_debug():
    cmd = (
        "uvicorn "
        "--reload "
        f"--reload-dir {quote(str(SERVER_FOLDER))} "
        f"--port {API_PORT} "
        f"{API_APP}"
    )
    _shell(cmd)
