# TODO — Mapa Apagones

Prioridad P0 (roto) → P1 (SEO/seguridad/fiabilidad/UX importante/datos) → P2 (diseño/rendimiento) → P3 (limpieza).

## P0 — Roto o incorrecto

- [x] `/api/zones` no exponía `created_at` → "Detectado: sin datos" para toda incidencia en producción. **Corregido**, ver `fix/incident-timestamps-and-health`.
- [ ] Ninguno más detectado en esta sesión. Revisar de nuevo tras cada cambio grande de UI (botones que no hagan nada, estados inconsistentes).

## P1 — SEO / seguridad / fiabilidad

- [x] CVEs en starlette/idna corregidos (PR #222).
- [x] Headers de seguridad (_headers) faltantes en Cloudflare Pages (PR #222).
- [x] Manifest PWA y canonical faltante en /seguridad/ (PR #224).
- [ ] Structured data (JSON-LD) adicional: valorar `FAQPage` en `/como-funciona/` y `BreadcrumbList` en páginas con jerarquía clara. No añadir schema sin que corresponda de verdad.
- [ ] Revisar `og:image`: hoy apunta a `favicon.png` (1024x1024 cuadrado). Sirve, pero una imagen 1200x630 específica para OG/Twitter mejoraría el preview en redes.
- [ ] `/healthz` "real" con detalle de subsistemas (web/backend/db/fuentes/último ciclo) — hoy `/api/health` solo cubre DB. Definir qué significa "fuentes" y "último ciclo" en este proyecto (no hay scraping de fuentes externas activo que yo haya encontrado; confirmar con el dueño del proyecto antes de inventar el concepto).

## P1 — Datos y cobertura de distribuidoras

Cobertura geográfica (comunidades autónomas): **completa, 19/19**. No confundir con cobertura de distribuidora eléctrica.

**2026-09-19: fuente pública real encontrada (CNMC, regulador nacional) e importada.** Ver `DISTRIBUTOR_RESEARCH.md` para el detalle técnico completo.

- [x] Castilla y León — 251/2.298 (10.9%), antes 0%.
- [x] Catalunya — 157/948 (16.6%), antes 0%.
- [x] Castilla-La Mancha — 154/921 (16.7%), antes 0%.
- [x] Aragón — 138/734 (18.8%), antes 0%.

Pendiente (no bloqueante): completar el resto de municipios con más FeatureServers de CNMC (generación, transporte), arreglar 7 municipios catalanes con artículo no estándar (Les/L'/Els/Es), y aplicar el mismo método a Madrid (actualmente 9/181, 5%).

Para el resto sin cobertura verificada: crowdsourcing anónimo ya implementado (`/api/distributor-suggestion`), visible en el panel de incidencia cuando `confidence === 'unknown'`.

## P1 — UX importante

- [x] Botón de refresco manual real (no simulado) — verificado end-to-end.
- [x] Fecha/hora exacta (detectado/actualizado) junto al relativo "hace X min".
- [ ] Revisar el resto de "botones que no hagan nada" en el flujo completo (reportar, filtros, cambio de ámbito geográfico) con pruebas de navegador reales, no solo lectura de código — así se encontró el bug de `/api/zones`.
- [ ] Filtros: confirmar que tras filtrar se muestra un recuento ("123 incidencias · 27 zonas") — pendiente de revisar si ya existe.

## P2 — Diseño

- [ ] Revisión de jerarquía visual completa (situación actual → mapa → filtros → datos → detalles → fuentes) pedida por el usuario. No iniciada aún en esta sesión: requiere auditoría visual con capturas reales, no solo lectura de JSX.
- [ ] Tarjetas de incidencia: confirmar que muestran solo lo esencial (estado, zona, hora, distribuidora, impacto) y que el detalle completo vive aparte — parece que ya es así por diseño, pendiente de confirmar visualmente.

## P2 — Rendimiento

- [ ] No detectado ningún problema de rendimiento evidente en esta sesión. Sin datos de producción (Lighthouse, Core Web Vitals reales) para priorizar aquí con confianza.

## P3 — Limpieza

- [x] Housekeeping de PRs de Dependabot ya integrados (#221) — parcialmente, 5 PRs viejos (#216, #215, #213, #212, #211) siguen abiertos en GitHub aunque su contenido ya está en main; se cerrarán solos en el próximo escaneo de Dependabot.
- [ ] `.claude/launch.json` de este agente (para levantar `vite` en pruebas locales) no está commiteado a propósito — es config de desarrollo local, no del proyecto.

## Pendiente de decisión del usuario

- React 18→19 (#217, #218): rompen el build de Cloudflare Pages. Requiere migración cuidadosa (breaking changes de React 19), no un merge directo. No se ha investigado la causa exacta del fallo de build todavía.
- Autorizar la clave SSH de este entorno en `.103`/`.104`, o indicar otro mecanismo, si se quiere que el agente despliegue directamente en vez de que el usuario ejecute `git pull && docker compose up -d --build` tras cada merge.
