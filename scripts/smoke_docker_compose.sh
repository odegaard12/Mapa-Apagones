#!/usr/bin/env bash
set -euo pipefail

PORT="${SMOKE_WEB_PORT:-18098}"
PROJECT="${SMOKE_PROJECT_NAME:-apagones_ci_smoke_$$}"
BASE_URL="http://127.0.0.1:${PORT}"

compose() {
  SMOKE_WEB_PORT="$PORT" docker compose -p "$PROJECT" -f docker-compose.ci.yml "$@"
}

cleanup() {
  compose down -v --remove-orphans >/dev/null 2>&1 || true
}

trap cleanup EXIT

echo "== Docker Compose smoke project: $PROJECT =="
cleanup

echo "== Compose config =="
compose config >/dev/null

echo "== Build + up =="
compose up -d --build

echo "== Wait /api/health through web proxy =="
last_error=""
for i in $(seq 1 60); do
  if curl -fsS "${BASE_URL}/api/health" >/tmp/apagones_compose_health.json; then
    python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/apagones_compose_health.json").read_text())
if data.get("ok") is not True:
    raise SystemExit(f"health no ok: {data}")
print("OK docker compose health")
PY
    break
  fi
  last_error="health not ready ${i}"
  sleep 1
done

if ! curl -fsS "${BASE_URL}/api/health" >/dev/null; then
  echo "ERROR: backend/web no respondió a /api/health: ${last_error}"
  compose ps
  compose logs --tail=120
  exit 1
fi

echo "== Check frontend index =="
curl -fsS "${BASE_URL}/" >/tmp/apagones_compose_index.html
grep -qi "<html" /tmp/apagones_compose_index.html

echo "== Check distributor public JSON =="
curl -fsS "${BASE_URL}/data/distributor_hints.json" >/tmp/apagones_compose_distributor_hints.json
python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/apagones_compose_distributor_hints.json").read_text())
items = data.get("items", [])
if not isinstance(items, list) or len(items) < 1000:
    raise SystemExit(f"distributor_hints inesperado: {len(items)} items")
print(f"OK distributor_hints public JSON: {len(items)} items")
PY

echo "== Check report flow through web proxy =="
BASE_URL="$BASE_URL" python3 - <<'PY'
import json
import os
import time
from urllib.request import Request, urlopen

base = os.environ["BASE_URL"]
token = f"compose-smoke-token-{int(time.time())}-0000000000000000"
payload = {
    "lat": 42.8782,
    "lng": -8.5448,
    "type": "sin_luz",
    "token": token,
}

def request_json(method, path, body=None):
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(base + path, data=data, headers=headers, method=method)
    with urlopen(req, timeout=8) as resp:
        raw = resp.read().decode("utf-8")
        return resp.status, json.loads(raw or "{}")

status, report = request_json("POST", "/api/report", payload)
if status != 200:
    raise SystemExit(f"report status inesperado: {status} {report}")

status, incidents = request_json("GET", "/api/incidents")
if status != 200:
    raise SystemExit(f"incidents status inesperado: {status} {incidents}")

print("OK docker compose report flow")
PY

echo "== Docker Compose smoke OK =="
compose ps
