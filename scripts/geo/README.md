# Pipeline GeoJSON CNIG

Herramienta para generar GeoJSON municipales normalizados para el frontend.

## Propiedades de salida

Cada municipio debe salir con estas propiedades estables:

```text
dataset_id
zone_id
municipio
province
display_name
```

## Regla de zone_id

No usamos IDs numericos internos como ID principal. Generamos IDs legibles:

```text
municipality:<provincia-slug>::<municipio-slug>
```

Ejemplos:

```text
municipality:asturias::allande
municipality:ourense::leiro
```

Si la fuente trae un ID propio, se conserva como:

```text
source_zone_id
```

## Uso basico

```bash
python3 scripts/geo/build_cnig_community.py \
  --input FUENTE.geojson \
  --output frontend/public/data/asturias_municipios.geojson \
  --dataset-id asturias \
  --label "Asturias" \
  --where codnut2=ES12
```

## Uso si la fuente no trae provincia clara

```bash
python3 scripts/geo/build_cnig_community.py \
  --input FUENTE.geojson \
  --output frontend/public/data/asturias_municipios.geojson \
  --dataset-id asturias \
  --label "Asturias" \
  --province "Asturias" \
  --where codnut2=ES12
```

## Test con Galicia raw actual

```bash
python3 scripts/geo/build_cnig_community.py \
  --input frontend/public/data/galicia_municipios_raw.geojson \
  --output /tmp/galicia_pipeline_test.geojson \
  --dataset-id galicia \
  --label "Galicia" \
  --where acom_name=Galicia
```

## Validacion

```bash
python3 -m json.tool frontend/public/data/asturias_municipios.geojson >/dev/null
python3 -m json.tool frontend/public/data/galicia_municipios.geojson >/dev/null
docker compose up -d --build
```
