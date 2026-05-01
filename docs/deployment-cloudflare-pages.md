# Despliegue en Cloudflare Pages

Mapa Apagones está preparado para separar frontend y API.

## Objetivo

- `mapa-apagones.es` y `www.mapa-apagones.es`: frontend en Cloudflare Pages.
- `api.mapa-apagones.es`: API FastAPI en servidor propio mediante túnel/reverse proxy seguro.

## Configuración de Cloudflare Pages

Configuración recomendada:

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

Variables de entorno del proyecto Pages:

- `VITE_API_BASE_URL=https://api.mapa-apagones.es`
- `VITE_TURNSTILE_SITE_KEY=<site-key-publica-de-turnstile>`

## Configuración de API en producción

La API sigue ejecutándose en la servidor propio con Docker Compose y se expone con túnel/reverse proxy seguro.

Variables recomendadas del backend:

- `TURNSTILE_ENABLED=1`
- `TURNSTILE_SECRET_KEY=<secret-key-privada-de-turnstile>`
- `ALLOWED_ORIGINS=https://mapa-apagones.es,https://www.mapa-apagones.es`
- `DEBUG_ENDPOINTS=0`

## Desarrollo local

Si `VITE_API_BASE_URL` está vacío, el frontend usa rutas relativas `/api/...`.

Eso mantiene funcionando el despliegue local actual con Nginx en el puerto configurable.
