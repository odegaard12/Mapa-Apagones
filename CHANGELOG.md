# Changelog

## v0.10.5.5-extremadura-distributor-review

### Distribuidoras / revisión Extremadura

- Añade una revisión previa de Extremadura antes de importar pistas públicas de distribuidora.
- Genera `docs/research/distributor_import_batches/extremadura_import_review.md` desde el GeoJSON real de Extremadura.
- Documenta que Extremadura tiene 388 municipios/zonas pendientes de clasificación.
- Documenta fuentes públicas de alto nivel y la razón para no importar toda la comunidad como una única distribuidora todavía.
- No importa nuevas distribuidoras.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, geografía ni datos productivos.

## v0.10.5.4-public-status-readonly-smoke

### Operaciones / producción pública

- Amplía `scripts/smoke_public_readonly.sh` para comprobar `/api/status` en producción pública.
- Renombra las claves públicas de `/api/status` relacionadas con HMAC anónimo para evitar exponer nombres internos de variables sensibles.
- Valida que `/api/status` devuelva JSON y no exponga secretos, rutas privadas, IPs privadas ni CIDRs reales.
- Actualiza la guardia `scripts/check_public_readonly_smoke.py` para exigir la comprobación de `/api/status`.
- Actualiza la documentación del runbook público read-only.
- No crea reportes, no llama a `/api/report` y no cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, geografía ni datos de distribuidoras.


## v0.10.5.3-reporting-timing-smoke

### Reportes / timing y salud operativa

- Añade `scripts/smoke_reporting_timing.py` para medir duración de los smokes locales críticos de reportes.
- Mide API básica, ciclo de vida de reportes, concurrencia y privacidad/abuso.
- Añade `scripts/check_reporting_timing_smoke.py` para asegurar que el timing smoke sigue siendo local y no llama a producción.
- Documenta el runbook en `docs/ops/reporting-timing-smoke.md`.
- Integra la guardia estática en repo guard y el timing smoke en post-merge validation.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, geografía ni datos de distribuidoras.


## v0.10.5.2-public-readonly-smoke

### Operaciones / producción pública

- Añade `scripts/smoke_public_readonly.sh` para comprobar producción pública sin crear reportes.
- El smoke valida web pública, changelog, JSON público de distribuidoras, `/api/health` y `/api/incidents?limit=5`.
- Añade `scripts/check_public_readonly_smoke.py` para asegurar que el smoke sigue siendo read-only y no llama a `/api/report`.
- Documenta el runbook en `docs/ops/public-readonly-smoke.md`.
- No integra el smoke externo como CI obligatorio para evitar dependencia de red/producción.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, geografía ni datos de distribuidoras.



## v0.10.5.1-hint-quality-reporting-audit

### Auditoría / calidad de datos y reportes

- Añade auditoría generada de calidad de pistas de distribuidora actuales.
- Añade auditoría generada de salud runtime del flujo de reportes.
- Integra ambas auditorías en las guardias del repositorio.
- Verifica cobertura de fuentes, fechas, confianza, duplicados y datasets con pistas.
- Verifica que los smokes de reportes cubren API, lifecycle, concurrencia, privacidad/abuso y Docker Compose.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, geografía ni datos de distribuidoras.



## v0.10.5.0-comunitat-valenciana-distributor-hints

### Distribuidoras / datos públicos

- Añade pistas públicas de distribuidora para los 544 municipios de Comunitat Valenciana.
- Usa i-DE como `regional_default` prudente donde no hay excepción local identificada.
- Añade 11 excepciones cooperativas/locales como `verified_partial`.
- Regenera la matriz de cobertura: 1.959 zonas con pista pública y 6.256 pendientes.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite ni datasets geográficos.



## v0.10.4.9-euskadi-distributor-hints

### Distribuidoras / datos públicos

- Añade pistas públicas de distribuidora para los 255 municipios de Euskadi.
- Usa i-DE como `regional_default` prudente donde no hay excepción local identificada.
- Añade excepciones locales `verified_partial` para Tolosa/Tolargi, Oñati/Oñargi y Aramaio/Aramaioko Argindar Banatzailea.
- Regenera la matriz de cobertura: 1.415 zonas con pista pública y 6.800 pendientes.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite ni datasets geográficos.



## v0.10.4.8-public-changelog-refresh

### Changelog público

- Corrige el changelog público para mostrar la versión actual en orden correcto.
- Añade la entrada pública que faltaba para `v0.10.4.7-melilla-distributor-plus-review`.
- Actualiza la fecha visible del changelog público a `2026-05-10`.
- Añade `scripts/check_public_changelog_current.py` para evitar que la versión actual falte o aparezca antes del encabezado.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, geografía ni datos de distribuidoras.



## v0.10.4.7-melilla-distributor-plus-review

### Distribuidoras / datos públicos

- Añade pista pública conservadora para Melilla con GASELEC.
- Añade revisión previa para Madrid antes de cualquier importación masiva.
- Añade plan de siguientes lotes de distribuidoras.
- Regenera la matriz de cobertura de distribuidoras desde los datos reales del repositorio.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite ni datasets geográficos.



## v0.10.4.6-distributor-coverage-metadata

### Distribuidoras / cobertura

- Corrige la matriz de cobertura para leer `confidence`, `source_name`, `source_url` y `last_reviewed` dentro de `distributors[]`.
- Regenera `docs/research/distributor_coverage_matrix.md` desde los datos reales del repositorio.
- Mantiene intactos los conteos de cobertura geográfica.
- No importa nuevas distribuidoras.
- No cambia backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite ni datasets geográficos.



## v0.10.4.5-distributor-coverage-matrix

### Distribuidoras / cobertura

- Añade `docs/research/distributor_coverage_matrix.md` generada desde los GeoJSON y `distributor_hints.json` reales del repositorio.
- Añade `scripts/generate_distributor_coverage_matrix.py` para regenerar y validar la matriz.
- Integra la validación de matriz en las guardias del repositorio.
- No importa nuevas distribuidoras.
- No cambia backend, reportes, Turnstile, HMAC, proxy/IP, SQLite ni datasets geográficos.



## v0.10.4.4-geo-dataset-province-guard

### Geografía / calidad de datos

