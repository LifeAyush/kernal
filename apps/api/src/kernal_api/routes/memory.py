from fastapi import APIRouter, Depends

from kernal_api.deps import require_storage
from kernal_api.schemas import ContextBody, ContextOut, PersonOut, RunOut
from kernal_core.storage import (
    PersonRecord,
    UserContextRecord,
    WorkflowRunRecord,
    get_context,
    list_people,
    list_runs,
    upsert_context,
)

router: APIRouter = APIRouter(prefix="/api", dependencies=[Depends(require_storage)])


@router.get("/context")
def read_context() -> ContextOut | None:
    row: UserContextRecord | None = get_context()
    if row is None:
        return None
    return ContextOut(interests=row.interests, topics=row.topics, updated_at=row.updated_at)


@router.put("/context")
def write_context(body: ContextBody) -> ContextOut:
    row: UserContextRecord = upsert_context(body.interests, body.topics)
    return ContextOut(interests=row.interests, topics=row.topics, updated_at=row.updated_at)


@router.get("/people")
def read_people() -> list[PersonOut]:
    rows: list[PersonRecord] = list_people()
    return [
        PersonOut(
            linkedin_url=row.linkedin_url,
            name=row.name,
            headline=row.headline,
            score=row.score,
            first_seen_at=row.first_seen_at,
            last_seen_at=row.last_seen_at,
        )
        for row in rows
    ]


@router.get("/runs")
def read_runs() -> list[RunOut]:
    rows: list[WorkflowRunRecord] = list_runs()
    return [
        RunOut(
            id=row.id,
            workflow_name=row.workflow_name,
            status=row.status,
            started_at=row.started_at,
            finished_at=row.finished_at,
            error=row.error,
        )
        for row in rows
    ]
