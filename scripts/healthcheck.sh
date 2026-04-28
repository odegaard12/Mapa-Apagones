#!/usr/bin/env bash
set -euo pipefail

HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8098/api/health}"
TIMEOUT_SEC="${TIMEOUT_SEC:-5}"

python3 - "$HEALTH_URL" "$TIMEOUT_SEC" <<'PY'
import json
import sys
import urllib.request

url = sys.argv[1]
timeout = float(sys.argv[2])

try:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        body = response.read().decode("utf-8")
        data = json.loads(body)
        if response.status != 200 or data.get("ok") is not True:
            raise SystemExit(1)
except Exception as exc:
    print(f"healthcheck failed: {exc}", file=sys.stderr)
    raise SystemExit(1)

print("ok")
PY
