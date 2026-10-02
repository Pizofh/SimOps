# Laboratorio de incidentes

El objetivo es repetir el ciclo **hipótesis → fallo → detección → diagnóstico → recuperación → postmortem → mejora → repetición** sobre el Compose local. Ejecutar un escenario a la vez y registrar resultados observados.

## Preparar el estado base

Requisitos: Docker con contenedores Linux, Docker Compose v2 y Windows PowerShell 5.1 o PowerShell 7. Los comandos siguientes se ejecutan desde la raíz del repositorio. En PowerShell 7 se puede sustituir `powershell` por `pwsh`.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose up --build -d
powershell -File scripts/lab.ps1 -Action Status
```

Esperar a que estén los ocho servicios en ejecución y `/ready` responda 200. Abrir el frontend (`http://localhost:8080`) y Grafana (`http://localhost:3000`), iniciar sesión con las credenciales de `.env` y abrir **SimOps Overview**. Comprobar que entran eventos y que aparecen logs recientes. Dejar correr al menos un minuto para tener varias muestras de Prometheus; el scrape ocurre cada 15 segundos y los paneles usan ventanas de cinco minutos.

Con los puertos por defecto, comprobar una escritura real:

```powershell
$apiBase = 'http://localhost:8000' # Ajustar si cambiaste BACKEND_PORT.
$payload = @{
    service_name = 'lab-probe'
    severity = 'info'
    message = 'Prueba funcional del laboratorio'
    environment = 'lab'
    source = 'manual-probe'
} | ConvertTo-Json
$created = Invoke-RestMethod -Method Post -Uri "$apiBase/events" -ContentType 'application/json' -Body $payload
Invoke-RestMethod -Uri "$apiBase/events/$($created.id)"
```

Registrar el ID y la hora UTC. Un evento `lab-probe` queda almacenado intencionalmente como evidencia funcional.

Antes de detener un servicio, escribir qué fallará, qué seguirá disponible y cuál señal permitirá distinguir la causa. Capturar la base si se desea:

```powershell
powershell -File scripts/lab.ps1 -Action Snapshot
```

## Ejecutar un ejercicio

```powershell
powershell -File scripts/lab.ps1 -Action Drill -Scenario database-down -DurationSeconds 30
```

`Drill` exige el stack completo en ejecución y `/ready` 200. Descubre el puerto publicado del backend para hacer las sondas desde `127.0.0.1`; funciona con puertos personalizados y enlaces locales. Requiere que ese acceso local esté permitido por `SIMOPS_ALLOWED_HOSTS`.

El script detiene **un servicio**, captura el fallo, deja tiempo para observarlo y ejecuta `start` en un bloque `finally`. La duración admite de 15 a 300 segundos y cuenta desde que finaliza `stop`; incluye la captura durante el fallo. Las sondas tienen timeout y la captura puede alargar un ejercicio corto. Después espera hasta aproximadamente un minuto por el servicio en ejecución, `/ready` 200 y lectura de eventos 200. Esto es una comprobación parcial: verificar también escritura, generación y logs según el escenario.

Las capturas quedan en `artifacts/lab/<sesión>/`, fuera de Git:

- `exercise.json`: escenario, servicio, duración solicitada y URL local.
- `timeline.txt`: solicitudes de stop/start, capturas y resultado de comprobaciones, con horas UTC.
- `before/`, `during/`, `after/`: estado Compose, logs recientes y sondas HTTP a `/health`, `/ready`, `/events` y `/metrics` con código, duración y respuesta/error.

Se crea un borrador en `docs/incidents/` para completar al terminar. Los logs están limitados a los últimos cinco minutos y 200 líneas por servicio: no permiten calcular por sí solos la pérdida total de eventos. Conservar evidencias adicionales cuando se necesiten.

No ejecutar `docker compose down -v` para recuperar: elimina los volúmenes y los datos del ejercicio. Si se cierra forzosamente la terminal, Docker deja de responder o falla `start`, la recuperación automática puede no completarse; usar el comando de recuperación de la tabla y volver a verificar el estado.

## Escenarios iniciales

| Escenario | Hipótesis y diagnóstico esperado | Recuperación manual | Criterio funcional de cierre |
| --- | --- | --- | --- |
| `database-down` | `/health` y `/metrics` siguen respondiendo; `/ready` 503 y operaciones de eventos fallan. `up` puede seguir en 1. Buscar `event_persist_failed`, `readiness_check_failed` y errores de conexión SQL. | `docker compose start db` | `/ready` 200, crear/leer `lab-probe` y nuevos `event_delivered` del simulador. Datos anteriores conservados. |
| `backend-down` | Frontend estático sigue cargando, pero sus consultas fallan. Simulador registra `event_delivery_failed`. Prometheus muestra `up` 0 después del siguiente scrape. | `docker compose start backend` | `/ready` 200, crear/leer evento, frontend consulta y simulador entrega otra vez. Ver reinicio de contadores. |
| `simulator-down` | API y base siguen disponibles; desaparecen nuevos eventos automáticos. `up` sigue en 1. La tasa se reduce gradualmente en paneles con ventana de 5 min. | `docker compose start simulator` | Nuevo evento con `source=simulator`, nuevo `event_delivered` y timestamps que avanzan. |
| `logs-down` | Al detener Promtail continúan las escrituras y métricas, pero Loki deja de recibir logs nuevos. Comparar con `docker compose logs --since 1m backend simulator`. | `docker compose start promtail` | Logs nuevos en Loki después de recuperar. Revisar huecos/duplicados por las posiciones no persistentes. |

