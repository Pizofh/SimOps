from __future__ import annotations

import json
import logging

from app.config import get_settings
from app.utils import utc_now


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        settings = get_settings()
        payload = {
            "timestamp": utc_now().isoformat(),
            "level": record.levelname.lower(),
            "service": getattr(record, "service", settings.service_name),
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

    if getattr(root_logger, "_simops_simulator_logging", False):
        return

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, settings.log_level, logging.INFO))
    root_logger._simops_simulator_logging = True  # type: ignore[attr-defined]

