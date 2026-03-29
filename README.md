# SimOps

SimOps is a lightweight operational event ingestion platform designed as a DevOps junior–mid portfolio project. The focus of the project is not functional complexity, but demonstrating operability, reproducible deployment, observability, technical quality, and good engineering practices within a realistic scope.

## Objective

The system allows:

* generating simulated events from a separate service
* receiving events through a backend API
* persisting them in PostgreSQL
* querying them from a minimal frontend
* exposing metrics for Prometheus
* centralizing logs in Loki via Promtail
* visualizing metrics and logs in Grafana

## Proposed Architecture

```text
frontend  -->  backend  -->  postgres
simulator -->  backend

backend /metrics ----------> prometheus --> grafana
backend logs --------------> promtail --> loki --> grafana
simulator logs ------------> promtail --> loki --> grafana
```

## Design Principles

* Monolithic and simple backend: a single FastAPI API.
* Clear separation of components: frontend, backend, simulator, database, and observability.
* Docker Compose as the main development and demo environment.
* Environment-based configuration using environment variables.
* Ready for a future Kubernetes phase, but without overinvesting in it now.
* Basic security and quality from the start: linting, tests, SAST, audit, and health checks.

## Stack

* Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn
* Frontend: Vue 3, Vite, ESLint
* Database: PostgreSQL
* Simulator: Python
* Observability: Prometheus, Grafana, Loki, Promtail
* Quality and security: Ruff, Pytest, Bandit, pip-audit, optional Semgrep
* Containers: Docker, Docker Compose
* CI: GitHub Actions

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
  infra/
    prometheus/
    grafana/
      dashboards/
      provisioning/
        datasources/
        dashboards/
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

## Required MVP

The MVP is considered complete when the following is met:

1. `POST /events` validates and persists events.
2. `GET /events` lists events with simple filters.
3. `GET /events/{id}` returns details and handles `404`.
4. `GET /health` responds with basic health status.
5. `GET /ready` validates connectivity with PostgreSQL.
6. `GET /metrics` exposes Prometheus metrics.
7. PostgreSQL persistently stores events in a reproducible way.
8. The simulator periodically sends events to the backend.
9. The frontend displays events, filters, and basic details.
10. Docker Compose brings up the entire environment.
11. Prometheus scrapes the backend.
12. Loki receives logs via Promtail.
13. Grafana displays basic dashboards.
14. The CI pipeline runs lint, tests, SAST, audit, and build verification.

## Roadmap by Phases

* Phase 1: technical design and repository structure
* Phase 2: functional backend with DB, metrics, logs, and minimal tests
* Phase 3: simulator configurable via environment variables
* Phase 4: minimal frontend with list, filters, and detail
* Phase 5: containerization and Docker Compose
* Phase 6: observability with Prometheus, Loki, Promtail, and Grafana
* Phase 7: CI pipeline in GitHub Actions
* Phase 8: basic hardening, final documentation, and lightweight Kubernetes preparation

## Suggested Git Best Practices

* protected `main` branch
* work in `feature/*` branches
* changes via Pull Requests
* mandatory checks before merge
* squash merge to keep history readable

## Overengineering Risks to Avoid

* business microservices
* queues or brokers from the start
* complex authentication
* initial Terraform setup
* initial GitOps setup
* overly complex frontend
* unnecessary abstraction patterns

## Current Status

Phase 1 has been documented and the repository has been initialized with Git. Implementation begins in the next phase.
