from __future__ import annotations

import json
import logging
from contextvars import ContextVar, Token

from app.config import get_settings
from app.utils import utc_now

request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(request_id: str) -> Token[str | None]:
    return request_id_context.set(request_id)


def reset_request_id(token: Token[str | None]) -> None:
    request_id_context.reset(token)


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        settings = get_settings()
        record.service = getattr(record, "service", settings.service_name)
        record.request_id = getattr(record, "request_id", request_id_context.get())
        record.event_id = getattr(record, "event_id", None)
        record.extra_fields = getattr(record, "extra_fields", None)
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": utc_now().isoformat(),
            "level": record.levelname.lower(),
            "service": getattr(record, "service", get_settings().service_name),
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", None)
        event_id = getattr(record, "event_id", None)
        extra_fields = getattr(record, "extra_fields", None)

        if request_id:
            payload["request_id"] = request_id
        if event_id:
            payload["event_id"] = str(event_id)
        if isinstance(extra_fields, dict):
            payload.update(extra_fields)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    settings = get_settings()
    root_logger = logging.getLogger()

    if getattr(root_logger, "_simops_json_logging", False):
        return

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestContextFilter())

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, settings.log_level, logging.INFO))
    root_logger._simops_json_logging = True  # type: ignore[attr-defined]

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True

