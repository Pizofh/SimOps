from __future__ import annotations

from uuid import uuid4


def build_event(**overrides):
    payload = {
        "service_name": "payments-api",
        "severity": "error",
        "message": "Timeout calling upstream dependency",
        "environment": "lab",
        "response_time_ms": 1450,
        "status_code": 504,
        "source": "simulator",
        "metadata": {"region": "us-east-1"},
    }
    payload.update(overrides)
    return payload


def test_post_event_persists_and_returns_201(client):
    response = client.post("/events", json=build_event())

    assert response.status_code == 201
    body = response.json()
    assert body["service_name"] == "payments-api"
    assert body["severity"] == "error"
    assert body["metadata"] == {"region": "us-east-1"}
    assert "id" in body
    assert "created_at" in body
    assert "ingested_at" in body


def test_get_events_supports_filters_and_descending_order(client):
    client.post(
        "/events",
        json=build_event(
            service_name="billing-api",
            severity="warning",
            message="Slow response detected",
            response_time_ms=900,
        ),
    )
    client.post(
        "/events",
        json=build_event(
            service_name="payments-api",
            severity="error",
            message="Timeout calling upstream dependency",
            response_time_ms=1450,
        ),
    )

    response = client.get(
        "/events",
        params={"severity": "error", "service_name": "payments-api", "limit": 10},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["service_name"] == "payments-api"
    assert body[0]["severity"] == "error"


def test_get_event_by_id_and_404(client):
    created = client.post("/events", json=build_event()).json()

    found = client.get(f"/events/{created['id']}")
    missing = client.get(f"/events/{uuid4()}")

    assert found.status_code == 200
    assert found.json()["id"] == created["id"]
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Event not found"

