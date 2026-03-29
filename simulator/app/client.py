from __future__ import annotations

import logging
from uuid import uuid4

import httpx

from app.config import Settings
from app.schemas import EventPayload

logger = logging.getLogger(__name__)


class BackendClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = httpx.Client(timeout=settings.request_timeout_seconds)

    def send_event(self, event: EventPayload) -> dict:
        request_id = str(uuid4())

        try:
            response = self.client.post(
                self.settings.api_url,
                headers={"X-Request-ID": request_id},
                json=event.model_dump(mode="json"),
            )
            response.raise_for_status()
        except httpx.HTTPError:
            logger.exception(
                "event_delivery_failed",
                extra={
                    "request_id": request_id,
                    "extra_fields": {
                        "target_url": self.settings.api_url,
                        "service_name": event.service_name,
                        "severity": event.severity.value,
                    },
                },
            )
            raise

        response_body = response.json()
        logger.info(
            "event_delivered",
            extra={
                "request_id": request_id,
                "event_id": response_body.get("id"),
                "extra_fields": {
                    "target_url": self.settings.api_url,
                    "service_name": event.service_name,
                    "severity": event.severity.value,
                    "status_code": response.status_code,
                },
            },
        )
        return response_body

    def close(self) -> None:
        self.client.close()

