# Changelog

## v0.9.1-public-legal

Fecha: 2026-04-28

### Público / producción

- Dominio público activo: `https://mapa-apagones.es`.
- `www.mapa-apagones.es` activo con SSL.
- Frontend preparado para Cloudflare Pages.
- Páginas públicas revisadas con textos aptos para producción:
  - Privacidad.
  - Aviso legal.
  - Cookies y almacenamiento local.
  - Cómo funciona.
  - No somos una distribuidora.
  - Estado del servicio.
- Correos públicos del proyecto:
  - `contacto@mapa-apagones.es`
  - `privacidad@mapa-apagones.es`
- Eliminadas referencias de plantilla tipo “versión pública del repositorio”.
- Textos redactados sin publicar Gmail personal, DNI, dirección exacta ni teléfono personal.

### SEO / información pública

- `robots.txt`.
- `sitemap.xml`.
- Metadatos SEO básicos.
- Open Graph básico.
- JSON-LD básico.
- Dominio corregido con guion: `mapa-apagones.es`.

### UX

- Vista inicial orientada a España.
- Escala visual más compacta en zoom 100%.
- Mapa como protagonista.
- Paneles menos invasivos.

### Seguridad / operación

- Cloudflare Turnstile preparado para reportes en producción.
- CORS restringido por `ALLOWED_ORIGINS`.
- Endpoints debug cerrados por defecto.
- API con `bbox`, `limit` y límite duro.
- SQLite con WAL, `busy_timeout`, healthchecks y scripts de backup.

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
- Interfaz React + Vite + Leaflet.
- Backend FastAPI + SQLite.

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
