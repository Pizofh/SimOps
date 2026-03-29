from __future__ import annotations

import logging
import time

import httpx

from app.client import BackendClient
from app.config import get_settings
from app.generator import EventGenerator
from app.logging_config import configure_logging

logger = logging.getLogger(__name__)


def run() -> None:
    configure_logging()
    settings = get_settings()
    generator = EventGenerator(settings)
    client = BackendClient(settings)

    logger.info(
        "simulator_started",
        extra={
            "extra_fields": {
                "api_url": settings.api_url,
                "event_interval_seconds": settings.event_interval_seconds,
                "failure_rate": settings.failure_rate,
                "burst_rate": settings.burst_rate,
                "service_names": settings.service_name_list,
            }
        },
    )

    try:
        while True:
            batch_size = generator.determine_batch_size()

            for batch_index in range(1, batch_size + 1):
                delay_seconds = generator.random_delay_seconds()
                if delay_seconds > 0:
                    time.sleep(delay_seconds)

                event = generator.generate_event(batch_size=batch_size, batch_index=batch_index)

                try:
                    client.send_event(event)
                except httpx.HTTPError:
                    continue

            time.sleep(settings.event_interval_seconds)
    except KeyboardInterrupt:
        logger.info("simulator_stopped")
    finally:
        client.close()


if __name__ == "__main__":
    run()

