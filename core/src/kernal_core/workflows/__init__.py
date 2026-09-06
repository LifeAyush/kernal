"""Workflow execution lifecycle. App modules supply the callable; Core writes runs."""

from collections.abc import Callable

from kernal_core.storage import WorkflowRunRecord, finish_run, start_run


def execute(workflow_name: str, fn: Callable[[], None]) -> WorkflowRunRecord:
    record: WorkflowRunRecord = start_run(workflow_name)
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 — workflow failures become run rows, not crashes
        return finish_run(record.id, "error", str(exc))
    return finish_run(record.id, "ok", None)