- Limpia del dataset público de Aragón features cuya provincia no pertenece a Aragón.
- Añade `scripts/check_geo_dataset_provinces.py` para validar que cada GeoJSON autonómico solo contenga provincias de su ámbito.
- Integra la nueva guardia en las validaciones del repositorio.
- No cambia backend, reportes, Turnstile, HMAC, proxy/IP, SQLite, distribuidoras ni datos sensibles.



## v0.10.4.3-distributor-data-safety-policy

### Seguridad / datos públicos

- Añadida política pública para futuras incorporaciones de distribuidoras.
- Añadida guardia `scripts/check_distributor_data_safety.py` para bloquear campos o patrones sensibles en `distributor_hints.json`.
- La guardia revisa CUPS, coordenadas privadas, direcciones exactas, datos de suministro, IP/token reales e indicios de infraestructura crítica.
- Integrada la nueva guardia en los scripts de validación del repositorio.
- No cambia runtime del backend, reportes, Turnstile, HMAC, proxy/IP, SQLite, datasets geográficos ni datos de distribuidoras existentes.

## v0.10.4.2-audit-closeout

- Añade `docs/audit/advanced-audit-closeout.md` como cierre de la fase de auditoría avanzada.
- Resume los hallazgos corregidos entre PR #102 y PR #119.
- Diferencia deuda crítica ya cerrada de pendientes no críticos de roadmap normal.
- Añade `scripts/check_audit_closeout.py` e integración en `scripts/repo_guard.sh` y `scripts/post_merge_validate.sh`.
- No cambia runtime de backend, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, distribuidoras ni datasets geográficos.

## v0.10.4.1-public-readme-version-sync

- Sincroniza la versión pública visible en `README.md`, `VERSION` y `APP_VERSION`.
- Corrige la deriva detectada por `scripts/post_merge_validate.sh` tras el merge de `v0.10.4.0-backend-privacy-module`.
- Mantiene el runbook post-merge como comprobación obligatoria después de merges relevantes.
- No cambia backend runtime, frontend funcional, reportes, Turnstile, HMAC, proxy/IP, SQLite, distribuidoras ni datasets geográficos.

## v0.10.4.0-backend-privacy-module

- Extrae helpers de privacidad/HMAC a `backend/app/privacy.py`.
- Mantiene `backend/app/main.py` usando `anon_hash`, `anon_hash_candidates` y `sql_in_clause` desde el nuevo módulo.
- Actualiza la guardia de hashes anónimos para validar `main.py` + `privacy.py`.
- Añade `scripts/check_backend_privacy_module.py` e integración en `scripts/repo_guard.sh`.
- Actualiza el runbook post-merge para incluir la nueva guardia.
- No cambia reportes, anonimización, Turnstile, proxy/IP, SQLite, frontend funcional, distribuidoras ni datasets geográficos.

## v0.10.3.9-backend-settings-module

- Extrae la configuración de backend a `backend/app/settings.py`.
- Reduce responsabilidad de `backend/app/main.py` sin cambiar comportamiento público.
- Centraliza variables de entorno, constantes de reportes, Turnstile, HMAC, proxy/IP, geografía y límites API.
- Añade `scripts/check_backend_settings_module.py` e integración en `scripts/repo_guard.sh`.
- No cambia reportes, privacidad, Turnstile, HMAC, proxy, SQLite, frontend funcional, distribuidoras ni datasets geográficos.

## v0.10.3.8-post-merge-validation-runbook

- Añade `scripts/post_merge_validate.sh` como runbook ejecutable de validación post-merge.
- Agrupa guardias de privacidad, proxy/IP, HMAC, schema SQLite, dependencias, geografía, frontend estático, backend runtime y Docker Compose.
- Añade `scripts/check_post_merge_validation.sh` e integración en `scripts/repo_guard.sh`.
- Documenta el uso del runbook en `README.md`.
- No cambia runtime de backend, frontend funcional, reportes, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.3.7-sqlite-schema-hardening

- Endurece el schema SQLite del backend.
- Limpia duplicados activos antiguos por `incident_id` + `reporter_token_hash` antes de crear constraints.
- Añade índice único parcial `uq_reports_active_incident_reporter` para impedir más de un reporte activo del mismo reporter anónimo en la misma incidencia.
- Añade índices útiles para reports, expiración, zonas y action_log.
- Añade `scripts/check_sqlite_schema_hardening.py`.
- Añade `scripts/smoke_backend_schema.py` e integración en GitHub Actions.
- No añade datos personales, no cambia frontend funcional, no cambia Turnstile, no cambia HMAC, no cambia distribuidoras ni datasets geográficos.

## v0.10.3.6-safe-runtime-status

- Añade `/api/status` como endpoint operativo seguro del backend.
- Expone solo checks agregados y booleanos: DB, tablas requeridas, HMAC, Turnstile, proxy confiable y debug.
- No devuelve secretos, tokens, IPs, rutas privadas, CIDRs reales ni datos de usuarios.
- Añade `scripts/check_safe_status_endpoint.py`.
- Añade `scripts/smoke_backend_status.py` e integración en GitHub Actions.
- Integra la guardia en `scripts/repo_guard.sh`.
- No cambia frontend funcional, reportes, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.3.5-frontend-static-smoke-ci

- Añade `scripts/smoke_frontend_static.py` para validar el build estático del frontend.
- Comprueba `dist/index.html`, assets JS/CSS, `changelog.html`, `robots.txt`, `sitemap.xml` y `dist/data/distributor_hints.json`.
- Verifica que la versión pública actual aparece en el JS construido y en el changelog público.
- Comprueba que el JSON público de distribuidoras se copia igual desde `frontend/public/data`.
- Añade una revisión básica contra artefactos o textos sensibles/locales dentro de `dist`.
- Integra el smoke en GitHub Actions después del build frontend.
- Añade `scripts/check_frontend_static_smoke.py` e integra la guardia en `repo_guard.sh`.
- No cambia backend, reportes, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.3.4-architecture-privacy-pipeline-docs

