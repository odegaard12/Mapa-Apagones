#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

DATA_PATH = Path("frontend/src/data/distributor_hints.json")

ALLOWED_CONFIDENCE = {
    "verified_municipal",
    "verified_partial",
    "regional_default",
    "unknown",
}

REQUIRED_ITEM_FIELDS = {
    "zone_id",
    "municipio",
    "province",
    "dataset_id",
    "distributors",
}

ALLOWED_ITEM_FIELDS = REQUIRED_ITEM_FIELDS | {
    "notes",
    "last_reviewed",
}

REQUIRED_DISTRIBUTOR_FIELDS = {
    "name",
    "confidence",
    "source_name",
    "source_url",
    "last_reviewed",
}

ALLOWED_DISTRIBUTOR_FIELDS = REQUIRED_DISTRIBUTOR_FIELDS | {
    "r1_code",
    "outage_phone",
    "website",
    "coverage_note",
}

BANNED_KEYS = {
    "cups",
    "address",
    "direccion",
    "dirección",
    "email",
    "mail",
    "dni",
    "nif_personal",
    "lat",
    "lng",
    "lon",
    "latitude",
    "longitude",
    "substation",
    "subestacion",
    "subestación",
    "power_line",
    "linea",
    "línea",
    "cable",
    "cableado",
    "transformer",
    "transformador",
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def assert_safe_keys(obj, where: str) -> None:
    for key in obj:
        if str(key).strip().lower() in BANNED_KEYS:
            fail(f"campo prohibido {key!r} en {where}")


def assert_string(value, where: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{where} debe ser string no vacío")


def main() -> None:
    if not DATA_PATH.exists():
        fail(f"no existe {DATA_PATH}")

    data = json.loads(DATA_PATH.read_text())

    if not isinstance(data, dict):
        fail("el dataset raíz debe ser objeto JSON")

    assert_safe_keys(data, "raíz")

    items = data.get("items")
    if not isinstance(items, list):
        fail("items debe ser lista")

    seen = set()

    for idx, item in enumerate(items):
        where = f"items[{idx}]"

        if not isinstance(item, dict):
            fail(f"{where} debe ser objeto")

        assert_safe_keys(item, where)

        extra = set(item) - ALLOWED_ITEM_FIELDS
        missing = REQUIRED_ITEM_FIELDS - set(item)

        if extra:
            fail(f"{where} tiene campos no permitidos: {sorted(extra)}")
        if missing:
            fail(f"{where} no tiene campos obligatorios: {sorted(missing)}")

        for field in ("zone_id", "municipio", "province", "dataset_id"):
            assert_string(item[field], f"{where}.{field}")

        if not item["zone_id"].startswith("municipality:"):
            fail(f"{where}.zone_id debe empezar por municipality:")

        distributors = item["distributors"]
        if not isinstance(distributors, list) or not distributors:
            fail(f"{where}.distributors debe ser lista no vacía")

        for d_idx, distributor in enumerate(distributors):
            d_where = f"{where}.distributors[{d_idx}]"

            if not isinstance(distributor, dict):
                fail(f"{d_where} debe ser objeto")

            assert_safe_keys(distributor, d_where)

            extra = set(distributor) - ALLOWED_DISTRIBUTOR_FIELDS
            missing = REQUIRED_DISTRIBUTOR_FIELDS - set(distributor)

            if extra:
                fail(f"{d_where} tiene campos no permitidos: {sorted(extra)}")
            if missing:
                fail(f"{d_where} no tiene campos obligatorios: {sorted(missing)}")

            for field in ("name", "confidence", "source_name", "source_url", "last_reviewed"):
                assert_string(distributor[field], f"{d_where}.{field}")

            if distributor["confidence"] not in ALLOWED_CONFIDENCE:
                fail(f"{d_where}.confidence no permitido: {distributor['confidence']}")

            if not distributor["source_url"].startswith(("https://", "http://")):
                fail(f"{d_where}.source_url debe ser URL pública")

            if not DATE_RE.match(distributor["last_reviewed"]):
                fail(f"{d_where}.last_reviewed debe ser YYYY-MM-DD")

            key = (
                item["zone_id"],
                distributor["name"].strip().lower(),
                distributor.get("r1_code", "").strip().lower(),
                distributor.get("coverage_note", "").strip().lower(),
            )

            if key in seen:
                fail(f"duplicado de distribuidora en {where}: {key}")

            seen.add(key)

    if not items:
        print("OK distributor hints: dataset inicial vacío, sin datos dudosos")
    else:
        print(f"OK distributor hints: {len(items)} zonas con pistas verificadas")


if __name__ == "__main__":
    main()
