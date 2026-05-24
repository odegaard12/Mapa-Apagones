#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

PENDING_CSV = Path("docs/audit/andalucia_pending_review_queue_v1072.csv")
WORKBENCH_CSV = Path("docs/audit/andalucia_batch2_candidate_workbench_v1074.csv")

MIN_CANDIDATES = 1


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    pending = read_csv(PENDING_CSV)
    workbench = read_csv(WORKBENCH_CSV)

    pending_zone_ids = {row["zone_id"] for row in pending}

    if len(workbench) < MIN_CANDIDATES:
        raise SystemExit(f"ERROR workbench has too few candidates: {len(workbench)}")

    seen: set[str] = set()

    for row in workbench:
        zone_id = row.get("zone_id", "")

        if not zone_id:
            raise SystemExit("ERROR workbench row without zone_id")
        if zone_id in seen:
            raise SystemExit(f"ERROR duplicated workbench zone_id={zone_id}")
        if zone_id not in pending_zone_ids:
            raise SystemExit(f"ERROR workbench zone_id not in pending queue={zone_id}")

        if row.get("dataset_id") != "andalucia":
            raise SystemExit(f"ERROR non-andalucia row={zone_id}")

        if row.get("candidate_confidence") != "manual_review_required":
            raise SystemExit(f"ERROR candidate_confidence must not be import confidence={zone_id}")

        if row.get("proposed_import_action") != "manual_review_only":
            raise SystemExit(f"ERROR proposed_import_action must be manual_review_only={zone_id}")

        if row.get("candidate_distributor") != "E-Distribución Redes Digitales, S.L.U.":
            raise SystemExit(f"ERROR unexpected candidate distributor={zone_id}")

        score = int(row.get("score") or "0")
        if score < 45:
            raise SystemExit(f"ERROR low score row={zone_id} score={score}")

        joined = " ".join(str(v or "") for v in row.values()).lower()
        for marker in ["cups", "token", "password", "secret", "private_key", "api_key", "authorization"]:
            if marker in joined:
                raise SystemExit(f"ERROR forbidden marker {marker!r} in row={zone_id}")

        seen.add(zone_id)

    print("OK Andalucía batch2 candidate workbench")
    print(f"pending_rows={len(pending)}")
    print(f"candidate_rows={len(workbench)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
