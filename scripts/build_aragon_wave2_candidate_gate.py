#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

WAVE1 = Path("docs/audit/aragon_wave1_review_queue_v1082.csv")
OUT_LEDGER = Path("docs/audit/aragon_wave2_evidence_ledger_v1083.csv")
OUT_MATRIX = Path("docs/audit/aragon_wave2_candidate_matrix_v1083.csv")
OUT_REPORT = Path("docs/audit/aragon-wave2-candidate-gate-v1083.md")

EXPECTED_ROWS = 734

SOURCES = [
    {
        "source_id": "edistribucion_aragon_regional_official",
        "source_family": "edistribucion_official",
        "source_url": (
            "https://www.edistribucion.com/es/conocenos/"
            "nuestro-negocio.html"
        ),
        "source_kind": "official_operator",
        "scope": "regional_aragon",
        "municipality": "",
        "candidate_distributor": "E-Distribución Redes Digitales, S.L.U.",
        "evidence_class": "regional_context_only",
        "municipality_exact": "no",
        "legal_entity_confirmed": "yes",
        "primary_source": "yes",
        "import_eligible": "no",
        "notes": (
            "Confirma presencia regional, pero no asignación municipal."
        ),
    },
    {
        "source_id": "cnmc_energy_discovery_official",
        "source_family": "cnmc_official",
        "source_url": (
            "https://www.cnmc.es/sectores-que-regulamos/energia"
        ),
        "source_kind": "official_regulator",
        "scope": "national_discovery",
        "municipality": "",
        "candidate_distributor": "",
        "evidence_class": "official_discovery_only",
        "municipality_exact": "no",
        "legal_entity_confirmed": "no",
        "primary_source": "yes",
        "import_eligible": "no",
        "notes": "Fuente regulatoria de descubrimiento.",
    },
    {
        "source_id": "boa_aragon_discovery_official",
        "source_family": "boa_official",
        "source_url": "https://www.boa.aragon.es/",
        "source_kind": "official_journal",
        "scope": "regional_discovery",
        "municipality": "",
        "candidate_distributor": "",
        "evidence_class": "official_discovery_only",
        "municipality_exact": "no",
        "legal_entity_confirmed": "no",
        "primary_source": "yes",
        "import_eligible": "no",
        "notes": "Fuente oficial para localizar resoluciones municipales.",
    },
    {
        "source_id": "ser_barbastro_network_2025_05",
        "source_family": "cadena_ser_aragon_oriental",
        "source_url": (
            "https://cadenaser.com/aragon/2025/05/26/"
            "un-mes-despues-del-apagon-ser-aragon-oriental/"
        ),
        "source_kind": "secondary_media",
        "scope": "municipality",
        "municipality": "Barbastro",
        "candidate_distributor": (
            "AB Energía / Eléctrica de Barbastro "
            "(entidad jurídica pendiente)"
        ),
        "evidence_class": "secondary_municipal_exact",
        "municipality_exact": "yes",
        "legal_entity_confirmed": "no",
        "primary_source": "no",
        "import_eligible": "no",
        "notes": "Referencia explícita a la red de distribución de Barbastro.",
    },
    {
        "source_id": "ser_barbastro_network_2025_10",
        "source_family": "cadena_ser_aragon_oriental",
        "source_url": (
            "https://cadenaser.com/aragon/2025/10/29/"
            "ab-energia-122-anos-de-compromiso-con-el-territorio-"
            "ser-aragon-oriental/"
        ),
        "source_kind": "secondary_media",
        "scope": "municipality",
        "municipality": "Barbastro",
        "candidate_distributor": (
            "AB Energía / Eléctrica de Barbastro "
            "(entidad jurídica pendiente)"
        ),
        "evidence_class": "secondary_municipal_exact",
        "municipality_exact": "yes",
        "legal_entity_confirmed": "no",
        "primary_source": "no",
        "import_eligible": "no",
        "notes": "Describe red propia y suministro en Barbastro.",
    },
    {
        "source_id": "ser_barbastro_network_2026_02",
        "source_family": "cadena_ser_aragon_oriental",
        "source_url": (
            "https://cadenaser.com/aragon/2026/02/12/"
            "ab-energia-se-consolida-como-referente-de-la-"
            "transicion-energetica-en-aragon-ser-aragon-oriental/"
        ),
        "source_kind": "secondary_media",
        "scope": "municipality",
        "municipality": "Barbastro",
        "candidate_distributor": (
            "AB Energía / Eléctrica de Barbastro "
            "(entidad jurídica pendiente)"
        ),
        "evidence_class": "secondary_municipal_exact",
        "municipality_exact": "yes",
        "legal_entity_confirmed": "no",
        "primary_source": "no",
        "import_eligible": "no",
        "notes": "Referencia explícita a gestión de red en Barbastro.",
    },
]


