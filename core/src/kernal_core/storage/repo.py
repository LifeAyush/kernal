from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from kernal_core.storage.engine import get_engine, session_scope
from kernal_core.storage.models import Base, Person, UserContext, WorkflowRun

_CONTEXT_ID: int = 1


@dataclass(frozen=True)
class UserContextRecord:
    interests: list[str]
    topics: list[str]
    updated_at: datetime


@dataclass(frozen=True)
class PersonRecord:
    linkedin_url: str
    name: str
    headline: str
    score: float | None
    first_seen_at: datetime
    last_seen_at: datetime


@dataclass(frozen=True)
class WorkflowRunRecord:
    id: int
    workflow_name: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    error: str | None


@dataclass(frozen=True)
class PersonInput:
    linkedin_url: str
    name: str
    headline: str
    score: float | None


def init_schema() -> None:
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_context() -> UserContextRecord | None:
    session: Session = session_scope()
    try:
        row: UserContext | None = session.get(UserContext, _CONTEXT_ID)
        if row is None:
            return None
        return UserContextRecord(
            interests=list(row.interests),
            topics=list(row.topics),
            updated_at=row.updated_at,
        )
    finally:
        session.close()


def upsert_context(interests: list[str], topics: list[str]) -> UserContextRecord:
    now: datetime = datetime.now(UTC)
    session: Session = session_scope()
    try:
        row: UserContext | None = session.get(UserContext, _CONTEXT_ID)
        if row is None:
            row = UserContext(
                id=_CONTEXT_ID,
                interests=interests,
                topics=topics,
                updated_at=now,
            )
            session.add(row)
        else:
            row.interests = interests
            row.topics = topics
            row.updated_at = now
        session.commit()
        session.refresh(row)
        return UserContextRecord(
            interests=list(row.interests),
            topics=list(row.topics),
            updated_at=row.updated_at,
        )
    finally:
        session.close()


def list_people() -> list[PersonRecord]:
    session: Session = session_scope()
    try:
        rows: list[Person] = list(session.scalars(select(Person).order_by(Person.last_seen_at.desc())))
        return [
            PersonRecord(
                linkedin_url=row.linkedin_url,
                name=row.name,
                headline=row.headline,
                score=row.score,
                first_seen_at=row.first_seen_at,
                last_seen_at=row.last_seen_at,
            )
            for row in rows
        ]
    finally:
        session.close()


def upsert_people(people: list[PersonInput]) -> tuple[int, int]:
    inserted: int = 0
    updated: int = 0
    now: datetime = datetime.now(UTC)
    session: Session = session_scope()
    try:
        person: PersonInput
        for person in people:
            row: Person | None = session.scalar(
                select(Person).where(Person.linkedin_url == person.linkedin_url)
            )
            if row is None:
                session.add(
                    Person(
                        linkedin_url=person.linkedin_url,
                        name=person.name,
                        headline=person.headline,
                        score=person.score,
                        first_seen_at=now,
                        last_seen_at=now,
                    )
                )
                inserted += 1
            else:
                row.name = person.name
                row.headline = person.headline
                row.score = person.score
                row.last_seen_at = now
                updated += 1
        session.commit()
        return inserted, updated
    finally:
        session.close()


def _run_record(row: WorkflowRun) -> WorkflowRunRecord:
    return WorkflowRunRecord(
        id=row.id,
        workflow_name=row.workflow_name,
        status=row.status,
        started_at=row.started_at,
        finished_at=row.finished_at,
        error=row.error,
    )


def list_runs() -> list[WorkflowRunRecord]:
    session: Session = session_scope()
    try:
        rows: list[WorkflowRun] = list(
            session.scalars(select(WorkflowRun).order_by(WorkflowRun.started_at.desc()))
        )
        return [_run_record(row) for row in rows]
    finally:
        session.close()


def start_run(workflow_name: str) -> WorkflowRunRecord:
    now: datetime = datetime.now(UTC)
    session: Session = session_scope()
    try:
        row: WorkflowRun = WorkflowRun(
            workflow_name=workflow_name,
            status="running",
            started_at=now,
            finished_at=None,
            error=None,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return _run_record(row)
    finally:
        session.close()


def finish_run(run_id: int, status: str, error: str | None) -> WorkflowRunRecord:
    now: datetime = datetime.now(UTC)
    session: Session = session_scope()
    try:
        row: WorkflowRun | None = session.get(WorkflowRun, run_id)
        if row is None:
            raise ValueError(f"workflow run {run_id} not found")
        row.status = status
        row.finished_at = now
        row.error = error
        session.commit()
        session.refresh(row)
        return _run_record(row)
    finally:
        session.close()
