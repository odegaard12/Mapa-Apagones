#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
doc = ROOT / "docs/audit/advanced-audit-closeout.md"
readme = ROOT / "README.md"
errors = []

if not doc.exists():
    errors.append("Falta docs/audit/advanced-audit-closeout.md")
    text = ""
else:
    text = doc.read_text(encoding="utf-8")

required = [
    "Cierre de auditoría avanzada",
    "deriva de versión pública",
    "privacidad de hashes",
    "confianza en IP/proxy",
    "concurrencia de reportes",
    "reproducibilidad",
    "CI más serio",
    "#102",
    "#103",
    "#104",
    "#105",
    "#106",
    "#107",
    "#108",
    "#109",
    "#110",
    "#111",
    "#112",
    "#113",
    "#114",
    "#115",
    "#116",
    "#117",
    "#118",
    "#119",
    "no CUPS",
    "no IPs reales",
    "no tokens reales",
    "scripts/post_merge_validate.sh",
    "fase de corrección de auditoría avanzada queda cerrada",
]

for item in required:
    if item not in text:
        errors.append(f"Documento de cierre no contiene: {item}")

readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
if "docs/audit/advanced-audit-closeout.md" not in readme_text:
    errors.append("README no enlaza docs/audit/advanced-audit-closeout.md")

if errors:
    print("ERROR audit closeout guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK audit closeout guard")
