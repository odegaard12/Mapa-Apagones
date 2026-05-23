#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

GEO_PATH = Path("frontend/public/data/andalucia_municipios.geojson")
HINTS_PATH = Path("frontend/src/data/distributor_hints.json")

OUT_CSV = Path("docs/audit/andalucia_pending_review_queue_v1072.csv")
OUT_MD = Path("docs/audit/andalucia-pending-review-queue-v1072.md")

EXPECTED_GEO_FEATURES = 786
EXPECTED_COVERED = 254
EXPECTED_PENDING = 532


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def clean(value: object) -> str:
    return str(value or "").strip()


def first_prop(props: dict[str, Any], names: list[str]) -> str:
    for name in names:
        value = clean(props.get(name))
        if value:
            return value
    return ""


def load_geo_rows() -> list[dict[str, str]]:
    data = load_json(GEO_PATH)
    features = data.get("features", [])

    if len(features) != EXPECTED_GEO_FEATURES:
        raise SystemExit(
            f"ERROR: Andalucía GeoJSON features={len(features)} "
            f"expected={EXPECTED_GEO_FEATURES}"
        )

    rows: list[dict[str, str]] = []
    seen: set[str] = set()

    for feature in features:
        props = feature.get("properties", {})
        if not isinstance(props, dict):
            raise SystemExit("ERROR: feature sin properties dict")

        dataset_id = clean(props.get("dataset_id"))
        if dataset_id != "andalucia":
            raise SystemExit(f"ERROR: dataset_id inesperado en geo: {dataset_id!r}")

        zone_id = first_prop(
            props,
            ["zone_id", "municipio", "mun_code", "ine", "id"],
        )
        municipality = first_prop(
            props,
            ["mun_name", "municipality", "name", "nombre", "municipio"],
        )
        province = first_prop(
            props,
            ["prov_name", "province", "provincia"],
        )

        if not zone_id:
            raise SystemExit(f"ERROR: feature sin zone_id usable: {props}")
        if zone_id in seen:
            raise SystemExit(f"ERROR: zone_id duplicado en Andalucía GeoJSON: {zone_id}")

        seen.add(zone_id)

        rows.append({
            "dataset_id": "andalucia",
            "zone_id": zone_id,
            "municipality": municipality,
            "province": province,
        })

    return rows


def load_covered_zone_ids() -> set[str]:
    data = load_json(HINTS_PATH)
    covered: set[str] = set()

    for item in data.get("items", []):
        if item.get("dataset_id") != "andalucia":
            continue

        zone_id = first_prop(
            item,
            ["zone_id", "municipio", "mun_code", "ine", "id", "name"],
        )
        if not zone_id:
            raise SystemExit(f"ERROR: hint Andalucía sin zone_id usable: {item}")

        covered.add(zone_id)

    if len(covered) != EXPECTED_COVERED:
        raise SystemExit(
            f"ERROR: Andalucía covered={len(covered)} expected={EXPECTED_COVERED}"
        )

    return covered


def assert_safe_rows(rows: list[dict[str, str]]) -> None:
    # Check generated schema first. Do not substring-match municipality names:
    # e.g. "Benizalón" contains "lon", but it is not a longitude.
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

    for row in rows:
        for key in row:
            key_l = str(key).lower()
            if key_l in forbidden_columns:
                raise SystemExit(
                    f"ERROR: columna sensible {key!r} en fila {row}"
                )

        # Values are allowed to contain normal municipality/province text.
        # Still block high-risk secret/CUPS markers in values.
        joined = " ".join(str(v or "") for v in row.values()).lower()
        for marker in ["cups", "token", "password", "secret", "private_key", "api_key", "authorization"]:
            if marker in joined:
                raise SystemExit(
                    f"ERROR: marcador sensible {marker!r} en fila {row}"
                )


def main() -> int:
    geo_rows = load_geo_rows()
    covered = load_covered_zone_ids()

    pending_rows = []
    for row in sorted(geo_rows, key=lambda r: (r["province"], r["municipality"], r["zone_id"])):
        if row["zone_id"] in covered:
            continue

        pending_rows.append({
            "dataset_id": row["dataset_id"],
            "zone_id": row["zone_id"],
            "municipality": row["municipality"],
            "province": row["province"],
            "review_status": "pending_municipal_review",
            "candidate_distributor": "",
            "candidate_confidence": "",
            "source_url": "",
            "source_label": "",
            "review_notes": "",
        })

    if len(pending_rows) != EXPECTED_PENDING:
        raise SystemExit(
            f"ERROR: pending={len(pending_rows)} expected={EXPECTED_PENDING} "
            f"geo={len(geo_rows)} covered={len(covered)}"
        )

    assert_safe_rows(pending_rows)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(pending_rows[0].keys()))
        writer.writeheader()
        writer.writerows(pending_rows)

    province_counts = Counter(row["province"] or "unknown" for row in pending_rows)

    lines = []
    lines.append("# Andalucía pending distributor review queue v0.10.7.2")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Andalucía municipal GeoJSON features: **{len(geo_rows)}**")
    lines.append(f"- Already covered by distributor hints: **{len(covered)}**")
    lines.append(f"- Pending municipal review rows: **{len(pending_rows)}**")
    lines.append(f"- CSV: `{OUT_CSV}`")
    lines.append("")
    lines.append("## Pending rows by province")
    lines.append("")
    lines.append("| province | pending rows |")
    lines.append("|---|---:|")
    for province, count in sorted(province_counts.items()):
        lines.append(f"| {province} | {count} |")
    lines.append("")
    lines.append("## Intended use")
    lines.append("")
    lines.append("This queue is a sanitized working list for future Andalucía distributor research.")
    lines.append("")
    lines.append("It does not import new distributor hints.")
    lines.append("")
    lines.append("Future imports must only promote rows from this queue when there is")
    lines.append("strong public, source-backed evidence for a `verified_partial` hint.")
    lines.append("")
    lines.append("## Safety constraints")
    lines.append("")
    lines.append("- No CUPS.")
    lines.append("- No addresses.")
    lines.append("- No exact coordinates.")
    lines.append("- No customer data.")
    lines.append("- No private grid inventory.")
    lines.append("- No raw external API responses.")
    lines.append("- No unsupported exclusivity claims.")
    lines.append("- No Red Eléctrica distributor hint.")
    lines.append("- No generic `Pequeña distribuidora` placeholder.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK wrote {OUT_CSV}")
    print(f"OK wrote {OUT_MD}")
    print(f"andalucia_geo_features={len(geo_rows)}")
    print(f"andalucia_covered={len(covered)}")
    print(f"andalucia_pending={len(pending_rows)}")
    print("pending_by_province=", dict(sorted(province_counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
