# Auditoría profunda de distribuidoras · Extremadura

Generado desde `frontend/public/data/extremadura_municipios.geojson` y fuentes públicas de alto nivel.

## Resumen ejecutivo

- Dataset: `extremadura`.
- Municipios/zonas en GeoJSON público: **388**.
- Pistas productivas importadas en este PR: **0**.
- Pistas productivas actuales en Extremadura: **0**.
- Estado del lote: **no importable todavía como `regional_default` único**.
- Motivo: hay presencia pública regional relevante de i-DE, pero también fuente oficial autonómica de mapa de distribuidoras y censo CNMC; requiere revisión municipal.

## Clasificación inicial

| Estado | Municipios |
|---|---:|
| `already_in_production` | 0 |
| `pending_municipal_review` | 388 |

## Distribución por provincia detectada

| Provincia | Municipios |
|---|---:|
| Badajoz | 165 |
| Cáceres | 223 |

## Fuentes públicas de alto nivel

- **Junta de Extremadura — mapa público de empresas distribuidoras de energía eléctrica** — `official_regional_map`. Fuente oficial útil para revisión municipal manual. No convertir automáticamente en cobertura masiva. Fuente: https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml
- **Iberdrola España / i-DE — plan de inversiones redes eléctricas Extremadura 2027-2029** — `regional_presence_confirmed`. Confirma presencia regional relevante de i-DE, pero no cobertura municipal completa. Fuente: https://www.iberdrolaespana.com/sala-comunicacion/noticias/plan-inversiones-redes-electricas-extremadura-2027-2029
- **CNMC — censo/listado público de distribuidoras de electricidad** — `national_registry`. Sirve para validar razón social/código, no para inferir municipio exacto. Fuente: https://sede.cnmc.gob.es/listado/censo/1
- **Política de exclusión de listados con campos sensibles** — `safety_policy`. No ingerir automáticamente listados/PDFs que puedan incluir CUPS, direcciones, teléfonos o datos de suministro. Solo usar fuentes sanitizadas o revisión manual.

## Decisión de seguridad

No se importan los 388 municipios como una única distribuidora regional.

La presencia regional de i-DE permite abrir revisión, pero no basta para afirmar cobertura municipal completa. Además, cualquier listado que incluya CUPS, direcciones, teléfonos o datos de suministro queda excluido de ingestión automática.

## Política de importación posterior

Para pasar un municipio a `verified_partial`:

1. Confirmar municipio en fuente pública oficial o herramienta pública de distribuidora.
2. Validar razón social con CNMC si procede.
3. No usar CUPS.
4. No usar direcciones exactas privadas.
5. No publicar coordenadas privadas.
6. No afirmar exclusividad de red.
7. Añadir fuente trazable y nota de cobertura prudente.

Para usar `regional_default`:

- Solo si el riesgo de excepción local es bajo.
- Solo después de revisar excepciones locales.
- No aplicable a Extremadura en este momento.

## Archivos generados

- `docs/research/distributor_import_batches/extremadura_deep_audit.md`
- `docs/research/distributor_import_batches/extremadura_municipality_review_queue.csv`
- `docs/research/distributor_import_batches/extremadura_distributor_sources.csv`

## Muestra de cola municipal

- Abadía — `pending_municipal_review`
- Abertura — `pending_municipal_review`
- Acebo — `pending_municipal_review`
- Acedera — `pending_municipal_review`
- Acehúche — `pending_municipal_review`
- Aceituna — `pending_municipal_review`
- Aceuchal — `pending_municipal_review`
- Ahigal — `pending_municipal_review`
- Ahillones — `pending_municipal_review`
- Alagón del Río — `pending_municipal_review`
- Alange — `pending_municipal_review`
- Albalá — `pending_municipal_review`
- Alburquerque — `pending_municipal_review`
- Alcántara — `pending_municipal_review`
- Alcollarín — `pending_municipal_review`
- Alconchel — `pending_municipal_review`
- Alconera — `pending_municipal_review`
- Alcuéscar — `pending_municipal_review`
- Aldea del Cano — `pending_municipal_review`
- Aldeacentenera — `pending_municipal_review`
- Aldeanueva de la Vera — `pending_municipal_review`
- Aldeanueva del Camino — `pending_municipal_review`
- Aldehuela de Jerte — `pending_municipal_review`
- Alía — `pending_municipal_review`
- Aliseda — `pending_municipal_review`
- Aljucén — `pending_municipal_review`
- Almaraz — `pending_municipal_review`
- Almendral — `pending_municipal_review`
- Almendralejo — `pending_municipal_review`
- Almoharín — `pending_municipal_review`
- Arroyo de la Luz — `pending_municipal_review`
- Arroyo de San Serván — `pending_municipal_review`
- Arroyomolinos — `pending_municipal_review`
- Arroyomolinos de la Vera — `pending_municipal_review`
- Atalaya — `pending_municipal_review`
- Azuaga — `pending_municipal_review`
- Baños de Montemayor — `pending_municipal_review`
- Barcarrota — `pending_municipal_review`
- Barrado — `pending_municipal_review`
- Baterno — `pending_municipal_review`

## Siguiente paso recomendado

Hacer un PR posterior de importación parcial, pequeño y verificable, solo con municipios donde la evidencia pública sea fuerte.

No hacer importación regional completa de Extremadura todavía.
