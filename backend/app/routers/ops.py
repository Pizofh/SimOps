from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_session
from app.metrics import ERRORS_TOTAL
from app.schemas import HealthResponse, ReadinessResponse

router = APIRouter(tags=["ops"])
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.service_name)


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessResponse}},
)
def ready(session: Session = Depends(get_session)) -> ReadinessResponse | JSONResponse:
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        ERRORS_TOTAL.labels(category="db_readiness_error").inc()
        logger.exception("readiness_check_failed")
        return JSONResponse(
            status_code=503,
            content=ReadinessResponse(status="not_ready", database="error").model_dump(),
        )

    return ReadinessResponse(status="ready", database="ok")


@router.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

