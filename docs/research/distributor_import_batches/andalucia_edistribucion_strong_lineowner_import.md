# Importación parcial verified_partial · Andalucía · E-Distribución

Fecha: `2026-05-13`.

## Resumen

- Dataset: `andalucia`.
- Municipios/zonas importadas: **254 / 786**.
- Confianza usada: `verified_partial`.
- Distribuidora importada: **E-Distribución Redes Digitales, S.L.U.**
- Criterio: propietario público de línea `E-Distribución Redes Digitales` con peso ≥95% en auditoría local saneada sobre WFS público MIEA `LineasElect`.

## Fuente pública

- Agencia Andaluza de la Energía / MIEA — WFS público `MIEA:LineasElect`.
- Endpoint público usado localmente: `https://www.agenciaandaluzadelaenergia.es/mapwms/wfs`.

## Decisión de importación

No se importa Andalucía completa.

No se usa `regional_default`.

Solo se importan municipios con evidencia fuerte de presencia de línea atribuida a E-Distribución. Esto no afirma exclusividad de red ni cobertura total municipal.

## Exclusiones aplicadas

- `Red Eléctrica` se trata como transporte y no se publica como distribuidora municipal.
- `Pequeña distribuidora` no se publica porque es un nombre genérico no identificable.
- Municipios sin match, con transporte dominante o con mezcla insuficiente quedan pendientes.

## Seguridad y privacidad

- No se añade CUPS.
- No se pide CUPS.
- No se añaden direcciones exactas.
- No se añaden teléfonos.
- No se añaden emails.
- No se añaden coordenadas.
- No se añaden geometrías WFS.
- No se añade respuesta WFS raw.
- No se añade inventario de infraestructura crítica.
- No se añaden cuentas.
- No se añaden tokens.
- No se añaden logs, backups, bases de datos reales ni artefactos locales.