- Añade documentación de arquitectura de reportes, privacidad, anti-abuso, proxy/IP, Turnstile, SQLite, CI y datos de distribuidoras.
- Documenta explícitamente qué datos no se piden ni se deben añadir: cuentas, login, CUPS, texto libre, fotos, direcciones exactas o coordenadas privadas.
- Explica el uso de HMAC-SHA256 para `reporter_token_hash` e `ip_hash`.
- Explica la confianza en proxy mediante `TRUST_PROXY_HEADERS` y `TRUSTED_PROXY_CIDRS`.
- Añade `scripts/check_architecture_docs.py` e integra la guardia en `repo_guard.sh`.
- No cambia runtime, frontend, reportes, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.3.3-backend-privacy-abuse-smoke

- Añade `scripts/smoke_backend_privacy_abuse.py` para validar privacidad y anti-abuso en runtime.
- Comprueba que `reporter_token_hash` e `ip_hash` se guardan como hashes HMAC hex64, no como tokens o IPs reales.
- Comprueba que los tokens de prueba y la IP raw no aparecen en columnas de texto de la SQLite temporal.
- Valida que el límite anti-abuso por IP responde con `429` al superar el umbral.
- Integra el smoke en GitHub Actions.
- Añade `scripts/check_backend_privacy_abuse_smoke.py` e integra la guardia en `repo_guard.sh`.
- No cambia el flujo público de usuario, Turnstile, distribuidoras ni datasets geográficos.

## v0.10.3.2-backend-report-lifecycle-smoke

- Añade `scripts/smoke_backend_lifecycle.py` para probar un ciclo de vida más real del backend de reportes.
- Valida errores básicos de `/api/report`, agrupación de reportes negativos, `/api/incidents`, filtro `bbox` y señales `Ya volvió`.
- Comprueba en SQLite temporal que varias señales quedan agrupadas y que las señales de restauración neutralizan la incidencia.
- Integra el smoke en GitHub Actions.
- Añade `scripts/check_backend_lifecycle_smoke.py` e integra la guardia en `repo_guard.sh`.
- No cambia el flujo público de usuario, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.3.1-docker-compose-smoke-ci

- Añade `docker-compose.ci.yml` para probar el stack Docker real sin tocar el stack local de producción/desarrollo.
- Añade `scripts/smoke_docker_compose.sh`.
- El smoke valida frontend, proxy `/api`, `/api/health`, `/api/report`, `/api/incidents` y `/data/distributor_hints.json`.
- Integra el smoke Docker Compose en GitHub Actions.
- Añade `scripts/check_docker_compose_smoke.py` e integra la guardia en `repo_guard.sh`.
- No cambia el flujo público de usuario, reportes, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.3.0-reproducible-build-lockfiles

- Añade lockfile de frontend con `frontend/package-lock.json`.
- Añade lockfile de backend con `backend/requirements.lock.txt`.
- Cambia CI y Dockerfiles para usar instalaciones reproducibles: `npm ci` y `requirements.lock.txt`.
- Añade `scripts/check_dependency_locks.py` e integra la guardia en `repo_guard.sh`.
- Mejora la reproducibilidad sin cambiar el flujo público de usuario, reportes, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.2.9-backend-report-concurrency-smoke

- Añade un smoke de concurrencia de backend para reportes simultáneos.
- Serializa con `BEGIN IMMEDIATE` el endpoint `/api/report` para evitar duplicados concurrentes en la misma celda.
- Añade una guardia automática para mantener esa protección transaccional.
- Arranca Uvicorn con SQLite temporal y entorno de test.
- Envía varios reportes concurrentes en la misma zona y verifica que quedan agrupados en una única incidencia activa.
- Integra el smoke en GitHub Actions después del smoke API básico.
- No cambia runtime de producción, frontend, Turnstile, HMAC, distribuidoras ni datasets geográficos.

## v0.10.2.8-backend-api-smoke-ci

- Añade un smoke real de backend que arranca Uvicorn con SQLite temporal.
- Prueba `/api/health`, `/api/report-preflight`, `/api/report` y `/api/incidents`.
- Integra el smoke en GitHub Actions instalando dependencias reales del backend.
- Usa Turnstile desactivado, IGN desactivado y HMAC anónimo temporal solo para test.
- No cambia runtime de producción, frontend, reportes, distribuidoras ni datasets geográficos.

## v0.10.2.7-trusted-proxy-client-ip

- Endurece la obtención de IP cliente para no confiar ciegamente en `X-Forwarded-For`.
- Solo usa `CF-Connecting-IP`, `X-Real-IP` o `X-Forwarded-For` si la conexión llega desde un proxy confiable.
- Añade `TRUST_PROXY_HEADERS` y `TRUSTED_PROXY_CIDRS` para configurar los proxies autorizados.
- Añade una guardia automática contra el patrón inseguro anterior.
- No cambia reportes, Turnstile, distribuidoras ni datasets geográficos.

## v0.10.2.6-compose-anon-hash-env

- Pasa `ANON_HASH_KEY`, `ANON_HASH_KEY_REQUIRED` y `ANON_HASH_LEGACY_COMPAT` al contenedor backend desde Docker Compose.
- Completa el despliegue operativo del HMAC anónimo añadido en v0.10.2.5.
- Evita depender del fallback transicional a `TURNSTILE_SECRET_KEY`.
- No cambia API, reportes, frontend, distribuidoras ni datasets geográficos.

## v0.10.2.5-hmac-anonymous-hashes

- Cambia los hashes anónimos de token e IP a HMAC-SHA256 con secreto de servidor.
- Añade `ANON_HASH_KEY` y opciones de transición para compatibilidad con hashes antiguos.
- Mantiene el almacenamiento de reportes anónimo y evita publicar IPs, tokens o identificadores reales.
- Añade una guardia automática para impedir volver a `sha256(IP/token)` sin secreto.
- No cambia el flujo público de reportes ni el frontend de usuario.

## v0.10.2.4-purge-tracked-backend-backups

- Elimina copias `.bak` trackeadas de `backend/app/` para evitar código backend obsoleto en el repositorio público.
- Añade una guardia automática contra backups, temporales y artefactos de edición trackeados.
- Reduce falsos positivos de auditoría sobre código antiguo que ya no forma parte del runtime.
- No cambia backend runtime, reportes, Turnstile, datos de distribuidoras ni datasets geográficos.

## v0.10.2.3-public-version-guard

