#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

MATRIX = Path("docs/audit/aragon_wave2_candidate_matrix_v1083.csv")
LEDGER = Path("docs/audit/aragon_wave2_evidence_ledger_v1083.csv")
REPORT = Path("docs/audit/aragon-wave2-candidate-gate-v1083.md")
WAVE1_REPORT = Path("docs/audit/aragon-wave1-source-audit-v1082.md")

EXPECTED_ROWS = 734
EXPECTED_SOURCES = 6


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    matrix = read_csv(MATRIX)
    ledger = read_csv(LEDGER)

    if len(matrix) != EXPECTED_ROWS:
        raise SystemExit(
            f"ERROR matrix rows={len(matrix)} expected={EXPECTED_ROWS}"
        )

    if len(ledger) != EXPECTED_SOURCES:
        raise SystemExit(
            f"ERROR ledger rows={len(ledger)} "
            f"expected={EXPECTED_SOURCES}"
        )

    ids = {row["source_id"] for row in ledger}

    if len(ids) != EXPECTED_SOURCES:
        raise SystemExit("ERROR source_id duplicado")

    seen: set[str] = set()
    stages: Counter[str] = Counter()
    barbastro: list[dict[str, str]] = []

    for row in matrix:
        zone_id = row.get("zone_id", "")

        if row.get("dataset_id") != "aragon":
            raise SystemExit(f"ERROR dataset inválido={zone_id}")

        if not zone_id or zone_id in seen:
            raise SystemExit(f"ERROR zone_id inválido={zone_id}")

        seen.add(zone_id)
        stages[row["candidate_stage"]] += 1

        source_ids = {
            item
            for item in row.get("source_ids", "").split(";")
            if item
        }

        if not source_ids <= ids:
            raise SystemExit(
                f"ERROR source desconocida={zone_id}: "
                f"{source_ids - ids}"
            )

        if row.get("import_eligible") != "no":
            raise SystemExit(
                f"ERROR importación prematura={zone_id}"
            )

        if row.get("municipality", "").strip().casefold() == "barbastro":
            barbastro.append(row)

    if stages != Counter({
        "regional_context_only": 733,
        "strong_secondary_candidate": 1,
    }):
        raise SystemExit(f"ERROR stages={dict(stages)}")

    if len(barbastro) != 1:
        raise SystemExit(
            f"ERROR Barbastro rows={len(barbastro)}"
        )

    item = barbastro[0]

    expected = {
        "primary_exact_sources": "0",
        "secondary_exact_sources": "3",
        "independent_source_families": "1",
        "municipality_exact": "yes",
        "legal_entity_confirmed": "no",
        "review_decision": "pending",
        "import_eligible": "no",
    }

    for field, value in expected.items():
        if item.get(field) != value:
            raise SystemExit(
                f"ERROR Barbastro {field}={item.get(field)!r}"
            )

    report = REPORT.read_text(encoding="utf-8")
    wave1 = WAVE1_REPORT.read_text(encoding="utf-8")

    for snippet in [
        "strong_secondary_candidate",
        "Municipios elegibles para importar: **0**",
        "repository-local reference hits",
    ]:
        if snippet not in report:
            raise SystemExit(
                f"ERROR informe wave2 sin: {snippet}"
            )

    if (
        "no constituyen por sí mismos evidencia municipal"
        not in wave1.casefold()
    ):
        raise SystemExit("ERROR wave1 sigue exagerando evidencia")

    for source in ledger:
        parsed = urlparse(source["source_url"])

        if parsed.scheme != "https":
            raise SystemExit(
                f"ERROR fuente no HTTPS={source['source_id']}"
            )

        if source["import_eligible"] != "no":
            raise SystemExit(
                f"ERROR fuente prematuramente importable="
                f"{source['source_id']}"
            )

    print("OK Aragón wave 2 candidate gate")
    print("rows=734")
    print("regional_context_only=733")
    print("strong_secondary_candidate=1")
    print("import_eligible=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
