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
- CORS support for the frontend
- minimal automated tests

## Environment Variables

- `SIMOPS_DATABASE_URL`
- `SIMOPS_LOG_LEVEL`
- `SIMOPS_ENVIRONMENT`
- `SIMOPS_CORS_ORIGINS`
- `SIMOPS_ALLOWED_HOSTS`
- `SIMOPS_DEFAULT_QUERY_LIMIT`
- `SIMOPS_MAX_QUERY_LIMIT`

For local host-based development with PostgreSQL exposed by Docker Compose:

```env
SIMOPS_DATABASE_URL=postgresql+psycopg://simops:simops@localhost:5434/simops
SIMOPS_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080,http://127.0.0.1:8080
SIMOPS_ALLOWED_HOSTS=localhost,127.0.0.1,backend,testserver
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

## Run in Docker Compose

From the repository root:

```bash
docker compose up --build backend
```

The container startup command applies the Alembic migration before starting Uvicorn.
Prometheus scrapes the backend through `GET /metrics`, and backend logs are available in Loki through Promtail when the observability services are running.
The backend also applies trusted host validation and returns a small set of security headers.