- Sincroniza la versión pública visible en README, `VERSION` y `APP_VERSION`.
- Añade una guardia automática para detectar deriva entre versión de app, README y changelog.
- Refuerza la confianza operativa del repositorio tras la auditoría avanzada.
- No cambia backend, reportes, Turnstile, datos de distribuidoras ni datasets geográficos.

## v0.10.2.2-data-edistribucion-safe-regional-with-exceptions

- Añade a producción pistas de distribuidora para Canarias, Illes Balears y Ceuta tras revisión enfocada.
- Importa 157 zonas: 154 como `regional_default` de e-distribución y 3 excepciones locales como `verified_partial`.
- Excepciones locales: Puerto de la Cruz, Sóller y Ceuta.
- Mantiene Andalucía, Aragón, Catalunya y Extremadura fuera de producción hasta revisión más detallada.
- Mantiene Castilla y León y Galicia fuera de este flujo de importación masiva.
- No añade CUPS, datos personales, direcciones exactas, coordenadas privadas ni inventario de infraestructura crítica.
- No toca backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.2.0-data-navarra-rioja-murcia-distributor-hints

- Añade pistas orientativas de distribuidora para Navarra, La Rioja y Región de Murcia.
- Usa `regional_default` para i-DE en estas tres comunidades.
- Mantiene las pistas en JSON público runtime para no inflar el bundle principal.
- No añade CUPS, datos personales, direcciones exactas, coordenadas privadas ni inventario de infraestructura crítica.
- No toca backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.9-data-asturias-cantabria-distributor-hints

- Añade pistas orientativas de distribuidora para Asturias y Cantabria.
- Usa `regional_default` para E-REDES en Asturias y Viesgo Distribución en Cantabria.
- Añade Electra de Carbayín como `verified_partial` en Bimenes y Siero por fuente pública de área de distribución.
- Mantiene las pistas en JSON público runtime para no inflar el bundle principal.
- No añade CUPS, datos personales, direcciones exactas, coordenadas privadas ni inventario de infraestructura crítica.
- No toca backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.8-geo-selector-cleanup

- Limpia el selector de ámbitos geográficos.
- Elimina el texto informativo obsoleto bajo el selector de comunidades.
- Evita renderizar chips vacíos si algún dataset no tiene etiqueta visible.
- No cambia datasets, polígonos, backend, privacidad ni flujo de reportes.

## v0.10.1.7-distributor-hints-public-json

- Mueve la carga de pistas de distribuidora a JSON público servido en runtime.
- Copia `frontend/src/data/distributor_hints.json` a `frontend/public/data/distributor_hints.json`.
- Evita incluir el dataset completo de distribuidoras en el bundle JavaScript principal.
- Mantiene fallback seguro si el JSON público todavía no ha cargado o falla.
- Prepara la app para importar más comunidades sin aumentar de forma lineal el JS inicial.
- No cambia el contenido del dataset, backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.6-data-galicia-distributor-hints

- Importa a producción la auditoría completa de distribuidoras para Galicia.
- Añade pistas para los 313 concellos gallegos.
- Conserva niveles de confianza diferenciados: `verified_partial` para fuentes concretas y `regional_default` para orientación regional/provincial.
- Mantiene el wording seguro añadido en v0.10.1.5 para no presentar orientación regional como verificación municipal.
- No añade CUPS, datos personales, direcciones exactas, coordenadas privadas ni inventario de infraestructura crítica.
- No toca backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.5-grid-distributor-confidence-wording

- Diferencia el texto público según el nivel de confianza de la pista de distribuidora.
- Mantiene `verified_partial` como distribuidora probable con aviso de varias distribuidoras posibles.
- Muestra `regional_default` como distribuidora orientativa con recomendación de confirmar.
- Mantiene el fallback seguro cuando no hay dato verificable.
- No añade nuevas distribuidoras ni cambia el dataset productivo.
- No toca backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.4-data-distributor-hints-galicia-moscoso

- Añade las primeras pistas reales y conservadoras de distribuidora eléctrica.
- Incorpora Eléctrica de Moscoso, S.L. para municipios de Pontevedra con fuente pública verificable.
- Marca las entradas como `verified_partial` para evitar afirmar exclusividad o cobertura total.
- Mantiene el fallback genérico en cualquier zona no verificada.
- No añade CUPS, direcciones, coordenadas privadas ni inventario de infraestructura crítica.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.3-grid-distributor-hints-foundation

- Añade la base técnica para futuras pistas de distribuidora por municipio o zona.
- Crea `frontend/src/data/distributor_hints.json` como dataset inicial vacío y conservador.
- Añade `frontend/src/grid/distributorHints.js` para resolver el texto público de distribuidora sin cambiar backend.
- Añade `scripts/check_distributor_hints.py` y lo integra en `scripts/repo_guard.sh`.
- Prepara soporte para distribuidoras pequeñas, múltiples distribuidoras y niveles de confianza.
- No añade datos reales de distribuidoras todavía.
- No pide CUPS ni publica infraestructura eléctrica sensible.
- No cambia mapa, polígonos, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.1.2-docs-public-polish

- Pule la documentación pública tras completar la fase geográfica.
- Actualiza el README con la lista real de ámbitos geográficos disponibles.
- Añade una sección de validaciones del repositorio.
- Documenta las guardias geográficas y de seguridad en CONTRIBUTING.md.
- Mantiene claro que los datasets individuales deben incluirse también en “Toda España”.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No toca datasets municipales, mapa, polígonos ni matching geográfico.

## v0.10.1.1-repo-purify

- Limpia artefactos locales/operativos redundantes si estaban trackeados.
- Refuerza `.gitignore` para evitar subir backups, auditorías, SARIF, bases de datos locales y GeoJSON raw.
- Añade configuración `.gitleaks.toml` para permitir el placeholder vacío documentado `TURNSTILE_SECRET_KEY=` sin ocultar secretos reales.
- Elimina GeoJSON raw redundantes si no están referenciados por la aplicación.
- Mantiene intactos backend, reportes, Turnstile, rate limiting, datasets municipales publicados y lógica de polígonos.

## v0.10.1.0-geo-complete-spain-audit

