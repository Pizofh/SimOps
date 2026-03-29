from __future__ import annotations

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import crud
from app.database import get_session
from app.enums import Severity
from app.metrics import ERRORS_TOTAL, record_event_ingested
from app.schemas import EventCreate, EventRead

router = APIRouter(tags=["events"])
logger = logging.getLogger(__name__)


@router.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, session: Session = Depends(get_session)) -> EventRead:
    try:
        event = crud.create_event(session, payload)
    except SQLAlchemyError as exc:
        session.rollback()
        ERRORS_TOTAL.labels(category="db_error").inc()
        logger.exception(
            "event_persist_failed",
            extra={
                "extra_fields": {
                    "service_name": payload.service_name,
                    "severity": payload.severity.value,
                }
            },
        )
        raise HTTPException(status_code=500, detail="Failed to persist event") from exc

    record_event_ingested(event.severity)
    logger.info(
        "event_ingested",
        extra={
            "event_id": event.id,
            "extra_fields": {
                "service_name": event.service_name,
                "severity": event.severity,
                "environment": event.environment,
            },
        },
    )
    return EventRead.from_event(event)


@router.get("/events", response_model=list[EventRead])
def list_events(
    severity: Severity | None = Query(default=None),
    service_name: str | None = Query(default=None, max_length=100),
    limit: int | None = Query(default=None, ge=1),
    session: Session = Depends(get_session),
) -> list[EventRead]:
    events = crud.list_events(
        session,
        severity=severity,
        service_name=service_name,
        limit=limit,
    )
    return [EventRead.from_event(event) for event in events]


@router.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: UUID, session: Session = Depends(get_session)) -> EventRead:
    event = crud.get_event(session, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return EventRead.from_event(event)

