#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse

QUEUE = Path(
    "docs/audit/aragon_wave1_review_queue_v1082.csv"
)
REGISTRY = Path(
    "docs/audit/aragon_wave1_source_registry_v1082.csv"
)

EXPECTED_ROWS = 734

ALLOWED_DOMAINS = {
    "www.edistribucion.com",
    "www.cnmc.es",
    "www.boa.aragon.es",
    "cadenaser.com",
}

REQUIRED_SOURCE_IDS = {
    "edistribucion_aragon_official",
    "cnmc_energy_official",
    "boa_aragon_official",
    "abenergia_barbastro_secondary_2026",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    queue = read_csv(QUEUE)
    registry = read_csv(REGISTRY)

    if len(queue) != EXPECTED_ROWS:
        raise SystemExit(
            f"ERROR queue rows={len(queue)}, "
            f"expected={EXPECTED_ROWS}"
        )

    source_ids = {
        row["source_id"]
        for row in registry
    }

    if source_ids != REQUIRED_SOURCE_IDS:
        raise SystemExit(
            f"ERROR source registry IDs={source_ids}"
        )

    for source in registry:
        parsed = urlparse(source["source_url"])

        if parsed.scheme != "https":
            raise SystemExit(
                f"ERROR non-HTTPS source={source['source_id']}"
            )

        if parsed.netloc not in ALLOWED_DOMAINS:
            raise SystemExit(
                f"ERROR unexpected domain={parsed.netloc}"
            )

        if source["municipal_import_eligible"] != "no":
            raise SystemExit(
                f"ERROR source marked importable="
                f"{source['source_id']}"
            )

    seen: set[str] = set()
    barbastro_rows = []

    for row in queue:
        zone_id = row.get("zone_id", "")

        if row.get("dataset_id") != "aragon":
            raise SystemExit(
                f"ERROR non-Aragón row={zone_id}"
            )
        if not zone_id:
            raise SystemExit("ERROR row without zone_id")
        if zone_id in seen:
            raise SystemExit(
                f"ERROR duplicated zone_id={zone_id}"
            )
        if row.get("import_eligible") != "no":
            raise SystemExit(
                f"ERROR importable row={zone_id}"
            )

        source_row_ids = {
            item
            for item in row.get("source_ids", "").split(";")
            if item
        }

        if not source_row_ids <= source_ids:
            raise SystemExit(
                f"ERROR unknown source ID in {zone_id}: "
                f"{source_row_ids - source_ids}"
            )

        if (
            "edistribucion_aragon_official"
            not in source_row_ids
        ):
            raise SystemExit(
                f"ERROR missing regional context={zone_id}"
            )

        municipality = row.get("municipality", "").strip().lower()

        if municipality == "barbastro":
            barbastro_rows.append(row)
            if (
                "abenergia_barbastro_secondary_2026"
                not in source_row_ids
            ):
                raise SystemExit(
                    "ERROR Barbastro missing secondary source"
                )
            if (
                row.get("evidence_class")
                != "secondary_municipal_evidence"
            ):
                raise SystemExit(
                    "ERROR Barbastro evidence class"
                )
            if row.get("import_eligible") != "no":
                raise SystemExit(
                    "ERROR Barbastro must not be importable"
                )
        else:
            if row.get("candidate_distributor"):
                raise SystemExit(
                    f"ERROR prefilled municipal candidate={zone_id}"
                )
            if (
                row.get("evidence_class")
                != "regional_context_only"
            ):
                raise SystemExit(
                    f"ERROR invalid evidence class={zone_id}"
                )

        joined = " ".join(
            str(value or "")
            for value in row.values()
        ).lower()

        for marker in [
            "cups",
            "password",
            "private_key",
            "api_key",
            "authorization",
            "latitude",
            "longitude",
            "coordinates",
            "address",
            "direccion",
            "dirección",
        ]:
            if marker in joined:
                raise SystemExit(
                    f"ERROR forbidden marker={marker} "
                    f"in {zone_id}"
                )

        seen.add(zone_id)

    if len(barbastro_rows) != 1:
        raise SystemExit(
            f"ERROR Barbastro rows={len(barbastro_rows)}"
        )

    print("OK Aragón wave 1 source audit")
    print(f"queue_rows={len(queue)}")
    print(f"registry_sources={len(registry)}")
    print("barbastro_secondary_rows=1")
    print("import_eligible_rows=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
