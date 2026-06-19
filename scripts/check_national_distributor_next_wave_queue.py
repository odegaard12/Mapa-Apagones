#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

CSV_PATH = Path(
    "docs/audit/national_distributor_next_wave_queue_v1081.csv"
)

EXPECTED = {
    "aragon": 734,
    "castilla_la_mancha": 921,
    "catalunya": 948,
    "castilla_leon": 2298,
}


def main() -> int:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if len(rows) != 4901:
        raise SystemExit(
            f"ERROR rows={len(rows)}, expected=4901"
        )

    seen: set[tuple[str, str]] = set()
    counts: Counter[str] = Counter()

    for row in rows:
        dataset_id = row.get("dataset_id", "")
        zone_id = row.get("zone_id", "")

        if dataset_id not in EXPECTED:
            raise SystemExit(
                f"ERROR dataset inesperado={dataset_id}"
            )
        if not zone_id:
            raise SystemExit("ERROR fila sin zone_id")

        key = (dataset_id, zone_id)
        if key in seen:
            raise SystemExit(
                f"ERROR zona duplicada={dataset_id}/{zone_id}"
            )

        if row.get("review_status") != \
                "pending_public_source_review":
            raise SystemExit(
                f"ERROR status inválido={dataset_id}/{zone_id}"
            )

        for field in [
            "candidate_distributor",
            "candidate_confidence",
            "source_url",
            "evidence_notes",
        ]:
            if row.get(field):
                raise SystemExit(
                    f"ERROR campo {field} prellenado en "
                    f"{dataset_id}/{zone_id}"
                )

        joined = " ".join(
            str(value or "") for value in row.values()
        ).lower()

        for marker in [
            "cups",
            "password",
            "private_key",
            "api_key",
            "authorization",
        ]:
            if marker in joined:
                raise SystemExit(
                    f"ERROR marcador prohibido={marker} "
                    f"en {dataset_id}/{zone_id}"
                )

        seen.add(key)
        counts[dataset_id] += 1

    if dict(counts) != EXPECTED:
        raise SystemExit(
            f"ERROR counts={dict(counts)}, expected={EXPECTED}"
        )

    print("OK national distributor next-wave queue")
    print(f"rows={len(rows)}")
    print("counts=", dict(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
