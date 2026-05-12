#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

DATASET_ID = "extremadura"
TODAY = "2026-05-12"

GEOJSON = Path("frontend/public/data/extremadura_municipios.geojson")
HINTS = Path("frontend/public/data/distributor_hints.json")

REPORT = Path("docs/research/distributor_import_batches/extremadura_deep_audit.md")
QUEUE = Path("docs/research/distributor_import_batches/extremadura_municipality_review_queue.csv")
SOURCES = Path("docs/research/distributor_import_batches/extremadura_distributor_sources.csv")

KNOWN_ZONE_NAMES = {
    "municipality:badajoz::badajoz": "Badajoz",
    "municipality:caceres::caceres": "Cáceres",
    "municipality:cáceres::cáceres": "Cáceres",
}

NAME_KEYS = (
    "municipio",
    "MUNICIPIO",
    "mun_name",
    "MUN_NAME",
    "nombre",
    "NOMBRE",
    "name",
    "NAME",
)

PROVINCE_KEYS = (
    "province",
    "provincia",
    "PROVINCIA",
    "prov_name",
    "PROV_NAME",
)

QUEUE_FIELDS = [
    "dataset_id",
    "province",
    "municipio",
    "zone_id_candidate",
    "current_distributor_hint",
    "current_confidence",
    "review_status",
    "bulk_import_allowed",
    "evidence_required",
    "safe_next_step",
]

SOURCES_FIELDS = ["source_id", "source_type", "title", "url", "safe_use_note"]


