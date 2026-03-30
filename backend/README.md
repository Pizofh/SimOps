# Backend

The backend is a single FastAPI application responsible for validating, storing, and exposing operational events.

## Implemented Scope

- `POST /events`
- `GET /events`
- `GET /events/{id}`
- `GET /health`
- `GET /ready`
- `GET /metrics`
- SQLAlchemy ORM model for `events`
- Alembic migration support
- structured JSON logging
- Prometheus metrics
- minimal automated tests

## Structure

```text
backend/
  app/
    config.py
    crud.py
    database.py
    enums.py
    logging_config.py
    main.py
    metrics.py
    middleware.py
    models.py
    schemas.py
    routers/
      events.py
      ops.py
  alembic/
    env.py
    versions/
  tests/
```

## Environment Variables

- `SIMOPS_DATABASE_URL`
- `SIMOPS_LOG_LEVEL`
- `SIMOPS_ENVIRONMENT`
- `SIMOPS_DEFAULT_QUERY_LIMIT`
- `SIMOPS_MAX_QUERY_LIMIT`

Recommended local database URL when PostgreSQL is started through Docker Compose:

```env
SIMOPS_DATABASE_URL=postgresql+psycopg://simops:simops@localhost:5432/simops
```

## Run Locally

Run from the `backend/` directory.

Install dependencies:

```bash
pip install -e .[dev]
```

Apply migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Run tests:

```bash
pytest
```

Lint:

```bash
ruff check .
```

Security scan:

```bash
bandit -r app
```

