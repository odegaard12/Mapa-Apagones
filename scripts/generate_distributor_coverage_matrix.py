#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "frontend" / "public" / "data"
HINTS_PATH = DATA_DIR / "distributor_hints.json"
OUTPUT_PATH = ROOT / "docs" / "research" / "distributor_coverage_matrix.md"

DATASET_ORDER = [
    "galicia",
    "asturias",
    "cantabria",
    "navarra",
    "la_rioja",
    "murcia",
    "canarias",
    "illes_balears",
    "ceuta",
    "melilla",
    "madrid",
    "euskadi",
    "comunitat_valenciana",
    "aragon",
    "extremadura",
    "castilla_la_mancha",
    "castilla_leon",
    "andalucia",
    "catalunya",
]

DATASET_LABELS = {
    "galicia": "Galicia",
    "asturias": "Asturias",
    "cantabria": "Cantabria",
    "navarra": "Navarra",
    "la_rioja": "La Rioja",
    "murcia": "Región de Murcia",
    "canarias": "Canarias",
    "illes_balears": "Illes Balears",
    "ceuta": "Ceuta",
    "melilla": "Melilla",
    "madrid": "Madrid",
    "euskadi": "Euskadi",
    "comunitat_valenciana": "Comunitat Valenciana",
    "aragon": "Aragón",
    "extremadura": "Extremadura",
    "castilla_la_mancha": "Castilla-La Mancha",
    "castilla_leon": "Castilla y León",
    "andalucia": "Andalucía",
    "catalunya": "Catalunya",
}

DATASET_ALIASES = {
    "region_de_murcia": "murcia",
    "murcia_region": "murcia",
    "comunidad_de_madrid": "madrid",
    "madrid_comunidad": "madrid",
    "comunidad_valenciana": "comunitat_valenciana",
    "valenciana": "comunitat_valenciana",
    "pais_vasco": "euskadi",
    "vasco": "euskadi",
    "islas_baleares": "illes_balears",
    "baleares": "illes_balears",
    "illes_balears": "illes_balears",
    "castilla_y_leon": "castilla_leon",
    "castilla_leon": "castilla_leon",
    "castilla_la_mancha": "castilla_la_mancha",
    "la_rioja": "la_rioja",
}

DATASET_KEYS = [
    "dataset_id",
    "dataset",
    "datasetId",
    "scope_id",
    "scope",
    "community_id",
    "comunidad_id",
    "autonomia_id",
    "ccaa_id",
    "region_id",
    "region",
]

ZONE_KEYS = [
    "zone_id",
    "id",
    "municipality_id",
    "municipio_id",
    "zone",
    "zona",
    "slug",
]

CONFIDENCE_KEYS = [
    "confidence",
    "confidence_level",
    "confidence_type",
    "status",
]

LAST_REVIEWED_KEYS = [
    "last_reviewed",
    "reviewed_at",
    "fecha_revision",
    "fecha_revisión",
]

SOURCE_KEYS = [
    "sources",
    "source",
    "fuentes",
    "fuente",
]

DISTRIBUTOR_KEYS = [
    "distributor",
    "distributor_name",
    "distribuidora",
    "distribuidoras",
    "distributors",
    "operator",
    "operators",
]


