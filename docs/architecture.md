# SimOps Architecture

## Overview

SimOps is a small event ingestion platform intended to showcase practical DevOps foundations: separated services, reproducible local environments, environment-based configuration, migrations, metrics exposure, and clear documentation.

## Current Implementation

The following components are implemented and wired together locally:

- PostgreSQL through Docker Compose
- FastAPI backend for event ingestion and querying
- standalone Python simulator for traffic generation
- Vue 3 frontend for browsing events

The observability stack is intentionally deferred to the next phase.

## Current Runtime Topology

```text
frontend  -> backend -> postgres
simulator -> backend
```

## Target Observability Topology

```text
backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki -> grafana
simulator logs --> promtail -> loki -> grafana
```

## Components

## Frontend

Status: implemented

- Vue 3 + Vite
- event list
- simple filters
- detail panel
- periodic polling

## Backend

Status: implemented

- FastAPI monolith
- SQLAlchemy ORM
- Alembic migrations
- structured JSON logging
- health, readiness, and metrics endpoints
- CORS enabled for local frontend development

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

Status: planned

- Prometheus
- Loki
- Promtail
- Grafana

## Key Design Decisions

## 1. Backend monolith first

A single backend keeps the system explainable and avoids premature service fragmentation while still covering API design, persistence, metrics, and operational endpoints.

## 2. Separate simulator

The simulator represents an external event source rather than an internal helper. This makes the architecture more realistic and demonstrates inter-service communication.

## 3. Compose-first local platform

Docker Compose is now the canonical local entry point for the application stack. This reduces host drift and makes the project easier to run, demo, and extend.

## 4. Runtime configuration where it matters

The frontend uses a runtime-generated `config.js` inside the container so that the API base URL can be changed without rebuilding the image. This is a practical pattern for real deployments.

## 5. Kubernetes-friendly structure without Kubernetes-first complexity

The project is intentionally organized so it can later move to Kubernetes with limited restructuring:

- services are already separated
- configuration is environment-based
- readiness and health endpoints already exist
- the Compose topology maps cleanly to future Deployments and Services

## Explicitly Out of Scope for the MVP

- business microservices
- message brokers
- complex authentication
- GitOps
- Terraform-first provisioning
- multi-tenant design

