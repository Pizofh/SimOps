from __future__ import annotations

import random

from app.config import Settings
from app.schemas import EventPayload, Severity
from app.utils import utc_now


class EventGenerator:
    def __init__(self, settings: Settings, rng: random.Random | None = None) -> None:
        self.settings = settings
        self.rng = rng or random.Random()

    def determine_batch_size(self) -> int:
        if self.rng.random() < self.settings.burst_rate:
            return self.rng.randint(self.settings.burst_min_size, self.settings.burst_max_size)
        return 1

    def generate_event(self, *, batch_size: int = 1, batch_index: int = 1) -> EventPayload:
        service_name = self.rng.choice(self.settings.service_name_list)
        severity = self._choose_severity()
        response_time_ms = self._response_time_ms(severity)
        status_code = self._status_code(severity)

        return EventPayload(
            service_name=service_name,
            severity=severity,
            message=self._message(service_name, severity, response_time_ms),
            environment=self.settings.environment,
            created_at=utc_now(),
            response_time_ms=response_time_ms,
            status_code=status_code,
            source=self.settings.source,
            metadata=self._metadata(
                severity=severity,
                batch_size=batch_size,
                batch_index=batch_index,
                response_time_ms=response_time_ms,
            ),
        )

    def random_delay_seconds(self) -> float:
        if self.settings.max_random_delay_ms == 0:
            return 0.0
        return self.rng.uniform(0, self.settings.max_random_delay_ms / 1000)

    def _choose_severity(self) -> Severity:
        if self.rng.random() < self.settings.failure_rate:
            return self.rng.choice([Severity.ERROR, Severity.TIMEOUT, Severity.LATENCY_SPIKE])
        return self.rng.choice([Severity.INFO, Severity.WARNING])

    def _response_time_ms(self, severity: Severity) -> int:
        if severity == Severity.INFO:
            return self.rng.randint(50, 250)
        if severity == Severity.WARNING:
            return self.rng.randint(250, 800)
        if severity == Severity.ERROR:
            return self.rng.randint(400, 1800)
        if severity == Severity.TIMEOUT:
            return self.rng.randint(3000, 5000)
        return self.rng.randint(1500, 3500)

    def _status_code(self, severity: Severity) -> int:
        if severity == Severity.INFO:
            return 200
        if severity == Severity.WARNING:
            return self.rng.choice([200, 202, 429])
        if severity == Severity.ERROR:
            return self.rng.choice([500, 502, 503])
        if severity == Severity.TIMEOUT:
            return 504
        return self.rng.choice([200, 503])

    def _message(self, service_name: str, severity: Severity, response_time_ms: int) -> str:
        if severity == Severity.INFO:
            return f"{service_name} processed request successfully"
        if severity == Severity.WARNING:
            return f"{service_name} reported elevated latency but remained available"
        if severity == Severity.ERROR:
            return f"{service_name} returned an upstream error"
        if severity == Severity.TIMEOUT:
            return f"{service_name} timed out after {response_time_ms} ms"
        return f"{service_name} experienced a latency spike of {response_time_ms} ms"

    def _metadata(
        self,
        *,
        severity: Severity,
        batch_size: int,
        batch_index: int,
        response_time_ms: int,
    ) -> dict[str, object]:
        metadata: dict[str, object] = {
            "generator": self.settings.service_name,
            "batch_size": batch_size,
            "batch_index": batch_index,
            "simulated_failure": severity in {Severity.ERROR, Severity.TIMEOUT, Severity.LATENCY_SPIKE},
            "simulated_response_time_ms": response_time_ms,
        }

        if batch_size > 1:
            metadata["burst"] = True

        return metadata