- Añade una auditoría de cobertura geográfica completa de España.
- Verifica que las 17 comunidades autónomas y Ceuta/Melilla están declaradas como datasets individuales.
- Verifica que todos los `municipiosPath` individuales están incluidos en `municipiosPaths` de “Toda España”.
- Verifica que los GeoJSON municipales publicados existen, tienen features, no superan el límite de tamaño y mantienen propiedades normalizadas.
- Añade comprobaciones de municipios críticos para detectar regresiones de cuadrado/celda.
- Integra la nueva auditoría en `scripts/repo_guard.sh`.
- No añade nuevas zonas geográficas.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni infraestructura eléctrica.

## v0.10.0.9-geo-andalucia-catalunya

- Añade Andalucía al selector geográfico.
- Añade Catalunya al selector geográfico.
- Publica los datasets municipales normalizados de Andalucía y Catalunya.
- Añade ambos datasets a la carga lazy de “Toda España”.
- Mantiene la guardia automática para impedir datasets individuales fuera de `municipiosPaths`.
- No regenera ningún GeoJSON gigante.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni infraestructura eléctrica.

## v0.10.0.8-geo-all-scope-new-datasets

- Corrige la carga de “Toda España” para incluir todos los datasets municipales individuales declarados.
- Evita que datasets nuevos como Euskadi, Extremadura y Castilla-La Mancha caigan al cuadrado/celda fallback en el ámbito general.
- Añade una guardia automática para detectar datasets individuales no incluidos en “Toda España”.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni infraestructura eléctrica.

## v0.10.0.7-geo-euskadi-extremadura-clm

- Añade Euskadi al selector geográfico.
- Añade Extremadura al selector geográfico.
- Añade Castilla-La Mancha al selector geográfico.
- Publica datasets municipales normalizados para las tres comunidades.
- Añade estos datasets a la carga lazy de “Toda España”.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni infraestructura eléctrica.

## v0.10.0.6-geo-loader-dataset-id

- Corrige el loader geográfico para aceptar tanto un ID de dataset como un objeto dataset.
- Restaura la carga real de polígonos municipales tras la carga lazy de “Toda España”.
- Evita que zonas con polígono válido caigan al rectángulo/celda fallback.
- No cambia backend, reportes, Turnstile, rate limiting ni datos personales.

## v0.10.0.5-geo-spatial-polygon-match

- Corrige el matching visual de incidencias activas contra polígonos municipales.
- Añade fallback espacial: si `zone_id` o nombre/provincia no encajan, usa el punto de la incidencia para buscar el polígono que lo contiene.
- Evita cuadrados/celdas en municipios con variantes oficiales, bilingües o diferencias de normalización.
- Mantiene el cuadrado solo cuando no hay polígono disponible o el punto no cae dentro de ningún municipio cargado.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni infraestructura eléctrica.

## v0.10.0.4-geo-normalize-municipality-datasets

- Normaliza todos los datasets municipales publicados para que compartan el mismo esquema.
- Asegura `municipio`, `mun_name`, `name`, `province`, `prov_name`, `dataset_id` y `zone_id` en cada feature.
- Corrige casos donde una incidencia activa caía a cuadrado/celda aunque existía polígono municipal.
- Añade `scripts/audit_geo_datasets.py` para detectar datasets incompletos antes de seguir añadiendo comunidades.
- Mantiene la carga lazy de “Toda España” por datasets individuales.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni infraestructura eléctrica.

## v0.10.0.3-geo-lazy-all-scope

- Cambia “Toda España” para cargar los polígonos desde los datasets municipales individuales ya publicados.
- Elimina el GeoJSON combinado `toda_espana_municipios.geojson` para evitar límites de tamaño de Cloudflare Pages.
- Mantiene el comportamiento visual: si existe polígono municipal, se pinta municipio; si no existe, queda fallback.
- Prepara la app para añadir comunidades grandes sin regenerar un archivo único gigante.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.
- No añade distribuidoras ni datos eléctricos nuevos.

## v0.10.0.2-geo-canarias

- Añade Canarias al selector geográfico.
- Publica `frontend/public/data/canarias_municipios.geojson` como dataset municipal normalizado.
- Regenera `toda_espana_municipios.geojson` incluyendo Canarias en versión slim compatible con Cloudflare Pages.
- Mantiene el GeoJSON nacional bruto fuera del repositorio.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.0.1-geo-valencia-balears

- Añade Comunitat Valenciana al selector geográfico.
- Añade Illes Balears al selector geográfico.
- Publica datasets municipales normalizados para ambas comunidades.
- Regenera `toda_espana_municipios.geojson` incluyendo las nuevas zonas en versión slim compatible con Cloudflare Pages.
- Mantiene el GeoJSON nacional bruto fuera del repositorio.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.10.0.0-geo-small-communities

- Añade La Rioja al selector geográfico.
- Añade Región de Murcia al selector geográfico.
- Añade Ceuta y Melilla al selector geográfico.
- Publica datasets municipales normalizados para las cuatro zonas.
- Regenera `toda_espana_municipios.geojson` incluyendo las nuevas zonas con versión slim compatible con Cloudflare Pages.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.9.9.9-mobile-active-zone-actions

- En móvil, al pulsar una zona activa del mapa se abre directamente el modo Reportar con esa zona preseleccionada.
- Mantiene en escritorio el flujo de explorar/detalle para evitar cambios bruscos de UX.
- Conserva la selección canónica por `zone_id`, `id` o `incident_id`.
- No cambia backend, Turnstile, rate limiting, privacidad ni datasets geográficos.

## v0.9.9.8-navarra-report-button

- Corrige el botón “Reportar” en móvil y escritorio: ahora siempre entra en modo reportar.
- Si hay una zona activa seleccionada, “Reportar” abre el reporte preasociado a esa zona sin crear un punto manual nuevo.
- Añade Navarra al selector geográfico.
- Publica `frontend/public/data/navarra_municipios.geojson`.
- Regenera `toda_espana_municipios.geojson` incluyendo Navarra para evitar cuadrados cuando hay polígono disponible.
- Añade compatibilidad explícita para `Valle de Elorz/Elortzibar`.
- No cambia backend, Turnstile, rate limiting, privacidad ni consenso de “Ya volvió”.

## v0.9.9.7-restore-consensus-mobile

