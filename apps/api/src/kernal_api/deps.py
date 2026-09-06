from fastapi import Header, HTTPException

from kernal_api.settings import settings
from kernal_core.storage import is_available


def require_storage() -> None:
    if not is_available():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set")


def require_cron_secret(x_cron_secret: str | None = Header(default=None)) -> None:
    expected: str | None = settings.cron_secret
    if expected is None or expected == "":
        return
    if x_cron_secret != expected:
        raise HTTPException(status_code=401, detail="Invalid cron secret")
