# Plan de siguientes lotes de distribuidoras

Fecha de revisión: 2026-05-10

## Objetivo

Ampliar cobertura de pistas públicas de distribuidoras con datos lo más reales posible, sin publicar datos sensibles y sin afirmar exclusividad cuando no esté demostrada.

## Estado tras importar Melilla

La matriz debe pasar de:

- 1.159 zonas con pista pública.
- 7.056 pendientes.

A:

- 1.160 zonas con pista pública.
- 7.055 pendientes.

## Prioridad recomendada

### 1. Madrid

No importar en bloque. Requiere revisión municipal porque hay presencia pública de UFD en 47 municipios y herramientas de comprobación de i-DE/UFD por zona.

Acción:
- Crear lote municipal confirmado.
- No usar CUPS.
- No usar direcciones.
- No usar coordenadas privadas.

### 2. Euskadi

No importar en bloque sin revisar excepciones locales.

Acción:
- Revisar fuentes públicas de i-DE y posibles distribuidoras locales.
- Separar excepciones como `verified_partial`.
- Usar fallback donde no haya fuente clara.

### 3. Comunitat Valenciana

No importar en bloque sin revisión.

Acción:
- Revisar presencia de i-DE y posibles distribuidoras locales.
- Evitar exclusividad.
- Usar lotes pequeños.

### 4. Aragón / Extremadura / Castilla-La Mancha / Castilla y León / Andalucía / Catalunya

Regiones grandes o con mezcla de distribuidoras. Requieren colas de revisión antes de producción.

## Reglas

- No añadir CUPS.
- No añadir direcciones exactas.
- No añadir coordenadas privadas.
- No añadir fotos.
- No añadir texto libre de usuarios.
- No añadir inventario de infraestructura crítica.
- No meter comunidades completas si la fuente pública solo confirma presencia parcial.
- Actualizar siempre `docs/research/distributor_coverage_matrix.md`.
