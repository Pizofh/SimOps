# API Contract

Base path: `/`

## POST /events

Accepts and persists an operational event.

### Request body

```json
{
  "service_name": "payments-api",
  "severity": "error",
  "message": "Timeout while calling upstream service",
  "environment": "lab",
  "created_at": "2026-03-30T17:00:00Z",
  "response_time_ms": 1450,
  "status_code": 504,
  "source": "simulator",
  "metadata": {
    "region": "us-east-1",
    "attempt": 2
  }
}
```

### Validation rules

- `service_name`: required, short string
- `severity`: required, one of `info`, `warning`, `error`, `timeout`, `latency_spike`
- `message`: required
- `environment`: required
- `created_at`: optional, defaults to current UTC time if omitted
- `response_time_ms`: optional, non-negative integer
- `status_code`: optional, integer from `0` to `999`
- `source`: optional
- `metadata`: optional JSON object

### Responses

- `201 Created`
- `422 Unprocessable Entity`

## GET /events

Returns events sorted by `created_at` in descending order.

### Query parameters

- `severity`: optional
- `service_name`: optional
- `limit`: optional, default `50`, current maximum `200`

### Example response

```json
[
  {
    "id": "28181bc7-1020-41a5-b887-e90629261a23",
    "service_name": "payments-api",
    "severity": "error",
    "message": "payments-api returned an upstream error",
    "environment": "lab",
    "response_time_ms": 482,
    "status_code": 502,
    "source": "simulator",
    "metadata": {
      "generator": "simops-simulator",
      "batch_size": 1,
      "batch_index": 1,
      "simulated_failure": true,
      "simulated_response_time_ms": 482
    },
    "created_at": "2026-03-30T17:02:23.522449Z",
    "ingested_at": "2026-03-30T17:02:25.577973Z"
  }
]
```

## GET /events/{id}

Returns a single event by ID.

### Responses

- `200 OK`
- `404 Not Found`

## GET /health

Basic process liveness endpoint.

### Example response

```json
{
  "status": "ok",
  "service": "simops-backend"
}
```

## GET /ready

Readiness endpoint with a minimal database connectivity check.

### Responses

- `200 OK`
- `503 Service Unavailable`

### Example responses

```json
{
  "status": "ready",
  "database": "ok"
}
```

```json
{
  "status": "not_ready",
  "database": "error"
}
```

## GET /metrics

Exposes Prometheus-compatible metrics.

### Current metric names

- `total_events_received`
- `total_events_by_severity`
- `http_requests_total`
- `http_request_duration_seconds`
- `backend_up`
- `errors_total`

## Logging Conventions

- structured JSON logs
- `request_id` when applicable
- `event_id` when available
- UTC timestamps

