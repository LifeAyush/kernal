import os
from pathlib import Path

_CLI_ROOT: Path = Path(__file__).resolve().parents[2]
_REPO_ROOT: Path = _CLI_ROOT.parent


def _env_file_value(path: Path, key: str) -> str | None:
    if not path.is_file():
        return None
    line: str
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped: str = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name: str
        raw: str
        name, raw = stripped.split("=", 1)
        if name.strip() != key:
            continue
        value: str = raw.strip().strip("'").strip('"')
        if value:
            return value
    return None


def database_url() -> str | None:
    env_value: str | None = os.environ.get("DATABASE_URL")
    if env_value:
        return env_value
    path: Path
    for path in (
        Path("apps/api/.env"),
        Path(".env"),
        _REPO_ROOT / "apps/api/.env",
        _REPO_ROOT / ".env",
    ):
        file_value: str | None = _env_file_value(path, "DATABASE_URL")
        if file_value:
            return file_value
    return None
