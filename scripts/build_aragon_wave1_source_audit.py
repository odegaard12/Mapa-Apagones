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

NATIONAL_QUEUE = Path(
    "docs/audit/national_distributor_next_wave_queue_v1081.csv"
)

OUT_QUEUE = Path(
    "docs/audit/aragon_wave1_review_queue_v1082.csv"
)
OUT_REGISTRY = Path(
    "docs/audit/aragon_wave1_source_registry_v1082.csv"
)
OUT_REPORT = Path(
    "docs/audit/aragon-wave1-source-audit-v1082.md"
)

EXPECTED_ARAGON = 734

SOURCE_REGISTRY = [
    {
        "source_id": "edistribucion_aragon_official",
        "source_name": "e-distribución — Nuestro negocio",
        "source_url": (
            "https://www.edistribucion.com/es/conocenos/"
            "nuestro-negocio.html"
        ),
        "source_type": "official_operator",
        "scope": "regional_aragon",
        "candidate_distributor": (
            "E-Distribución Redes Digitales, S.L.U."
        ),
        "evidence_strength": "regional_presence_only",
        "municipal_import_eligible": "no",
        "review_status": "reviewed_context",
        "notes": (
            "La fuente oficial declara actividad en Aragón, "
            "pero no aporta una matriz municipal reproducible."
        ),
    },
    {
        "source_id": "cnmc_energy_official",
        "source_name": "CNMC — Energía",
        "source_url": (
            "https://www.cnmc.es/sectores-que-regulamos/energia"
        ),
        "source_type": "official_regulator",
        "scope": "national",
        "candidate_distributor": "",
        "evidence_strength": "regulatory_discovery_source",
        "municipal_import_eligible": "no",
        "review_status": "source_registry",
        "notes": (
            "Portal regulatorio para localizar estadísticas, "
            "resoluciones y documentación pública reproducible."
        ),
    },
    {
        "source_id": "boa_aragon_official",
        "source_name": "Boletín Oficial de Aragón",
        "source_url": "https://www.boa.aragon.es/",
        "source_type": "official_journal",
        "scope": "regional_aragon",
        "candidate_distributor": "",
        "evidence_strength": "official_discovery_source",
        "municipal_import_eligible": "no",
        "review_status": "source_registry",
        "notes": (
            "Fuente para buscar autorizaciones, concesiones, "
            "instalaciones y anuncios con ámbito municipal."
        ),
    },
    {
        "source_id": "abenergia_barbastro_secondary_2026",
        "source_name": (
            "Referencia pública sobre red de distribución "
            "de AB Energía en Barbastro"
        ),
        "source_url": (
            "https://cadenaser.com/aragon/2026/02/12/"
            "ab-energia-se-consolida-como-referente-de-la-"
            "transicion-energetica-en-aragon-ser-aragon-oriental/"
        ),
        "source_type": "secondary_media",
        "scope": "municipality_barbastro",
        "candidate_distributor": (
            "AB Energía — división de distribución de Barbastro"
        ),
        "evidence_strength": "secondary_public_claim",
        "municipal_import_eligible": "no",
        "review_status": "needs_primary_confirmation",
        "notes": (
            "Indicio municipal útil, pero antes de importar debe "
            "confirmarse la entidad jurídica y el ámbito mediante "
            "fuente oficial o del propio operador."
        ),
    },
]


def norm(value: object) -> str:
    text = str(value or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        errors="ignore",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def load_aragon_rows() -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(NATIONAL_QUEUE)
        if row.get("dataset_id") == "aragon"
    ]

    if len(rows) != EXPECTED_ARAGON:
        raise SystemExit(
            f"ERROR Aragón rows={len(rows)}, "
            f"expected={EXPECTED_ARAGON}"
        )

    seen: set[str] = set()

    for row in rows:
        zone_id = clean(row.get("zone_id"))
        if not zone_id:
            raise SystemExit("ERROR: fila Aragón sin zone_id")
        if zone_id in seen:
            raise SystemExit(
                f"ERROR: zone_id Aragón duplicado={zone_id}"
            )
        seen.add(zone_id)

    return rows


def discover_repo_evidence(
    aragon_rows: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    by_zone = {
        clean(row["zone_id"]): row
        for row in aragon_rows
    }

    by_name_province: dict[
        tuple[str, str],
        list[dict[str, str]],
    ] = defaultdict(list)

    for row in aragon_rows:
        key = (
            norm(row.get("municipality")),
            norm(row.get("province")),
        )
        if key[0]:
            by_name_province[key].append(row)

    evidence: dict[str, dict[str, Any]] = {
        zone_id: {
            "files": set(),
            "hits": 0,
        }
        for zone_id in by_zone
    }

    excluded = {
        NATIONAL_QUEUE.resolve(),
        OUT_QUEUE.resolve(),
        OUT_REGISTRY.resolve(),
    }

    roots = [
        Path("docs/research"),
        Path("docs/audit"),
    ]

    for root in roots:
        if not root.exists():
            continue

        for path in root.rglob("*.csv"):
            try:
                resolved = path.resolve()
            except OSError:
                continue

            if resolved in excluded:
                continue

            try:
                rows = read_csv(path)
            except Exception:
                continue

            for source_row in rows:
                dataset_id = clean(
                    source_row.get("dataset_id")
                )
                zone_id = clean(source_row.get("zone_id"))

                matched_zone = ""

                if zone_id in by_zone:
                    matched_zone = zone_id
                elif dataset_id == "aragon":
                    municipality = norm(
                        source_row.get("municipality")
                        or source_row.get("mun_name")
                        or source_row.get("name")
                    )
                    province = norm(
                        source_row.get("province")
                        or source_row.get("prov_name")
                    )

                    matches = by_name_province.get(
                        (municipality, province),
                        [],
                    )

                    if len(matches) == 1:
                        matched_zone = clean(
                            matches[0]["zone_id"]
                        )

                if not matched_zone:
                    continue

                evidence[matched_zone]["hits"] += 1
                evidence[matched_zone]["files"].add(
                    str(path)
                )

    return evidence


def write_registry() -> None:
    OUT_REGISTRY.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUT_REGISTRY.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(SOURCE_REGISTRY[0].keys()),
        )
        writer.writeheader()
        writer.writerows(SOURCE_REGISTRY)