- Cambia “Ya volvió” a lógica de consenso: no borra toda la zona si quedan más avisos activos.
- Una señal de vuelta neutraliza una confirmación activa: 1 corte + 1 vuelve resuelve, 5 cortes + 1 vuelve deja 4 activas.
- Hace que la señal “Ya volvió” dure lo mismo que el aviso activo para no reactivar zonas a los pocos minutos.
- En móvil, al pulsar una zona activa se prioriza abrir la incidencia real y sus acciones.
- Mejora mensajes cuando una zona sigue activa tras registrar una señal de vuelta.
- No añade comunidades, no cambia Turnstile, privacidad, rate limiting ni dependencias.

## v0.9.9.6-restore-clears-active-zone

- Corrige el flujo “Ya volvió” para que resuelva la zona activa objetivo.
- Si otro navegador/dispositivo marca que volvió la luz, se cierran los reportes negativos activos de esa zona.
- Evita que una zona siga marcada/activa después de resolverla correctamente.
- Limpia selección, punto manual y destino tras una resolución correcta.
- Añade validación con base de datos temporal para probar el caso: usuario A reporta, usuario B marca “Ya volvió”.
- No toca datasets geográficos, Turnstile, rate limiting, privacidad ni dependencias.

## v0.9.9.5-all-scope-polygons

- Corrige el ámbito “Toda España” para que use polígonos municipales combinados de las comunidades disponibles.
- Evita que zonas como Zuera o Madrid caigan a cuadrado/celda cuando ya existe GeoJSON municipal.
- Mantiene el cuadrado solo como fallback o selección manual temporal cuando no hay polígono disponible.
- Genera `toda_espana_municipios.geojson` desde datasets ya publicados, en formato ligero para no superar el límite de Cloudflare Pages.
- No cambia backend, Turnstile, rate limiting, privacidad ni flujo de reportes.

## v0.9.9.4-report-selection-state

- Corrige selección de zonas activas usando una clave canónica compatible con `zone_id`, `id` e `incident_id`.
- Corrige clicks sobre polígonos/celdas activas para que seleccionen siempre la incidencia, también en modo reportar.
- Evita que el botón “Reportar” borre una zona activa ya seleccionada.
- Limpia selección, punto manual y destino cuando una zona queda resuelta o desaparece de la lista activa.
- No cambia backend, Turnstile, rate limiting, privacidad, dependencias ni datasets geográficos.

## v0.9.9.3-geo-aragon

- Añade Aragón al selector geográfico.
- Publica `frontend/public/data/aragon_municipios.geojson` como dataset municipal curado.
- Normaliza propiedades municipales para matching visual: `municipio`, `province`, `dataset_id` y `zone_id`.
- Limpia el listado geográfico del README para evitar comunidades pegadas en una sola línea.
- No cambia backend, Turnstile, reportes, overlays ni dependencias.
- No sube el GeoJSON nacional bruto.

## v0.9.9.2-geo-madrid-polygon-match

- Normaliza el GeoJSON de Comunidad de Madrid para enlazar incidencias con polígonos municipales reales.
- Añade `municipio`, `province`, `zone_id` y `dataset_id` a cada feature de Madrid.
- Corrige la selección frontend para aceptar `id`, `zone_id` o `incident_id`.
- No cambia backend, Turnstile, paquetes, privacidad ni flujo de reportes.
- Mantiene “Toda España” sin cambio automático de ámbito.

## v0.9.9.1-geo-madrid

- Añade Comunidad de Madrid al selector geográfico.
- Genera y publica solo el GeoJSON municipal curado de Madrid.
- No añade overlays nuevos ni cambia el flujo de reportes.
- No toca backend, Turnstile, privacidad ni rate limiting.
- Mantiene el GeoJSON nacional bruto fuera del repositorio.

## v0.9.9.0-repo-hygiene-guardrails

- Limpia el repositorio tras el rollback de estabilidad.
- Elimina `_backups/` del control de versiones si se había colado.
- Refuerza `.gitignore` para backups, diagnósticos, logs, bases de datos, `.env` y GeoJSON brutos.
- Añade `scripts/repo_guard.sh` para bloquear errores repetidos antes de mergear.
- Añade CI básico de GitHub Actions con guardas, sintaxis backend y build frontend.
- Documenta un plan de estabilidad para no mezclar geografía, UX, Turnstile y backend en el mismo PR.

## v0.9.8.9-stability-rollback

- Rollback conservador al último frontend estable: `v0.9.8.3-black-screen-fix`.
- Retira las capas experimentales de comunidades nuevas, selección municipal persistente y overlays que estaban provocando pantalla negra y estados visuales inconsistentes.
- Mantiene el flujo estable de reportes, Turnstile, privacidad, rate limiting y API.
- Limpia el estado público para volver a una base fiable antes de rehacer geografía de forma incremental.
- No añade cuentas, CUPS, texto libre, fotos ni coordenadas exactas públicas.

## v0.9.8.3-black-screen-fix

- Corrige pantalla negra tras enviar o resolver un aviso.
- Elimina llamadas a `setToastTone`, que no existía y provocaba un `ReferenceError` fatal en React.
- Mantiene el cálculo automático del tono del toast sin estado duplicado.
- Pasa correctamente el texto `footer` al overlay de reporte.
- No cambia backend, privacidad, Turnstile ni lógica de reportes.

## v0.9.8.2-report-overlay-stability

- Unifica el overlay de reporte para evitar el efecto de “se cierra uno y se abre otro”.
- Mantiene un único flujo visual estable durante validación, protección anti-abuso, guardado anónimo y refresco.
- Añade limpieza/failsafe del overlay para evitar pantalla oscura bloqueada tras confirmar.
- Fuerza reajuste del mapa tras cerrar el overlay para evitar pantalla negra/tiles sin pintar.

## v0.9.8.1-report-actions-restore

- Corrige el flujo de acciones directas: “Yo también” y “Ya volvió” ya no abren el panel manual de reportar.
- Mejora “Ya volvió” manual para reconocer incidencias activas cercanas/visibles cuando el punto cae en la zona aproximada.
- Evita que errores de preflight/verificación se muestren como toast verde.
- Reduce el parpadeo de overlay/panel durante el envío y mantiene el flujo acorde a la acción real.

