#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

smoke = ROOT / "scripts/smoke_backend_privacy_abuse.py"
ci = ROOT / ".github/workflows/ci.yml"

if not smoke.exists():
    errors.append("Falta scripts/smoke_backend_privacy_abuse.py")
else:
    text = smoke.read_text(encoding="utf-8")
    for snippet in [
        "/api/health",
        "/api/report",
        "ANON_HASH_KEY",
        "ANON_HASH_KEY_REQUIRED",
        "ANON_HASH_LEGACY_COMPAT",
        "reporter_token_hash",
        "ip_hash",
        "rate_limit_status",
        "429",
        "assert_no_raw_values",
    ]:
        if snippet not in text:
            errors.append(f"smoke_backend_privacy_abuse.py no contiene: {snippet}")

if not ci.exists():
    errors.append("Falta .github/workflows/ci.yml")
else:
    text = ci.read_text(encoding="utf-8")
    if "scripts/smoke_backend_privacy_abuse.py" not in text:
        errors.append("CI no ejecuta scripts/smoke_backend_privacy_abuse.py")

if errors:
    print("ERROR backend privacy/abuse smoke guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK backend privacy/abuse smoke guard")
