#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

DATA_DIR = Path("frontend/public/data")
HINTS_PATH = Path("frontend/src/data/distributor_hints.json")

OUT_CSV = Path(
    "docs/audit/national_distributor_next_wave_queue_v1081.csv"
)
OUT_MD = Path(
    "docs/audit/national-distributor-next-wave-v1081.md"
)

TARGETS = {
    "aragon": {
        "label": "Aragón",
        "expected": 734,
        "wave": "wave_1",
    },
    "castilla_la_mancha": {
        "label": "Castilla-La Mancha",
        "expected": 921,
        "wave": "wave_2",
    },
    "catalunya": {
        "label": "Catalunya",
        "expected": 948,
        "wave": "wave_2",
    },
    "castilla_leon": {
        "label": "Castilla y León",
        "expected": 2298,
        "wave": "wave_3",
    },
}

EXPECTED_TOTAL = 4901


def clean(value: object) -> str:
    return str(value or "").strip()


def first(props: dict[str, Any], names: list[str]) -> str:
    for name in names:
        value = clean(props.get(name))
        if value:
            return value
    return ""


def discover_geo_files() -> dict[str, Path]:
    found: dict[str, Path] = {}

    for path in DATA_DIR.glob("*_municipios.geojson"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        features = data.get("features", [])
        if not features:
            continue

        props = features[0].get("properties", {})
        dataset_id = clean(props.get("dataset_id"))

        if dataset_id in TARGETS:
            if dataset_id in found:
                raise SystemExit(
                    f"ERROR: GeoJSON duplicado para {dataset_id}: "
                    f"{found[dataset_id]} y {path}"
                )
            found[dataset_id] = path

    missing = sorted(set(TARGETS) - set(found))
    if missing:
        raise SystemExit(
            f"ERROR: faltan GeoJSON de datasets objetivo: {missing}"
        )

    return found


def main() -> int:
    geo_files = discover_geo_files()

    hints = json.loads(HINTS_PATH.read_text(encoding="utf-8"))
    existing = [
        item
        for item in hints.get("items", [])
        if item.get("dataset_id") in TARGETS
    ]

    if existing:
        raise SystemExit(
            "ERROR: algún dataset objetivo ya tiene hints públicos; "
            f"items encontrados={len(existing)}"
        )

    rows: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    seen: set[tuple[str, str]] = set()

    for dataset_id, config in TARGETS.items():
        path = geo_files[dataset_id]
        data = json.loads(path.read_text(encoding="utf-8"))
        features = data.get("features", [])

        if len(features) != config["expected"]:
            raise SystemExit(
                f"ERROR {dataset_id}: features={len(features)}, "
                f"expected={config['expected']}"
            )

        for feature in features:
            props = feature.get("properties", {})
            if not isinstance(props, dict):
                raise SystemExit(
                    f"ERROR {dataset_id}: properties inválidas"
                )

            actual_dataset = clean(props.get("dataset_id"))
            if actual_dataset != dataset_id:
                raise SystemExit(
                    f"ERROR dataset_id={actual_dataset!r}, "
                    f"expected={dataset_id!r}"
                )

            zone_id = first(
                props,
                ["zone_id", "municipio", "mun_code", "ine", "id"],
            )
            municipality = first(
                props,
                [
                    "mun_name",
                    "municipality",
                    "name",
                    "nombre",
                    "municipio",
                ],
            )
            province = first(
                props,
                ["prov_name", "province", "provincia"],
            )

            if not zone_id:
                raise SystemExit(
                    f"ERROR {dataset_id}: feature sin zone_id"
                )

            key = (dataset_id, zone_id)
            if key in seen:
                raise SystemExit(
                    f"ERROR zone duplicada: {dataset_id}/{zone_id}"
                )

            seen.add(key)
            counts[dataset_id] += 1

            rows.append({
                "dataset_id": dataset_id,
                "community": config["label"],
                "zone_id": zone_id,
                "municipality": municipality,
                "province": province,
                "research_wave": config["wave"],
                "review_status": "pending_public_source_review",
                "candidate_distributor": "",
                "candidate_confidence": "",
                "source_url": "",
                "evidence_notes": "",
            })

    if len(rows) != EXPECTED_TOTAL:
        raise SystemExit(
            f"ERROR total={len(rows)}, expected={EXPECTED_TOTAL}"
        )

    rows.sort(
        key=lambda row: (
            row["research_wave"],
            row["community"],
            row["province"],
            row["municipality"],
            row["zone_id"],
        )
    )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# National distributor next-wave queue v0.10.8.1",
        "",
        "## Summary",
        "",
        f"- Pending public-source review rows: **{len(rows)}**",
        "- No distributor hints are imported.",
        "- Candidate and source fields remain empty.",
        "",
        "## Queue by community",
        "",
        "| Community | Dataset | Rows | Research wave |",
        "|---|---|---:|---|",
    ]

    for dataset_id, config in TARGETS.items():
        lines.append(
            f"| {config['label']} | `{dataset_id}` | "
            f"{counts[dataset_id]} | `{config['wave']}` |"
        )

    lines.extend([
        "",
        "## Research rules",
        "",
        "- Review reproducible public sources before assigning candidates.",
        "- Import only source-backed municipal or partial evidence.",
        "- Use `verified_partial`; never infer exclusivity.",
        "- Never prefill distributor names without reviewed evidence.",
        "- Do not publish CUPS, addresses, exact coordinates or grid geometry.",
        "",
    ])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK wrote {OUT_CSV}")
    print(f"OK wrote {OUT_MD}")
    print(f"rows={len(rows)}")
    print("counts=", dict(counts))
    print(
        "geo_files=",
        {key: str(value) for key, value in geo_files.items()},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
