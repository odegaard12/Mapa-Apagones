# Matriz de cobertura de pistas de distribuidoras

Generado desde los datos reales del repositorio el 2026-05-10.

> Esta matriz mide cobertura de **pistas públicas de distribuidora en el repositorio**, no cobertura eléctrica real ni exclusividad de red.

## Resumen

- Datasets geográficos autonómicos: **19**.
- Municipios/zonas normalizadas en GeoJSON: **8.215**.
- Municipios/zonas con pista pública de distribuidora: **1.159**.
- Municipios/zonas pendientes de pista pública: **7.056**.
- Cobertura actual de pistas públicas: **14,1%**.

## Matriz por comunidad/dataset

| Zona | Dataset | GeoJSON | Con pista | Pendiente | Cobertura | Estado | Confianza | Con fecha | Con fuente |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| Galicia | `galicia` | 313 | 313 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 172, `verified_partial` 154 | 313 | 0 |
| Asturias | `asturias` | 78 | 78 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 78, `verified_partial` 2 | 78 | 0 |
| Cantabria | `cantabria` | 103 | 103 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 103 | 103 | 0 |
| Navarra | `navarra` | 288 | 288 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 288 | 288 | 0 |
| La Rioja | `la_rioja` | 175 | 175 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 175 | 175 | 0 |
| Región de Murcia | `murcia` | 45 | 45 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 45 | 45 | 0 |
| Canarias | `canarias` | 88 | 88 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 87, `verified_partial` 1 | 88 | 0 |
| Illes Balears | `illes_balears` | 68 | 68 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 67, `verified_partial` 1 | 68 | 0 |
| Ceuta | `ceuta` | 1 | 1 | 0 | 100,0% | con pista en todas las zonas | `verified_partial` 1 | 1 | 0 |
| Melilla | `melilla` | 1 | 0 | 1 | 0,0% | pendiente | — | 0 | 0 |
| Madrid | `madrid` | 181 | 0 | 181 | 0,0% | pendiente | — | 0 | 0 |
| Euskadi | `euskadi` | 255 | 0 | 255 | 0,0% | pendiente | — | 0 | 0 |
| Comunitat Valenciana | `comunitat_valenciana` | 544 | 0 | 544 | 0,0% | pendiente | — | 0 | 0 |
| Aragón | `aragon` | 734 | 0 | 734 | 0,0% | pendiente | — | 0 | 0 |
| Extremadura | `extremadura` | 388 | 0 | 388 | 0,0% | pendiente | — | 0 | 0 |
| Castilla-La Mancha | `castilla_la_mancha` | 921 | 0 | 921 | 0,0% | pendiente | — | 0 | 0 |
| Castilla y León | `castilla_leon` | 2.298 | 0 | 2.298 | 0,0% | pendiente | — | 0 | 0 |
| Andalucía | `andalucia` | 786 | 0 | 786 | 0,0% | pendiente | — | 0 | 0 |
| Catalunya | `catalunya` | 948 | 0 | 948 | 0,0% | pendiente | — | 0 | 0 |

## Zonas pendientes ordenadas por volumen

| Zona | Pendientes | GeoJSON | Con pista |
|---|---:|---:|---:|
| Castilla y León | 2.298 | 2.298 | 0 |
| Catalunya | 948 | 948 | 0 |
| Castilla-La Mancha | 921 | 921 | 0 |
| Andalucía | 786 | 786 | 0 |
| Aragón | 734 | 734 | 0 |
| Comunitat Valenciana | 544 | 544 | 0 |
| Extremadura | 388 | 388 | 0 |
| Euskadi | 255 | 255 | 0 |
| Madrid | 181 | 181 | 0 |
| Melilla | 1 | 1 | 0 |

## Lectura recomendada

- Priorizar PRs pequeños y verificables.
- No importar comunidades completas si hay dudas de excepciones locales.
- Mantener `regional_default` como pista orientativa, no como afirmación de exclusividad.
- Mantener `verified_partial` para presencia pública razonablemente verificada pero no exclusiva.
- Cuando no haya fuente pública suficiente, mantener fallback sin pista.

## Seguridad y privacidad

Esta matriz no contiene CUPS, cuentas, texto libre de usuarios, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, contratos, facturas ni inventario de infraestructura crítica.

La matriz se debe regenerar con:

```bash
python3 scripts/generate_distributor_coverage_matrix.py
```

Y validar con:

```bash
python3 scripts/generate_distributor_coverage_matrix.py --check
```
