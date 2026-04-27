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
