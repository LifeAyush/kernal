from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException

from kernal_api.deps import require_cron_secret, require_storage
from kernal_api.schemas import RunOut
from kernal_core.storage import WorkflowRunRecord
from kernal_core.workflows import execute
from kernal_linkedin.workflows import get_workflow

router: APIRouter = APIRouter(
    prefix="/api/workflows",
    dependencies=[Depends(require_storage), Depends(require_cron_secret)],
)


@router.post("/{workflow_name}/run")
def trigger_workflow(workflow_name: str) -> RunOut:
    fn: Callable[[], None] | None = get_workflow(workflow_name)
    if fn is None:
        raise HTTPException(status_code=404, detail=f"Unknown workflow: {workflow_name}")
    row: WorkflowRunRecord = execute(workflow_name, fn)
    return RunOut(
        id=row.id,
        workflow_name=row.workflow_name,
        status=row.status,
        started_at=row.started_at,
        finished_at=row.finished_at,
        error=row.error,
    )
