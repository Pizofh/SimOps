# Backend

Backend monolítico de SimOps implementado con FastAPI, SQLAlchemy, Alembic, Pydantic y Uvicorn.

## Alcance de esta fase

- modelo `Event`
- endpoints del MVP backend
- conexión SQLAlchemy
- migración inicial Alembic
- métricas Prometheus
- logs estructurados JSON
- tests mínimos con Pytest

## Estructura

```text
backend/
  app/
    config.py
    crud.py
    database.py
    enums.py
    logging_config.py
    main.py
    metrics.py
    middleware.py
    models.py
    schemas.py
    routers/
      events.py
      ops.py
  alembic/
    env.py
    versions/
  tests/
```

## Variables de entorno

- `SIMOPS_DATABASE_URL`
- `SIMOPS_LOG_LEVEL`
- `SIMOPS_ENVIRONMENT`
- `SIMOPS_DEFAULT_QUERY_LIMIT`
- `SIMOPS_MAX_QUERY_LIMIT`

Referencia inicial:

- `backend/.env.example`
- Si usas PostgreSQL local, `SIMOPS_DATABASE_URL` debe incluir credenciales validas.
- Si usas la base en Docker Compose, la URL inicial recomendada es `postgresql+psycopg://simops:simops@localhost:5432/simops`.

## Comandos esperados

Ejecutar desde `backend/`.

Instalación:

```bash
pip install -e .[dev]
```

Migraciones:

```bash
alembic upgrade head
```

Ejecutar API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Tests:

```bash
pytest
```

Lint:

```bash
ruff check .
```

Bandit:

```bash
bandit -r app
```
