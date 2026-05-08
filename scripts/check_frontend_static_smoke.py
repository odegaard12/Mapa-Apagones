#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

smoke = ROOT / "scripts/smoke_frontend_static.py"
ci = ROOT / ".github/workflows/ci.yml"

if not smoke.exists():
    errors.append("Falta scripts/smoke_frontend_static.py")
else:
    text = smoke.read_text(encoding="utf-8")
    for snippet in [
        "frontend",
        "dist",
        "index.html",
        "changelog.html",
        "robots.txt",
        "sitemap.xml",
        "distributor_hints.json",
        "VERSION",
        "OK frontend static smoke",
    ]:
        if snippet not in text:
            errors.append(f"smoke_frontend_static.py no contiene: {snippet}")

if not ci.exists():
    errors.append("Falta .github/workflows/ci.yml")
else:
    text = ci.read_text(encoding="utf-8")
    if "scripts/smoke_frontend_static.py" not in text:
        errors.append("CI no ejecuta scripts/smoke_frontend_static.py")

if errors:
    print("ERROR frontend static smoke guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK frontend static smoke guard")
