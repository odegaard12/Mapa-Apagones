#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

csv.field_size_limit(sys.maxsize)

NATIONAL_QUEUE = Path("docs/audit/national_distributor_next_wave_queue_v1081.csv")
OUT_QUEUE = Path("docs/audit/clm_wave2_review_queue.csv")
OUT_REGISTRY = Path("docs/audit/clm_wave2_source_registry.csv")
OUT_REPORT = Path("docs/audit/clm-wave2-source-audit.md")

EXPECTED_CLM = 919 # INE oficial Castilla-La Mancha (Albacete, C.Real, Cuenca, Guadalajara, Toledo)

SOURCE_REGISTRY = [
    {
        "source_id": "ufd_clm_official",
        "source_name": "UFD (Grupo Naturgy) — Mapa de red CLM",
        "source_url": "https://www.ufd.es/quienes-somos/nuestra-red/",
        "source_type": "official_operator",
        "scope": "regional_clm",
        "candidate_distributor": "UFD Distribución Electricidad, S.A.",
        "evidence_strength": "regional_presence_only",
        "municipal_import_eligible": "no",
        "review_status": "reviewed_context",
        "notes": "Fuerte presencia histórica regional (Unión Fenosa), requiere verificación municipal por DOCM."
    },
    {
        "source_id": "ide_clm_official",
        "source_name": "i-DE (Iberdrola) — Zonas de distribución",
        "source_url": "https://www.i-de.es/conocenos/nuestra-red",
        "source_type": "official_operator",
        "scope": "regional_clm",
        "candidate_distributor": "i-DE Redes Eléctricas Inteligentes, S.A.U.",
        "evidence_strength": "regional_presence_only",
        "municipal_import_eligible": "no",
        "review_status": "reviewed_context",
        "notes": "Presencia histórica (Iberdrola) cruzada con UFD. Requiere verificación explícita."
    },
    {
        "source_id": "docm_clm_official",
        "source_name": "Diario Oficial de Castilla-La Mancha (DOCM)",
        "source_url": "https://docm.castillalamancha.es/",
        "source_type": "official_journal",
        "scope": "regional_clm",
        "candidate_distributor": "",
        "evidence_strength": "official_discovery_source",
        "municipal_import_eligible": "no",
        "review_status": "source_registry",
        "notes": "Fuente primaria exigida para autorizaciones de red municipal en CLM."
    }
]

def clean(value: object) -> str:
    return str(value or "").strip()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))

def load_clm_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv(NATIONAL_QUEUE) if row.get("dataset_id") == "castilla_la_mancha"]
    if not rows:
        raise SystemExit("ERROR: No se encontraron filas de CLM en la cola nacional.")
    if len(rows) != EXPECTED_CLM:
        print(f"WARNING: Filas encontradas ({len(rows)}) difiere del esperado oficial ({EXPECTED_CLM})")
    
    seen = set()
    for row in rows:
        zone_id = clean(row.get("zone_id"))
        if not zone_id: raise SystemExit("ERROR: fila CLM sin zone_id")
        if zone_id in seen: raise SystemExit(f"ERROR: zone_id duplicado={zone_id}")
        seen.add(zone_id)
    return rows

def write_registry() -> None:
    OUT_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with OUT_REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(SOURCE_REGISTRY[0].keys()))
        writer.writeheader()
        writer.writerows(SOURCE_REGISTRY)

def write_queue(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output = []
    for row in rows:
        output.append({
            "dataset_id": "castilla_la_mancha",
            "zone_id": clean(row["zone_id"]),
            "municipality": clean(row.get("municipality")),
            "province": clean(row.get("province")),
            "research_wave": "wave_2",
            "regional_context_candidate": "UFD / i-DE",
            "candidate_distributor": "",
            "evidence_class": "regional_context_only",
            "source_ids": "ufd_clm_official;ide_clm_official",
            "repo_evidence_hits": "0",
            "repo_evidence_files": "",
            "review_status": "needs_municipal_primary_source",
            "import_eligible": "no",
            "review_notes": "Zona dividida. Se exige contraste con DOCM/CNMC antes de publicar."
        })
    output.sort(key=lambda x: (x["province"], x["municipality"], x["zone_id"]))
    
    with OUT_QUEUE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)
    return output

def write_report(rows: list[dict[str, str]]) -> None:
    province_counts = Counter(row["province"] or "unknown" for row in rows)
    lines = [
        "# Castilla-La Mancha distributor source audit wave 2", "",
        "## Summary", "",
        f"- CLM review rows: **{len(rows)}**",
        "- Imported distributor hints: **0**",
        "- Every row remains `import_eligible=no`.", "",
        "## Evidence policy (Strict)", "",
        "- Dual regional presence (UFD / i-DE) prohibits assumptions.",
        "- Municipal imports require reproducible municipal evidence from DOCM.", "",
        "## Rows by province", "", "| Province | Rows |", "|---|---:|"
    ]
    for province, count in sorted(province_counts.items()):
        lines.append(f"| {province} | {count} |")
    
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

def main() -> int:
    rows = load_clm_rows()
    write_registry()
    output = write_queue(rows)
    write_report(output)

    print(f"✅ OK wrote {OUT_REGISTRY}")
    print(f"✅ OK wrote {OUT_QUEUE}")
    print(f"✅ OK wrote {OUT_REPORT}")
    print(f"clm_rows={len(output)}")
    print("imported_hints=0 (Audit Gate Locked - Pending Human Review via DOCM)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
