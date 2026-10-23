from datetime import date, datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator
Status = Literal["sanction_pending", "in_progress", "completed", "on_hold", "unknown"]
class WorkIn(BaseModel):
    work_id: str = Field(min_length=1, max_length=80)
    district: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=80)
    sanction_date: date | None = None
    status: Status = "unknown"
    amount_sanctioned: float = Field(default=0, ge=0, le=1e12)
    amount_paid: float = Field(default=0, ge=0, le=1e12)
    last_progress_date: date | None = None
    completion_date: date | None = None
    description: str = Field(default="", max_length=1000)
    source_url: str | None = Field(default=None, max_length=500)
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    @field_validator("work_id", "district", "category")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()
class IngestRequest(BaseModel):
    source: str = Field(default="api", max_length=100)
    records: list[dict[str, Any]] = Field(min_length=1, max_length=1000)
class ReviewRequest(BaseModel):
    decision: Literal["valid_signal", "not_applicable", "needs_information"]
    note: str = Field(default="", max_length=2000)
class Explanation(BaseModel):
    alert_id: str
    audience: Literal["citizen", "officer", "admin"]
    summary: str
    claims: list[str]
    evidence_ids: list[str]
    limitations: list[str]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
