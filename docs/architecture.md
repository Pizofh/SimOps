# SimOps Architecture

## Overview

SimOps is a small event ingestion platform intended to showcase practical DevOps foundations: separated services, reproducible local environments, environment-based configuration, migrations, metrics exposure, and clear documentation.

## Current Implementation

The following components are implemented and wired together locally:

- PostgreSQL through Docker Compose
- FastAPI backend for event ingestion and querying
- standalone Python simulator for traffic generation
- Vue 3 frontend for browsing events
- Prometheus for metrics scraping
- Loki for centralized log storage
- Promtail for Docker log collection
- Grafana for dashboards and log exploration

## Current Runtime Topology

```text
frontend  -> backend -> postgres
simulator -> backend
backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki ------> grafana
simulator logs --> promtail -> loki ------> grafana
```

## Components

## Frontend

Status: implemented

- Vue 3 + Vite
- event list
- simple filters
- detail panel
- periodic polling
- security headers served by Nginx

## Backend

Status: implemented

- FastAPI monolith
- SQLAlchemy ORM
- Alembic migrations
- structured JSON logging
- health, readiness, and metrics endpoints
- CORS enabled for local frontend development
- trusted host validation
- common security response headers

## PostgreSQL

Status: implemented

- Docker Compose managed
- persistent volume
- health check enabled
- used by both local and containerized backend flows

## Simulator

Status: implemented

- separate Python workload generator
- random failures
- burst generation
- configurable intervals and latency

## Observability

Status: implemented

- Prometheus
- Loki
- Promtail
- Grafana
- starter dashboard provisioning
- backend metrics scraping
- backend and simulator log collection via Docker discovery

## Key Design Decisions

## 1. Backend monolith first

A single backend keeps the system explainable and avoids premature service fragmentation while still covering API design, persistence, metrics, and operational endpoints.

## 2. Separate simulator

The simulator represents an external event source rather than an internal helper. This makes the architecture more realistic and demonstrates inter-service communication.

## 3. Compose-first local platform

Docker Compose is now the canonical local entry point for the application stack. This reduces host drift and makes the project easier to run, demo, and extend.

## 4. Runtime configuration where it matters

The frontend uses a runtime-generated `config.js` inside the container so that the API base URL can be changed without rebuilding the image. This is a practical pattern for real deployments.

## 5. Deployment-friendly structure without platform-first complexity

The project is intentionally organized so it can move to a small VM or VPS deployment without major restructuring:

- services are already separated
- configuration is environment-based
- readiness and health endpoints already exist
- dashboards and scraper configuration are already externalized
- the Compose topology maps cleanly to a reverse-proxy-based deployment

## 6. Hardening before platform expansion

The project favors a small but real hardening baseline before adding orchestration complexity:

- restrict allowed host headers in the backend
- use non-root users where practical
- prefer read-only filesystems for simple stateless services
- rotate Docker logs to avoid unbounded local growth
- document which default credentials must be changed before deployment

## Explicitly Out of Scope for the MVP

- business microservices
- message brokers
- complex authentication
- GitOps
- Terraform-first provisioning
- multi-tenant design

