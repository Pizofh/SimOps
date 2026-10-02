# Registro de ejercicios

Guardar aquí los postmortems completados con el nombre `fecha-UTC-escenario-id.md`.

El comando `powershell -File scripts/lab.ps1 -Action NewPostmortem -Scenario database-down` crea un borrador desde [la plantilla](../postmortem-template.md). `-Action Drill` también crea uno y enlaza sus evidencias locales.

Para publicar un postmortem, completar hipótesis, impacto, línea de tiempo, recuperación y acciones verificables. Adjuntar o enlazar las evidencias relevantes: `artifacts/lab/` está excluido de Git y sus enlaces solo funcionarán en la máquina donde se ejecutó el ejercicio. Revisar logs antes de compartirlos.

No se incluyen incidentes ficticios como si fueran resultados medidos. Añadir cada resultado después de ejecutar el laboratorio y verificar la recuperación.
