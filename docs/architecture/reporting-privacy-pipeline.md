# Arquitectura de reportes, privacidad y anti-abuso

Mapa Apagones está diseñado para mostrar señales ciudadanas agregadas de incidencias eléctricas sin convertir la aplicación en un sistema de identificación de personas, viviendas o puntos de suministro.

## Principios

El flujo público mantiene estos límites:

- Sin cuentas.
- Sin login.
- Sin CUPS.
- Sin texto libre.
- Sin fotos.
- Sin direcciones exactas.
- Sin publicar coordenadas exactas de usuarios.
- Reportes agrupados por zona aproximada.
- Privacidad por diseño.
- Código abierto.

## Qué datos introduce una persona

El formulario público permite indicar solo:

- Tipo de señal: `sin_luz`, `microcortes`, `baja_tension` o `vuelve`.
- Ubicación aproximada seleccionada en mapa o detectada por navegador.
- Token local anónimo generado en el navegador.
- Token Turnstile cuando está activado en producción.

No se piden nombre, email, cuenta, teléfono, CUPS, dirección postal, fotos ni texto libre.

## Agrupación geográfica

El backend no publica la coordenada exacta del usuario como vivienda o punto individual.

El sistema agrupa reportes en zonas aproximadas:

- Celdas agregadas.
- Incidencias activas por zona.
- Estados de confianza como señal débil, probable, activa, degradándose o resuelta.
- Polígonos municipales/datasets geográficos usados para visualización y contexto.

La finalidad es mostrar señal comunitaria, no localizar viviendas concretas.

## Token anónimo y hashes

El navegador usa un token local anónimo para poder:

- Evitar duplicados de la misma persona.
- Aplicar cooldowns.
- Actualizar una señal propia.
- Evitar abuso básico sin login.

No se guarda el token real. El backend guarda `reporter_token_hash`.

Desde `v0.10.2.5`, los hashes anónimos se calculan con HMAC-SHA256 y secreto de servidor mediante `ANON_HASH_KEY`.

Esto evita que, si una base de datos se filtrase, alguien pueda comprobar fácilmente valores por diccionario sin conocer la clave del servidor.

Variables relevantes:

- `ANON_HASH_KEY`
- `ANON_HASH_KEY_REQUIRED`
- `ANON_HASH_LEGACY_COMPAT`

## IP y anti-abuso

El backend usa una IP derivada solo para rate limiting y anti-abuso.

No se guarda la IP real. Se guarda `ip_hash`, también mediante HMAC-SHA256.

Desde `v0.10.2.7`, el backend no confía ciegamente en cabeceras como `X-Forwarded-For`.

Solo acepta cabeceras de IP real si la conexión inmediata llega desde un proxy confiable configurado con:

- `TRUST_PROXY_HEADERS`
- `TRUSTED_PROXY_CIDRS`

Orden de preferencia cuando el proxy es confiable:

1. `CF-Connecting-IP`
2. `X-Real-IP`
3. Primer valor de `X-Forwarded-For`

Si el origen inmediato no es confiable, se usa `request.client.host`.

## Turnstile

Turnstile se usa como defensa anti-abuso complementaria.

Reglas del proyecto:

- No sustituye al rate limiting.
- No se guarda el token Turnstile.
- En tests y smokes se desactiva para no depender de servicios externos.
- En producción puede exigirse según configuración.

Variables relevantes:

- `TURNSTILE_ENABLED`
- `TURNSTILE_REQUIRED`
- `TURNSTILE_SECRET_KEY`
- `VITE_TURNSTILE_SITE_KEY`

## Base de datos

El backend usa SQLite.

Tablas principales:

- `incidents`: incidencias agregadas por zona.
- `reports`: señales individuales anonimizadas.
- `action_log`: acciones usadas para rate limiting.
- `geocode_cache`: caché de contexto geográfico aproximado.
- Tablas auxiliares de zonas.

Las escrituras de `/api/report` usan una sección crítica transaccional con `BEGIN IMMEDIATE` para evitar que varios reportes simultáneos creen incidencias duplicadas en la misma celda.

## Ciclo de vida de una incidencia

1. Llega un reporte negativo (`sin_luz`, `microcortes`, `baja_tension`).
2. Se calcula zona/celda.
3. Se busca una incidencia reciente cercana o en la misma celda.
4. Si existe, se reutiliza.
5. Si no existe, se crea una incidencia agregada.
6. Se guarda el reporte con hashes HMAC.
7. Se recalcula el estado de la incidencia.
8. Las señales `vuelve` neutralizan señales negativas.
9. Los reportes caducan.
10. La incidencia puede pasar a resuelta o probablemente resuelta.

## API pública relevante

Endpoints principales:

- `GET /api/health`
- `POST /api/report`
- `POST /api/report/preflight` si está disponible
- `GET /api/incidents`
- `GET /api/zones` o endpoints de zonas según versión

## Qué no debe añadirse

No deben añadirse al backend, frontend, datasets, docs o research:

- CUPS reales.
- Campos `cups`, `cup`, `cups_id` o campos equivalentes de identificador de punto de suministro.
- Cuentas de usuario.
- Login público.
- Texto libre de usuario.
- Fotos.
- Direcciones exactas.
- Coordenadas exactas de viviendas o usuarios.
- Contadores o puntos de suministro.
- Subestaciones, líneas, cables, centros de transformación o inventario de infraestructura crítica.
- Logs, backups, bases de datos reales o secretos.

## Datos de distribuidoras

Las pistas de distribuidora son datos públicos orientativos por municipio o zona.

Reglas:

- Solo se muestran con fuente pública verificable.
- No se usan CUPS ni puntos de suministro.
- No se publican direcciones exactas.
- No se publica infraestructura crítica.
- Si el dato es regional o no exclusivo, se muestra como orientación.
- Si hay varias posibles distribuidoras, debe indicarse cobertura parcial o múltiple.
- Si no hay dato suficiente, se mantiene el mensaje genérico: consultar distribuidora de la zona.

## CI y guardias

El repositorio tiene guardias para evitar regresiones en:

- Versión pública sincronizada.
- Hashes anónimos HMAC.
- IP real solo desde proxy confiable.
- Transacción de reportes concurrentes.
- Smokes backend.
- Smokes Docker Compose.
- Lockfiles de dependencias.
- Artefactos temporales o backups trackeados.
- Distribuidoras.
- Cobertura geográfica.
- Datasets incluidos en “Toda España”.
- Tamaño de assets para Cloudflare Pages.

Smokes principales:

- `scripts/smoke_backend_api.py`
- `scripts/smoke_backend_concurrency.py`
- `scripts/smoke_backend_lifecycle.py`
- `scripts/smoke_backend_privacy_abuse.py`
- `scripts/smoke_docker_compose.sh`

## Modelo de despliegue

Frontend:

- React + Vite.
- Cloudflare Pages para despliegue público.
- Docker/Nginx para desarrollo o smoke completo.

Backend:

- FastAPI.
- SQLite.
- Despliegue en servidor propio.
- Exposición pública por túnel/reverse proxy.
- Turnstile y rate limiting.

## Nota operativa

El repositorio público puede documentar el modelo general, pero no debe publicar detalles reales de red, rutas privadas, túneles, puertos internos sensibles, credenciales, backups ni bases de datos.
