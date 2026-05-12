# Auditoría profunda de distribuidoras · Extremadura

Generado desde `frontend/public/data/extremadura_municipios.geojson` y fuentes públicas de alto nivel.

## Resumen ejecutivo

- Dataset: `extremadura`.
- Municipios/zonas en GeoJSON público: **388**.
- Pistas productivas importadas en este PR: **0**.
- Pistas productivas actuales en Extremadura: **388**.
- Estado del lote: **no importable como `regional_default` único**.
- Motivo: Extremadura tiene varias distribuidoras detectadas; la importación correcta es municipal `verified_partial`.

## Clasificación inicial

| Estado | Municipios |
|---|---:|
| `already_in_production` | 388 |
| `pending_municipal_review` | 0 |

## Distribución por provincia detectada

| Provincia | Municipios |
|---|---:|
| Badajoz | 165 |
| Cáceres | 223 |

## Fuentes públicas de alto nivel

- **Junta de Extremadura — visor público de empresas distribuidoras de energía eléctrica** — `official_regional_map`. Fuente oficial útil para revisión municipal. No convertir automáticamente en cobertura regional única. Fuente: https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml
- **Iberdrola España / i-DE — plan de inversiones redes eléctricas Extremadura 2027-2029** — `regional_presence_confirmed`. Confirma presencia regional relevante de i-DE, pero no cobertura municipal completa. Fuente: https://www.iberdrolaespana.com/sala-comunicacion/noticias/plan-inversiones-redes-electricas-extremadura-2027-2029
- **CNMC — censo/listado público de distribuidoras de electricidad** — `national_registry`. Sirve para validar razón social/código, no para inferir municipio exacto. Fuente: https://sede.cnmc.gob.es/listado/censo/1
- **Política de exclusión de listados con campos sensibles** — `safety_policy`. No ingerir automáticamente listados/PDFs que puedan incluir CUPS, direcciones, teléfonos o datos de suministro. Solo usar fuentes sanitizadas o revisión manual.

## Decisión de seguridad

No se importa Extremadura como una única distribuidora regional.

La importación segura es municipal y prudente, usando `verified_partial`, sin afirmar exclusividad de red ni cobertura total municipal.

## Archivos generados

- `docs/research/distributor_import_batches/extremadura_deep_audit.md`
- `docs/research/distributor_import_batches/extremadura_municipality_review_queue.csv`
- `docs/research/distributor_import_batches/extremadura_distributor_sources.csv`

## Muestra de cola municipal

- Acedera — `already_in_production`
- Aceuchal — `already_in_production`
- Ahillones — `already_in_production`
- Alange — `already_in_production`
- Alburquerque — `already_in_production`
- Alconchel — `already_in_production`
- Alconera — `already_in_production`
- Aljucén — `already_in_production`
- Almendral — `already_in_production`
- Almendralejo — `already_in_production`
- Arroyo de San Serván — `already_in_production`
- Atalaya — `already_in_production`
- Azuaga — `already_in_production`
- Badajoz — `already_in_production`
- Barcarrota — `already_in_production`
- Baterno — `already_in_production`
- Benquerencia de la Serena — `already_in_production`
- Berlanga — `already_in_production`
- Bienvenida — `already_in_production`
- Bodonal de la Sierra — `already_in_production`
- Burguillos del Cerro — `already_in_production`
- Cabeza del Buey — `already_in_production`
- Cabeza la Vaca — `already_in_production`
- Calamonte — `already_in_production`
- Calera de León — `already_in_production`
- Calzadilla de los Barros — `already_in_production`
- Campanario — `already_in_production`
- Campillo de Llerena — `already_in_production`
- Capilla — `already_in_production`
- Carmonita — `already_in_production`
- Casas de Don Pedro — `already_in_production`
- Casas de Reina — `already_in_production`
- Castilblanco — `already_in_production`
- Castuera — `already_in_production`
- Cheles — `already_in_production`
- Cordobilla de Lácara — `already_in_production`
- Corte de Peleas — `already_in_production`
- Cristina — `already_in_production`
- Don Álvaro — `already_in_production`
- Don Benito — `already_in_production`

## Pendientes

- Ninguno.

## Siguiente paso recomendado

Mantener esta importación como pistas municipales `verified_partial`. No usar `regional_default` para Extremadura.
