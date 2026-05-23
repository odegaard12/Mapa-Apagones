#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

GEO_PATH = Path("frontend/public/data/andalucia_municipios.geojson")
HINTS_PATH = Path("frontend/src/data/distributor_hints.json")
CSV_PATH = Path("docs/audit/andalucia_pending_review_queue_v1072.csv")

EXPECTED_GEO_FEATURES = 786
EXPECTED_COVERED = 254
EXPECTED_PENDING = 532


def clean(value: object) -> str:
    return str(value or "").strip()


def first_prop(props: dict, names: list[str]) -> str:
    for name in names:
        value = clean(props.get(name))
        if value:
            return value
    return ""


def main() -> int:
    geo = json.loads(GEO_PATH.read_text(encoding="utf-8"))
    features = geo.get("features", [])
    if len(features) != EXPECTED_GEO_FEATURES:
        raise SystemExit(f"ERROR geo features={len(features)} expected={EXPECTED_GEO_FEATURES}")

    geo_zone_ids = set()
    for feature in features:
        props = feature.get("properties", {})
        if clean(props.get("dataset_id")) != "andalucia":
            raise SystemExit("ERROR non-andalucia feature in Andalucía GeoJSON")
        zone_id = first_prop(props, ["zone_id", "municipio", "mun_code", "ine", "id"])
        if not zone_id:
            raise SystemExit("ERROR feature without zone_id")
        geo_zone_ids.add(zone_id)

    hints = json.loads(HINTS_PATH.read_text(encoding="utf-8"))
    covered = set()
    for item in hints.get("items", []):
        if item.get("dataset_id") != "andalucia":
            continue
        zone_id = first_prop(item, ["zone_id", "municipio", "mun_code", "ine", "id", "name"])
        if not zone_id:
            raise SystemExit("ERROR Andalucía hint without zone_id")
        covered.add(zone_id)

    if len(covered) != EXPECTED_COVERED:
        raise SystemExit(f"ERROR covered={len(covered)} expected={EXPECTED_COVERED}")

    with CSV_PATH.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if len(rows) != EXPECTED_PENDING:
        raise SystemExit(f"ERROR queue rows={len(rows)} expected={EXPECTED_PENDING}")

    queue_zone_ids = set()
    for row in rows:
        zone_id = clean(row.get("zone_id"))
        if not zone_id:
            raise SystemExit(f"ERROR row without zone_id: {row}")
        if zone_id in queue_zone_ids:
            raise SystemExit(f"ERROR duplicated queue zone_id={zone_id}")
        if zone_id not in geo_zone_ids:
            raise SystemExit(f"ERROR queue zone_id not in geo={zone_id}")
        if zone_id in covered:
            raise SystemExit(f"ERROR queue zone_id already covered={zone_id}")
        if row.get("review_status") != "pending_municipal_review":
            raise SystemExit(f"ERROR invalid review_status for {zone_id}")
        if row.get("candidate_distributor") or row.get("source_url"):
            raise SystemExit(f"ERROR queue must not pre-fill source/distributor for {zone_id}")

        forbidden_columns = {
            "cups",
            "token",
            "password",
            "secret",
            "private_key",
            "api_key",
            "authorization",
            "lat",
            "latitude",
            "lon",
            "longitude",
            "coord",
            "coordinates",
            "address",
            "direccion",
            "dirección",
        }

        for key in row:
            key_l = str(key).lower()
            if key_l in forbidden_columns:
                raise SystemExit(f"ERROR forbidden sensitive column {key!r} in row {zone_id}")

        joined = " ".join(str(v or "") for v in row.values()).lower()
        for marker in ["cups", "token", "password", "secret", "private_key", "api_key", "authorization"]:
            if marker in joined:
                raise SystemExit(f"ERROR forbidden marker {marker!r} in row {zone_id}")

        queue_zone_ids.add(zone_id)

    if len(covered | queue_zone_ids) != EXPECTED_GEO_FEATURES:
        raise SystemExit(
            f"ERROR coverage mismatch covered+queue={len(covered | queue_zone_ids)} "
            f"expected={EXPECTED_GEO_FEATURES}"
        )

    print("OK Andalucía pending review queue")
    print(f"geo_features={len(features)}")
    print(f"covered={len(covered)}")
    print(f"pending={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
