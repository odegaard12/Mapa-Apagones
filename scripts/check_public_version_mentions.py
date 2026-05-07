#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

errors = []

app = (ROOT / "frontend/src/App.jsx").read_text(encoding="utf-8")
match = re.search(r"const APP_VERSION = '([^']+)'", app)
if not match:
    errors.append("No encuentro APP_VERSION en frontend/src/App.jsx")
elif match.group(1) != version:
    errors.append(f"APP_VERSION no coincide: {match.group(1)} != {version}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
match = re.search(r"^Versión actual visible:\s*(.+?)\.?\s*$", readme, re.MULTILINE)
if not match:
    errors.append("No encuentro 'Versión actual visible' en README.md")
else:
    readme_version = match.group(1).strip()
    if readme_version != version:
        errors.append(f"README versión visible no coincide: {readme_version} != {version}")

changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
first_heading = re.search(r"^##\s+(.+)$", changelog, re.MULTILINE)
if not first_heading:
    errors.append("No encuentro primera versión en CHANGELOG.md")
elif first_heading.group(1).strip() != version:
    errors.append(f"CHANGELOG no empieza por VERSION: {first_heading.group(1).strip()} != {version}")

public_changelog = (ROOT / "frontend/public/changelog.html").read_text(encoding="utf-8")
if f"<h2>{version}</h2>" not in public_changelog:
    errors.append(f"frontend/public/changelog.html no contiene <h2>{version}</h2>")

if errors:
    print("ERROR: deriva de versión pública detectada")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"OK public version guard: {version}")
