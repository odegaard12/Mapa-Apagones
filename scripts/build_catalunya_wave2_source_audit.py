#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

csv.field_size_limit(sys.maxsize)

NATIONAL_QUEUE = Path("docs/audit/national_distributor_next_wave_queue_v1081.csv")
OUT_QUEUE = Path("docs/audit/catalunya_wave2_review_queue.csv")
OUT_REGISTRY = Path("docs/audit/catalunya_wave2_source_registry.csv")
OUT_REPORT = Path("docs/audit/catalunya-wave2-source-audit.md")

EXPECTED_CATALUNYA = 947 # Catalunya tiene 947 municipios

SOURCE_REGISTRY = [
    {
        "source_id": "edistribucion_catalunya_official",
        "source_name": "e-distribución — Nuestro negocio (Catalunya)",
        "source_url": "https://www.edistribucion.com/es/conocenos/nuestro-negocio.html",
        "source_type": "official_operator",
        "scope": "regional_catalunya",
        "candidate_distributor": "E-Distribución Redes Digitales, S.L.U.",
        "evidence_strength": "regional_presence_only",
        "municipal_import_eligible": "no",
        "review_status": "reviewed_context",
        "notes": "La fuente oficial declara actividad mayoritaria en Catalunya, pero no aporta matriz municipal reproducible."
    },
    {
        "source_id": "cnmc_energy_official",
        "source_name": "CNMC — Energía",
        "source_url": "https://www.cnmc.es/sectores-que-regulamos/energia",
        "source_type": "official_regulator",
        "scope": "national",
        "candidate_distributor": "",
        "evidence_strength": "regulatory_discovery_source",
        "municipal_import_eligible": "no",
        "review_status": "source_registry",
        "notes": "Portal regulatorio nacional."
    },
    {
        "source_id": "dogc_catalunya_official",
        "source_name": "Diari Oficial de la Generalitat de Catalunya (DOGC)",
        "source_url": "https://dogc.gencat.cat/",
        "source_type": "official_journal",
        "scope": "regional_catalunya",
        "candidate_distributor": "",
        "evidence_strength": "official_discovery_source",
        "municipal_import_eligible": "no",
        "review_status": "source_registry",
        "notes": "Fuente primaria para concesiones y autorizaciones de red municipal en Catalunya."
    }
]

def norm(value: object) -> str:
    text = str(value or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text)).strip()

def clean(value: object) -> str:
    return str(value or "").strip()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))

def load_catalunya_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv(NATIONAL_QUEUE) if row.get("dataset_id") == "catalunya"]
    if not rows:
        raise SystemExit("ERROR: No se encontraron filas de Catalunya en la cola nacional.")
    if len(rows) != EXPECTED_CATALUNYA:
        print(f"WARNING: Filas encontradas ({len(rows)}) difiere del esperado ({EXPECTED_CATALUNYA})")
    
    seen = set()
    for row in rows:
        zone_id = clean(row.get("zone_id"))
        if not zone_id:
            raise SystemExit("ERROR: fila Catalunya sin zone_id")
        if zone_id in seen:
            raise SystemExit(f"ERROR: zone_id Catalunya duplicado={zone_id}")
        seen.add(zone_id)
    return rows

def discover_repo_evidence(rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    by_zone = {clean(row["zone_id"]): row for row in rows}
    evidence = {zone_id: {"files": set(), "hits": 0} for zone_id in by_zone}
    # Simulamos el descubrimiento de evidencia cruzando con docs/research (simplificado para el setup)
    roots = [Path("docs/research"), Path("docs/audit")]
    for root in roots:
        if not root.exists(): continue
        for path in root.rglob("*.csv"):
            if "catalunya" in str(path).lower():
                # Lógica de match real iría aquí. Añadimos hits dummy si el archivo coincide.
                pass
    return evidence

def write_registry() -> None:
    OUT_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with OUT_REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(SOURCE_REGISTRY[0].keys()))
        writer.writeheader()
        writer.writerows(SOURCE_REGISTRY)

def write_queue(rows: list[dict[str, str]], evidence: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    output = []
    for row in rows:
        zone_id = clean(row["zone_id"])
        repo = evidence[zone_id]
        
        output.append({
            "dataset_id": "catalunya",
            "zone_id": zone_id,
            "municipality": clean(row.get("municipality")),
            "province": clean(row.get("province")),
            "research_wave": "wave_2",
            "regional_context_candidate": "E-Distribución Redes Digitales, S.L.U.",
            "candidate_distributor": "",
            "evidence_class": "regional_context_only",
            "source_ids": "edistribucion_catalunya_official",
            "repo_evidence_hits": str(repo["hits"]),
            "repo_evidence_files": ";".join(repo["files"]),
            "review_status": "needs_municipal_primary_source",
            "import_eligible": "no",
            "review_notes": "Presencia regional fuerte. Requiere confirmación municipal (DOGC o similar) para importar."
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
        "# Catalunya distributor source audit wave 2", "",
        "## Summary", "",
        f"- Catalunya review rows: **{len(rows)}**",
        "- Imported distributor hints: **0**",
        "- Every row remains `import_eligible=no`.", "",
        "## Evidence policy", "",
        "- Regional operator presence is context only.",
        "- Municipal imports require reproducible municipal evidence from DOGC or CNMC.", "",
        "## Rows by province", "", "| Province | Rows |", "|---|---:|"
    ]
    for province, count in sorted(province_counts.items()):
        lines.append(f"| {province} | {count} |")
    
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

def main() -> int:
    rows = load_catalunya_rows()
    evidence = discover_repo_evidence(rows)
    write_registry()
    output = write_queue(rows, evidence)
    write_report(output)

    print(f"✅ OK wrote {OUT_REGISTRY}")
    print(f"✅ OK wrote {OUT_QUEUE}")
    print(f"✅ OK wrote {OUT_REPORT}")
    print(f"catalunya_rows={len(output)}")
    print("imported_hints=0 (Audit Gate Locked - Pending Human Review)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
