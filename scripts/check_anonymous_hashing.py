#!/usr/bin/env python3
import hashlib
import hmac
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")

errors = []

required_snippets = [
    "import hmac",
    "ANON_HASH_KEY",
    "def anon_hash(",
    "def anon_hash_candidates(",
    "token_hash = anon_hash(raw_token)",
    "ip_hash = anon_hash(raw_ip)",
    "assert_not_rate_limited(conn, token_hashes, ip_hashes)",
]

for snippet in required_snippets:
    if snippet not in main:
        errors.append(f"Falta snippet esperado: {snippet}")


if "def validate_report_preflight(conn, payload: ReportIn, token_hash: str, ip_hash: str, token_hashes, ip_hashes)" not in main:
    errors.append("validate_report_preflight debe recibir token_hashes/ip_hashes")

if "validate_report_preflight(conn, payload, token_hash, ip_hash, token_hashes, ip_hashes)" not in main:
    errors.append("report_preflight debe pasar token_hashes/ip_hashes a validate_report_preflight")

for forbidden in [
    "token_hash = sha256(payload.token.strip())",
    "ip_hash = sha256(client_ip(request))",
]:
    if forbidden in main:
        errors.append(f"Uso prohibido encontrado: {forbidden}")

def hmac_hash(key: str, value: str) -> str:
    return hmac.new(
        key.encode("utf-8"),
        f"mapa-apagones-anon-v1:{value}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

same_a = hmac_hash("key-a", "token-example")
same_b = hmac_hash("key-a", "token-example")
different = hmac_hash("key-b", "token-example")
plain = hashlib.sha256("token-example".encode("utf-8")).hexdigest()

if same_a != same_b:
    errors.append("HMAC no es determinista con misma clave y valor")

if same_a == different:
    errors.append("HMAC no cambia al cambiar la clave")

if same_a == plain:
    errors.append("HMAC coincide con sha256 plano, inesperado")

if errors:
    print("ERROR anonymous hashing guard")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK anonymous hashing guard")