def write_queue(
    aragon_rows: list[dict[str, str]],
    evidence: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []

    for row in aragon_rows:
        zone_id = clean(row["zone_id"])
        municipality = clean(row.get("municipality"))
        municipality_norm = norm(municipality)

        source_ids = "edistribucion_aragon_official"
        evidence_class = "regional_context_only"
        candidate_distributor = ""
        review_status = "needs_municipal_primary_source"
        review_notes = (
            "La presencia regional de e-distribución no prueba "
            "la distribuidora concreta de este municipio."
        )

        if municipality_norm == "barbastro":
            source_ids += (
                ";abenergia_barbastro_secondary_2026"
            )
            evidence_class = "secondary_municipal_evidence"
            candidate_distributor = (
                "AB Energía — división de distribución "
                "de Barbastro"
            )
            review_status = "needs_primary_operator_confirmation"
            review_notes = (
                "Existe un indicio público municipal. Confirmar "
                "entidad jurídica y ámbito exacto con fuente "
                "oficial antes de cualquier importación."
            )

        repo = evidence[zone_id]
        repo_files = sorted(repo["files"])

        output.append({
            "dataset_id": "aragon",
            "zone_id": zone_id,
            "municipality": municipality,
            "province": clean(row.get("province")),
            "research_wave": "wave_1",
            "regional_context_candidate": (
                "E-Distribución Redes Digitales, S.L.U."
            ),
            "candidate_distributor": candidate_distributor,
            "evidence_class": evidence_class,
            "source_ids": source_ids,
            "repo_evidence_hits": str(repo["hits"]),
            "repo_evidence_files": ";".join(repo_files),
            "review_status": review_status,
            "import_eligible": "no",
            "review_notes": review_notes,
        })

    output.sort(
        key=lambda row: (
            row["province"],
            row["municipality"],
            row["zone_id"],
        )
    )

    with OUT_QUEUE.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(output[0].keys()),
        )
        writer.writeheader()
        writer.writerows(output)

    return output


def write_report(
    rows: list[dict[str, str]],
) -> None:
    province_counts = Counter(
        row["province"] or "unknown"
        for row in rows
    )
    status_counts = Counter(
        row["review_status"]
        for row in rows
    )
    repo_hit_rows = sum(
        int(row["repo_evidence_hits"]) > 0
        for row in rows
    )

    lines = [
        "# Aragón distributor source audit wave 1 v0.10.8.2",
        "",
        "## Summary",
        "",
        f"- Aragón review rows: **{len(rows)}**",
        f"- Rows with repository-local evidence hits: "
        f"**{repo_hit_rows}**",
        "- Imported distributor hints: **0**",
        "- Every row remains `import_eligible=no`.",
        "",
        "## Evidence policy",
        "",
        "- Regional operator presence is context only.",
        "- Municipal imports require reproducible municipal evidence.",
        "- Secondary media evidence cannot be imported directly.",
        "- Candidate legal entity and geographic scope must be confirmed.",
        "- Future imports must use `verified_partial` and never claim exclusivity.",
        "",
        "## Rows by province",
        "",
        "| Province | Rows |",
        "|---|---:|",
    ]

    for province, count in sorted(
        province_counts.items()
    ):
        lines.append(f"| {province} | {count} |")

    lines.extend([
        "",
        "## Review status",
        "",
        "| Status | Rows |",
        "|---|---:|",
    ])

    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count} |")

    lines.extend([
        "",
        "## Registered public sources",
        "",
        "- Official e-distribución business/scope page.",
        "- CNMC energy portal.",
        "- Boletín Oficial de Aragón.",
        "- Secondary Barbastro reference pending primary confirmation.",
        "",
        "## Safety",
        "",
        "- No CUPS.",
        "- No addresses.",
        "- No exact coordinates.",
        "- No network geometry.",
        "- No raw API responses.",
        "- No customer data.",
        "",
    ])

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> int:
    aragon_rows = load_aragon_rows()
    evidence = discover_repo_evidence(aragon_rows)

    write_registry()
    output = write_queue(aragon_rows, evidence)
    write_report(output)

    barbastro = [
        row for row in output
        if norm(row["municipality"]) == "barbastro"
    ]

    print(f"OK wrote {OUT_REGISTRY}")
    print(f"OK wrote {OUT_QUEUE}")
    print(f"OK wrote {OUT_REPORT}")
    print(f"aragon_rows={len(output)}")
    print(
        "repo_evidence_rows=",
        sum(
            int(row["repo_evidence_hits"]) > 0
            for row in output
        ),
    )
    print(f"barbastro_rows={len(barbastro)}")
    print("imported_hints=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
