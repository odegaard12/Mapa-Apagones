# Cierre de auditoría avanzada · Mapa Apagones

Este documento resume el cierre de la fase de corrección derivada de la auditoría avanzada del repositorio `Mapa-Apagones`.

La auditoría señalaba riesgos en estas áreas:

- deriva de versión pública;
- privacidad de hashes;
- confianza en IP/proxy;
- smokes reales de backend;
- concurrencia de reportes;
- reproducibilidad de dependencias;
- CI más serio;
- schema SQLite;
- observabilidad segura;
- documentación de arquitectura;
- modularización inicial del backend;
- higiene de repositorio público.

## Estado final

A fecha de este cierre, los puntos críticos de auditoría quedan corregidos o cubiertos por guardias automáticas, smokes o documentación.

| Área | Estado | PRs de cierre |
| --- | --- | --- |
| Higiene pública del repo | Resuelto | #102 |
| Deriva de versión pública | Resuelto y protegido por guardia | #102, #119 |
| Hashes anónimos de token/IP | Resuelto con HMAC-SHA256 | #103, #104 |
| Confianza en IP/proxy | Resuelto con proxies confiables | #105 |
| Smoke real backend | Resuelto | #106 |
| Concurrencia de reportes | Resuelto con `BEGIN IMMEDIATE` y smoke concurrente | #107 |
| Reproducibilidad | Resuelto con lockfiles y `npm ci` / requirements lock | #108 |
| Docker Compose en CI | Resuelto | #109 |
| Ciclo de vida de reportes | Cubierto por smoke runtime | #110 |
| Privacidad y anti-abuso runtime | Cubierto por smoke específico | #111 |
| Arquitectura de privacidad/reportes | Documentada | #112 |
| Frontend estático construido | Cubierto por smoke | #113 |
| Observabilidad segura | Añadido `/api/status` seguro | #114 |
| Schema SQLite | Endurecido con índices e invariante parcial | #115 |
| Validación post-merge | Centralizada en runbook | #116 |
| Configuración backend | Modularizada en `settings.py` | #117 |
| Privacidad backend | Modularizada en `privacy.py` | #118 |
| Revalidación de versión tras refactor | Resuelta | #119 |

## Resultado técnico

El repositorio queda con:

- versión pública sincronizada entre `VERSION`, `APP_VERSION`, README y changelog;
- hashing HMAC-SHA256 para identificadores anónimos;
- no almacenamiento de IP real ni token real;
- confianza en cabeceras de proxy limitada a orígenes confiables;
- SQLite con WAL, transacción de escritura para reportes y constraint parcial contra duplicados activos;
- smokes backend reales: API, status, schema, concurrencia, ciclo de vida y privacidad/anti-abuso;
- smoke Docker Compose con frontend, backend y proxy `/api`;
- smoke del frontend estático construido;
- lockfiles para frontend y backend;
- documentación de arquitectura de privacidad/reportes;
- runbook único post-merge;
- guardias automáticas en `scripts/repo_guard.sh`.

## Comando principal de validación

Después de merges relevantes en `main`:

```bash
SMOKE_PYTHON=/tmp/apagones-smoke-venv/bin/python SMOKE_WEB_PORT=18098 scripts/post_merge_validate.sh
```

El runbook ejecuta guardias estáticas, build frontend, smokes runtime de backend, cobertura geográfica y smoke Docker Compose aislado.

## Privacidad

El cierre mantiene los principios del proyecto:

- no cuentas;
- no CUPS;
- no texto libre;
- no fotos;
- no direcciones exactas;
- no coordenadas privadas;
- no tokens reales;
- no IPs reales;
- no secretos en repositorio;
- no inventario de infraestructura crítica.

## Pendientes no críticos

Estos puntos quedan fuera de la fase urgente de auditoría y pasan a roadmap normal:

1. Seguir modularizando `backend/app/main.py` en módulos pequeños: reportes, SQLite/storage, Turnstile/anti-abuso y geocodificación.
2. Dividir `frontend/src/App.jsx` en componentes y hooks para mejorar mantenibilidad.
3. Añadir E2E de navegador cuando el flujo público esté más estable visualmente.
4. Revisar los `WARN` de `zone_id` duplicados para distinguir enclaves reales de artefactos de dataset.
5. Añadir métricas/observabilidad más avanzada si el tráfico público crece.

## Conclusión

La fase de corrección de auditoría avanzada queda cerrada.

A partir de aquí, los cambios deberían tratarse como evolución ordinaria del producto, no como deuda crítica pendiente.
