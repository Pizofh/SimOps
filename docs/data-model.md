# Data Model

## Primary Entity

The current MVP persists a single entity: `events`.

## Table: `events`

| Column | Type | Nullable | Description |
| --- | --- | --- | --- |
| `id` | UUID | no | Unique event identifier |
| `service_name` | VARCHAR(100) | no | Name of the originating service |
| `severity` | VARCHAR(32) | no | Event severity or type |
| `message` | TEXT | no | Event message |
| `environment` | VARCHAR(32) | no | Logical environment such as `dev`, `lab`, or `prod-sim` |
| `response_time_ms` | INTEGER | yes | Observed response time |
| `status_code` | INTEGER | yes | HTTP status code or simulated code |
| `source` | VARCHAR(64) | yes | Source system, for example `simulator` |
| `metadata` | JSONB conceptually, JSON in current migration | yes | Flexible additional attributes |
| `created_at` | TIMESTAMPTZ | no | Logical event creation time |
| `ingested_at` | TIMESTAMPTZ | no | Backend persistence time |

## Modeling Notes

- `id` is a UUID to avoid predictable sequences and to keep the model friendly to distributed demos.
- `created_at` represents when the event happened.
- `ingested_at` represents when the backend stored it.
- `metadata` remains flexible to avoid premature normalization.
- `severity` is currently validated at the application layer rather than split into a separate catalog table.

## Supported Severities

- `info`
- `warning`
- `error`
- `timeout`
- `latency_spike`

`burst` is not a severity. It is modeled as simulator behavior and represented through metadata.

## Current Index Strategy

- index on `created_at`
- index on `severity`
- index on `service_name`
- composite index on `environment, created_at`

## Out of Scope for the MVP

- user tables
- service registry tables
- advanced auditing
- retention policies
- partitioning
- archival workflows