def slug(value: Any = "") -> str:
    text = (
        unicodedata.normalize("NFD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def get_first(entry: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        value = entry.get(key)
        if value not in (None, "", []):
            return value
    return None


def normalise_dataset(value: Any) -> str:
    raw = slug(value)
    return DATASET_ALIASES.get(raw, raw)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_geo_counts() -> dict[str, int]:
    counts: dict[str, int] = {}

    for path in sorted(DATA_DIR.glob("*_municipios.geojson")):
        if path.name == "toda_espana_municipios.geojson":
            continue

        dataset_id = path.name.replace("_municipios.geojson", "")
        data = load_json(path)
        features = data.get("features") or []
        counts[dataset_id] = len(features)

    return counts


def looks_like_hint(entry: dict[str, Any]) -> bool:
    keys = set(entry.keys())

    has_dataset = any(key in keys for key in DATASET_KEYS)
    has_zone = any(key in keys for key in ZONE_KEYS)
    has_distributor = any(key in keys for key in DISTRIBUTOR_KEYS)
    has_confidence = any(key in keys for key in CONFIDENCE_KEYS)

    return (has_distributor or has_confidence) and (has_dataset or has_zone)


def collect_hint_entries(node: Any, inherited_key: str | None = None) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    if isinstance(node, list):
        for child in node:
            entries.extend(collect_hint_entries(child))
        return entries

    if isinstance(node, dict):
        candidate = dict(node)

        if inherited_key and not get_first(candidate, ZONE_KEYS):
            candidate["zone_id"] = inherited_key

        if looks_like_hint(candidate):
            entries.append(candidate)
            return entries

        for key, child in node.items():
            entries.extend(collect_hint_entries(child, str(key)))

    return entries


def load_hint_entries() -> list[dict[str, Any]]:
    data = load_json(HINTS_PATH)
    entries = collect_hint_entries(data)

    if not entries:
        raise SystemExit(f"ERROR: no se pudieron detectar entradas de distribuidora en {HINTS_PATH.relative_to(ROOT)}")

    return entries


def confidence_label(value: Any) -> str:
    if value in (None, "", []):
        return "sin_confianza_explicita"
    return slug(value) or "sin_confianza_explicita"


def nested_distributors(entry: dict[str, Any]) -> list[dict[str, Any]]:
    distributors: list[dict[str, Any]] = []

    for key in DISTRIBUTOR_KEYS:
        value = entry.get(key)

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    distributors.append(item)
                elif item not in (None, ""):
                    distributors.append({"name": str(item)})

        elif isinstance(value, dict):
            distributors.append(value)

        elif value not in (None, ""):
            distributors.append({"name": str(value)})

    return distributors


def has_value(entry: dict[str, Any], keys: list[str]) -> bool:
    if get_first(entry, keys) not in (None, "", []):
        return True

    for distributor in nested_distributors(entry):
        if get_first(distributor, keys) not in (None, "", []):
            return True

    return False


def confidence_labels(entry: dict[str, Any]) -> list[str]:
    top_level = get_first(entry, CONFIDENCE_KEYS)

    if top_level not in (None, "", []):
        return [confidence_label(top_level)]

    labels: list[str] = []

    for distributor in nested_distributors(entry):
        value = get_first(distributor, CONFIDENCE_KEYS)
        if value not in (None, "", []):
            labels.append(confidence_label(value))

    return labels or ["sin_confianza_explicita"]


def build_stats() -> dict[str, Any]:
    geo_counts = load_geo_counts()
    hint_entries = load_hint_entries()

    zones_by_dataset: dict[str, set[str]] = defaultdict(set)
    confidence_by_dataset: dict[str, Counter[str]] = defaultdict(Counter)
    reviewed_by_dataset: dict[str, set[str]] = defaultdict(set)
    sourced_by_dataset: dict[str, set[str]] = defaultdict(set)
    unknown_entries: list[dict[str, Any]] = []

    for index, entry in enumerate(hint_entries):
        dataset_value = get_first(entry, DATASET_KEYS)
        dataset_id = normalise_dataset(dataset_value) if dataset_value is not None else "unknown"

        zone_value = get_first(entry, ZONE_KEYS)
        zone_id = str(zone_value) if zone_value not in (None, "") else f"{dataset_id}::__entry_{index}"

        if dataset_id == "unknown":
            unknown_entries.append(entry)

        zones_by_dataset[dataset_id].add(zone_id)

        for confidence in confidence_labels(entry):
            confidence_by_dataset[dataset_id][confidence] += 1

        if has_value(entry, LAST_REVIEWED_KEYS):
            reviewed_by_dataset[dataset_id].add(zone_id)

        if has_value(entry, SOURCE_KEYS):
            sourced_by_dataset[dataset_id].add(zone_id)

    ordered_datasets = [item for item in DATASET_ORDER if item in geo_counts]
    ordered_datasets.extend(sorted(set(geo_counts) - set(ordered_datasets)))

    rows = []

    for dataset_id in ordered_datasets:
        geo_total = geo_counts.get(dataset_id, 0)
        hint_total = len(zones_by_dataset.get(dataset_id, set()))
        pending = max(geo_total - hint_total, 0)
        coverage = (hint_total / geo_total * 100) if geo_total else 0.0

        if hint_total == 0:
            state = "pendiente"
        elif hint_total < geo_total:
            state = "parcial"
        elif hint_total == geo_total:
            state = "con pista en todas las zonas"
        else:
            state = "revisar: más pistas que zonas geográficas"

        rows.append(
            {
                "dataset_id": dataset_id,
                "label": DATASET_LABELS.get(dataset_id, dataset_id),
                "geo_total": geo_total,
                "hint_total": hint_total,
                "pending": pending,
                "coverage": coverage,
                "state": state,
                "confidence": confidence_by_dataset.get(dataset_id, Counter()),
                "reviewed": len(reviewed_by_dataset.get(dataset_id, set())),
                "sourced": len(sourced_by_dataset.get(dataset_id, set())),
            }
        )

    total_geo = sum(geo_counts.values())
    total_hints_known = sum(len(zones_by_dataset.get(dataset_id, set())) for dataset_id in geo_counts)
    total_pending = sum(max(row["geo_total"] - row["hint_total"], 0) for row in rows)
    total_coverage = (total_hints_known / total_geo * 100) if total_geo else 0.0

    return {
        "geo_counts": geo_counts,
        "hint_entries": hint_entries,
        "zones_by_dataset": zones_by_dataset,
        "confidence_by_dataset": confidence_by_dataset,
        "unknown_entries": unknown_entries,
        "rows": rows,
        "total_geo": total_geo,
        "total_hints_known": total_hints_known,
        "total_pending": total_pending,
        "total_coverage": total_coverage,
    }


def fmt_int(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def fmt_percent(value: float) -> str:
    return f"{value:.1f}%".replace(".", ",")


def fmt_counter(counter: Counter[str]) -> str:
    if not counter:
        return "—"

    parts = []
    for key, value in sorted(counter.items()):
        parts.append(f"`{key}` {value}")
    return ", ".join(parts)


def render_markdown() -> str:
    stats = build_stats()
    rows = stats["rows"]

    generated = date.today().isoformat()

    lines: list[str] = []

    lines.append("# Matriz de cobertura de pistas de distribuidoras")
    lines.append("")
    lines.append(f"Generado desde los datos reales del repositorio el {generated}.")
    lines.append("")
    lines.append("> Esta matriz mide cobertura de **pistas públicas de distribuidora en el repositorio**, no cobertura eléctrica real ni exclusividad de red.")
    lines.append("")
    lines.append("## Resumen")
    lines.append("")
    lines.append(f"- Datasets geográficos autonómicos: **{fmt_int(len(stats['geo_counts']))}**.")
    lines.append(f"- Municipios/zonas normalizadas en GeoJSON: **{fmt_int(stats['total_geo'])}**.")
    lines.append(f"- Municipios/zonas con pista pública de distribuidora: **{fmt_int(stats['total_hints_known'])}**.")
    lines.append(f"- Municipios/zonas pendientes de pista pública: **{fmt_int(stats['total_pending'])}**.")
    lines.append(f"- Cobertura actual de pistas públicas: **{fmt_percent(stats['total_coverage'])}**.")
    lines.append("")
    lines.append("## Matriz por comunidad/dataset")
    lines.append("")
    lines.append("| Zona | Dataset | GeoJSON | Con pista | Pendiente | Cobertura | Estado | Confianza | Con fecha | Con fuente |")
    lines.append("|---|---:|---:|---:|---:|---:|---|---|---:|---:|")

    for row in rows:
        lines.append(
            "| "
            f"{row['label']} | "
            f"`{row['dataset_id']}` | "
            f"{fmt_int(row['geo_total'])} | "
            f"{fmt_int(row['hint_total'])} | "
            f"{fmt_int(row['pending'])} | "
            f"{fmt_percent(row['coverage'])} | "
            f"{row['state']} | "
            f"{fmt_counter(row['confidence'])} | "
            f"{fmt_int(row['reviewed'])} | "
            f"{fmt_int(row['sourced'])} |"
        )

    lines.append("")
    lines.append("## Zonas pendientes ordenadas por volumen")
    lines.append("")
    lines.append("| Zona | Pendientes | GeoJSON | Con pista |")
    lines.append("|---|---:|---:|---:|")

    for row in sorted(rows, key=lambda item: item["pending"], reverse=True):
        if row["pending"] <= 0:
            continue

        lines.append(
            "| "
            f"{row['label']} | "
            f"{fmt_int(row['pending'])} | "
            f"{fmt_int(row['geo_total'])} | "
            f"{fmt_int(row['hint_total'])} |"
        )

    lines.append("")
    lines.append("## Lectura recomendada")
    lines.append("")
    lines.append("- Priorizar PRs pequeños y verificables.")
    lines.append("- No importar comunidades completas si hay dudas de excepciones locales.")
    lines.append("- Mantener `regional_default` como pista orientativa, no como afirmación de exclusividad.")
    lines.append("- Mantener `verified_partial` para presencia pública razonablemente verificada pero no exclusiva.")
    lines.append("- Cuando no haya fuente pública suficiente, mantener fallback sin pista.")
    lines.append("")
    lines.append("## Seguridad y privacidad")
    lines.append("")
    lines.append("Esta matriz no contiene CUPS, cuentas, texto libre de usuarios, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, contratos, facturas ni inventario de infraestructura crítica.")
    lines.append("")
    lines.append("La matriz se debe regenerar con:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/generate_distributor_coverage_matrix.py")
    lines.append("```")
    lines.append("")
    lines.append("Y validar con:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/generate_distributor_coverage_matrix.py --check")
    lines.append("```")
    lines.append("")

    if stats["unknown_entries"]:
        lines.append("## Avisos")
        lines.append("")
        lines.append(f"- Hay **{fmt_int(len(stats['unknown_entries']))}** entradas de distribuidora sin dataset identificable. Revisar antes de nuevas importaciones.")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Comprueba que la matriz generada está actualizada")
    args = parser.parse_args()

    rendered = render_markdown()

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"ERROR: falta {OUTPUT_PATH.relative_to(ROOT)}")
            return 1

        current = OUTPUT_PATH.read_text(encoding="utf-8")

        if current != rendered:
            tmp_path = Path("/tmp/distributor_coverage_matrix.generated.md")
            tmp_path.write_text(rendered, encoding="utf-8")
            print("ERROR: la matriz de cobertura de distribuidoras no está actualizada.")
            print(f"Generado esperado en: {tmp_path}")
            print("Ejecuta: python3 scripts/generate_distributor_coverage_matrix.py")
            return 1

        print("OK distributor coverage matrix actualizada")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"OK matriz generada: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
