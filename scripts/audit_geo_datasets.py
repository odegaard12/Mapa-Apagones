#!/usr/bin/env python3
import argparse
import json
import re
import unicodedata
from pathlib import Path

DATA_DIR = Path("frontend/public/data")

MUNICIPIO_KEYS = [
    "municipio",
    "mun_name",
    "mun_name_local",
    "name",
    "name_es",
    "nombre",
    "NOMBRE",
    "Texto",
    "texto",
    "label",
    "LAU_NAME",
    "lau_name",
    "NAMEUNIT",
    "nameunit",
]

PROVINCE_KEYS = [
    "province",
    "prov_name",
    "prov_name_local",
    "province_name",
    "provincia",
    "PROVINCIA",
    "NPRO",
    "name_prov",
]

SINGLE_PROVINCE_DEFAULTS = {
    "asturias": "Asturias",
    "cantabria": "Cantabria",
    "madrid": "Madrid",
    "navarra": "Navarra",
    "la_rioja": "La Rioja",
    "murcia": "Murcia",
    "illes_balears": "Illes Balears",
    "ceuta": "Ceuta",
    "melilla": "Melilla",
}

DATASET_LABELS = {
    "galicia": "Galicia",
    "asturias": "Asturias",
    "cantabria": "Cantabria",
    "castilla_leon": "Castilla y León",
    "madrid": "Comunidad de Madrid",
    "aragon": "Aragón",
    "navarra": "Navarra",
    "la_rioja": "La Rioja",
    "murcia": "Región de Murcia",
    "ceuta": "Ceuta",
    "melilla": "Melilla",
    "comunitat_valenciana": "Comunitat Valenciana",
    "illes_balears": "Illes Balears",
    "canarias": "Canarias",
    "andalucia": "Andalucía",
    "extremadura": "Extremadura",
    "castilla_la_mancha": "Castilla-La Mancha",
    "cataluna": "Cataluña",
    "pais_vasco": "País Vasco",
}

CRITICAL_CHECKS = [
    ("asturias", "San Martín de Oscos"),
    ("galicia", "Catoira"),
    ("aragon", "Zuera"),
    ("madrid", "Madrid"),
    ("navarra", "Valle de Elorz/Elortzibar"),
    ("la_rioja", "Logroño"),
    ("murcia", "Murcia"),
    ("canarias", "Las Palmas de Gran Canaria"),
]

def normalize_text(value=""):
    return (
        unicodedata.normalize("NFD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )

def slug(value=""):
    s = normalize_text(value)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_")

def title_from_slug(value=""):
    return " ".join(part.capitalize() for part in str(value).split("_") if part)

def first_prop(props, keys):
    for key in keys:
        value = props.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""

def parse_zone_id(zone_id):
    if not zone_id or not isinstance(zone_id, str):
        return "", ""
    m = re.match(r"^municipality:([^:]+)::(.+)$", zone_id)
    if not m:
        return "", ""
    return title_from_slug(m.group(1)), title_from_slug(m.group(2))

def normalize_feature(feature, dataset_id):
    props = feature.get("properties") or {}
    geometry = feature.get("geometry")

    existing_zone_id = props.get("zone_id") or ""
    zone_province, zone_municipio = parse_zone_id(existing_zone_id)

    municipio = first_prop(props, MUNICIPIO_KEYS) or zone_municipio
    province = first_prop(props, PROVINCE_KEYS) or zone_province

    if not province and dataset_id in SINGLE_PROVINCE_DEFAULTS:
        province = SINGLE_PROVINCE_DEFAULTS[dataset_id]

    if not municipio:
        raise ValueError(f"{dataset_id}: feature sin municipio")

    if not province:
        raise ValueError(f"{dataset_id}: feature sin provincia para municipio={municipio!r}")

    if not geometry:
        raise ValueError(f"{dataset_id}: feature sin geometría para municipio={municipio!r}")

    zone_id = f"municipality:{slug(province)}::{slug(municipio)}"

    new_props = {
        "municipio": municipio,
        "mun_name": municipio,
        "name": municipio,
        "province": province,
        "prov_name": province,
        "dataset_id": dataset_id,
        "zone_id": zone_id,
    }

    return {
        "type": "Feature",
        "properties": new_props,
        "geometry": geometry,
    }

def dataset_id_from_path(path):
    return path.name.replace("_municipios.geojson", "")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    files = sorted(
        p for p in DATA_DIR.glob("*_municipios.geojson")
        if p.name != "toda_espana_municipios.geojson"
    )

    if not files:
        raise SystemExit("ERROR: no hay datasets *_municipios.geojson")

    all_seen = {}
    total = 0

    for path in files:
        dataset_id = dataset_id_from_path(path)
        raw = json.loads(path.read_text())
        features = raw.get("features") or []

        normalized = []
        seen = set()

        for feature in features:
            nf = normalize_feature(feature, dataset_id)
            zone_id = nf["properties"]["zone_id"]

            if zone_id in seen:
                continue

            seen.add(zone_id)
            normalized.append(nf)

        if not normalized:
            raise SystemExit(f"ERROR: dataset vacío tras normalizar: {path}")

        fc = {
            "type": "FeatureCollection",
            "features": normalized,
        }

        if args.write:
            path.write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")))

        total += len(normalized)
        all_seen[dataset_id] = {
            "count": len(normalized),
            "names": {normalize_text(f["properties"]["municipio"]) for f in normalized},
            "size": path.stat().st_size,
        }

        if path.stat().st_size >= 25 * 1024 * 1024:
            raise SystemExit(f"ERROR: {path} supera 25 MiB")

        print(f"OK {dataset_id}: {len(normalized)} municipios · {path.stat().st_size / 1024 / 1024:.2f} MiB")

    for dataset_id, municipio in CRITICAL_CHECKS:
        if dataset_id not in all_seen:
            continue
        target = normalize_text(municipio)
        names = all_seen[dataset_id]["names"]
        if target not in names:
            close = [name for name in names if target[:8] in name or name[:8] in target][:10]
            raise SystemExit(
                f"ERROR: no encuentro municipio crítico {municipio!r} en {dataset_id}. Parecidos={close}"
            )

    print(f"OK audit total: {len(files)} datasets · {total} municipios normalizados")

if __name__ == "__main__":
    main()
