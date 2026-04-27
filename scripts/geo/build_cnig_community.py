#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

MUNICIPIO_KEYS = [
    "municipio", "mun_name", "mun_name_local", "nombre", "name",
    "nameunit", "NAMEUNIT", "NOMBRE", "NOM_MUN", "MUNICIPIO",
]
PROVINCE_KEYS = [
    "province", "prov_name", "provincia", "NPRO", "PROVINCIA", "Provincia",
]
CODE_KEYS_TO_KEEP = [
    "mun_code", "prov_code", "mun_area_code", "codnut1", "codnut2", "codnut3",
    "acom_code", "acom_name", "ine_code", "source_zone_id",
]


def slugify(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def first_non_empty(props: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        value = props.get(key)
        if value is not None and str(value).strip():
            return value
    return None


def parse_where(values: list[str]) -> list[tuple[str, str]]:
    filters: list[tuple[str, str]] = []
    for item in values:
        if "=" not in item:
            raise SystemExit(f"Filtro invalido: {item!r}. Usa KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise SystemExit(f"Filtro invalido: {item!r}. Falta KEY.")
        filters.append((key, value))
    return filters


def matches_filters(props: dict[str, Any], filters: list[tuple[str, str]]) -> bool:
    return all(str(props.get(key)).strip() == expected for key, expected in filters)


def normalize_feature(feature: dict[str, Any], dataset_id: str, province_arg: str | None) -> dict[str, Any]:
    props = feature.get("properties") or {}
    municipio = first_non_empty(props, MUNICIPIO_KEYS)
    province = province_arg or first_non_empty(props, PROVINCE_KEYS)

    if not municipio:
        raise ValueError(f"Feature sin municipio reconocible. Properties={props}")
    if not province:
        raise ValueError(f"Feature sin provincia reconocible. Usa --province. Properties={props}")

    municipio = str(municipio).strip()
    province = str(province).strip()
    source_zone_id = props.get("zone_id") or props.get("id") or props.get("ID")
    zone_id = f"municipality:{slugify(province)}::{slugify(municipio)}"

    out_props: dict[str, Any] = {
        "dataset_id": dataset_id,
        "zone_id": zone_id,
        "municipio": municipio,
        "province": province,
        "display_name": f"{municipio} · {province}",
    }

    if source_zone_id and str(source_zone_id) != zone_id:
        out_props["source_zone_id"] = str(source_zone_id)

    for key in CODE_KEYS_TO_KEEP:
        if key in props and key not in out_props and props.get(key) not in (None, ""):
            out_props[key] = props.get(key)

    return {
        "type": "Feature",
        "properties": out_props,
        "geometry": feature.get("geometry"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normaliza GeoJSON municipal CNIG para Apagones Web.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--province")
    parser.add_argument("--where", action="append", default=[])
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    filters = parse_where(args.where)

    source = json.loads(input_path.read_text(encoding="utf-8"))
    features = source.get("features")
    if source.get("type") != "FeatureCollection" or not isinstance(features, list):
        raise SystemExit("Input no parece un FeatureCollection GeoJSON valido.")

    selected = [f for f in features if matches_filters(f.get("properties") or {}, filters)]
    if not selected:
        raise SystemExit(f"No se selecciono ninguna feature para {args.label}. Revisa --where.")

    normalized = [normalize_feature(f, args.dataset_id, args.province) for f in selected]
    normalized.sort(key=lambda f: (slugify(f["properties"]["province"]), slugify(f["properties"]["municipio"])))

    output = {"type": "FeatureCollection", "features": normalized}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(output, ensure_ascii=False, indent=2 if args.pretty else None)
    if not args.pretty:
        text = json.dumps(output, ensure_ascii=False, separators=(",", ":"))
    output_path.write_text(text + "\n", encoding="utf-8")

    print(f"OK: {args.label}")
    print(f"input: {input_path}")
    print(f"output: {output_path}")
    print(f"features_source: {len(features)}")
    print(f"features_selected: {len(selected)}")
    print(f"features_written: {len(normalized)}")
    print(f"dataset_id: {args.dataset_id}")
    print("sample_properties:")
    for key, value in sorted(normalized[0]["properties"].items()):
        print(f"  {key}: {value!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
