from __future__ import annotations

import random

from app.config import Settings
from app.generator import EventGenerator
from app.schemas import Severity


def build_settings(**overrides) -> Settings:
    settings = {
        "service_names": "payments-api,auth-api",
        "environment": "lab",
        "source": "simulator",
        "failure_rate": 0.0,
        "burst_rate": 0.0,
        "burst_min_size": 2,
        "burst_max_size": 4,
        "max_random_delay_ms": 0,
    }
    settings.update(overrides)
    return Settings(**settings)


def test_determine_batch_size_returns_one_when_burst_disabled():
    generator = EventGenerator(build_settings(burst_rate=0.0), rng=random.Random(7))

    assert generator.determine_batch_size() == 1


def test_generate_event_contains_required_fields():
    generator = EventGenerator(build_settings(), rng=random.Random(7))

    event = generator.generate_event()

    assert event.service_name in {"payments-api", "auth-api"}
    assert event.environment == "lab"
    assert event.source == "simulator"
    assert event.created_at is not None
    assert event.metadata["generator"] == "simops-simulator"


def test_failure_rate_one_generates_failure_severities():
    generator = EventGenerator(build_settings(failure_rate=1.0), rng=random.Random(3))

    severities = {generator.generate_event().severity for _ in range(10)}

    assert severities.issubset({Severity.ERROR, Severity.TIMEOUT, Severity.LATENCY_SPIKE})

