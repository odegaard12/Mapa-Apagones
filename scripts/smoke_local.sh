#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-http://127.0.0.1:8098}"

echo "== smoke: health =="
curl -fsS "$BASE/api/health"
echo

echo "== smoke: zones =="
curl -fsS "$BASE/api/zones?hours=24&include_resolved=0&limit=5" | python3 -m json.tool >/tmp/apagones-zones-smoke.json
head -80 /tmp/apagones-zones-smoke.json

echo
echo "== smoke: changelog version =="
curl -fsS "$BASE/changelog.html" | grep -n "v0.9" | head -10
