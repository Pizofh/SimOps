from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    TIMEOUT = "timeout"
    LATENCY_SPIKE = "latency_spike"


class EventPayload(BaseModel):
    service_name: str = Field(min_length=2, max_length=100)
    severity: Severity
    message: str = Field(min_length=3, max_length=1000)
    environment: str = Field(min_length=2, max_length=32)
    created_at: datetime
    response_time_ms: int | None = Field(default=None, ge=0)
    status_code: int | None = Field(default=None, ge=0, le=999)
    source: str | None = Field(default=None, max_length=64)
    metadata: dict[str, Any] | None = None

