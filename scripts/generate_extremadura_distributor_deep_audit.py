#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEOJSON = ROOT / "frontend/public/data/extremadura_municipios.geojson"
HINTS = ROOT / "frontend/public/data/distributor_hints.json"
REVIEW_MD = ROOT / "docs/research/distributor_import_batches/extremadura_deep_audit.md"
QUEUE_CSV = ROOT / "docs/research/distributor_import_batches/extremadura_municipality_review_queue.csv"
SOURCES_CSV = ROOT / "docs/research/distributor_import_batches/extremadura_distributor_sources.csv"

DATASET_ID = "extremadura"
EXPECTED_MUNICIPALITIES = 388

NAME_KEYS = [
    "name", "NAME", "nombre", "NOMBRE", "municipio", "MUNICIPIO",
    "mun_name", "MUN_NAME", "NMUN", "NOM_MUN", "NOMBRE_MUN",
    "ETIQUETA", "label", "LABEL", "Texto", "TEXTO", "rotulo", "ROTULO",
]

PROVINCE_KEYS = [
    "province", "PROVINCE", "provincia", "PROVINCIA", "NPRO", "NOM_PROV",
    "prov_name", "PROV_NAME",
]

SOURCES = [
    {
        "source_id": "junta_extremadura_map",
        "source_name": "Junta de Extremadura — mapa público de empresas distribuidoras de energía eléctrica",
        "source_url": "https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml",
        "evidence_level": "official_regional_map",
        "safe_use": "Fuente oficial útil para revisión municipal manual. No convertir automáticamente en cobertura masiva.",
    },
    {
        "source_id": "ide_iberdrola_extremadura_2027_2029",
        "source_name": "Iberdrola España / i-DE — plan de inversiones redes eléctricas Extremadura 2027-2029",
        "source_url": "https://www.iberdrolaespana.com/sala-comunicacion/noticias/plan-inversiones-redes-electricas-extremadura-2027-2029",
        "evidence_level": "regional_presence_confirmed",
        "safe_use": "Confirma presencia regional relevante de i-DE, pero no cobertura municipal completa.",
    },
    {
        "source_id": "cnmc_distributor_registry",
        "source_name": "CNMC — censo/listado público de distribuidoras de electricidad",
        "source_url": "https://sede.cnmc.gob.es/listado/censo/1",
        "evidence_level": "national_registry",
        "safe_use": "Sirve para validar razón social/código, no para inferir municipio exacto.",
    },
    {
        "source_id": "excluded_sensitive_lists_policy",
        "source_name": "Política de exclusión de listados con campos sensibles",
        "source_url": "",
        "evidence_level": "safety_policy",
        "safe_use": "No ingerir automáticamente listados/PDFs que puedan incluir CUPS, direcciones, teléfonos o datos de suministro. Solo usar fuentes sanitizadas o revisión manual.",
    },
]


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def clean(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def looks_like_name(value: str) -> bool:
    if not value:
        return False
    if len(value) < 3:
        return False
    if re.fullmatch(r"[0-9._/\- ]+", value):
        return False
    if value.lower() in {"extremadura", "badajoz", "caceres", "cáceres"}:
        return False
    return any(ch.isalpha() for ch in value)


def extract_name(feature: dict, index: int) -> str:
    props = feature.get("properties") or {}
    for key in NAME_KEYS:
        value = clean(props.get(key))
        if looks_like_name(value):
            return value

    candidates = []
    for key, value in props.items():
        text = clean(value)
        if looks_like_name(text):
            candidates.append((key, text))

    if candidates:
        candidates.sort(key=lambda pair: (len(pair[1]), pair[0]))
        return candidates[0][1]

    raise SystemExit(f"ERROR: no pude extraer municipio feature #{index}; keys={sorted(props.keys())}")


def extract_province(feature: dict) -> str:
    props = feature.get("properties") or {}
    for key in PROVINCE_KEYS:
        value = clean(props.get(key))
        if value:
            return value
    for value in props.values():
        text = clean(value)
        if text.lower() in {"badajoz", "caceres", "cáceres"}:
            return text
    return ""


def load_geo() -> list[dict[str, str]]:
    data = json.loads(GEOJSON.read_text(encoding="utf-8"))
    features = data.get("features", [])
    rows = []
    seen = set()

    for index, feature in enumerate(features):
        municipio = extract_name(feature, index)
        key = norm(municipio)
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "municipio": municipio,
            "province": extract_province(feature),
            "zone_id_candidate": f"municipality:{DATASET_ID}::{key}",
        })

    rows.sort(key=lambda row: norm(row["municipio"]))

    if len(rows) != EXPECTED_MUNICIPALITIES:
        raise SystemExit(f"ERROR: esperaba {EXPECTED_MUNICIPALITIES} municipios, detectados {len(rows)}")

    return rows


def load_existing_hints() -> dict[str, dict]:
    data = json.loads(HINTS.read_text(encoding="utf-8"))
    return {
        item.get("municipio", ""): item
        for item in data.get("items", [])
        if item.get("dataset_id") == DATASET_ID
    }


