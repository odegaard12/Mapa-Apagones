# Contribuir a Mapa Apagones

Gracias por querer ayudar.

Mapa Apagones es un proyecto ciudadano, sin cuentas y con privacidad por diseño.

## Principios que no se deben romper

Antes de proponer cambios, ten en cuenta que el proyecto debe seguir siendo:

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

### Seguridad y anti-abuso

- Revisar rate limits.
- Revisar Turnstile.
- Revisar CORS.
- Cerrar endpoints debug.
- Mejorar límites de API.

### Privacidad

- Revisar que no se expongan viviendas exactas.
- Revisar mensajes públicos.
- Revisar documentación de privacidad.
- Minimizar datos almacenados.

### Mapa y datos geográficos

- Añadir comunidades autónomas.
- Mejorar la pipeline CNIG/IGN.
- Optimizar GeoJSON.
- Reducir peso de carga.
- Revisar matching municipio/provincia.

### Frontend

- Mejorar UX móvil.
- Mejorar accesibilidad.
- Mejorar paneles.
- Mejorar feedback visual.
- Mejorar página pública para dominio.

### Operación

- Backups SQLite.
- Healthchecks.
- Cloudflare Tunnel.
- Cloudflare Pages.
- Observabilidad básica.

## Cómo proponer cambios

Preferimos PRs pequeños y revisables.

Ejemplos:

    feat(security): add Turnstile verification for reports
    fix(api): restrict debug endpoints in production
    perf(geo): enable gzip for GeoJSON assets
    docs: document public launch security model

## Qué no subir nunca

No subas:

- .env
- claves
- tokens
- secretos
- bases de datos reales
- backups
- logs con IPs o datos sensibles
- capturas con datos privados
- credenciales de Cloudflare

## Desarrollo local

    docker compose up --build -d

URL local:

    http://TU_IP:8098

## Validación mínima antes de PR

    python3 -m py_compile backend/app/main.py
    docker compose up -d --build
    curl -s http://127.0.0.1:8098/api/health

## Estilo de PR

Cada PR debería explicar:

- Qué cambia.
- Por qué.
- Cómo se validó.
- Riesgos.
- Si afecta a privacidad o seguridad.
