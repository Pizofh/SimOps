from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.enums import Severity
from app.models import Event
from app.schemas import EventCreate
from app.utils import utc_now


def create_event(session: Session, payload: EventCreate) -> Event:
    event = Event(
        service_name=payload.service_name,
        severity=payload.severity.value,
        message=payload.message,
        environment=payload.environment,
        response_time_ms=payload.response_time_ms,
        status_code=payload.status_code,
        source=payload.source,
        event_metadata=payload.metadata,
        created_at=payload.created_at or utc_now(),
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def list_events(
    session: Session,
    *,
    severity: Severity | None = None,
    service_name: str | None = None,
    limit: int | None = None,
) -> list[Event]:
    settings = get_settings()
    effective_limit = min(limit or settings.default_query_limit, settings.max_query_limit)

    query: Select[tuple[Event]] = select(Event)

    if severity is not None:
        query = query.where(Event.severity == severity.value)

    if service_name:
        query = query.where(Event.service_name == service_name)

    query = query.order_by(Event.created_at.desc()).limit(effective_limit)
    return list(session.scalars(query))


def get_event(session: Session, event_id: UUID) -> Event | None:
    return session.get(Event, event_id)

