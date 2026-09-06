from datetime import datetime

from pydantic import BaseModel


class ContextBody(BaseModel):
    interests: list[str]
    topics: list[str]


class ContextOut(BaseModel):
    interests: list[str]
    topics: list[str]
    updated_at: datetime


class PersonOut(BaseModel):
    linkedin_url: str
    name: str
    headline: str
    score: float | None
    first_seen_at: datetime
    last_seen_at: datetime


class RunOut(BaseModel):
    id: int
    workflow_name: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    error: str | None
