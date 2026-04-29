# Stability plan

## Regla principal

No mezclar cambios de UX, geografía, backend, Turnstile y limpieza de estado en el mismo PR.

## Orden obligatorio antes de nuevas mejoras

1. Base estable.
2. Guardas de repo y CI.
3. Tests/smoke manuales.
4. Refactor pequeño.
5. Nueva funcionalidad detrás de un cambio aislado.

## Cosas que no deben volver a entrar al repo

- `_backups/`
- `diagnostics/`
- bases SQLite reales
- logs
- `.env`
- GeoJSON nacionales brutos o ficheros generados pesados no curados

## Checklist antes de mergear

- `bash scripts/repo_guard.sh`
- `npm --prefix frontend run build`
- `docker compose up -d --build`
- `bash scripts/smoke_local.sh`
- probar en navegador:
  - cargar página
  - reportar incidencia
  - confirmar “Yo también”
  - marcar “Ya volvió”
  - recargar
  - revisar consola sin errores rojos

## Geografía

Las comunidades nuevas deben volver en PR separado y pequeño.

Primero se debe diseñar una arquitectura clara para:
- datasets municipales,
- zonas agregadas,
- selección manual,
- incidencia guardada,
- visualización de polígonos,
- fallback de celda.

No se debe volver a pintar a la vez celda y municipio para la misma incidencia.
