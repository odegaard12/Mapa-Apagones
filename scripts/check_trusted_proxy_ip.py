#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
nginx = (ROOT / "frontend/nginx.conf").read_text(encoding="utf-8")

errors = []

required_main = [
    "import ipaddress",
    "TRUST_PROXY_HEADERS",
    "TRUSTED_PROXY_CIDRS",
    "def is_trusted_proxy(",
    "def first_header_ip(",
    "if TRUST_PROXY_HEADERS and is_trusted_proxy(remote_host):",
    '"x-real-ip"',
    '"x-forwarded-for"',
]

for snippet in required_main:
    if snippet not in main:
        errors.append(f"Falta en backend/app/main.py: {snippet}")

for forbidden in [
    'forwarded = request.headers.get("x-forwarded-for"',
    "if forwarded:\n        return forwarded",
]:
    if forbidden in main:
        errors.append(f"Patrón inseguro encontrado: {forbidden}")

for snippet in ["TRUST_PROXY_HEADERS", "TRUSTED_PROXY_CIDRS"]:
    if snippet not in compose:
        errors.append(f"Falta en docker-compose.yml: {snippet}")
    if snippet not in env_example:
        errors.append(f"Falta en .env.example: {snippet}")

for snippet in [
    "proxy_set_header X-Forwarded-For $remote_addr;",
    "proxy_set_header X-Real-IP $remote_addr;",
]:
    if snippet not in nginx:
        errors.append(f"Falta en frontend/nginx.conf: {snippet}")

if errors:
    print("ERROR trusted proxy IP guard")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK trusted proxy IP guard")