## v0.9.8.0-report-overlay-flow

- Mejora el overlay de reporte para describir mejor el flujo real.
- Sustituye mensajes genéricos como “detectando ayuntamiento” por validación de zona, protección anti-abuso, guardado anónimo y actualización de zona agregada.
- Añade textos de ayuda menos alarmistas y más claros durante el envío.
- Mantiene la lógica de privacidad: sin CUPS, sin nombre, sin dirección exacta y sin texto libre.

## v0.9.7.9-manual-restore-target

- Corrige “Ya volvió” desde el modo Reportar manual cuando el punto elegido cae sobre una zona activa.
- El frontend intenta deducir `incident_id`/`zone_id` desde las incidencias visibles.
- El backend añade fallback por bounds/celda activa antes de depender solo de proximidad.
- Evita repetir `preflight` después de Turnstile cuando ya se validó antes.
- Reordena el changelog público para mostrar las últimas versiones arriba.

## v0.9.7.8-report-flow-stability

- Corrige el flujo de “Yo también” / “Ya volvió” usando `incident_id`/`zone_id` cuando la UI trabaja con zonas agregadas.
- Añade preflight de reporte para mostrar cooldowns antes del flujo visual de envío.
- Mantiene Turnstile con fallback suave y evita mensajes de preparación como toast verde separado.
- Mejora autocierre/cierre manual de mensajes y estabilidad móvil del panel de acciones.

# Changelog

## v0.9.7.7-stable-rollback

- Rollback de la pasada `v0.9.7.6-feedback-banners`.
- Recupera el flujo estable de `v0.9.7.5-turnstile-soft-fallback`.
- Corrige regresiones de integración en móvil:
  - selección de zona en modo reportar;
  - acciones de incidencia en modo explorar;
  - botón “Ya volvió”;
  - banners verdes duplicados o fuera del flujo.
- Mantiene Turnstile con fallback suave y rate limiting local.

## v0.9.7.5-turnstile-soft-fallback

- Hotfix de estabilidad para reportes cuando Turnstile queda bloqueado por navegador, CSP, tracking prevention o estado interno del iframe.
- Turnstile sigue activo como protección principal.
- Si Turnstile no devuelve token, el reporte continúa con protección local y rate limiting del backend.
- Evita que el botón quede colgado en “Enviando…” o “Preparando…”.
- Mantiene privacidad: no añade cuentas, CUPS, fotos ni texto libre.

## v0.9.7.4-turnstile-managed

- Hotfix de Turnstile para widget Managed/Gestionado.
- Sustituye `size: invisible` por `flexible`/`compact` según pantalla.
- Mantiene `execution: execute` para lanzar la comprobación al confirmar.
- Usa `appearance: interaction-only` para que solo aparezca si Cloudflare necesita interacción.
- Mejora compatibilidad en PC, iPhone/Safari y móviles pequeños.
- Amplía el margen de espera de Turnstile antes de mostrar error.

## v0.9.7.3-ios-turnstile-submit

- Hotfix del flujo de reporte en iPhone/Safari.
- El botón Confirmar ya no depende de que Turnstile esté listo antes del toque.
- Se reintenta la preparación del widget invisible durante unos segundos.
- Si la verificación no responde, se libera el botón y se muestra un mensaje claro.
- Mantiene Turnstile invisible y API pública.

## v0.9.7.2-mobile-responsive

Fecha: 2026-04-28

### Responsive / móvil

- Ajusta la app para móviles con `100dvh` y `safe-area`.
- Evita cortes en botones inferiores en iPhone y Android.
- Hace los paneles inferiores scrollables y menos invasivos.
- Mejora footer de privacidad, aviso legal, cookies y versión en pantallas pequeñas.
- Mejora las páginas públicas y changelog en móvil.
- No cambia backend, API ni datos.

## v0.9.7.1-render-hotfix

Fecha: 2026-04-28

### Hotfix

- Corrige un posible fallo de render tras la versión v0.9.7.
- Mueve la autolimpieza de mensajes después de inicializar el estado `message`.
- Mantiene el cierre automático de mensajes de éxito.
- Mantiene Turnstile invisible activo.
- No cambia backend, datos ni configuración de Cloudflare.

## v0.9.7-report-feedback

Fecha: 2026-04-28

### UX / reporte

- Mejora el feedback del flujo de reporte.
- Sustituye textos técnicos de verificación por estados más naturales.
- El envío muestra estado discreto en el botón.
- Los mensajes de éxito, como nueva incidencia o zona resuelta, se limpian automáticamente tras unos segundos.
- Mantiene Turnstile invisible y la protección anti-abuso activa.

## v0.9.6-invisible-turnstile

Fecha: 2026-04-28

### UX / seguridad

- Turnstile pasa a modo invisible.
- La verificación anti-abuso se ejecuta al pulsar Confirmar.
- Se elimina el bloque blanco visible que se cortaba en móvil y desktop.
- El formulario de reporte queda más limpio y compacto.
- Mantiene protección anti-abuso sin ocupar espacio visual.

## v0.9.5-mobile-usability

Fecha: 2026-04-28

### UX móvil

- Recupera filtros, lista y enlaces legales en móvil dentro de un panel inferior con scroll.
- Oculta el panel vacío de explorar en móvil.
- Reportar queda como panel inferior separado.
- Ajusta Turnstile para que no se corte en PC ni móvil.
- Usa Turnstile normal en escritorio y compacto en móvil.
- Reduce textos, botones, chips y espaciados.

## v0.9.4-mobile-compact-sheet

Fecha: 2026-04-28

### UX móvil

- Reduce mucho la altura del panel inferior en modo explorar.
- Rediseña el panel de reportar como bottom sheet compacto.
- Evita que reportar ocupe media pantalla o más.
- Turnstile vuelve a modo horizontal normal y se controla por CSS para no cortarse.
- Reduce botones, pestañas, chips, textos y espaciados en móvil.
- Mantiene el mapa visible como protagonista.

## v0.9.3-mobile-shell

Fecha: 2026-04-28

### UX móvil

