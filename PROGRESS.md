# Progreso — Mapa Apagones

Registro vivo de qué funciona, qué cambió y qué sigue. Se actualiza en cada sesión de trabajo relevante.

## Arquitectura verificada (2026-09-16)

```
GitHub (odegaard12/Mapa-Apagones)
  └─ push a main
       ├─ Cloudflare Pages → build automático del frontend estático (frontend/, dist/ con _headers)
       └─ (sin Cloudflare Workers/wrangler: solo Pages)

Backend real:
  Raspberry .103 (srv-web-01-lan) → docker-compose.yml → apagones_backend + apagones_web (nginx proxy /api/)
  Raspberry .104 → no confirmado si participa; no se ha detectado que sirva Mapa-Apagones
```

**VERIFICADO** (no repetir investigación):
- CSP, HSTS, Referrer-Policy, X-Frame-Options, Permissions-Policy: en `frontend/public/_headers` (Cloudflare Pages) y `frontend/nginx.conf` (Docker local).
- CORS: `ALLOWED_ORIGINS` restringido, `allow_credentials=False`.
- SQL parametrizado en todo `backend/app/main.py`; el único `f"..."` interpola un identificador validado por regex whitelist (`quote_sqlite_identifier`), no input de usuario.
- Hashing anónimo (HMAC-SHA256) para token/IP, sin PII.
- Rate limiting: `assert_not_rate_limited` (escritura) y `assert_not_public_read_rate_limited` (lectura).
- CI (`ci.yml`): smokes backend/frontend/docker + repo_guard. Secret-scan (`secret-scan.yml`): gitleaks pinneado a SHA.
- Dependencias backend sin CVEs conocidos tras upgrade de starlette 1.0.1→1.6.0 e idna 3.13→3.19 (PR #222).
- Cobertura geográfica: 19/19 comunidades y ciudades autónomas de España ya incluidas en el dataset "Toda España".

**BLOQUEADO** (documentado, no perder tiempo re-intentando sin nueva info):
- Acceso SSH directo a `.103`/`.104` desde este entorno de agente: red alcanzable (puerto 22 abierto) pero la clave `~/.ssh/id_ed25519_oscar_admin_2026` local es rechazada (`Permission denied (publickey)`). El despliegue real a la Raspberry requiere que el usuario ejecute `git pull && docker compose up -d --build` él mismo, o que autorice la clave pública en `authorized_keys` de esas máquinas.
- Docker no está instalado en este entorno Windows del agente → pruebas de frontend/backend se hacen con `uvicorn` + `vite` directos, no con `docker compose`.
- Cierre manual de PRs viejos de Dependabot (#216, #215, #213, #212, #211) vía la UI del navegador embebido: la UI de GitHub requiere doble-clic consistente para el diálogo de confirmación; se dejó pendiente porque Dependabot los cerrará solo en su próximo escaneo al detectar que main ya tiene versiones iguales o más recientes.

## Qué funciona

- Reporte ciudadano de incidencia → creación/actualización de incidente → agregación por zona → visible en mapa.
- Auto-detección de "corte confirmado" (5+ reportes en 10 min en la misma zona) — PR #220.
- Health check real: `/api/health` ahora hace `SELECT 1` contra la base de datos en vez de devolver `{"ok": true}` fijo.
- Botón manual "↻ Actualizar" en el panel de zonas, conectado a `loadIncidents()` real (verificado con petición HTTP real en el navegador).
- Panel de detalle de incidencia muestra fecha/hora exacta de detección y última actualización, además del relativo "hace X min".

## Qué cambió en esta sesión (2026-09-16)

1. **Bug real corregido, afecta a producción**: `/api/zones` (el endpoint que el frontend usa de verdad para listar incidencias, no `/api/incidents`) nunca seleccionaba `created_at` de la tabla `incidents`. Resultado: el panel de detalle mostraba "Detectado: sin datos" para *toda* incidencia, en producción, desde siempre. Encontrado abriendo la app real en un navegador con datos reales, no por lectura de código. Corregido en `backend/app/main.py::zones()`.
2. `/api/health` mejorado: valida conexión real a SQLite; mantiene el campo `"ok"` para no romper el healthcheck de Docker ni los smoke tests existentes.
3. Botón de refresco manual añadido y verificado end-to-end (disparó petición HTTP real a `/api/zones` en el navegador).
4. Fecha/hora exacta de detección y actualización en el panel de detalle (`formatExactDateTime`).
5. Auditoría de seguridad: 4 CVEs reales corregidos en `starlette` (SSRF en Windows vía UNC paths, DoS por parsing de formularios, confusión host/path, `HTTPEndpoint` sin restricción de método) y 1 en `idna` — PR #222.
6. `frontend/public/_headers` creado: la web en producción (Cloudflare Pages) no aplicaba ningún header de seguridad porque solo vivían en `nginx.conf`, que Cloudflare Pages no usa.
7. SEO: manifest PWA, canonical faltante en `/seguridad/`, sitemap/README/changelog sincronizados con la versión real (v0.12.1) — PRs #223, #224.
8. 5 actualizaciones de Dependabot mergeadas (#221); 2 actualizaciones de React 18→19 (#217, #218) dejadas sin mergear porque rompen el build de Cloudflare Pages.

## Siguiente tarea

Ver `TODO.md` para la lista priorizada. Lo inmediato: abrir y mergear el PR de esta rama (`fix/incident-timestamps-and-health`), luego continuar con la auditoría UX/diseño pedida (jerarquía visual, tarjetas, filtros, responsive, accesibilidad, animaciones) y con la investigación de fuentes de distribuidora para Castilla y León, Catalunya, Castilla-La Mancha y Aragón.
