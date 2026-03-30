# Roadmap

## Completed

## Phase 1: Technical Design

- repository structure defined
- architecture documented
- initial API contract documented
- initial data model documented

## Phase 2: Backend

- FastAPI application implemented
- SQLAlchemy, Alembic, and Pydantic configured
- event ingestion and query endpoints implemented
- health, readiness, and metrics endpoints implemented
- structured JSON logging added
- minimal backend tests added

## Phase 3: Simulator

- standalone Python simulator implemented
- environment-based configuration added
- periodic event delivery implemented
- random failures, latency, and burst generation implemented
- structured JSON logging added
- minimal simulator tests added

## Next

## Phase 4: Frontend

- create a minimal Vue 3 + Vite application
- list events
- support simple filters
- show a basic detail panel

## Phase 5: Docker and Compose

- add Dockerfiles for backend, frontend, and simulator
- extend Compose beyond PostgreSQL
- connect application services with health checks

## Phase 6: Observability

- configure Prometheus
- configure Loki and Promtail
- provision Grafana
- add starter dashboards

## Phase 7: CI

- add GitHub Actions workflow
- backend lint, tests, and security checks
- frontend lint and build verification
- container build validation

## Phase 8: Basic Hardening

- non-root containers where practical
- safer runtime defaults
- final documentation pass
- lightweight Kubernetes preparation notes

## MVP Definition of Done

The MVP is complete when:

- the backend persists and exposes events
- the simulator produces useful traffic
- the frontend can browse events
- Docker Compose brings up the full local environment
- Prometheus collects metrics
- Loki centralizes logs
- Grafana visualizes metrics and logs
- CI validates quality and security checks

