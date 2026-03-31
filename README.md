# SimOps

SimOps is a lightweight operational event ingestion platform built as a junior-to-mid DevOps portfolio project. The goal is to demonstrate reproducible local environments, service separation, engineering quality, and a realistic path toward observability without overengineering the business domain.

## Current Status

The project is currently complete through:

- Phase 1: technical design
- Phase 2: backend API
- Phase 3: simulator service
- Phase 4: frontend UI
- Phase 5: Dockerfiles and full local Docker Compose stack

The following phases are still pending:

- observability stack
- CI pipeline
- basic hardening pass

## Current Runtime Topology

```text
frontend  -> backend -> postgres
simulator -> backend
```

Planned observability topology for later phases:

```text
backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki -> grafana
simulator logs --> promtail -> loki -> grafana
```

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn
- Frontend: Vue 3, Vite, ESLint
- Database: PostgreSQL
- Simulator: Python, HTTPX
- Containers: Docker, Docker Compose
- Quality and security target: Ruff, Pytest, Bandit, pip-audit, optional Semgrep
- Observability target: Prometheus, Grafana, Loki, Promtail
- CI target: GitHub Actions

## Quick Start

Copy `.env.example` to `.env` in the repository root, then start the stack:

```bash
docker compose up --build
```

Default host ports:

- frontend: `http://localhost:8080`
- backend: `http://localhost:8000`
- database: `localhost:5434`

The frontend calls the backend through the browser, and the simulator continuously sends events into the API.

## Environment Variables

Root Compose variables:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `BACKEND_PORT`
- `FRONTEND_PORT`
- `SIMULATOR_INTERVAL_SECONDS`
- `SIMULATOR_FAILURE_RATE`
- `SIMULATOR_BURST_RATE`
- `SIMULATOR_BURST_MIN_SIZE`
- `SIMULATOR_BURST_MAX_SIZE`
- `SIMULATOR_SERVICE_NAMES`
- `SIMULATOR_ENVIRONMENT`
- `SIMULATOR_MAX_RANDOM_DELAY_MS`

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
    Dockerfile
  frontend/
    public/
    src/
    Dockerfile
    nginx.conf
  simulator/
    app/
    tests/
    Dockerfile
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

## Next Steps

- Phase 6: Prometheus, Loki, Promtail, and Grafana
- Phase 7: CI pipeline
- Phase 8: basic hardening and final documentation pass