def norm(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def clean_name(value: str) -> str:
    text = str(value or "").strip()
    return KNOWN_ZONE_NAMES.get(text, text)


def pick(props: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = props.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def extract_municipio(feature: dict, index: int) -> str:
    props = feature.get("properties") or {}
    value = clean_name(pick(props, NAME_KEYS))
    if not value:
        value = clean_name(str(feature.get("id") or "").strip())
    if not value:
        value = f"municipio_{index + 1}"
    if value.startswith("municipality:"):
        value = KNOWN_ZONE_NAMES.get(value, value)
    return value


def extract_province(feature: dict, municipio: str) -> str:
    props = feature.get("properties") or {}
    province = pick(props, PROVINCE_KEYS)
    if province:
        return province
    # Fallback seguro: las dos capitales estaban llegando como name técnico.
    if municipio == "Badajoz":
        return "Badajoz"
    if municipio == "Cáceres":
        return "Cáceres"
    return ""


def extract_zone_id(feature: dict, municipio: str) -> str:
    props = feature.get("properties") or {}
    raw = str(
        props.get("zone_id")
        or props.get("zoneId")
        or props.get("id")
        or feature.get("id")
        or ""
    ).strip()

    # Si viene un identificador de otro dataset/provincia, no lo propagamos.
    if raw.startswith(f"municipality:{DATASET_ID}::") and "::municipality_" not in raw:
        return raw

    return f"municipality:{DATASET_ID}::{norm(municipio)}"


def load_geo_rows() -> list[dict]:
    data = json.loads(GEOJSON.read_text(encoding="utf-8"))
    features = data.get("features") or []
    rows = []

    for index, feature in enumerate(features):
        municipio = extract_municipio(feature, index)
        province = extract_province(feature, municipio)
        zone_id = extract_zone_id(feature, municipio)

        rows.append(
            {
                "dataset_id": DATASET_ID,
                "province": province,
                "municipio": municipio,
                "zone_id_candidate": zone_id,
            }
        )

    rows.sort(key=lambda r: (r["province"], norm(r["municipio"]), r["zone_id_candidate"]))
    return rows


def distributor_names(item: dict) -> list[str]:
    names: list[str] = []

    for key in ("distributors", "distributor_hints", "hints"):
        values = item.get(key)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, dict):
                    name = (
                        value.get("name")
                        or value.get("distributor")
                        or value.get("distributor_name")
                        or value.get("company")
                    )
                    if name:
                        names.append(str(name).strip())
                elif isinstance(value, str) and value.strip():
                    names.append(value.strip())

    for key in ("distributor", "distributor_name", "name"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            names.append(value.strip())

    return sorted(set(n for n in names if n))


def confidence(item: dict) -> str:
    value = (
        item.get("confidence")
        or item.get("source_confidence")
        or item.get("coverage_confidence")
        or ""
    )
    return str(value or "").strip()


def load_distributor_hints_payload(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("items", "hints", "distributor_hints", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return value

    raise SystemExit(
        f"ERROR: {path} debe ser una lista o un objeto con items/hints/distributor_hints/data"
    )


def load_existing_hints() -> list[dict]:
    data = load_distributor_hints_payload(HINTS)
    return [
        item
        for item in data
        if isinstance(item, dict) and item.get("dataset_id") == DATASET_ID
    ]


def build_existing_indexes(items: list[dict]) -> tuple[dict[str, dict], dict[str, dict]]:
    by_zone: dict[str, dict] = {}
    by_name: dict[str, dict] = {}

    for item in items:
        zone_id = str(item.get("zone_id") or "").strip()
        municipio = str(item.get("municipio") or item.get("name") or "").strip()

        if zone_id:
            by_zone[zone_id] = item
        if municipio:
            by_name[norm(municipio)] = item

    return by_zone, by_name


def build_queue_rows() -> tuple[list[dict], dict]:
    geo_rows = load_geo_rows()
    existing_items = load_existing_hints()
    existing_by_zone, existing_by_name = build_existing_indexes(existing_items)

    queue_rows = []

    for geo in geo_rows:
        item = (
            existing_by_zone.get(geo["zone_id_candidate"])
            or existing_by_name.get(norm(geo["municipio"]))
        )

        if item:
            names = distributor_names(item)
            conf = confidence(item) or "verified_partial"
            status = "already_in_production"
            bulk = "no"
            evidence = "Ya existe pista productiva saneada en distributor_hints.json."
            next_step = "Mantener como verified_partial prudente; no afirmar exclusividad de red."
        else:
            names = []
            conf = ""
            status = "pending_municipal_review"
            bulk = "no"
            evidence = "Fuente pública municipal o herramienta oficial sin CUPS, dirección exacta privada ni datos de suministro."
            next_step = "Revisar en mapa oficial de Junta, herramienta de distribuidora y CNMC antes de importar."

        queue_rows.append(
            {
                **geo,
                "current_distributor_hint": " | ".join(names),
                "current_confidence": conf,
                "review_status": status,
                "bulk_import_allowed": bulk,
                "evidence_required": evidence,
                "safe_next_step": next_step,
            }
        )

    summary = {
        "municipios": len(geo_rows),
        "existing_items": len(existing_items),
        "status": Counter(row["review_status"] for row in queue_rows),
        "province": Counter(row["province"] for row in geo_rows),
    }

    return queue_rows, summary


def render_queue_csv(rows: list[dict]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=QUEUE_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def render_sources_csv() -> str:
    rows = [
        {
            "source_id": "junta_extremadura_visor_distribuidoras",
            "source_type": "official_regional_map",
            "title": "Junta de Extremadura — visor público de empresas distribuidoras de energía eléctrica",
            "url": "https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml",
            "safe_use_note": "Usar solo datos saneados; no guardar CUPS, direcciones, teléfonos, coordenadas, geometrías ni respuesta raw.",
        },
        {
            "source_id": "iberdrola_ide_extremadura_inversiones_2027_2029",
            "source_type": "regional_presence_confirmed",
            "title": "Iberdrola España / i-DE — plan de inversiones redes eléctricas Extremadura 2027-2029",
            "url": "https://www.iberdrolaespana.com/sala-comunicacion/noticias/plan-inversiones-redes-electricas-extremadura-2027-2029",
            "safe_use_note": "Confirma presencia regional, no cobertura municipal completa.",
        },
        {
            "source_id": "cnmc_censo_distribuidoras",
            "source_type": "national_registry",
            "title": "CNMC — censo/listado público de distribuidoras de electricidad",
            "url": "https://sede.cnmc.gob.es/listado/censo/1",
            "safe_use_note": "Sirve para validar razón social/código, no para inferir municipio exacto.",
        },
    ]

    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=SOURCES_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def render_report(rows: list[dict], summary: dict) -> str:
    status = summary["status"]
    provinces = summary["province"]
    pending = [row for row in rows if row["review_status"] != "already_in_production"]

    lines = [
        "# Auditoría profunda de distribuidoras · Extremadura",
        "",
        "Generado desde `frontend/public/data/extremadura_municipios.geojson` y fuentes públicas de alto nivel.",
        "",
        "## Resumen ejecutivo",
        "",
        f"- Dataset: `{DATASET_ID}`.",
        f"- Municipios/zonas en GeoJSON público: **{summary['municipios']}**.",
        "- Pistas productivas importadas en este PR: **0**.",
        f"- Pistas productivas actuales en Extremadura: **{summary['existing_items']}**.",
        "- Estado del lote: **no importable como `regional_default` único**.",
        "- Motivo: Extremadura tiene varias distribuidoras detectadas; la importación correcta es municipal `verified_partial`.",
        "",
        "## Clasificación inicial",
        "",
        "| Estado | Municipios |",
        "|---|---:|",
    ]

    for key in ("already_in_production", "pending_municipal_review"):
        lines.append(f"| `{key}` | {status.get(key, 0)} |")

    lines.extend(
        [
            "",
            "## Distribución por provincia detectada",
            "",
            "| Provincia | Municipios |",
            "|---|---:|",
        ]
    )

    for province, count in sorted(provinces.items()):
        lines.append(f"| {province or 'Sin provincia'} | {count} |")

    lines.extend(
        [
            "",
            "## Fuentes públicas de alto nivel",
            "",
            "- **Junta de Extremadura — visor público de empresas distribuidoras de energía eléctrica** — `official_regional_map`. Fuente oficial útil para revisión municipal. No convertir automáticamente en cobertura regional única. Fuente: https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml",
            "- **Iberdrola España / i-DE — plan de inversiones redes eléctricas Extremadura 2027-2029** — `regional_presence_confirmed`. Confirma presencia regional relevante de i-DE, pero no cobertura municipal completa. Fuente: https://www.iberdrolaespana.com/sala-comunicacion/noticias/plan-inversiones-redes-electricas-extremadura-2027-2029",
            "- **CNMC — censo/listado público de distribuidoras de electricidad** — `national_registry`. Sirve para validar razón social/código, no para inferir municipio exacto. Fuente: https://sede.cnmc.gob.es/listado/censo/1",
            "- **Política de exclusión de listados con campos sensibles** — `safety_policy`. No ingerir automáticamente listados/PDFs que puedan incluir CUPS, direcciones, teléfonos o datos de suministro. Solo usar fuentes sanitizadas o revisión manual.",
            "",
            "## Decisión de seguridad",
            "",
            "No se importa Extremadura como una única distribuidora regional.",
            "",
            "La importación segura es municipal y prudente, usando `verified_partial`, sin afirmar exclusividad de red ni cobertura total municipal.",
            "",
            "## Archivos generados",
            "",
            "- `docs/research/distributor_import_batches/extremadura_deep_audit.md`",
            "- `docs/research/distributor_import_batches/extremadura_municipality_review_queue.csv`",
            "- `docs/research/distributor_import_batches/extremadura_distributor_sources.csv`",
            "",
            "## Muestra de cola municipal",
            "",
        ]
    )

    for row in rows[:40]:
        lines.append(f"- {row['municipio']} — `{row['review_status']}`")

    lines.extend(["", "## Pendientes", ""])

    if pending:
        for row in pending:
            lines.append(f"- {row['municipio']} ({row['province']}) — `{row['review_status']}`")
    else:
        lines.append("- Ninguno.")

    lines.extend(
        [
            "",
            "## Siguiente paso recomendado",
            "",
            "Mantener esta importación como pistas municipales `verified_partial`. No usar `regional_default` para Extremadura.",
            "",
        ]
    )

    return "\n".join(lines)


def generate() -> dict[Path, str]:
    rows, summary = build_queue_rows()
    return {
        REPORT: render_report(rows, summary),
        QUEUE: render_queue_csv(rows),
        SOURCES: render_sources_csv(),
    }


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def check_outputs(outputs: dict[Path, str]) -> bool:
    ok = True
    for path, expected in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != expected:
            print(f"ERROR: {path} no está actualizado", file=sys.stderr)
            ok = False
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    outputs = generate()

    if args.check:
        return 0 if check_outputs(outputs) else 1

    write_outputs(outputs)

    rows, summary = build_queue_rows()
    print("OK auditoría profunda Extremadura generada")
    print(f"municipios={summary['municipios']}")
    print(f"pistas_existentes={summary['existing_items']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
