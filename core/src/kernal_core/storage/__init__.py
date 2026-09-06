"""Postgres memory. The only place that may know how we connect to Supabase."""

from kernal_core.storage.engine import (
    StorageUnavailable,
    configure,
    configure_from_env,
    is_available,
)
from kernal_core.storage.repo import (
    PersonInput,
    PersonRecord,
    UserContextRecord,
    WorkflowRunRecord,
    finish_run,
    get_context,
    init_schema,
    list_people,
    list_runs,
    start_run,
    upsert_context,
    upsert_people,
)

__all__ = [
    "PersonInput",
    "PersonRecord",
    "StorageUnavailable",
    "UserContextRecord",
    "WorkflowRunRecord",
    "configure",
    "configure_from_env",
    "finish_run",
    "get_context",
    "init_schema",
    "is_available",
    "list_people",
    "list_runs",
    "start_run",
    "upsert_context",
    "upsert_people",
]
