# Contrato inicial de API

Base path inicial: `/`

## POST /events

Recibe y persiste un evento.

### Request body

```json
{
  "service_name": "payments-api",
  "severity": "error",
  "message": "Timeout while calling upstream service",
  "environment": "lab",
  "created_at": "2026-03-28T21:00:00Z",
  "response_time_ms": 1450,
  "status_code": 504,
  "source": "simulator",
  "metadata": {
    "region": "us-east-1",
    "attempt": 2
  }
}
```

### Reglas

- `service_name`: requerido, string corto
- `severity`: requerido, enum `info|warning|error|timeout|latency_spike`
- `message`: requerido
- `environment`: requerido
- `created_at`: opcional, si no se envia el backend usa UTC actual
- `response_time_ms`: opcional, entero no negativo
- `status_code`: opcional, entero entre `0` y `999`
- `source`: opcional
- `metadata`: opcional, objeto JSON

### Responses

- `201 Created`: evento persistido
- `422 Unprocessable Entity`: payload invalido

## GET /events

Lista eventos ordenados por fecha descendente.

### Query params

- `severity`: opcional
- `service_name`: opcional
- `limit`: opcional, por defecto `50`, maximo inicial recomendado `200`

### Responses

- `200 OK`

### Response example

```json
[
  {
    "id": "bfed2bb1-7dd5-4c9e-b7ec-393b8c063f56",
    "service_name": "payments-api",
    "severity": "error",
    "message": "Timeout while calling upstream service",
    "environment": "lab",
    "response_time_ms": 1450,
    "status_code": 504,
    "source": "simulator",
    "metadata": {
      "region": "us-east-1",
      "attempt": 2
    },
    "created_at": "2026-03-28T21:00:00Z",
    "ingested_at": "2026-03-28T21:00:01Z"
  }
]
```

## GET /events/{id}

Devuelve detalle de un evento por `id`.

### Responses

- `200 OK`
- `404 Not Found`

## GET /health

Salud basica del proceso.

### Uso

- prueba rapida de que el backend esta vivo
- no depende de la base de datos

### Response example

```json
{
  "status": "ok",
  "service": "simops-backend"
}
```

## GET /ready

Readiness del servicio.

### Uso

- verifica conectividad minima con PostgreSQL
- pensado para `healthcheck` y futura adaptacion a `readinessProbe`

### Responses

- `200 OK`
- `503 Service Unavailable`

### Response examples

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

Expone metricas compatibles con Prometheus.

### Metricas minimas

- `total_events_received`
- `total_events_by_severity`
- `http_requests_total`
- `http_request_duration_seconds`
- `backend_up`
- `errors_total`

## Convenciones operativas

- logs estructurados JSON
- `request_id` por request cuando aplique
- `event_id` en logs de persistencia cuando exista
- timestamps en UTC

