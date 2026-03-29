# Simulator

Standalone Python service that generates simulated operational events and sends them to the SimOps backend.

## Scope of this phase

* periodic event delivery to the backend
* support for multiple `service_name` values
* random failures controlled by `FAILURE_RATE`
* optional bursts controlled by `BURST_RATE`
* configurable random latency
* structured JSON logging

## Environment variables

* `API_URL`
* `EVENT_INTERVAL_SECONDS`
* `FAILURE_RATE`
* `BURST_RATE`
* `BURST_MIN_SIZE`
* `BURST_MAX_SIZE`
* `SERVICE_NAMES`
* `ENVIRONMENT`
* `SOURCE`
* `REQUEST_TIMEOUT_SECONDS`
* `MAX_RANDOM_DELAY_MS`

Initial reference:

* `simulator/.env.example`

## Expected commands

Run from the `simulator/` directory.

Install:

```bash
pip install -e .[dev]
```

Run simulator:

```bash
python -m app.main
```

Tests:

```bash
pytest
```
