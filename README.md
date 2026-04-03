# SimOps

SimOps is a lightweight operational event ingestion platform built as a junior-to-mid DevOps portfolio project. The goal is to demonstrate reproducible local environments, service separation, engineering quality, and a realistic path toward observability without overengineering the business domain.

## Current Status

The project is currently complete through:

- Phase 1: technical design
- Phase 2: backend API
- Phase 3: simulator service
- Phase 4: frontend UI
- Phase 5: Dockerfiles and full local Docker Compose stack
- Phase 6: observability stack
- Phase 7: CI pipeline

## Current Runtime Topology

```text
frontend  -> backend -> postgres
simulator -> backend
backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki ------> grafana
simulator logs --> promtail -> loki ------> grafana
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
- Prometheus: `http://localhost:9090`
- Loki: `http://localhost:3100`
- Grafana: `http://localhost:3000`

The frontend calls the backend through the browser, and the simulator continuously sends events into the API.

Grafana is provisioned automatically with:

- a Prometheus datasource
- a Loki datasource
- a starter dashboard named `SimOps Overview`

## Environment Variables

Root Compose variables:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `BACKEND_PORT`
- `FRONTEND_PORT`
- `PROMETHEUS_PORT`
- `LOKI_PORT`
- `GRAFANA_PORT`
- `GRAFANA_ADMIN_USER`
- `GRAFANA_ADMIN_PASSWORD`
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
- [infra/README.md](C:/Users/steve/Documents/DevsR/infra/README.md)
- [backend/README.md](C:/Users/steve/Documents/DevsR/backend/README.md)
- [frontend/README.md](C:/Users/steve/Documents/DevsR/frontend/README.md)
- [simulator/README.md](C:/Users/steve/Documents/DevsR/simulator/README.md)

## CI Pipeline

The repository includes a GitHub Actions workflow at [ci.yml](C:/Users/steve/Documents/DevsR/.github/workflows/ci.yml).

Implemented checks:

- `backend-quality`: installs the backend, runs Ruff, and executes Pytest
- `backend-security`: runs Bandit and `pip-audit`
- `frontend-quality`: installs frontend dependencies, runs ESLint, and verifies the production build
- `docker-build`: validates `docker-compose.yml` and builds the `backend`, `frontend`, and `simulator` images

Recommended Git workflow:

- create short-lived branches such as `feature/<name>`, `fix/<name>`, or `chore/<name>`
- open pull requests into `main`
- keep `main` protected and merge only when required checks pass

Recommended branch protection for `main`:

1. Require a pull request before merging.
2. Require status checks to pass before merging.
3. Mark these checks as required:
   - `backend-quality`
   - `backend-security`
   - `frontend-quality`
   - `docker-build`
4. Optionally require branches to be up to date before merging.

## Next Steps

- Phase 8: basic hardening and final documentation pass


