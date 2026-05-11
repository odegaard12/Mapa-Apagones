#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEOJSON = ROOT / "frontend" / "public" / "data" / "madrid_municipios.geojson"
DOC = ROOT / "docs" / "research" / "distributor_import_batches" / "madrid_deep_review.md"
CSV_OUT = ROOT / "docs" / "research" / "distributor_import_batches" / "madrid_municipality_review_queue.csv"

SOURCES = {
    "ufd_madrid_47": "https://www.naturgy.com/notas-de-prensa/ufd-refuerza-la-calidad-del-suministro-electrico-en-el-sur-de-la-comunidad-de-madrid/",
    "ufd_checker": "https://www.ufd.es/quienes-somos/donde-estamos/",
    "ide_checker": "https://www.i-de.es/conexion-red-electrica/mapa-de-distribuidoras",
    "cnmc_census": "https://sede.cnmc.gob.es/listado/censo/1",
    "comunidad_madrid_ufd": "https://www.comunidad.madrid/transparencia/agenda/reunion-ufd-distribucion-electricidad-sa",
}

UFD_NAMED_MUNICIPALITIES = {
    "alcala de henares",
    "aranjuez",
    "ciempozuelos",
    "colmenar de oreja",
    "getafe",
    "rivas vaciamadrid",
    "san martin de la vega",
    "valdemoro",
    "villaconejos",
}

MULTI_REVIEW_MUNICIPALITIES = {
    "madrid",
}


def norm(value: str) -> str:
    value = value or ""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    for old, new in {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
        "-": " ",
        "/": " ",
        ".": " ",
        ",": " ",
        "  ": " ",
    }.items():
        value = value.replace(old, new)
    return " ".join(value.split())


