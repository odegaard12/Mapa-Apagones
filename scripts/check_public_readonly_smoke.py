#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smoke_public_readonly.sh"

FORBIDDEN_TOKENS = [
    " -X POST",
    "--request POST",
    "curl -X POST",
    "/api/report ",
    "/api/report'",
    '/api/report"',
    "/api/report?",
    "api/report",
]

REQUIRED_TOKENS = [
    "curl -fsSL",
    "/changelog.html",
    "/data/distributor_hints.json",
    "/api/health",
    "/api/status",
    "/api/incidents?limit=5",
    "EXPECTED_DISTRIBUTOR_HINTS_ITEMS",
]


def main() -> int:
    if not SCRIPT.exists():
        print(f"ERROR: falta {SCRIPT.relative_to(ROOT)}")
        return 1

    text = SCRIPT.read_text(encoding="utf-8")
    errors: list[str] = []

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"falta token requerido en smoke público: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"token prohibido en smoke público read-only: {token}")

    if errors:
        print("ERROR public readonly smoke guard:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("OK public readonly smoke guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
