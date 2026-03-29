# Simulator

Servicio Python separado para generar eventos operativos simulados y enviarlos al backend de SimOps.

## Alcance de esta fase

- envio periodico de eventos al backend
- soporte para varios `service_name`
- fallos aleatorios controlados por `FAILURE_RATE`
- bursts opcionales controlados por `BURST_RATE`
- latencia aleatoria configurable
- logs estructurados JSON

## Variables de entorno

- `API_URL`
- `EVENT_INTERVAL_SECONDS`
- `FAILURE_RATE`
- `BURST_RATE`
- `BURST_MIN_SIZE`
- `BURST_MAX_SIZE`
- `SERVICE_NAMES`
- `ENVIRONMENT`
- `SOURCE`
- `REQUEST_TIMEOUT_SECONDS`
- `MAX_RANDOM_DELAY_MS`

Referencia inicial:

- `simulator/.env.example`

## Comandos esperados

Ejecutar desde `simulator/`.

Instalacion:

```bash
pip install -e .[dev]
```

Ejecutar simulator:

```bash
python -m app.main
```

Tests:

```bash
pytest
```

