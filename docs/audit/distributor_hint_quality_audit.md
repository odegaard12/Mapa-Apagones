# Auditoría de calidad de pistas de distribuidora

Generado desde `frontend/public/data/distributor_hints.json`.

## Resumen

- Total de zonas con pista pública: **2610**.
- Datasets con pistas: **15**.
- Zone IDs duplicados: **0**.
- Errores bloqueantes detectados: **0**.
- Avisos no bloqueantes detectados: **0**.

## Confianza global

| Confianza | Entradas/distribuidoras |
|---|---:|
| `regional_default` | 1800 |
| `verified_partial` | 967 |

## Calidad por dataset

| Dataset | Zonas | Con fuente | Con fecha | Con notas | regional_default | verified_partial |
|---|---:|---:|---:|---:|---:|---:|
| `andalucia` | 254 | 254 | 254 | 254 | 0 | 254 |
| `asturias` | 78 | 78 | 78 | 78 | 78 | 2 |
| `canarias` | 88 | 88 | 88 | 88 | 87 | 1 |
| `cantabria` | 103 | 103 | 103 | 103 | 103 | 0 |
| `ceuta` | 1 | 1 | 1 | 1 | 0 | 1 |
| `comunitat_valenciana` | 544 | 544 | 544 | 544 | 533 | 11 |
| `euskadi` | 255 | 255 | 255 | 255 | 252 | 3 |
| `extremadura` | 388 | 388 | 388 | 388 | 0 | 530 |
| `galicia` | 313 | 313 | 313 | 313 | 172 | 154 |
| `illes_balears` | 68 | 68 | 68 | 68 | 67 | 1 |
| `la_rioja` | 175 | 175 | 175 | 175 | 175 | 0 |
| `madrid` | 9 | 9 | 9 | 9 | 0 | 9 |
| `melilla` | 1 | 1 | 1 | 1 | 0 | 1 |
| `murcia` | 45 | 45 | 45 | 45 | 45 | 0 |
| `navarra` | 288 | 288 | 288 | 288 | 288 | 0 |

## Lectura operativa

- `regional_default` debe leerse como pista orientativa, no como exclusividad.
- `verified_partial` debe leerse como presencia pública razonablemente verificada, no como cobertura total exclusiva.
- Las zonas sin fuente o sin fecha deben priorizarse para backfill documental antes de nuevas importaciones masivas.
- Esta auditoría no publica CUPS, direcciones, coordenadas privadas ni infraestructura crítica.