def build_queue(geo_rows: list[dict[str, str]], existing: dict[str, dict]) -> list[dict[str, str]]:
    rows = []

    for geo in geo_rows:
        municipio = geo["municipio"]
        item = existing.get(municipio)

        if item:
            distributors = item.get("distributors", [])
            current_names = " | ".join(str(d.get("name", "")) for d in distributors)
            confidence = " | ".join(str(d.get("confidence", "")) for d in distributors)
            status = "already_in_production"
            allowed = "no"
            next_step = "Mantener. Revalidar solo si cambia la fuente pública."
        else:
            current_names = ""
            confidence = ""
            status = "pending_municipal_review"
            allowed = "no"
            next_step = "Revisar en mapa oficial de Junta, herramienta de distribuidora y CNMC antes de importar."

        rows.append({
            "dataset_id": DATASET_ID,
            "province": geo["province"],
            "municipio": municipio,
            "zone_id_candidate": geo["zone_id_candidate"],
            "current_distributor_hint": current_names,
            "current_confidence": confidence,
            "review_status": status,
            "bulk_import_allowed": allowed,
            "evidence_required": "Fuente pública municipal o herramienta oficial sin CUPS, dirección exacta privada ni datos de suministro.",
            "safe_next_step": next_step,
        })

    return rows


def csv_render(rows: list[dict[str, str]], fieldnames: list[str]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def sources_csv() -> str:
    fields = ["source_id", "source_name", "source_url", "evidence_level", "safe_use"]
    return csv_render(SOURCES, fields)


def markdown(geo_rows: list[dict[str, str]], queue_rows: list[dict[str, str]], existing: dict[str, dict]) -> str:
    status_counts = Counter(row["review_status"] for row in queue_rows)
    province_counts = Counter(row["province"] or "desconocida" for row in queue_rows)

    sources_md = "\n".join(
        f"- **{s['source_name']}** — `{s['evidence_level']}`. {s['safe_use']}"
        + (f" Fuente: {s['source_url']}" if s["source_url"] else "")
        for s in SOURCES
    )

    province_md = "\n".join(
        f"| {province} | {count} |"
        for province, count in sorted(province_counts.items())
    )

    sample_md = "\n".join(
        f"- {row['municipio']} — `{row['review_status']}`"
        for row in queue_rows[:40]
    )

    return f"""# Auditoría profunda de distribuidoras · Extremadura

Generado desde `frontend/public/data/extremadura_municipios.geojson` y fuentes públicas de alto nivel.

## Resumen ejecutivo

- Dataset: `extremadura`.
- Municipios/zonas en GeoJSON público: **{len(geo_rows)}**.
- Pistas productivas importadas en este PR: **0**.
- Pistas productivas actuales en Extremadura: **{len(existing)}**.
- Estado del lote: **no importable todavía como `regional_default` único**.
- Motivo: hay presencia pública regional relevante de i-DE, pero también fuente oficial autonómica de mapa de distribuidoras y censo CNMC; requiere revisión municipal.

## Clasificación inicial

| Estado | Municipios |
|---|---:|
| `already_in_production` | {status_counts.get("already_in_production", 0)} |
| `pending_municipal_review` | {status_counts.get("pending_municipal_review", 0)} |

## Distribución por provincia detectada

| Provincia | Municipios |
|---|---:|
{province_md}

## Fuentes públicas de alto nivel

{sources_md}

## Decisión de seguridad

No se importan los 388 municipios como una única distribuidora regional.

La presencia regional de i-DE permite abrir revisión, pero no basta para afirmar cobertura municipal completa. Además, cualquier listado que incluya CUPS, direcciones, teléfonos o datos de suministro queda excluido de ingestión automática.

## Política de importación posterior

Para pasar un municipio a `verified_partial`:

1. Confirmar municipio en fuente pública oficial o herramienta pública de distribuidora.
2. Validar razón social con CNMC si procede.
3. No usar CUPS.
4. No usar direcciones exactas privadas.
5. No publicar coordenadas privadas.
6. No afirmar exclusividad de red.
7. Añadir fuente trazable y nota de cobertura prudente.

Para usar `regional_default`:

- Solo si el riesgo de excepción local es bajo.
- Solo después de revisar excepciones locales.
- No aplicable a Extremadura en este momento.

## Archivos generados

- `docs/research/distributor_import_batches/extremadura_deep_audit.md`
- `docs/research/distributor_import_batches/extremadura_municipality_review_queue.csv`
- `docs/research/distributor_import_batches/extremadura_distributor_sources.csv`

## Muestra de cola municipal

{sample_md}

## Siguiente paso recomendado

Hacer un PR posterior de importación parcial, pequeño y verificable, solo con municipios donde la evidencia pública sea fuerte.

No hacer importación regional completa de Extremadura todavía.
"""


def write(path: Path, content: str) -> bool:
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    geo_rows = load_geo()
    existing = load_existing_hints()
    queue_rows = build_queue(geo_rows, existing)

    queue_fields = [
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

    outputs = {
        REVIEW_MD: markdown(geo_rows, queue_rows, existing),
        QUEUE_CSV: csv_render(queue_rows, queue_fields),
        SOURCES_CSV: sources_csv(),
    }

    if args.check:
        for path, content in outputs.items():
            if not path.exists():
                print(f"ERROR: falta {path.relative_to(ROOT)}")
                return 1
            if path.read_text(encoding="utf-8") != content:
                print(f"ERROR: {path.relative_to(ROOT)} no está actualizado")
                return 1
        print("OK auditoría profunda Extremadura actualizada")
        return 0

    changed = []
    for path, content in outputs.items():
        if write(path, content):
            changed.append(path.relative_to(ROOT))

    print("OK auditoría profunda Extremadura generada")
    print(f"municipios={len(geo_rows)}")
    print(f"pistas_existentes={len(existing)}")
    for item in changed:
        print(f"actualizado: {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
