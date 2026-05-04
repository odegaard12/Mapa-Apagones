# Contribuir a Mapa Apagones

Gracias por querer ayudar.

Mapa Apagones es un proyecto ciudadano, sin cuentas y con privacidad por diseño.

## Principios que no se deben romper

- Sin cuentas.
- Sin login obligatorio.
- Sin CUPS.
- Sin texto libre.
- Sin fotos.
- Sin direcciones exactas.
- Sin coordenadas exactas públicas.
- Sin publicar datos personales.
- Sin guardar tokens Turnstile.
- Sin subir bases de datos reales ni backups.

## Áreas donde puedes ayudar

- Seguridad anti-abuso: rate limits, Turnstile, CORS, endpoints debug y límites de API.
- Privacidad: minimizar datos y evitar exposición de viviendas exactas.
- Mapa y datos: nuevas comunidades, pipeline CNIG/IGN y optimización GeoJSON.
- Frontend: UX móvil, accesibilidad, paneles y feedback visual.
- Operación: backups SQLite, healthchecks, Cloudflare Tunnel y Cloudflare Pages.
- Documentación pública y revisión legal/comunicativa.

## Qué no subir nunca

No subas .env reales, claves, tokens, secretos, bases de datos, backups, logs con datos sensibles, capturas privadas ni credenciales de Cloudflare.

## Desarrollo local

    docker compose up --build -d

## Validación mínima antes de PR

    python3 -m py_compile backend/app/main.py
    docker compose up -d --build
    curl -s http://127.0.0.1:8098/api/health

## Guardias geográficas y de seguridad

Para cambios relacionados con geografía municipal, datasets, selector de ámbitos o carga de “Toda España”, ejecuta siempre:

```bash
node --check frontend/src/geo/datasets.js
python3 scripts/check_all_scope_datasets.py
python3 scripts/audit_geo_datasets.py
python3 scripts/check_spain_geo_coverage.py
bash scripts/repo_guard.sh --no-build
npm --prefix frontend run build
```

Si se añade un `municipiosPath` individual, también debe quedar incluido en `municipiosPaths` de “Toda España”. Esto evita que una zona con polígono disponible caiga al fallback de cuadrado/celda.

No subas `.env`, bases de datos, backups, logs, SARIF locales, GeoJSON raw de trabajo, auditorías locales ni secretos. Usa `.env.example`, documentación genérica y configuración privada fuera del repositorio.

## Guardias para distribuidoras eléctricas

Las pistas de distribuidora deben añadirse de forma conservadora y verificable.

Reglas obligatorias:

- No añadir datos sin fuente pública.
- No asumir una distribuidora por comunidad autónoma si existen distribuidoras pequeñas.
- No pedir ni almacenar CUPS.
- No añadir texto libre de usuarios.
- No publicar subestaciones, tendidos, cables, centros de transformación ni infraestructura crítica.
- Usar `confidence` para diferenciar datos verificados municipales, coberturas parciales y aproximaciones regionales.
- Ejecutar `python3 scripts/check_distributor_hints.py` antes de abrir PR.

Si no se puede verificar la distribuidora de una zona, debe mantenerse el fallback público: `Consultar distribuidora de la zona`.

