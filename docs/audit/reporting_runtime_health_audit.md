# Auditoría de salud runtime de reportes

Esta auditoría documenta las comprobaciones automáticas que protegen el flujo de reportes ciudadanos.

## Cobertura esperada

- Crear reportes mediante `/api/report`.
- Ver incidencias recién creadas mediante `/api/incidents`.
- Validar ciclo de vida de reportes, agrupación y resolución.
- Validar concurrencia para evitar incidencias duplicadas.
- Validar privacidad: hashes HMAC y ausencia de IP/token raw en SQLite temporal.
- Validar anti-abuso con respuesta `429`.
- Validar Docker Compose real con frontend, backend, proxy `/api` y JSON público de distribuidoras.

## Scripts requeridos

| Script | Existe | Incluido en post-merge |
|---|---:|---:|
| `scripts/smoke_backend_api.py` | sí | sí |
| `scripts/smoke_backend_lifecycle.py` | sí | sí |
| `scripts/smoke_backend_concurrency.py` | sí | sí |
| `scripts/smoke_backend_privacy_abuse.py` | sí | sí |
| `scripts/smoke_docker_compose.sh` | sí | sí |
| `scripts/post_merge_validate.sh` | sí | no |

## Tokens funcionales revisados

| Script | Token esperado | Estado |
|---|---|---|
| `scripts/smoke_backend_api.py` | `/api/health` | OK |
| `scripts/smoke_backend_api.py` | `/api/report` | OK |
| `scripts/smoke_backend_api.py` | `/api/incidents` | OK |
| `scripts/smoke_backend_lifecycle.py` | `/api/report` | OK |
| `scripts/smoke_backend_lifecycle.py` | `/api/incidents` | OK |
| `scripts/smoke_backend_concurrency.py` | `/api/report` | OK |
| `scripts/smoke_backend_privacy_abuse.py` | `429` | OK |
| `scripts/smoke_backend_privacy_abuse.py` | `ip_hash` | OK |
| `scripts/smoke_backend_privacy_abuse.py` | `reporter_token_hash` | OK |
| `scripts/smoke_docker_compose.sh` | `/api/health` | OK |
| `scripts/smoke_docker_compose.sh` | `/api/report` | OK |
| `scripts/smoke_docker_compose.sh` | `/api/incidents` | OK |
| `scripts/smoke_docker_compose.sh` | `/data/distributor_hints.json` | OK |

## Lectura operativa

- La comprobación fuerte se ejecuta con `scripts/post_merge_validate.sh`.
- El smoke de lifecycle cubre que un reporte se vea en incidencias y que el estado cambie al resolver.
- El smoke de concurrencia cubre reportes simultáneos en la misma zona.
- El smoke de privacidad/abuso cubre HMAC, ausencia de datos raw y rate limit.
- El smoke Docker Compose cubre el camino frontend/proxy/backend de forma aislada.

## Seguridad y privacidad

Esta auditoría no introduce CUPS, cuentas, texto libre, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, logs, bases de datos reales ni inventario de infraestructura crítica.
