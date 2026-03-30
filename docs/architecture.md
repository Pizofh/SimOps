# SimOps Architecture

## Overview

SimOps is a lightweight event ingestion platform intended to showcase practical DevOps skills through a small but operationally meaningful system. The architecture favors clarity and reproducibility over business complexity.

## Current Implementation

As of the current milestone, the following components are implemented:

- PostgreSQL running through Docker Compose
- FastAPI backend for ingestion, querying, health, readiness, and metrics
- standalone Python simulator for synthetic event generation

The frontend and observability stack are planned for later phases.

## Current Runtime Topology

```text
simulator -> backend -> postgres
```

## Target Runtime Topology

```text
frontend  -> backend -> postgres
simulator -> backend

backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki -> grafana
simulator logs --> promtail -> loki -> grafana
```

## Components

## Frontend

Status: planned

- Vue 3 + Vite
- minimal event list and detail view
- simple filters for `severity` and `service_name`

## Backend

Status: implemented

- FastAPI monolith
- SQLAlchemy ORM
- Alembic migrations
- Pydantic models
- structured JSON logging
- health, readiness, and metrics endpoints

## PostgreSQL

Status: implemented

- primary persistence store
- single `events` table for the MVP
- Docker Compose bootstrap already available

## Simulator

Status: implemented

- separate Python service
- periodic event delivery
- random failures
- burst generation
- configurable target API and timing

## Observability

Status: planned

- Prometheus for metrics scraping
- Loki for log aggregation
- Promtail for log shipping
- Grafana for dashboards

## Design Decisions

## 1. Monolithic backend first

A single API keeps the system understandable and easier to operate while still demonstrating service integration, metrics, logging, migrations, and environment-based configuration.

## 2. Dedicated simulator service

The simulator lives outside the backend to represent an external workload source. This makes the architecture more realistic and creates a clean producer-consumer flow.

## 3. Compose-first local platform

Docker Compose is the target local orchestration model. PostgreSQL has already been moved there because it improves reproducibility and removes machine-specific database drift early.

## 4. Real observability, but not yet

Observability is a core goal of the project, not an optional extra. It is intentionally delayed until the application flow is complete enough to make the dashboards meaningful.

## 5. Kubernetes-ready structure without Kubernetes-first complexity

The project is intentionally organized so it can later move toward Kubernetes with minimal reshaping:

- services are separated by responsibility
- configuration is environment-driven
- readiness and health endpoints already exist
- Compose services can later map to Deployments and Services

## Explicitly Out of Scope for the MVP

- business microservices
- message brokers
- complex authentication and authorization
- GitOps
- Terraform-first provisioning
- advanced multi-tenant features

