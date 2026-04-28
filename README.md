# Mapa Apagones

Mapa ciudadano de avisos de apagones, cortes eléctricos e incidencias de suministro.

Repositorio público del proyecto publicado en:

    https://mapa-apagones.es

Estado actual:

Versión actual visible: `v0.9.7.2-mobile-responsive`.

    Publicado en Cloudflare Pages con dominio público activo, API pública por Cloudflare Tunnel y Turnstile activo para reportes.

## Identidad pública

Antes de seguir con mejoras técnicas, este repositorio deja clara la identidad pública del proyecto:

- Nombre público: Mapa Apagones.
- Dominio público: mapa-apagones.es.
- Estado actual: publicado en Cloudflare Pages con API pública mediante Cloudflare Tunnel.
- Principios de privacidad: sin cuentas, sin CUPS, sin texto libre, sin fotos y sin mostrar viviendas exactas.
- Licencia: MIT.
- Cómo puede ayudar otra gente: privacidad, seguridad anti-abuso, accesibilidad, UX móvil, documentación, despliegue y nuevas comunidades autónomas.
- Qué no debe subirse nunca: .env reales, claves, tokens, bases de datos, backups, logs con datos sensibles ni credenciales.

## Objetivo

Crear un mapa ciudadano, sencillo y respetuoso con la privacidad para visualizar zonas donde varias personas reportan incidencias eléctricas.

El proyecto no pretende sustituir a las distribuidoras eléctricas ni a los canales oficiales de emergencia. Su objetivo es ayudar a detectar señales ciudadanas agregadas por zona.

## Principios del proyecto

- Sin cuentas.
- Sin login.
- Sin CUPS.
- Sin texto libre.
- Sin fotos.
- Sin mostrar viviendas exactas.
- Sin publicar coordenadas exactas de usuarios.
- Reportes agrupados por zona.
- Código abierto.
- Privacidad por diseño.

## Qué es

Mapa ciudadano de incidencias eléctricas basado en reportes anónimos.

Permite reportar, de forma rápida:

- Sin luz.
- Microcortes.
- Baja tensión.
- Ya volvió.

La aplicación agrupa los reportes por zona aproximada y muestra estados de confianza como señal débil, probable, activa o resuelta.

## Qué no es

Mapa Apagones no es una distribuidora eléctrica.

No gestiona averías, no repara cortes, no sustituye a los teléfonos oficiales y no debe utilizarse para emergencias.

Para incidencias oficiales, averías peligrosas o riesgos personales, debe contactarse con la distribuidora correspondiente o con los servicios de emergencia.

## Stack

Frontend:

    React + Vite + Leaflet

Backend:

    FastAPI + SQLite

Despliegue actual:

    Docker Compose en Raspberry Pi
    Puerto local: 8098

Despliegue objetivo:

    mapa-apagones.es y www.mapa-apagones.es -> Cloudflare Pages
    api.mapa-apagones.es -> Raspberry Pi vía Cloudflare Tunnel

## Estado geográfico actual

Ámbitos disponibles:

- Toda España, combinando datasets disponibles.
- Galicia.
- Asturias.
- Cantabria.
- Castilla y León.

Los polígonos municipales se generan desde fuentes CNIG/IGN normalizadas mediante scripts del repositorio.

## Seguridad y anti-abuso

El proyecto mantiene un enfoque anónimo, pero incluye medidas anti-abuso:

- Token local anónimo del navegador.
- Hash de token.
- Hash de IP para rate limiting.
- Rate limit temporal.
- Cloudflare Turnstile para reportes en producción.
- Sin almacenamiento del token Turnstile.
- Caducidad de reportes.

Turnstile complementa el rate limit; no lo sustituye.

## Privacidad

El proyecto evita recoger información innecesaria.

No se solicitan:

- Nombre.
- Email.
- Cuenta de usuario.
- CUPS.
- Dirección exacta.
- Fotos.
- Texto libre.

Los reportes se agrupan en zonas aproximadas para no mostrar viviendas exactas.

## Páginas públicas y SEO

El frontend incluye una capa pública básica para el dominio previsto:

- `robots.txt`
- `sitemap.xml`
- Open Graph en la portada
- JSON-LD básico
- `/como-funciona/`
- `/privacidad/`
- `/no-somos-distribuidora/`
- `/estado/`
- `/aviso-legal/`
- `/cookies/`

Estas páginas son informativas y no cambian el flujo de reportes.

## Desarrollo local

    docker compose up --build -d

URL local:

    http://TU_IP:8098

## Variables de entorno principales

Backend:

    DB_PATH=/data/app.db
    TURNSTILE_ENABLED=0
    TURNSTILE_SECRET_KEY=
    IGN_WFS_ENABLED=1

Frontend en Cloudflare Pages:

    VITE_API_BASE_URL=https://api.mapa-apagones.es
    VITE_TURNSTILE_SITE_KEY=...

## Estructura

    backend/
    frontend/
    scripts/
    VERSION
    docker-compose.yml

## Cómo ayudar

Se agradecen contribuciones en:

- Revisión de privacidad.
- Seguridad anti-abuso.
- Optimización de GeoJSON.
- Mejoras de accesibilidad.
- Diseño móvil.
- Documentación.
- Despliegue Cloudflare Pages / Tunnel.
- Guía de Cloudflare Pages: `docs/deployment-cloudflare-pages.md`.
- Añadir nuevas comunidades autónomas desde la pipeline CNIG.
- Revisión legal/comunicativa del mensaje público.

Antes de contribuir, revisa CONTRIBUTING.md.

## Contacto público

- Contacto general: `contacto@mapa-apagones.es`
- Privacidad: `privacidad@mapa-apagones.es`

No se publica correo personal, DNI, dirección personal exacta ni teléfono personal en este repositorio.

## Licencia

MIT. Ver LICENSE.

## Aviso

Este proyecto está publicado en fase temprana. Los datos ciudadanos pueden contener errores, retrasos o zonas incompletas. No debe usarse como única fuente para decisiones críticas.