Cambiar `-Scenario` en el comando para practicar cada uno. Conservar un evento previo y consultarlo después de la recuperación de base/API para comprobar persistencia. Los envíos fallidos del simulador se descartan; recuperar el servicio permite nuevas entregas, pero no reconstruye los envíos descartados. Un fallo de entrega tampoco demuestra siempre ausencia del evento: pudo persistirse antes de perderse la respuesta.

## Consultas para diagnosticar

En Grafana Explore seleccionar **Prometheus**. Usar la ventana que abarque todo el incidente.

Disponibilidad del endpoint de métricas:

```promql
up{job="simops-backend"}
```

Eventos persistidos por segundo:

```promql
sum(rate(total_events_received_total{job="simops-backend"}[1m]))
```

HTTP 5xx de operaciones de eventos por minuto; si no existe aún la serie, el resultado puede estar vacío:

```promql
sum(increase(http_requests_total{job="simops-backend",path=~"/events.*",status_code=~"5.."}[1m]))
```

p95 de latencia de operaciones de eventos, en segundos:

```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{job="simops-backend",path=~"/events.*"}[5m])))
```

Separar las categorías de errores:

```promql
sum by (category) (increase(errors_total{job="simops-backend"}[1m]))
```

`event_error` y `event_timeout` cuentan eventos sintéticos aceptados; `db_error`, `db_readiness_error`, `request_exception` y `http_5xx` señalan otros fallos. Una misma petición puede incrementar varias categorías. El `status_code` y `response_time_ms` dentro del payload describen un servicio ficticio; el código HTTP y la duración registrados por el middleware describen la API real.

En Explore seleccionar **Loki**:

```logql
{compose_service="simulator"} |= "event_delivery_failed"
```

```logql
{compose_service="backend"} |= "event_persist_failed"
```

Para correlacionar una solicitud, copiar su `request_id` desde el log del simulador y buscarlo:

```logql
{compose_service=~"backend|simulator"} |= "PEGAR_REQUEST_ID"
```

Las sondas de la herramienta usan un `X-Request-ID` con prefijo `simops-lab-`. Las sondas también generan tráfico y logs; considerar esa actividad al interpretar las métricas.

## Dos ejercicios manuales adicionales

### Payload inválido

Con la API recuperada, ejecutar:

```powershell
Invoke-WebRequest -UseBasicParsing -Method Post -Uri "$apiBase/events" -ContentType 'application/json' -Body '{"severity":"invalid"}'
```

Esperar HTTP 422 (PowerShell lo presenta como excepción), sin evento persistido. Comprobar que sigue funcionando la escritura válida y que no se confunde validación con indisponibilidad. Crear un borrador copiando [la plantilla](postmortem-template.md), con escenario `invalid-payload`.

### Ráfagas y severidades sintéticas

Registrar los valores originales de estas variables en `.env`. Cambiar temporalmente:

```dotenv
SIMULATOR_INTERVAL_SECONDS=0.5
SIMULATOR_BURST_RATE=1
SIMULATOR_BURST_MIN_SIZE=5
SIMULATOR_BURST_MAX_SIZE=5
SIMULATOR_MAX_RANDOM_DELAY_MS=0
SIMULATOR_FAILURE_RATE=0.8
```

Aplicar con `docker compose up -d --no-deps --force-recreate simulator`. Observar durante un minuto, capturar evidencias y restaurar los valores originales con el mismo comando. Guardar el resultado como escenario `synthetic-burst` usando la plantilla.

Este productor envía peticiones secuenciales; no es una prueba de carga concurrente ni garantiza saturar el sistema. `FAILURE_RATE` cambia severidades del payload y `MAX_RANDOM_DELAY_MS` retrasa al productor antes del envío. Para medir saturación o latencia real de la API se necesita un ejercicio adicional, basado en las duraciones HTTP observadas.

## Completar y repetir el postmortem

1. Confirmar recuperación funcional con los criterios de la tabla y guardar evidencia del evento nuevo.
2. Completar impacto, hipótesis frente a resultado, línea de tiempo UTC y mecanismo causal en el borrador.
3. Anotar lo desconocido: no inventar número de eventos perdidos ni tiempos exactos a partir de paneles agregados.
4. Elegir una mejora con responsable y prueba de aceptación.
5. Repetir el mismo ejercicio y comparar detección, recuperación y continuidad de entrega.

Posibles primeras mejoras basadas en los hallazgos: sondeo de readiness y alertas; un contador de fallos de entrega del simulador; reintentos con backoff más idempotencia para evitar duplicados; persistencia de posiciones del recolector. Priorizar después de observar el fallo.

Para detener el laboratorio conservando datos: `docker compose down`.
