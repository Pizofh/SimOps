from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import Severity


class EventBase(BaseModel):
    service_name: str = Field(min_length=2, max_length=100)
    severity: Severity
    message: str = Field(min_length=3, max_length=1000)
    environment: str = Field(min_length=2, max_length=32)
    response_time_ms: int | None = Field(default=None, ge=0)
    status_code: int | None = Field(default=None, ge=0, le=999)
    source: str | None = Field(default=None, max_length=64)
    metadata: dict[str, Any] | None = None


class EventCreate(EventBase):
    created_at: datetime | None = None


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    metadata: dict[str, Any] | None = None
    created_at: datetime
    ingested_at: datetime

    @classmethod
    def from_event(cls, event) -> "EventRead":
        return cls(
            id=event.id,
            service_name=event.service_name,
            severity=event.severity,
            message=event.message,
            environment=event.environment,
            response_time_ms=event.response_time_ms,
            status_code=event.status_code,
            source=event.source,
            metadata=event.event_metadata,
            created_at=event.created_at,
            ingested_at=event.ingested_at,
        )


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
