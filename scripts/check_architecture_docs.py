#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
doc = ROOT / "docs/architecture/reporting-privacy-pipeline.md"

errors = []

if not doc.exists():
    errors.append("Falta docs/architecture/reporting-privacy-pipeline.md")
else:
    text = doc.read_text(encoding="utf-8").lower()
    required = [
        "sin cuentas",
        "sin login",
        "sin cups",
        "sin texto libre",
        "sin fotos",
        "hmac-sha256",
        "anon_hash_key",
        "trust_proxy_headers",
        "trusted_proxy_cidrs",
        "begin immediate",
        "turnstile",
        "sqlite",
        "no se guarda la ip real",
        "no se guarda el token real",
        "no se publican direcciones exactas",
        "no se publica infraestructura crítica",
        "smoke_backend_api.py",
        "smoke_backend_privacy_abuse.py",
        "smoke_docker_compose.sh",
    ]
    for item in required:
        if item not in text:
            errors.append(f"Documento de arquitectura no contiene: {item}")

    forbidden = [
        "cups reales como dato",
        "supply_id",
        "dirección exacta del usuario",
    ]
    for item in forbidden:
        if item in text:
            errors.append(f"Documento contiene expresión peligrosa/no deseada: {item}")

if errors:
    print("ERROR architecture docs guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK architecture docs guard")
