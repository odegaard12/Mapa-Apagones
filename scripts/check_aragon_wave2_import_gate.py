#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

MATRIX = Path("docs/audit/aragon_wave2_candidate_matrix_v1083.csv")

PRIMARY_STAGES = {
    "primary_operator_exact",
    "official_regulator_exact",
    "official_journal_exact",
}


def main() -> int:
    with MATRIX.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    eligible = []

    for row in rows:
        allowed = (
            row.get("candidate_stage") in PRIMARY_STAGES
            and int(row.get("primary_exact_sources") or 0) >= 1
            and row.get("municipality_exact") == "yes"
            and row.get("legal_entity_confirmed") == "yes"
            and row.get("review_decision") == "approved"
        )

        declared = row.get("import_eligible") == "yes"

        if declared != allowed:
            raise SystemExit(
                "ERROR import gate inconsistente en "
                f"{row.get('zone_id')}: "
                f"declared={declared} allowed={allowed}"
            )

        if declared:
            eligible.append(row)

    if eligible:
        print("OK Aragón import gate")
        print(f"eligible={len(eligible)}")
    else:
        print("OK Aragón import gate cerrado")
        print("eligible=0")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