def prop(props: dict, *names: str) -> str:
    for name in names:
        value = props.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def load_features() -> list[dict]:
    data = json.loads(GEOJSON.read_text(encoding="utf-8"))
    features = data.get("features", [])
    if not isinstance(features, list) or not features:
        raise SystemExit(f"ERROR: {GEOJSON.relative_to(ROOT)} no contiene features[]")
    return features


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for feature in load_features():
        props = feature.get("properties", {}) or {}
        municipality = prop(props, "municipio", "mun_name", "name", "NOMBRE", "NAME")
        province = prop(props, "province", "prov_name", "PROVINCIA") or "Madrid"
        zone_id = prop(props, "zone_id", "id") or f"municipality:madrid::{norm(municipality).replace(' ', '-')}"

        key = norm(municipality)

        if key in UFD_NAMED_MUNICIPALITIES:
            review_status = "candidate_ufd_verified_partial_review"
            candidate_distributors = "UFD Distribución Electricidad, S.A."
            source_name = "Naturgy/UFD — presencia pública citada en municipios de la Comunidad de Madrid"
            source_url = SOURCES["ufd_madrid_47"]
            notes = "Municipio citado en comunicación pública de UFD/Naturgy; revisar contra herramienta oficial antes de importar."
        elif key in MULTI_REVIEW_MUNICIPALITIES:
            review_status = "multi_distributor_review_required"
            candidate_distributors = "UFD / i-DE / revisión oficial requerida"
            source_name = "Comunidad de Madrid + herramientas oficiales UFD/i-DE"
            source_url = SOURCES["comunidad_madrid_ufd"]
            notes = "Madrid capital requiere revisión específica: presencia pública de UFD, pero no se debe afirmar exclusividad."
        else:
            review_status = "pending_municipal_review"
            candidate_distributors = "revisión municipal requerida"
            source_name = "Herramientas oficiales UFD/i-DE y censo CNMC"
            source_url = SOURCES["ufd_checker"]
            notes = "No importar hasta confirmar distribuidora por municipio o fuente pública suficientemente acotada."

        rows.append({
            "dataset_id": "madrid",
            "municipality": municipality,
            "province": province,
            "zone_id": zone_id,
            "review_status": review_status,
            "candidate_distributors": candidate_distributors,
            "source_name": source_name,
            "source_url": source_url,
            "notes": notes,
        })

    rows.sort(key=lambda row: norm(row["municipality"]))
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "dataset_id",
        "municipality",
        "province",
        "zone_id",
        "review_status",
        "candidate_distributors",
        "source_name",
        "source_url",
        "notes",
    ]

    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_doc(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["review_status"] for row in rows)
    ufd_rows = [row for row in rows if row["review_status"] == "candidate_ufd_verified_partial_review"]
    pending_rows = [row for row in rows if row["review_status"] == "pending_municipal_review"]

    doc = f"""# Revisión profunda de distribuidoras · Comunidad de Madrid

Generado desde `{GEOJSON.relative_to(ROOT)}`.

## Resumen

- Dataset: `madrid`.
- Municipios/zonas en GeoJSON público: **{len(rows)}**.
- Pistas productivas importadas en este PR: **0**.
- Estado del lote: **no importable todavía como regional_default único**.
- Motivo: Madrid tiene presencia pública relevante de más de una distribuidora y requiere revisión municipal.

## Clasificación inicial

| Estado | Municipios |
|---|---:|
| `candidate_ufd_verified_partial_review` | {counts.get("candidate_ufd_verified_partial_review", 0)} |
| `multi_distributor_review_required` | {counts.get("multi_distributor_review_required", 0)} |
| `pending_municipal_review` | {counts.get("pending_municipal_review", 0)} |

## Fuentes públicas de alto nivel

- UFD/Naturgy: comunicación pública indicando servicio a más de 1,2 millones de puntos de suministro en 47 municipios de la Comunidad de Madrid y citando actuaciones en varios municipios: {SOURCES["ufd_madrid_47"]}
- UFD: herramienta pública para comprobar si una zona pertenece a su red de distribución: {SOURCES["ufd_checker"]}
- i-DE: herramienta pública para localizar municipio/dirección y conocer si opera en esa zona: {SOURCES["ide_checker"]}
- CNMC: censo/listado público de distribuidoras de electricidad: {SOURCES["cnmc_census"]}
- Comunidad de Madrid: agenda/reunión con UFD Distribución Electricidad, S.A.: {SOURCES["comunidad_madrid_ufd"]}

## Candidatos UFD citados por fuente pública

Estos municipios aparecen citados en la comunicación pública de UFD/Naturgy o encajan con actuaciones descritas públicamente, pero **no se importan todavía**. Deben comprobarse con herramienta oficial o fuente municipal antes de pasar a `verified_partial`.

"""

    for row in ufd_rows:
        doc += f"- {row['municipality']} — `{row['review_status']}`.\n"

    doc += f"""
## Municipios pendientes

Quedan **{len(pending_rows)}** municipios marcados como `pending_municipal_review`.

No se deben importar como UFD ni como i-DE hasta tener evidencia pública municipal suficiente.

## Criterio de seguridad

- No usar CUPS para generar datos públicos.
- No publicar direcciones exactas.
- No publicar coordenadas privadas.
- No publicar infraestructura crítica.
- No afirmar exclusividad de red.
- No convertir fuentes regionales en cobertura municipal sin comprobación.
- Mantener `regional_default` solo cuando el riesgo de excepción local sea bajo.
- Usar `verified_partial` solo para presencia pública razonablemente verificada, nunca como cobertura exclusiva.

## Siguiente paso recomendado

1. Revisar la cola municipal en `{CSV_OUT.relative_to(ROOT)}`.
2. Confirmar municipios con herramientas públicas oficiales y fuentes municipales.
3. Importar solo subconjunto conservador:
   - municipios UFD con evidencia municipal fuerte;
   - municipios i-DE con evidencia municipal fuerte;
   - dejar el resto como pendiente.
"""

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(doc, encoding="utf-8")


def main() -> int:
    check = "--check" in sys.argv
    rows = build_rows()

    expected_csv = CSV_OUT
    expected_doc = DOC

    if check:
        old_csv = expected_csv.read_text(encoding="utf-8") if expected_csv.exists() else None
        old_doc = expected_doc.read_text(encoding="utf-8") if expected_doc.exists() else None

        write_csv(rows)
        write_doc(rows)

        new_csv = expected_csv.read_text(encoding="utf-8")
        new_doc = expected_doc.read_text(encoding="utf-8")

        if old_csv != new_csv or old_doc != new_doc:
            print("ERROR revisión Madrid no está actualizada")
            return 1

        print("OK revisión Madrid actualizada")
        return 0

    write_csv(rows)
    write_doc(rows)
    print(f"OK revisión Madrid generada: {DOC.relative_to(ROOT)}")
    print(f"OK cola municipal Madrid generada: {CSV_OUT.relative_to(ROOT)}")
    print(f"municipios={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
