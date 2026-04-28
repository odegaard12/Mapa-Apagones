# Changelog

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
