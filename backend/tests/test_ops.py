from __future__ import annotations


def test_health_and_ready_endpoints(client):
    health_response = client.get("/health")
    ready_response = client.get("/ready")

    assert health_response.status_code == 200
    assert health_response.json()["status"] == "ok"
    assert health_response.json()["service"] == "simops-backend"

    assert ready_response.status_code == 200
    assert ready_response.json() == {"status": "ready", "database": "ok"}


def test_metrics_endpoint_exposes_required_metrics(client):
    client.get("/metrics")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "total_events_received" in response.text
    assert "total_events_by_severity" in response.text
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text
    assert "backend_up" in response.text
    assert "errors_total" in response.text

