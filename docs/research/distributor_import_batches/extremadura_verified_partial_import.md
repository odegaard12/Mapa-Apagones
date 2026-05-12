# Importación verified_partial de distribuidoras · Extremadura

Fecha: `2026-05-12`.

## Resumen

- Dataset: `extremadura`.
- Municipios/zonas importadas: **388 / 388**.
- Pistas productivas importadas en este PR: **388**.
- Confianza usada: `verified_partial`.
- Municipios con una distribuidora detectada: **277**.
- Municipios con múltiples distribuidoras detectadas: **111**.
- Distribuidoras detectadas: **28**.

## Fuente pública

- Junta de Extremadura — visor público de empresas distribuidoras de energía eléctrica:
  https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml

## Método

Se usó una auditoría local saneada, sin guardar respuesta WFS raw ni geometrías, calculando intersección por área entre la capa pública autonómica y el GeoJSON municipal del repositorio.

Umbral usado: **0,25%** del área municipal.

## Decisión de importación

No se importa Extremadura como `regional_default`.

Se importan pistas municipales `verified_partial`, incluyendo varios distribuidores cuando la fuente pública cruza más de una distribuidora con el municipio.

Esto no afirma exclusividad de red ni cobertura total municipal.

## Seguridad y privacidad

- No se añade CUPS.
- No se pide CUPS.
- No se añaden direcciones exactas.
- No se añaden teléfonos.
- No se añaden emails.
- No se añaden coordenadas privadas.
- No se añaden geometrías WFS.
- No se añade respuesta WFS raw.
- No se añade inventario de infraestructura crítica.
- No se añaden cuentas.
- No se añaden tokens.
- No se añaden logs, backups, bases de datos reales ni artefactos locales.

## Distribuidoras detectadas

- Alconera de Electricidad, S.L.U.
- Anselmo León Distribución S.L.
- Distribución de Electricidad Valle de Santa Ana, S.L.
- Distribuidora Eléctrica Carrión, S.L.
- Distribuidora Eléctrica Monesterio, S.L.
- Distribuidora Eléctrica de Granja de Torrehermosa, S.L.
- Distribuidora de Energía Eléctrica de Don Benito, S.L.U.
- Edistribución Redes Digitales, S.L.U.
- Eléctrica San Serván, S.L.
- Eléctrica Santa Marta y Villalba, S.L.
- Eléctrica de Aldeacentenera, S.L.U.
- Eléctrica de Malcocinado, S.L.
- Eléctrica del Oeste Distribución, S.L.U.
- Eléctricas Pitarch Distribución, S.L.U.
- Eléctricas Santa Leonor, S.L.
- Emdecoria, S.L.
- Energética de Alcocer, S.L.
- Energía de Miajadas, S.A.
- Fuentes y Compañía, S.L.
- Herederos de García Baz, S.L.
- Hijos de Francisco Escaso, S.L.
- Hijos de Jacinto Guillén, D.E., S.L.
- I-DE Redes Eléctricas Inteligentes, S.A.U.
- La Ernestina Energía, S.L.
- Luis Rangel y Hermanos, S.A.
- Relkia Distribuidora de Electricidad, SL (Repsol)
- Sociedad Eléctrica de Ribera del Fresno S.L.
- UFD Distribución Electricidad. S.A.
