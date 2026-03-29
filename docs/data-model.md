# Modelo de datos inicial

## Entidad principal: Event

El MVP requiere una sola entidad persistida: `events`.

## Tabla `events`

| Campo | Tipo | Nulo | Descripción |
| --- | --- | --- | --- |
| `id` | UUID | no | Identificador único del evento |
| `service_name` | VARCHAR(100) | no | Nombre del servicio origen |
| `severity` | VARCHAR(32) | no | Nivel o tipo principal del evento |
| `message` | TEXT | no | Descripción del evento |
| `environment` | VARCHAR(32) | no | Entorno lógico, por ejemplo `dev`, `lab`, `prod-sim` |
| `response_time_ms` | INTEGER | sí | Tiempo de respuesta observado |
| `status_code` | INTEGER | sí | Código HTTP o código simulado |
| `source` | VARCHAR(64) | sí | Fuente del evento, por ejemplo `simulator` |
| `metadata` | JSONB | sí | Información adicional flexible |
| `created_at` | TIMESTAMPTZ | no | Fecha lógica del evento |
| `ingested_at` | TIMESTAMPTZ | no | Fecha de persistencia en backend |

## Decisiones de modelado

- `id` será UUID para facilitar demos distribuidas y evitar exponer secuencias.
- `created_at` representa el tiempo del evento.
- `ingested_at` representa el tiempo real en que el backend lo guardó.
- `metadata` se mantiene libre para no sobrediseñar subtablas.
- `severity` inicia como string validado por aplicación; no hace falta un catálogo separado.

## Severidades iniciales soportadas

- `info`
- `warning`
- `error`
- `timeout`
- `latency_spike`

Nota: el concepto de "burst de errores" se tratará como patrón de generación del simulator, no como una severidad adicional.

## Índices iniciales recomendados

- índice por `created_at DESC`
- índice por `severity`
- índice por `service_name`
- índice compuesto por `environment, created_at DESC`

## Fuera de alcance del MVP

- tablas de usuarios
- tablas de servicios registradas
- auditoría avanzada
- retención por políticas
- particionamiento
- archivado

