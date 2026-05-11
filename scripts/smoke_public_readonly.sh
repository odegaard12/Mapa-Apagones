#!/usr/bin/env bash
set -euo pipefail

PUBLIC_BASE_URL="${PUBLIC_BASE_URL:-https://mapa-apagones.es}"
PUBLIC_API_BASE_URL="${PUBLIC_API_BASE_URL:-https://api.mapa-apagones.es}"
EXPECTED_VERSION="${EXPECTED_VERSION:-}"
EXPECTED_DISTRIBUTOR_HINTS_ITEMS="${EXPECTED_DISTRIBUTOR_HINTS_ITEMS:-1959}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

INDEX_HTML="$TMP_DIR/index.html"
CHANGELOG_HTML="$TMP_DIR/changelog.html"
DISTRIBUTOR_JSON="$TMP_DIR/distributor_hints.json"
HEALTH_JSON="$TMP_DIR/health.json"
INCIDENTS_JSON="$TMP_DIR/incidents.json"

echo "== Mapa Apagones · public read-only smoke =="
echo "PUBLIC_BASE_URL=$PUBLIC_BASE_URL"
echo "PUBLIC_API_BASE_URL=$PUBLIC_API_BASE_URL"

echo
echo "== 1) Web pública =="
curl -fsSL "$PUBLIC_BASE_URL/" -o "$INDEX_HTML"
test -s "$INDEX_HTML"
echo "OK web pública: /"

echo
echo "== 2) Changelog público =="
curl -fsSL "$PUBLIC_BASE_URL/changelog.html" -o "$CHANGELOG_HTML"
test -s "$CHANGELOG_HTML"

if [ -n "$EXPECTED_VERSION" ]; then
  grep -F "$EXPECTED_VERSION" "$CHANGELOG_HTML" >/dev/null
  echo "OK changelog contiene versión esperada: $EXPECTED_VERSION"
else
  grep -E "v[0-9]+\.[0-9]+\.[0-9]+" "$CHANGELOG_HTML" >/dev/null
  echo "OK changelog contiene versión pública"
fi

grep -E "Actualizado: [0-9]{4}-[0-9]{2}-[0-9]{2}" "$CHANGELOG_HTML" >/dev/null
echo "OK changelog contiene fecha de actualización"

echo
echo "== 3) JSON público de distribuidoras =="
curl -fsSL "$PUBLIC_BASE_URL/data/distributor_hints.json" -o "$DISTRIBUTOR_JSON"
python3 - "$DISTRIBUTOR_JSON" "$EXPECTED_DISTRIBUTOR_HINTS_ITEMS" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
expected = int(sys.argv[2])

data = json.loads(path.read_text(encoding="utf-8"))
items = data.get("items", [])

if not isinstance(items, list):
    raise SystemExit("ERROR: distributor_hints.json no contiene items[]")

print(f"items={len(items)}")

if len(items) != expected:
    raise SystemExit(f"ERROR: distributor_hints items={len(items)} esperado={expected}")

print("OK distributor_hints público")
PY

echo
echo "== 4) API pública health =="
curl -fsSL "$PUBLIC_API_BASE_URL/api/health" -o "$HEALTH_JSON"
python3 - "$HEALTH_JSON" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

if not isinstance(data, dict):
    raise SystemExit("ERROR: /api/health no devuelve objeto JSON")

print("OK /api/health JSON")
PY

echo
echo "== 5) API pública incidents read-only =="
curl -fsSL "$PUBLIC_API_BASE_URL/api/incidents?limit=5" -o "$INCIDENTS_JSON"
python3 - "$INCIDENTS_JSON" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

if not isinstance(data, (dict, list)):
    raise SystemExit("ERROR: /api/incidents no devuelve JSON objeto/lista")

print("OK /api/incidents JSON read-only")
PY

echo
echo "== Public read-only smoke OK =="
