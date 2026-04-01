# Infra

This directory contains the local observability configuration used by the Docker Compose stack.

## Implemented Contents

- `prometheus/prometheus.yml`: scrapes the backend metrics endpoint and Prometheus itself
- `loki/config.yml`: stores logs locally for the Compose-based demo environment
- `promtail/promtail.yml`: discovers Docker containers and forwards backend and simulator logs to Loki
- `grafana/provisioning/datasources/`: automatically provisions Prometheus and Loki as datasources
- `grafana/provisioning/dashboards/`: automatically provisions dashboard loading
- `grafana/dashboards/simops-overview.json`: starter dashboard for event volume, error trends, request metrics, and logs

## Runtime Flow

```text
backend /metrics -> prometheus -> grafana
backend logs ----> promtail -> loki ------> grafana
simulator logs --> promtail -> loki ------> grafana
```

## Default Access

- Prometheus: `http://localhost:9090`
- Loki: `http://localhost:3100`
- Grafana: `http://localhost:3000`

Grafana credentials are controlled through the root `.env` file:

- `GRAFANA_ADMIN_USER`
- `GRAFANA_ADMIN_PASSWORD`

## Notes

- Promtail currently targets only the `backend` and `simulator` containers to keep the MVP focused on application-level observability.
- Grafana is provisioned from files so the dashboard setup is reproducible and versioned in Git.
