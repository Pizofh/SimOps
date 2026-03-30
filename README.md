# SimOps

SimOps is a lightweight operational event ingestion platform built as a junior-to-mid DevOps portfolio project. Its purpose is to demonstrate reproducible environments, containerized dependencies, operational visibility, engineering quality, and clear technical documentation without introducing unnecessary business complexity.

## What SimOps Does

SimOps is designed to:

- receive simulated operational events through a backend API
- persist events in PostgreSQL
- generate synthetic incidents from a dedicated simulator service
- expose backend metrics for Prometheus
- emit structured logs that can later be collected by Loki via Promtail
- provide a minimal UI for browsing events in a future frontend phase

## Current Status

The project is currently complete through:

- Phase 1: technical design
- Phase 2: backend API
- Phase 3: simulator service
- Phase 4: frontend UI

The following pieces are not implemented yet:

- full multi-service Docker Compose stack
- Prometheus, Grafana, Loki, and Promtail configuration
- CI pipeline

At the moment, PostgreSQL is already available through Docker Compose, while the backend and simulator run as local Python services and the frontend runs through Vite during development.

## Current Working Flow

```text
frontend  -> backend -> postgres
simulator -> backend
```

Target observability flow for later phases:

```text
backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki -> grafana
simulator logs --> promtail -> loki -> grafana
```

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn
- Frontend: Vue 3, Vite
- Database: PostgreSQL
- Simulator: Python, HTTPX
- Observability target: Prometheus, Grafana, Loki, Promtail
- Quality and security target: Ruff, Pytest, Bandit, pip-audit, optional Semgrep
- Containers: Docker, Docker Compose
- CI target: GitHub Actions

## Quick Start

## 1. Start PostgreSQL

From the repository root:

```bash
docker compose up -d db
```

The root environment file should contain:

```env
POSTGRES_DB=simops
POSTGRES_USER=simops
POSTGRES_PASSWORD=simops
POSTGRES_PORT=5432
```

## 2. Run the Backend

From `backend/`:

```bash
pip install -e .[dev]
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Example backend database URL:

```env
SIMOPS_DATABASE_URL=postgresql+psycopg://simops:simops@localhost:5432/simops
```

## 3. Run the Simulator

From `simulator/`:

```bash
pip install -e .[dev]
python -m app.main
```

Default simulator target:

```env
API_URL=http://localhost:8000/events
```

## 4. Run the Frontend

From `frontend/`:

```bash
npm install
npm run dev
```

Example frontend configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_POLL_INTERVAL_MS=10000
```

## API Endpoints

- `POST /events`
- `GET /events`
- `GET /events/{id}`
- `GET /health`
- `GET /ready`
- `GET /metrics`

Detailed API documentation:

- [docs/api-contract.md](C:/Users/steve/Documents/DevsR/docs/api-contract.md)

## Repository Structure

```text
SimOps/
  backend/
    app/
    alembic/
    tests/
  frontend/
    src/
  simulator/
    app/
    tests/
  infra/
    prometheus/
    grafana/
    loki/
    promtail/
  docs/
    architecture.md
    api-contract.md
    data-model.md
    roadmap.md
  .github/
    workflows/
  docker-compose.yml
  .env.example
  README.md
```

## Documentation

- [docs/architecture.md](C:/Users/steve/Documents/DevsR/docs/architecture.md)
- [docs/api-contract.md](C:/Users/steve/Documents/DevsR/docs/api-contract.md)
- [docs/data-model.md](C:/Users/steve/Documents/DevsR/docs/data-model.md)
- [docs/roadmap.md](C:/Users/steve/Documents/DevsR/docs/roadmap.md)
- [backend/README.md](C:/Users/steve/Documents/DevsR/backend/README.md)
- [frontend/README.md](C:/Users/steve/Documents/DevsR/frontend/README.md)
- [simulator/README.md](C:/Users/steve/Documents/DevsR/simulator/README.md)

## Roadmap

- Phase 5: full Dockerfiles and complete Docker Compose orchestration
- Phase 6: Prometheus, Loki, Promtail, and Grafana
- Phase 7: CI pipeline
- Phase 8: basic hardening and final documentation pass
