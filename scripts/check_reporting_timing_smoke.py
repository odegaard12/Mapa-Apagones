#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smoke_reporting_timing.py"

REQUIRED_TOKENS = [
    "smoke_backend_api.py",
    "smoke_backend_lifecycle.py",
    "smoke_backend_concurrency.py",
    "smoke_backend_privacy_abuse.py",
    "threshold",
    "elapsed",
    "OK reporting timing smoke",
]

FORBIDDEN_TOKENS = [
    "https://mapa-apagones.es",
    "https://api.mapa-apagones.es",
    "curl ",
]


def main() -> int:
    if not SCRIPT.exists():
        print(f"ERROR: falta {SCRIPT.relative_to(ROOT)}")
        return 1

    text = SCRIPT.read_text(encoding="utf-8")
    errors: list[str] = []

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"falta token requerido en timing smoke: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"token prohibido en timing smoke local: {token}")

    if errors:
        print("ERROR reporting timing smoke guard:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("OK reporting timing smoke guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
