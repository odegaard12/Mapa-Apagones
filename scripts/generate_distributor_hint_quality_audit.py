#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HINTS_PATH = ROOT / "frontend" / "public" / "data" / "distributor_hints.json"
OUTPUT_PATH = ROOT / "docs" / "audit" / "distributor_hint_quality_audit.md"

ALLOWED_CONFIDENCE = {
    "regional_default",
    "verified_partial",
}

SOURCE_KEYS = [
    "source",
    "sources",
    "source_name",
    "source_url",
    "fuente",
    "fuentes",
]

DATE_KEYS = [
    "last_reviewed",
    "reviewed_at",
    "fecha_revision",
    "fecha_revisión",
]


def get_first(entry: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        value = entry.get(key)
        if value not in (None, "", []):
            return value
    return None


def distributors(item: dict[str, Any]) -> list[dict[str, Any]]:
    value = item.get("distributors")

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]

    if isinstance(value, dict):
        return [value]

    return []


def has_source(item: dict[str, Any]) -> bool:
    if get_first(item, SOURCE_KEYS) not in (None, "", []):
        return True

    return any(get_first(distributor, SOURCE_KEYS) not in (None, "", []) for distributor in distributors(item))


def has_date(item: dict[str, Any]) -> bool:
    if get_first(item, DATE_KEYS) not in (None, "", []):
        return True

    return any(get_first(distributor, DATE_KEYS) not in (None, "", []) for distributor in distributors(item))


def confidence_values(item: dict[str, Any]) -> list[str]:
    values: list[str] = []

    top = item.get("confidence")
    if top not in (None, "", []):
        values.append(str(top))

    for distributor in distributors(item):
        value = distributor.get("confidence")
        if value not in (None, "", []):
            values.append(str(value))

    return values or ["sin_confianza"]


def render() -> tuple[str, int]:
    data = json.loads(HINTS_PATH.read_text(encoding="utf-8"))
    items = data.get("items")

    if not isinstance(items, list):
        raise SystemExit("ERROR: distributor_hints.json no contiene lista items")

    by_dataset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    duplicate_counter: Counter[str] = Counter()
    confidence_counter: Counter[str] = Counter()
    errors: list[str] = []
    warnings: list[str] = []

    for item in items:
        dataset_id = str(item.get("dataset_id") or "unknown")
        zone_id = str(item.get("zone_id") or "")
        by_dataset[dataset_id].append(item)

        if not zone_id:
            errors.append(f"Entrada sin zone_id en dataset {dataset_id}")
        else:
            duplicate_counter[zone_id] += 1

        if not item.get("municipio"):
            warnings.append(f"{zone_id}: falta municipio")

        if not item.get("province"):
            warnings.append(f"{zone_id}: falta province")

        if not distributors(item):
            errors.append(f"{zone_id}: no tiene distributors[]")

        for confidence in confidence_values(item):
            confidence_counter[confidence] += 1
            if confidence not in ALLOWED_CONFIDENCE:
                errors.append(f"{zone_id}: confidence no permitida: {confidence}")

    duplicates = sorted(zone_id for zone_id, count in duplicate_counter.items() if count > 1)

    for zone_id in duplicates:
        errors.append(f"zone_id duplicado: {zone_id}")

    lines: list[str] = []
    lines.append("# Auditoría de calidad de pistas de distribuidora")
    lines.append("")
    lines.append("Generado desde `frontend/public/data/distributor_hints.json`.")
    lines.append("")
    lines.append("## Resumen")
    lines.append("")
    lines.append(f"- Total de zonas con pista pública: **{len(items)}**.")
    lines.append(f"- Datasets con pistas: **{len(by_dataset)}**.")
    lines.append(f"- Zone IDs duplicados: **{len(duplicates)}**.")
    lines.append(f"- Errores bloqueantes detectados: **{len(errors)}**.")
    lines.append(f"- Avisos no bloqueantes detectados: **{len(warnings)}**.")
    lines.append("")
    lines.append("## Confianza global")
    lines.append("")
    lines.append("| Confianza | Entradas/distribuidoras |")
    lines.append("|---|---:|")
    for key, value in sorted(confidence_counter.items()):
        lines.append(f"| `{key}` | {value} |")

    lines.append("")
    lines.append("## Calidad por dataset")
    lines.append("")
    lines.append("| Dataset | Zonas | Con fuente | Con fecha | Con notas | regional_default | verified_partial |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    for dataset_id in sorted(by_dataset):
        dataset_items = by_dataset[dataset_id]
        source_count = sum(1 for item in dataset_items if has_source(item))
        date_count = sum(1 for item in dataset_items if has_date(item))
        notes_count = sum(1 for item in dataset_items if item.get("notes"))
        conf = Counter()
        for item in dataset_items:
            for value in confidence_values(item):
                conf[value] += 1

        lines.append(
            "| "
            f"`{dataset_id}` | "
            f"{len(dataset_items)} | "
            f"{source_count} | "
            f"{date_count} | "
            f"{notes_count} | "
            f"{conf.get('regional_default', 0)} | "
            f"{conf.get('verified_partial', 0)} |"
        )

    lines.append("")
    lines.append("## Lectura operativa")
    lines.append("")
    lines.append("- `regional_default` debe leerse como pista orientativa, no como exclusividad.")
    lines.append("- `verified_partial` debe leerse como presencia pública razonablemente verificada, no como cobertura total exclusiva.")
    lines.append("- Las zonas sin fuente o sin fecha deben priorizarse para backfill documental antes de nuevas importaciones masivas.")
    lines.append("- Esta auditoría no publica CUPS, direcciones, coordenadas privadas ni infraestructura crítica.")
    lines.append("")

    if errors:
        lines.append("## Errores bloqueantes")
        lines.append("")
        for error in errors:
            lines.append(f"- {error}")
        lines.append("")

    if warnings:
        lines.append("## Avisos no bloqueantes")
        lines.append("")
        for warning in warnings[:200]:
            lines.append(f"- {warning}")
        if len(warnings) > 200:
            lines.append(f"- ... {len(warnings) - 200} avisos adicionales omitidos en el resumen.")
        lines.append("")

    return "\n".join(lines), len(errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered, error_count = render()

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"ERROR: falta {OUTPUT_PATH.relative_to(ROOT)}")
            return 1

        current = OUTPUT_PATH.read_text(encoding="utf-8")
        if current != rendered:
            tmp = Path("/tmp/distributor_hint_quality_audit.generated.md")
            tmp.write_text(rendered, encoding="utf-8")
            print("ERROR: auditoría de calidad de distribuidoras desactualizada.")
            print(f"Generado esperado en: {tmp}")
            print("Ejecuta: python3 scripts/generate_distributor_hint_quality_audit.py")
            return 1

        if error_count:
            print(f"ERROR: auditoría con {error_count} errores bloqueantes")
            return 1

        print("OK distributor hint quality audit actualizada")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")

    if error_count:
        print(f"WARN auditoría generada con {error_count} errores bloqueantes: {OUTPUT_PATH.relative_to(ROOT)}")
        return 1

    print(f"OK auditoría generada: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
