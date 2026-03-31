# Simulator

The simulator is a standalone Python service that continuously generates synthetic operational events and sends them to the backend API.

## Implemented Scope

- periodic event generation
- support for multiple service names
- configurable failure rate
- configurable burst rate and burst size
- configurable random latency before delivery
- structured JSON logs for successful and failed deliveries

## Environment Variables

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

Example:

```env
API_URL=http://localhost:8000/events
EVENT_INTERVAL_SECONDS=5
FAILURE_RATE=0.25
BURST_RATE=0.15
BURST_MIN_SIZE=3
BURST_MAX_SIZE=6
SERVICE_NAMES=payments-api,auth-api,inventory-worker
ENVIRONMENT=lab
SOURCE=simulator
REQUEST_TIMEOUT_SECONDS=5
MAX_RANDOM_DELAY_MS=250
```

## Run Locally

Run from the `simulator/` directory.

Install dependencies:

```bash
pip install -e .[dev]
```

Start the simulator:

```bash
python -m app.main
```

Run tests:

```bash
pytest
```

## Run in Docker Compose

From the repository root:

```bash
docker compose up --build simulator
```

In Compose, the simulator targets the backend through the internal service name `backend`.

