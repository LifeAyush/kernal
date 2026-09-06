from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


class StorageUnavailable(Exception):
    """Raised when DATABASE_URL is not configured."""


def _normalize_url(database_url: str) -> str:
    url: str = database_url
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    if url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def configure(database_url: str | None) -> None:
    global _engine, _SessionLocal
    if not database_url:
        _engine = None
        _SessionLocal = None
        return
    _engine = create_engine(_normalize_url(database_url), pool_pre_ping=True)
    _SessionLocal = sessionmaker(bind=_engine)


def is_available() -> bool:
    return _engine is not None


def get_engine() -> Engine:
    if _engine is None:
        raise StorageUnavailable("DATABASE_URL is not set")
    return _engine


def session_scope() -> Session:
    if _SessionLocal is None:
        raise StorageUnavailable("DATABASE_URL is not set")
    return _SessionLocal()
