#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

smoke = ROOT / "scripts/smoke_backend_lifecycle.py"
ci = ROOT / ".github/workflows/ci.yml"

if not smoke.exists():
    errors.append("Falta scripts/smoke_backend_lifecycle.py")
else:
    text = smoke.read_text(encoding="utf-8")
    for snippet in [
        "/api/health",
        "/api/report",
        "/api/incidents",
        "tipo_invalido",
        "microcortes",
        "vuelve",
        "report_count_active",
        "unique_reporters_active",
    ]:
        if snippet not in text:
            errors.append(f"smoke_backend_lifecycle.py no contiene: {snippet}")

if not ci.exists():
    errors.append("Falta .github/workflows/ci.yml")
else:
    text = ci.read_text(encoding="utf-8")
    if "scripts/smoke_backend_lifecycle.py" not in text:
        errors.append("CI no ejecuta scripts/smoke_backend_lifecycle.py")

if errors:
    print("ERROR backend lifecycle smoke guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK backend lifecycle smoke guard")
