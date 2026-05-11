# Smoke de timing de reportes

Este smoke mide tiempos de los smokes locales de reportes y privacidad.

## Objetivo

Detectar regresiones claras en el flujo de reportes sin tocar producción real.

## Qué mide

- `backend_api`: API básica de backend.
- `report_lifecycle`: creación, lectura en incidencias y resolución en SQLite temporal.
- `report_concurrency`: reportes simultáneos agrupados sin duplicar incidencias.
- `privacy_abuse`: privacidad HMAC, ausencia de IP/token raw y rate limit 429.

## Qué no hace

- No llama a producción.
- No crea reportes reales.
- No llama a `https://mapa-apagones.es`.
- No llama a `https://api.mapa-apagones.es`.
- No pide CUPS.
- No usa cuentas.
- No añade texto libre.
- No sube fotos.
- No publica direcciones exactas ni coordenadas privadas.

## Uso

    SMOKE_PYTHON=/tmp/apagones-smoke-venv/bin/python scripts/smoke_reporting_timing.py

## Interpretación

Los umbrales tienen margen para Raspberry Pi / aarch64. No son benchmark de producción. Sirven para detectar cambios que degraden claramente el flujo de reportes.
