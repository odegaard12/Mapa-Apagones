#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CANDIDATE_FILES = [
    ROOT / "frontend" / "public" / "data" / "distributor_hints.json",
    ROOT / "frontend" / "src" / "data" / "distributor_hints.json",
]

CUPS_RE = re.compile(r"\bES[0-9A-Z]{16,24}\b", re.IGNORECASE)

BANNED_KEY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"cups", re.IGNORECASE), "CUPS"),
    (re.compile(r"(?:^|_)(lat|lng|lon|latitude|longitude)(?:_|$)", re.IGNORECASE), "coordenadas"),
    (re.compile(r"coord", re.IGNORECASE), "coordenadas"),
    (re.compile(r"address|direccion|dirección|street|calle|rua|rúa|portal", re.IGNORECASE), "dirección exacta"),
    (re.compile(r"contador|meter|supply|suministro|contrato|factura", re.IGNORECASE), "dato de suministro/contrato"),
    (re.compile(r"ip_real|real_ip|token_real|raw_ip|raw_token", re.IGNORECASE), "IP/token real"),
    (re.compile(r"substation|subestaci[oó]n", re.IGNORECASE), "infraestructura crítica"),
    (re.compile(r"centro.*transformaci[oó]n|transformer|transformador", re.IGNORECASE), "infraestructura crítica"),
    (re.compile(r"feeder|alimentador|linea|línea|cable|poste|torre", re.IGNORECASE), "infraestructura crítica"),
]

BANNED_VALUE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (CUPS_RE, "CUPS"),
]


def iter_existing_files() -> list[Path]:
    return [path for path in CANDIDATE_FILES if path.exists()]


def location(path: list[str]) -> str:
    return ".".join(path) if path else "<root>"


def walk(value: Any, path: list[str], errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)

            for pattern, reason in BANNED_KEY_PATTERNS:
                if pattern.search(key_text):
                    errors.append(
                        f"Campo prohibido por {reason}: {location(path + [key_text])}"
                    )

            walk(child, path + [key_text], errors)

    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk(child, path + [str(index)], errors)

    elif isinstance(value, str):
        for pattern, reason in BANNED_VALUE_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"Valor prohibido por {reason}: {location(path)}"
                )


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: JSON inválido en {path.relative_to(ROOT)}: {exc}") from exc


def main() -> int:
    files = iter_existing_files()

    if not files:
        print("ERROR: no se encontró ningún distributor_hints.json conocido.")
        print("Rutas esperadas:")
        for path in CANDIDATE_FILES:
            print(f" - {path.relative_to(ROOT)}")
        return 1

    total_errors: list[str] = []

    for path in files:
        rel = path.relative_to(ROOT)
        data = load_json(path)
        errors: list[str] = []
        walk(data, [str(rel)], errors)

        if errors:
            total_errors.extend(errors)
        else:
            print(f"OK seguridad distribuidoras: {rel}")

    if total_errors:
        print("ERROR: se detectaron datos/campos no permitidos en distributor_hints:")
        for error in total_errors:
            print(f" - {error}")
        return 1

    print("OK: distributor_hints no contiene campos/patrones sensibles conocidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
