#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
errors = []

required = [
    '@app.get("/api/status")',
    "def api_status(",
    '"service": "mapa-apagones-api"',
    '"anonymous_hashing": "hmac-sha256"',
    '"stores_raw_ip": False',
    '"stores_raw_token": False',
    '"anon_hash_key_configured": bool(ANON_HASH_KEY)',
    '"trusted_proxy_cidrs_configured": bool(TRUSTED_PROXY_CIDRS)',
]

for snippet in required:
    if snippet not in main:
        errors.append(f"Falta snippet esperado: {snippet}")

start = main.find('@app.get("/api/status")')
status_block = main[start:] if start != -1 else ""

# No debe devolver variables secretas directamente.
danger_patterns = [
    r'"[^"]*secret[^"]*"\s*:\s*TURNSTILE_SECRET_KEY',
    r'"[^"]*key[^"]*"\s*:\s*ANON_HASH_KEY\s*[,}]',
    r'"db_path"\s*:\s*DB_PATH',
    r'"trusted_proxy_cidrs"\s*:\s*TRUSTED_PROXY_CIDRS',
    r'"client_ip"',
    r'"raw_ip"',
    r'"raw_token"',
]

for pattern in danger_patterns:
    if re.search(pattern, status_block, flags=re.IGNORECASE):
        errors.append(f"Patrón peligroso en /api/status: {pattern}")

if errors:
    print("ERROR safe status endpoint guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK safe status endpoint guard")
