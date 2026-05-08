#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

compose = ROOT / "docker-compose.ci.yml"
smoke = ROOT / "scripts/smoke_docker_compose.sh"
ci = ROOT / ".github/workflows/ci.yml"

if not compose.exists():
    errors.append("Falta docker-compose.ci.yml")
else:
    text = compose.read_text(encoding="utf-8")
    for snippet in [
        "services:",
        "backend:",
        "web:",
        "SMOKE_WEB_PORT",
        "ANON_HASH_KEY",
        "TURNSTILE_ENABLED",
        "IGN_WFS_ENABLED",
    ]:
        if snippet not in text:
            errors.append(f"docker-compose.ci.yml no contiene: {snippet}")
    if "container_name:" in text:
        errors.append("docker-compose.ci.yml no debe fijar container_name para evitar conflictos locales/CI")

if not smoke.exists():
    errors.append("Falta scripts/smoke_docker_compose.sh")
else:
    text = smoke.read_text(encoding="utf-8")
    for snippet in [
        "docker compose",
        "docker-compose.ci.yml",
        "/api/health",
        "/api/report",
        "/api/incidents",
        "/data/distributor_hints.json",
    ]:
        if snippet not in text:
            errors.append(f"smoke_docker_compose.sh no contiene: {snippet}")

if not ci.exists():
    errors.append("Falta .github/workflows/ci.yml")
else:
    text = ci.read_text(encoding="utf-8")
    if "scripts/smoke_docker_compose.sh" not in text:
        errors.append("CI no ejecuta scripts/smoke_docker_compose.sh")

if errors:
    print("ERROR docker compose smoke guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK docker compose smoke guard")
