# Matriz de cobertura de pistas de distribuidoras

Generado desde los datos reales del repositorio el 2026-06-19.

> Esta matriz mide cobertura de **pistas públicas de distribuidora en el repositorio**, no cobertura eléctrica real ni exclusividad de red.

## Resumen

- Datasets geográficos autonómicos: **19**.
- Municipios/zonas normalizadas en GeoJSON: **8.215**.
- Municipios/zonas con pista pública de distribuidora: **2.610**.
- Municipios/zonas pendientes de pista pública: **5.605**.
- Cobertura actual de pistas públicas: **31,8%**.

## Matriz por comunidad/dataset

| Zona | Dataset | GeoJSON | Con pista | Pendiente | Cobertura | Estado | Confianza | Con fecha | Con fuente |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| Galicia | `galicia` | 313 | 313 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 172, `verified_partial` 154 | 313 | 313 |
| Asturias | `asturias` | 78 | 78 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 78, `verified_partial` 2 | 78 | 78 |
| Cantabria | `cantabria` | 103 | 103 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 103 | 103 | 103 |
| Navarra | `navarra` | 288 | 288 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 288 | 288 | 288 |
| La Rioja | `la_rioja` | 175 | 175 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 175 | 175 | 175 |
| Región de Murcia | `murcia` | 45 | 45 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 45 | 45 | 45 |
| Canarias | `canarias` | 88 | 88 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 87, `verified_partial` 1 | 88 | 88 |
| Illes Balears | `illes_balears` | 68 | 68 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 67, `verified_partial` 1 | 68 | 68 |
| Ceuta | `ceuta` | 1 | 1 | 0 | 100,0% | con pista en todas las zonas | `verified_partial` 1 | 1 | 1 |
| Melilla | `melilla` | 1 | 1 | 0 | 100,0% | con pista en todas las zonas | `verified_partial` 1 | 1 | 1 |
| Madrid | `madrid` | 181 | 9 | 172 | 5,0% | parcial | `verified_partial` 9 | 9 | 9 |
| Euskadi | `euskadi` | 255 | 255 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 252, `verified_partial` 3 | 255 | 255 |
| Comunitat Valenciana | `comunitat_valenciana` | 544 | 544 | 0 | 100,0% | con pista en todas las zonas | `regional_default` 533, `verified_partial` 11 | 544 | 544 |
| Aragón | `aragon` | 734 | 0 | 734 | 0,0% | pendiente | — | 0 | 0 |
| Extremadura | `extremadura` | 388 | 388 | 0 | 100,0% | con pista en todas las zonas | `verified_partial` 530 | 388 | 388 |
| Castilla-La Mancha | `castilla_la_mancha` | 921 | 0 | 921 | 0,0% | pendiente | — | 0 | 0 |
| Castilla y León | `castilla_leon` | 2.298 | 0 | 2.298 | 0,0% | pendiente | — | 0 | 0 |
| Andalucía | `andalucia` | 786 | 254 | 532 | 32,3% | parcial | `verified_partial` 254 | 254 | 254 |
| Catalunya | `catalunya` | 948 | 0 | 948 | 0,0% | pendiente | — | 0 | 0 |

## Zonas pendientes ordenadas por volumen

| Zona | Pendientes | GeoJSON | Con pista |
|---|---:|---:|---:|
| Castilla y León | 2.298 | 2.298 | 0 |
| Catalunya | 948 | 948 | 0 |
| Castilla-La Mancha | 921 | 921 | 0 |
| Aragón | 734 | 734 | 0 |
| Andalucía | 532 | 786 | 254 |
| Madrid | 172 | 181 | 9 |

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
