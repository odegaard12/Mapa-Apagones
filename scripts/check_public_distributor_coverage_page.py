#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "frontend" / "public" / "cobertura-distribuidoras.html"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

REQUIRED_TOKENS = [
    VERSION,
    "Cobertura pública de distribuidoras",
    "No pedimos CUPS",
    "No afirma exclusividad",
    "regional_default",
    "verified_partial",
    "Matriz por comunidad",
    "https://mapa-apagones.es/cobertura-distribuidoras.html",
]

FORBIDDEN_TOKENS = [
    "/api/report",
    "reporter_token_hash",
    "ip_hash",
    "ANON_HASH_KEY",
    "TURNSTILE_SECRET",
    "BEGIN PRIVATE KEY",
    "PRIVATE KEY",
]


def main() -> int:
    if not PAGE.exists():
        print(f"ERROR: falta {PAGE.relative_to(ROOT)}")
        return 1

    text = PAGE.read_text(encoding="utf-8")
    errors: list[str] = []

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"falta token requerido: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"token prohibido en página pública: {token}")

    if errors:
        print("ERROR public distributor coverage page guard:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("OK public distributor coverage page guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
