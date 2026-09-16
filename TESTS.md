# Registro de pruebas reales — Mapa Apagones

Solo pruebas realmente ejecutadas, con resultado observado. No se registran pruebas "deberían pasar".

## 2026-09-16 — fix/incident-timestamps-and-health

**Entorno**: sin Docker disponible en el agente. Backend con `uvicorn` directo (`DB_PATH` temporal, Turnstile desactivado), frontend con `vite` directo (`.env.local` temporal apuntando a `http://127.0.0.1:8000`, no commiteado).

| Prueba | Comando / acción | Resultado |
|---|---|---|
| Health check | `curl http://127.0.0.1:8000/api/health` | `{"ok":true,"database":"ok","checked_at":"..."}` — 200 OK |
| Smoke backend API | `python scripts/smoke_backend_api.py` | OK backend preflight smoke + OK backend API smoke |
| Smoke backend schema | `python scripts/smoke_backend_schema.py` | OK |
| Smoke backend status | `python scripts/smoke_backend_status.py` | OK |
| Smoke backend lifecycle | `python scripts/smoke_backend_lifecycle.py` | OK |
| Build frontend | `npm run build` (frontend) | Compila sin errores, 65 módulos, `_headers` presente en `dist/` |
| Smoke frontend estático | `python scripts/smoke_frontend_static.py` | OK, `version=v0.12.1` |
| Reporte real | `curl -X POST /api/report {lat, lng, type: sin_luz, token}` | Crea incidente real (`af09a1d7-...`), `report_count_active: 1` |
| **Bug encontrado**: detalle de incidencia en navegador | Abrí la app en `http://localhost:5173`, clic en la zona creada, leí el panel de detalle | "Detectado" mostraba **"sin datos"** pese a que `/api/incidents` sí trae `created_at` — el frontend usa `/api/zones`, que no lo traía |
| Verificación de causa | `curl /api/zones?hours=24` | Confirmado: el `SELECT` de `latest_incident` en `zones()` no pedía `created_at` |
| Fix aplicado + reinicio backend | Editar `main.py`, matar proceso viejo en :8000 (`taskkill`), reiniciar `uvicorn` | `curl /api/zones` ahora incluye `created_at` |
| Verificación en navegador tras fix | Recargar `http://localhost:5173`, clic en la misma zona | "Detectado: 16/09/2026, 20:42" — correcto |
| Botón "↻ Actualizar" | Click real vía `dispatchEvent`/`.click()` en el botón, `read_network_requests` con `urlPattern=zones` | Confirmadas múltiples peticiones `GET /api/zones?...` disparadas por el botón — funciona |
| Re-run smoke suite tras fix | Los 4 scripts de backend de nuevo | Todos OK |
| Re-run build + smoke frontend tras fix | `npm run build` + `smoke_frontend_static.py` | OK |

**Nota de plataforma (no bug real)**: `smoke_backend_api.py` y `smoke_backend_status.py` imprimen su `OK ...` correctamente pero luego lanzan `RuntimeError: uvicorn terminó con código 1` en el bloque `finally`. Causa: `proc.terminate()` en Windows no produce los códigos de salida POSIX (`-15`/`143`) que el script espera tras `SIGTERM`; en el CI real (Ubuntu) esto no ocurre. Preexistente, no introducido en esta sesión.

## Pendiente de probar

- Flujo completo de reporte (`sendReport`) con Turnstile activo — se probó con Turnstile desactivado únicamente.
- Docker Compose real (`docker compose up -d --build`) — no disponible en este entorno; requiere ejecutarse en la Raspberry `.103` o en una máquina con Docker.
- Despliegue real en Cloudflare Pages tras merge — pendiente de confirmación con `curl` a `mapa-apagones.es` después de cada PR mergeado.
