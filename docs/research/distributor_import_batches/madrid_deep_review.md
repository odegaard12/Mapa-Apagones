# Revisión profunda de distribuidoras · Comunidad de Madrid

Generado desde `frontend/public/data/madrid_municipios.geojson`.

## Resumen

- Dataset: `madrid`.
- Municipios/zonas en GeoJSON público: **181**.
- Pistas productivas importadas en este PR: **0**.
- Estado del lote: **no importable todavía como regional_default único**.
- Motivo: Madrid tiene presencia pública relevante de más de una distribuidora y requiere revisión municipal.

## Clasificación inicial

| Estado | Municipios |
|---|---:|
| `candidate_ufd_verified_partial_review` | 9 |
| `multi_distributor_review_required` | 1 |
| `pending_municipal_review` | 171 |

## Fuentes públicas de alto nivel

- UFD/Naturgy: comunicación pública indicando servicio a más de 1,2 millones de puntos de suministro en 47 municipios de la Comunidad de Madrid y citando actuaciones en varios municipios: https://www.naturgy.com/notas-de-prensa/ufd-refuerza-la-calidad-del-suministro-electrico-en-el-sur-de-la-comunidad-de-madrid/
- UFD: herramienta pública para comprobar si una zona pertenece a su red de distribución: https://www.ufd.es/quienes-somos/donde-estamos/
- i-DE: herramienta pública para localizar municipio/dirección y conocer si opera en esa zona: https://www.i-de.es/conexion-red-electrica/mapa-de-distribuidoras
- CNMC: censo/listado público de distribuidoras de electricidad: https://sede.cnmc.gob.es/listado/censo/1
- Comunidad de Madrid: agenda/reunión con UFD Distribución Electricidad, S.A.: https://www.comunidad.madrid/transparencia/agenda/reunion-ufd-distribucion-electricidad-sa

## Candidatos UFD citados por fuente pública

Estos municipios aparecen citados en la comunicación pública de UFD/Naturgy o encajan con actuaciones descritas públicamente, pero **no se importan todavía**. Deben comprobarse con herramienta oficial o fuente municipal antes de pasar a `verified_partial`.

- Alcalá de Henares — `candidate_ufd_verified_partial_review`.
- Aranjuez — `candidate_ufd_verified_partial_review`.
- Ciempozuelos — `candidate_ufd_verified_partial_review`.
- Colmenar de Oreja — `candidate_ufd_verified_partial_review`.
- Getafe — `candidate_ufd_verified_partial_review`.
- Rivas-Vaciamadrid — `candidate_ufd_verified_partial_review`.
- San Martín de la Vega — `candidate_ufd_verified_partial_review`.
- Valdemoro — `candidate_ufd_verified_partial_review`.
- Villaconejos — `candidate_ufd_verified_partial_review`.

## Municipios pendientes

Quedan **171** municipios marcados como `pending_municipal_review`.

No se deben importar como UFD ni como i-DE hasta tener evidencia pública municipal suficiente.

## Criterio de seguridad

- No usar CUPS para generar datos públicos.
- No publicar direcciones exactas.
- No publicar coordenadas privadas.
- No publicar infraestructura crítica.
- No afirmar exclusividad de red.
- No convertir fuentes regionales en cobertura municipal sin comprobación.
- Mantener `regional_default` solo cuando el riesgo de excepción local sea bajo.
- Usar `verified_partial` solo para presencia pública razonablemente verificada, nunca como cobertura exclusiva.

## Siguiente paso recomendado

1. Revisar la cola municipal en `docs/research/distributor_import_batches/madrid_municipality_review_queue.csv`.
2. Confirmar municipios con herramientas públicas oficiales y fuentes municipales.
3. Importar solo subconjunto conservador:
   - municipios UFD con evidencia municipal fuerte;
   - municipios i-DE con evidencia municipal fuerte;
   - dejar el resto como pendiente.