- Rediseño móvil adicional del modo explorar y reportar.
- Reportar pasa a comportarse como panel inferior compacto, no como desktop encogido.
- Turnstile usa tamaño compacto en móvil/tablet para evitar cortes.
- Ajuste de topbar, botones, filtros, paneles, chips y controles.
- Mapa sigue siendo protagonista en móvil.

### Producción

- Frontend publicado en Cloudflare Pages.
- API pública en `https://api.mapa-apagones.es`.
- Turnstile activo para reportes.
- Repo público sin secretos ni datos reales.

## v0.9.2-mobile-report

- Rediseño inicial del flujo de reporte en móvil.
- Panel de reporte menos invasivo.
- Turnstile compacto en pantallas pequeñas.
- Changelog público actualizado.
- README ajustado al estado publicado.

## v0.9.1-public-legal

- Dominio público activo: `https://mapa-apagones.es`.
- `www.mapa-apagones.es` activo con SSL.
- API prevista y después activada en `https://api.mapa-apagones.es`.
- Páginas públicas legales revisadas:
  - Privacidad.
  - Aviso legal.
  - Cookies.
  - Cómo funciona.
  - No somos una distribuidora.
  - Estado del servicio.
- Correos públicos:
  - `contacto@mapa-apagones.es`
  - `privacidad@mapa-apagones.es`
- Eliminadas referencias de plantilla.
- Dominio corregido con guion.
- SEO básico, Open Graph, JSON-LD, robots.txt y sitemap.xml.

## v0.9.0-geo-north-cyl

- Mapa ciudadano funcional.
- Reportes por zona.
- Filtros y estados de confianza.
- Base geográfica inicial:
  - Galicia.
  - Asturias.
  - Cantabria.
  - Castilla y León.
- Pipeline CNIG/IGN para datasets municipales.
- React + Vite + Leaflet.
- FastAPI + SQLite.

## v0.8.x-public-infra

- Cloudflare Pages preparado.
- `VITE_API_BASE_URL` para separar frontend y API.
- CORS restringido para producción.
- Debug cerrado por defecto.
- Dockerignore para reducir contexto de build.
- Backups SQLite.
- Healthchecks Docker.
- SQLite WAL, busy timeout y foreign keys.

## v0.7.x-security-abuse

- Integración Cloudflare Turnstile.
- Verificación anti-abuso en reportes.
- Rate limiting por hashes técnicos.
- Control de duplicados y ventanas temporales.
- Endpoints públicos limitados con `bbox`, `limit` y `hours`.

## v0.6.0-foundation

- Base legal inicial.
- Scripts iniciales de backup/restore.
- Limpieza de diseño de incidencias.
- Primeras mejoras de estados y confirmaciones.

## v0.5.0-alpha

- Mapa ciudadano funcional inicial.
- Incidencias por zona.
- Lógica inicial de estados.
- Primer prototipo de reporte ciudadano anónimo.

## Historial técnico reciente desde Git

- `2026-04-28` `0ed074f` PR #31 from odegaard12/feat/mobile-report-redesign-v2
- `2026-04-28` `42ee120` PR #30 from odegaard12/feat/ux-turnstile-mobile-density-v1
- `2026-04-28` `7241812` PR #29 from odegaard12/fix/public-legal-legacy-pages-v1
- `2026-04-28` `05e23ac` PR #28 from odegaard12/fix/public-changelog-page-v1
- `2026-04-28` `371347a` PR #27 from odegaard12/docs/legal-production-texts-v1
- `2026-04-28` `a8106cb` PR #26 from odegaard12/feat/ux-initial-spain-scale-v1
- `2026-04-28` `618b82e` PR #25 from odegaard12/feat/public-pages-seo-v1
- `2026-04-28` `f2ce6dc` PR #23 from odegaard12/ops/sqlite-backup-health-v1
- `2026-04-27` `e25093d` PR #22 from odegaard12/chore/frontend-dockerignore-v1
- `2026-04-27` `d802ab0` PR #21 from odegaard12/feat/cloudflare-pages-ready-v1
- `2026-04-27` `b87b044` PR #20 from odegaard12/feat/api-bbox-limit-v1
- `2026-04-27` `c1ea5e0` PR #19 from odegaard12/fix/prod-cors-debug-v1
- `2026-04-27` `3df7d17` PR #18 from odegaard12/docs/public-project-identity-v1
- `2026-04-27` `90b9cb9` PR #17 from odegaard12/docs/public-project-identity-v1
- `2026-04-27` `358d356` PR #16 from odegaard12/feat/security-turnstile-v1
- `2026-04-27` `1aae301` PR #15 from odegaard12/feat/geo-castilla-leon-v1
- `2026-04-27` `f75f323` PR #14 from odegaard12/feat/geo-cantabria-v1
- `2026-04-27` `91cfab6` PR #13 from odegaard12/fix/geo-normalize-galicia-asturias-pipeline-v1
- `2026-04-27` `508c84a` PR #12 from odegaard12/fix/zone-id-accent-slug-normalization-v1
- `2026-04-27` `028c6a0` PR #11 from odegaard12/feat/geo-cnig-pipeline-v1
- `2026-04-27` `8b5d134` PR #10 from odegaard12/fix/geo-all-dataset-remount-hardening-v1
- `2026-04-27` `0fa3540` PR #9 from odegaard12/fix/report-feedback-and-scope-freedom
- `2026-04-27` `1fe8878` PR #8 from odegaard12/feat/geo-spain-source-pipeline
- `2026-04-26` `d644c83` PR #7 from odegaard12/feat/geo-multidataset-state
- `2026-04-26` `6606992` PR #6 from odegaard12/feat/geo-loader-spain-ready
- `2026-04-26` `1e2fe94` PR #5 from odegaard12/chore/geo-version-sync-and-state-hardening
- `2026-04-26` `a505b80` PR #4 from odegaard12/fix/geo-live-refresh-clarity
- `2026-04-26` `8d61cb4` PR #3 from odegaard12/fix/polygon-resolution-v1
- `2026-04-26` `6d4f1ce` PR #2 from odegaard12/feat/municipality-polygons
- `2026-04-25` `142b0a2` PR #1 from odegaard12/feat/zones-backend-wip
- `2026-04-24` `d4f6494` docs: improve README and restore license
- `2026-04-24` `7ee5442` chore: public-safe snapshot without personal or runtime data