def norm(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").strip().lower())
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    return re.sub(r"[^a-z0-9]+", "", text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def validate_sources() -> None:
    allowed_domains = {
        "www.edistribucion.com",
        "www.cnmc.es",
        "www.boa.aragon.es",
        "cadenaser.com",
    }

    ids: set[str] = set()

    for source in SOURCES:
        source_id = source["source_id"]

        if source_id in ids:
            raise SystemExit(f"ERROR source_id duplicado={source_id}")

        ids.add(source_id)
        parsed = urlparse(source["source_url"])

        if parsed.scheme != "https":
            raise SystemExit(f"ERROR URL no HTTPS={source_id}")

        if parsed.netloc not in allowed_domains:
            raise SystemExit(
                f"ERROR dominio no permitido={parsed.netloc}"
            )

        if source["import_eligible"] != "no":
            raise SystemExit(
                f"ERROR fuente importable prematuramente={source_id}"
            )


def main() -> int:
    validate_sources()

    rows = read_csv(WAVE1)

    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(
            f"ERROR wave1 rows={len(rows)} expected={EXPECTED_ROWS}"
        )

    seen: set[str] = set()
    matrix: list[dict[str, str]] = []

    barbastro_sources = [
        source
        for source in SOURCES
        if norm(source["municipality"]) == "barbastro"
    ]

    secondary_count = sum(
        source["primary_source"] == "no"
        for source in barbastro_sources
    )
    primary_exact_count = sum(
        source["primary_source"] == "yes"
        and source["municipality_exact"] == "yes"
        for source in barbastro_sources
    )
    families = {
        source["source_family"]
        for source in barbastro_sources
    }

    for row in rows:
        zone_id = str(row.get("zone_id") or "").strip()
        municipality = str(row.get("municipality") or "").strip()
        province = str(row.get("province") or "").strip()

        if not zone_id:
            raise SystemExit("ERROR fila sin zone_id")

        if zone_id in seen:
            raise SystemExit(f"ERROR zone_id duplicado={zone_id}")

        seen.add(zone_id)

        if norm(municipality) == "barbastro":
            candidate = (
                "AB Energía / Eléctrica de Barbastro "
                "(entidad jurídica pendiente)"
            )
            stage = "strong_secondary_candidate"
            source_ids = ";".join(
                source["source_id"]
                for source in barbastro_sources
            )
            municipality_exact = "yes"
            legal_entity_confirmed = "no"
            next_action = (
                "Obtener fuente primaria del operador, regulador "
                "o boletín oficial que confirme entidad y ámbito."
            )
            row_secondary = str(secondary_count)
            row_primary = str(primary_exact_count)
            row_families = str(len(families))
        else:
            candidate = ""
            stage = "regional_context_only"
            source_ids = "edistribucion_aragon_regional_official"
            municipality_exact = "no"
            legal_entity_confirmed = "no"
            next_action = (
                "Buscar fuente primaria municipal reproducible; "
                "no inferir desde presencia regional."
            )
            row_secondary = "0"
            row_primary = "0"
            row_families = "0"

        matrix.append({
            "dataset_id": "aragon",
            "zone_id": zone_id,
            "municipality": municipality,
            "province": province,
            "candidate_distributor": candidate,
            "candidate_stage": stage,
            "primary_exact_sources": row_primary,
            "secondary_exact_sources": row_secondary,
            "independent_source_families": row_families,
            "municipality_exact": municipality_exact,
            "legal_entity_confirmed": legal_entity_confirmed,
            "review_decision": "pending",
            "import_eligible": "no",
            "source_ids": source_ids,
            "next_action": next_action,
        })

    matrix.sort(
        key=lambda row: (
            row["province"],
            row["municipality"],
            row["zone_id"],
        )
    )

    write_csv(OUT_LEDGER, SOURCES)
    write_csv(OUT_MATRIX, matrix)

    stage_counts = Counter(
        row["candidate_stage"]
        for row in matrix
    )
    eligible = sum(
        row["import_eligible"] == "yes"
        for row in matrix
    )

    report = f"""# Aragón wave 2 candidate gate v0.10.8.3

## Resultado

- Municipios revisados: **{len(matrix)}**
- Contexto regional únicamente: **{stage_counts['regional_context_only']}**
- Candidatos secundarios fuertes: **{stage_counts['strong_secondary_candidate']}**
- Candidatos con fuente primaria municipal exacta: **0**
- Municipios elegibles para importar: **{eligible}**
- Hints productivos importados por esta fase: **0**

## Barbastro

Barbastro queda clasificado como `strong_secondary_candidate`.

Hay varias referencias municipales explícitas, pero pertenecen a una única
familia editorial y todavía no confirman de forma primaria la entidad jurídica
de la distribuidora. Por ello continúa con `import_eligible=no`.

## Puerta de importación

Una futura fila solo puede pasar a `import_eligible=yes` cuando cumpla todo:

1. fuente primaria oficial;
2. municipio mencionado de forma exacta;
3. entidad jurídica confirmada;
4. decisión de revisión aprobada;
5. ninguna inferencia basada únicamente en cobertura regional.

## Corrección de wave 1

Los 734 `repository-local reference hits` son referencias cruzadas de
inventario, no 734 pruebas de distribuidora.

## Privacidad y seguridad

No se incluyen CUPS, direcciones, coordenadas exactas, geometría de red,
respuestas raw, contratos ni datos de clientes.
"""

    OUT_REPORT.write_text(report, encoding="utf-8")

    print(f"OK wrote {OUT_LEDGER}")
    print(f"OK wrote {OUT_MATRIX}")
    print(f"OK wrote {OUT_REPORT}")
    print(f"rows={len(matrix)}")
    print("stage_counts=", dict(stage_counts))
    print(f"import_eligible={eligible}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
