#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
privacy_path = ROOT / "backend/app/privacy.py"

errors = []

if not privacy_path.exists():
    errors.append("Falta backend/app/privacy.py")
    privacy = ""
else:
    privacy = privacy_path.read_text(encoding="utf-8")

required_privacy = [
    "import hmac",
    "def anonymization_secret(",
    "def anon_hash(",
    "def anon_hash_candidates(",
    "def normalize_hash_values(",
    "def sql_in_clause(",
    "mapa-apagones-anon-v1:",
    "ANON_HASH_KEY",
    "ANON_HASH_LEGACY_COMPAT",
    "ANON_HASH_KEY_REQUIRED",
    "ANON_HASH_DEV_FALLBACK",
]

for snippet in required_privacy:
    if snippet not in privacy:
        errors.append(f"privacy.py no contiene {snippet}")

required_main = [
    "from app.privacy import (",
    "anon_hash,",
    "anon_hash_candidates,",
    "normalize_hash_values,",
    "sql_in_clause,",
    "token_hash = anon_hash(raw_token)",
    "ip_hash = anon_hash(raw_ip)",
    "token_hashes = anon_hash_candidates(raw_token)",
    "ip_hashes = anon_hash_candidates(raw_ip)",
]

for snippet in required_main:
    if snippet not in main:
        errors.append(f"main.py no contiene {snippet}")

for forbidden in [
    "def anonymization_secret(",
    "def anon_hash(",
    "def anon_hash_candidates(",
    "def normalize_hash_values(",
    "def sql_in_clause(",
]:
    if forbidden in main:
        errors.append(f"helper de privacidad duplicado en main.py: {forbidden}")

if "token_hash = sha256(payload.token.strip())" in main:
    errors.append("main.py vuelve a calcular token_hash con sha256 plano")

if "ip_hash = sha256(client_ip(request))" in main:
    errors.append("main.py vuelve a calcular ip_hash con sha256 plano")

if errors:
    print("ERROR backend privacy module guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK backend privacy module guard")
