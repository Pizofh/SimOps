# SimOps

SimOps es una plataforma ligera de ingestión de eventos operativos pensada como proyecto de portafolio DevOps jr-mid. El foco del proyecto no es la complejidad funcional, sino demostrar operabilidad, despliegue reproducible, observabilidad, calidad técnica y buenas prácticas de ingeniería con un alcance realista.

## Objetivo

El sistema permite:

- generar eventos simulados desde un servicio separado
- recibir eventos mediante una API backend
- persistirlos en PostgreSQL
- consultarlos desde un frontend mínimo
- exponer métricas para Prometheus
- centralizar logs en Loki mediante Promtail
- visualizar métricas y logs en Grafana

## Arquitectura propuesta

```text
frontend  -->  backend  -->  postgres
simulator -->  backend

backend /metrics ----------> prometheus --> grafana
backend logs --------------> promtail --> loki --> grafana
simulator logs ------------> promtail --> loki --> grafana
```

## Principios de diseño

- Backend monolítico y sobrio: una sola API FastAPI.
- Separación clara de componentes: frontend, backend, simulador, base de datos y observabilidad.
- Docker Compose como entorno principal de desarrollo y demo.
- Configuración por entorno con variables de entorno.
- Listo para una fase futura de Kubernetes, pero sin sobreinvertir en ello ahora.
- Seguridad y calidad básicas desde el inicio: linting, tests, SAST, audit y healthchecks.

## Stack

- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn
- Frontend: Vue 3, Vite, ESLint
- Base de datos: PostgreSQL
- Simulator: Python
- Observabilidad: Prometheus, Grafana, Loki, Promtail
- Calidad y seguridad: Ruff, Pytest, Bandit, pip-audit, Semgrep opcional
- Contenedores: Docker, Docker Compose
- CI: GitHub Actions

## Estructura del repositorio

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

## MVP obligatorio

El MVP queda aceptado cuando se cumpla lo siguiente:

1. `POST /events` valida y persiste eventos.
2. `GET /events` lista eventos con filtros simples.
3. `GET /events/{id}` devuelve detalle y maneja `404`.
4. `GET /health` responde salud básica.
5. `GET /ready` valida conectividad con PostgreSQL.
6. `GET /metrics` expone métricas Prometheus.
7. PostgreSQL persiste eventos de manera reproducible.
8. El simulador envía eventos periódicamente al backend.
9. El frontend muestra eventos, filtros y detalle simple.
10. Docker Compose levanta todo el entorno.
11. Prometheus scrapea el backend.
12. Loki recibe logs mediante Promtail.
13. Grafana muestra dashboards básicos.
14. El pipeline CI ejecuta lint, tests, SAST, audit y verificación de build.

## Roadmap por fases

- Fase 1: diseño técnico y estructura del repo
- Fase 2: backend funcional con DB, métricas, logs y tests mínimos
- Fase 3: simulador configurable por variables de entorno
- Fase 4: frontend mínimo con lista, filtros y detalle
- Fase 5: dockerización y Docker Compose
- Fase 6: observabilidad con Prometheus, Loki, Promtail y Grafana
- Fase 7: pipeline CI en GitHub Actions
- Fase 8: hardening básico, documentación final y preparación liviana para Kubernetes

## Buenas prácticas Git sugeridas

- `main` protegida
- trabajo en ramas `feature/*`
- cambios vía Pull Request
- checks obligatorios antes de merge
- squash merge para mantener historial legible

## Riesgos de sobreingeniería que vamos a evitar

- microservicios de negocio
- colas o brokers desde el inicio
- autenticación compleja
- Terraform inicial
- GitOps inicial
- frontend recargado
- patrones de abstracción innecesarios

## Estado actual

La Fase 1 quedó documentada y el repositorio fue inicializado con Git. La implementación empieza en la siguiente fase.

