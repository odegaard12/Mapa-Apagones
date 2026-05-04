#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS_JS = ROOT / "frontend/src/geo/datasets.js"
PUBLIC_DATA = ROOT / "frontend/public/data"

EXPECTED_DATASETS = {
    "galicia": "/data/galicia_municipios.geojson",
    "asturias": "/data/asturias_municipios.geojson",
    "cantabria": "/data/cantabria_municipios.geojson",
    "castilla_leon": "/data/castilla_leon_municipios.geojson",
    "aragon": "/data/aragon_municipios.geojson",
    "madrid": "/data/madrid_municipios.geojson",
    "navarra": "/data/navarra_municipios.geojson",
    "la_rioja": "/data/la_rioja_municipios.geojson",
    "murcia": "/data/murcia_municipios.geojson",
    "ceuta": "/data/ceuta_municipios.geojson",
    "melilla": "/data/melilla_municipios.geojson",
    "comunitat_valenciana": "/data/comunitat_valenciana_municipios.geojson",
    "illes_balears": "/data/illes_balears_municipios.geojson",
    "canarias": "/data/canarias_municipios.geojson",
    "euskadi": "/data/euskadi_municipios.geojson",
    "extremadura": "/data/extremadura_municipios.geojson",
    "castilla_la_mancha": "/data/castilla_la_mancha_municipios.geojson",
    "andalucia": "/data/andalucia_municipios.geojson",
    "catalunya": "/data/catalunya_municipios.geojson",
}

REQUIRED_PROPS = {
    "municipio",
    "mun_name",
    "name",
    "province",
    "prov_name",
    "dataset_id",
    "zone_id",
}

KNOWN_ZONE_IDS = {
    "municipality:pontevedra::catoira",
    "municipality:asturias::siero",
    "municipality:madrid::madrid",
    "municipality:caceres::caceres",
    "municipality:sevilla::sevilla",
    "municipality:barcelona::barcelona",
    "municipality:zaragoza::zaragoza",
}

MAX_FILE_BYTES = 24 * 1024 * 1024
MIN_TOTAL_FEATURES = 8200

def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def load_text(path: Path) -> str:
    if not path.exists():
        fail(f"no existe {path}")
    return path.read_text(encoding="utf-8")

def extract_all_scope_paths(text: str) -> set[str]:
    match = re.search(r"municipiosPaths\s*:\s*\[(.*?)\]", text, re.S)
    if not match:
        fail("no encuentro municipiosPaths de Toda España en datasets.js")
    return set(re.findall(r"'([^']+_municipios\.geojson)'", match.group(1)))

def main() -> None:
    text = load_text(DATASETS_JS)

    declared_ids = set(re.findall(r"id:\s*'([^']+)'", text))
    expected_ids = set(EXPECTED_DATASETS)
    missing_ids = sorted(expected_ids - declared_ids)
    if missing_ids:
        fail(f"faltan datasets declarados en GEO_DATASETS: {missing_ids}")

    individual_paths = set(re.findall(r"municipiosPath\s*:\s*'([^']+_municipios\.geojson)'", text))
    expected_paths = set(EXPECTED_DATASETS.values())

    missing_individual_paths = sorted(expected_paths - individual_paths)
    if missing_individual_paths:
        fail(f"faltan municipiosPath individuales: {missing_individual_paths}")

    all_scope_paths = extract_all_scope_paths(text)
    missing_in_all = sorted(expected_paths - all_scope_paths)
    if missing_in_all:
        fail(f"faltan paths en Toda España municipiosPaths: {missing_in_all}")

    extra_in_all = sorted(all_scope_paths - expected_paths)
    if extra_in_all:
        fail(f"Toda España contiene paths no esperados o antiguos: {extra_in_all}")

    total_features = 0
    zone_counter = Counter()
    zone_locations = defaultdict(list)
    seen_known_zone_ids = set()

    for dataset_id, public_path in EXPECTED_DATASETS.items():
        file_path = ROOT / "frontend/public" / public_path.lstrip("/")
        if not file_path.exists():
            fail(f"no existe dataset publicado: {file_path}")

        size = file_path.stat().st_size
        if size > MAX_FILE_BYTES:
            fail(f"{file_path} supera 24 MiB: {size} bytes")

        data = json.loads(file_path.read_text(encoding="utf-8"))
        features = data.get("features") or []
        if not features:
            fail(f"dataset vacío: {file_path}")

        missing_required = Counter()
        wrong_dataset_id = 0

        for idx, feature in enumerate(features):
            props = feature.get("properties") or {}
            for key in REQUIRED_PROPS:
                if props.get(key) in (None, ""):
                    missing_required[key] += 1

            if props.get("dataset_id") != dataset_id:
                wrong_dataset_id += 1

            zone_id = props.get("zone_id")
            if zone_id:
                zone_counter[zone_id] += 1
                zone_locations[zone_id].append((dataset_id, props.get("municipio"), props.get("province")))
                if zone_id in KNOWN_ZONE_IDS:
                    seen_known_zone_ids.add(zone_id)

        if missing_required:
            fail(f"{dataset_id} tiene propiedades requeridas vacías: {dict(missing_required)}")

        if wrong_dataset_id:
            fail(f"{dataset_id} tiene {wrong_dataset_id} features con dataset_id incorrecto")

        total_features += len(features)
        print(f"OK {dataset_id}: {len(features)} municipios · {size / 1024 / 1024:.2f} MiB")

    if total_features < MIN_TOTAL_FEATURES:
        fail(f"total de municipios demasiado bajo: {total_features} < {MIN_TOTAL_FEATURES}")

    missing_known = sorted(KNOWN_ZONE_IDS - seen_known_zone_ids)
    if missing_known:
        fail(f"faltan municipios críticos conocidos: {missing_known}")

    duplicates = {z: c for z, c in zone_counter.items() if c > 1}
    if duplicates:
        print()
        print("WARN duplicados zone_id detectados, revisar si son enclaves/artefactos:")
        for zone_id, count in sorted(duplicates.items()):
            print(f" - {zone_id}: {count} -> {zone_locations[zone_id]}")

    print()
    print(f"OK cobertura España: {len(EXPECTED_DATASETS)} datasets individuales")
    print(f"OK total municipios normalizados: {total_features}")
    print("OK todos los municipiosPath individuales están incluidos en Toda España")
    print("OK guardia de cobertura completa superada")

if __name__ == "__main__":
    main()
