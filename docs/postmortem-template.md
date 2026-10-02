# Postmortem: {{TITLE}}

Estado: borrador · Ejercicio: `{{SCENARIO}}`

Fecha de creación (UTC): {{CREATED_AT}}

Evidencias: {{EVIDENCE}}

## Resumen e impacto

Describir qué dejó de funcionar, para quién y durante cuánto tiempo. Separar indisponibilidad, degradación, pérdida de eventos y pérdida de visibilidad. Distinguir el impacto medido del estimado; marcar lo desconocido.

| Dato | Valor / evidencia |
| --- | --- |
| Inicio del impacto (UTC) | Pendiente |
| Detección (UTC) | Pendiente |
| Mitigación aplicada (UTC) | Pendiente |
| Recuperación verificada (UTC) | Pendiente |
| Tiempo hasta detección | Detección − inicio del impacto |
| Tiempo hasta recuperación | Recuperación verificada − inicio del impacto |
| Eventos perdidos / entrega ambigua | Pendiente; indicar método y límites de la medición |

## Hipótesis y resultado

- Estado inicial y tasa de ingesta:
- Fallo inyectado, comando y duración:
- Síntomas y señales esperados:
- Síntomas y señales observados:
- Diferencias entre predicción y resultado:

## Línea de tiempo

Usar UTC y vincular cada afirmación a logs, captura, consulta o comando. La hora de arranque de un contenedor no demuestra por sí sola recuperación del servicio.

| Hora UTC | Observación / acción | Evidencia |
| --- | --- | --- |
| Pendiente | Estado base | |
| Pendiente | Inyección | |
| Pendiente | Primera señal detectada | |
| Pendiente | Diagnóstico | |
| Pendiente | Mitigación | |
| Pendiente | Recuperación funcional verificada | |

## Causa y factores contribuyentes

- Disparador deliberado del ejercicio:
- Mecanismo técnico que produjo el impacto:
- Decisiones de diseño que ampliaron el impacto:
- Por qué las señales existentes detectaron o no detectaron el fallo:
- Hipótesis descartadas y evidencia:

Describir comportamientos del sistema y condiciones de trabajo, sin atribuir culpas personales. Detener un servicio es el disparador; explicar por qué el sistema no absorbió el fallo.

## Recuperación y validación

- Comandos aplicados y resultado:
- `/health`, `/ready` y lectura de eventos después de recuperar:
- Evidencia de un nuevo evento persistido y visible:
- Estado de métricas y logs después de recuperar:
- Datos que permanecieron y envíos que no se recuperaron:
- Cómo se comprobó que el fallo no seguía activo:

## Qué funcionó y qué dificultó la respuesta

- Señales y herramientas útiles:
- Puntos ciegos, confusiones o pasos manuales:
- Información faltante:

## Acciones de seguimiento

Proponer cambios concretos. Una tarea termina cuando su prueba de aceptación pasa, no solo cuando se añade código.

| Prioridad | Acción / issue | Responsable | Fecha objetivo | Prueba de aceptación | Estado |
| --- | --- | --- | --- | --- | --- |
| Pendiente | | | | | Abierta |

## Repetición del ejercicio

- Cambio que se probará:
- Hipótesis revisada:
- Métrica o comportamiento que debería mejorar:
- Resultado del nuevo ejercicio y enlace a su postmortem:
