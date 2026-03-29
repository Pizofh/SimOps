# Roadmap de ejecución

## Fase 1: Diseño técnico

- definir estructura del repo
- documentar arquitectura
- definir contrato inicial de API
- definir modelo de datos
- fijar criterios de aceptación del MVP

Entregable: base documental coherente y lista para implementar.

## Fase 2: Backend funcional

- crear app FastAPI
- configurar SQLAlchemy, Alembic y Pydantic
- implementar endpoints del MVP
- conectar PostgreSQL
- añadir logs estructurados
- exponer métricas Prometheus
- crear tests mínimos con Pytest

Entregable: API funcional y testeada.

## Fase 3: Simulator

- crear servicio Python separado
- configurar variables de entorno
- enviar eventos periódicos al backend
- simular fallos, latencia y bursts
- emitir logs estructurados

Entregable: generador de carga/eventos reproducible.

## Fase 4: Frontend mínimo

- crear app Vue 3 + Vite
- listar eventos
- añadir filtros simples
- mostrar resumen y detalle

Entregable: UI mínima para demostrar consumo de API.

## Fase 5: Docker + Compose

- dockerizar backend, frontend y simulator
- definir `docker-compose.yml`
- conectar DB, observabilidad y app
- añadir healthchecks

Entregable: entorno local completo levantado con un comando.

## Fase 6: Observabilidad

- configurar Prometheus
- configurar Loki y Promtail
- provisionar Grafana
- crear dashboards básicos

Entregable: métricas y logs visibles en Grafana.

## Fase 7: CI

- workflow GitHub Actions
- lint backend
- tests backend
- SAST y audit
- lint frontend
- verificación de build

Entregable: checks obligatorios para PRs.

## Fase 8: Hardening básico

- ejecutar contenedores con usuario no root cuando aplique
- revisar headers y defaults inseguros
- mejorar README final
- dejar notas para futura carpeta `k8s/`

Entregable: cierre de portfolio con mejor señal de madurez operativa.

## Definition of done del MVP

- el sistema levanta completo con Docker Compose
- el simulador genera tráfico útil
- el backend persiste y expone eventos
- el frontend consulta y muestra eventos
- Prometheus recoge métricas
- Loki centraliza logs
- Grafana visualiza ambos
- CI valida calidad y seguridad básica

