#!/usr/bin/env bash
set -euo pipefail

NO_BUILD=0
if [ "${1:-}" = "--no-build" ]; then
  NO_BUILD=1
fi

fail=0
bad_files=()

while IFS= read -r path; do
  base="$(basename "$path")"

  case "$path" in
    _backups/*|*/_backups/*|backups/*|*/backups/*|diagnostics/*|*/diagnostics/*)
      bad_files+=("$path")
      ;;
    *__pycache__*|*.pyc|*.pyo|*.pyd)
      bad_files+=("$path")
      ;;
    *.db|*.db-wal|*.db-shm|*.sqlite|*.sqlite-wal|*.sqlite-shm|*.sqlite3|*.sqlite3-wal|*.sqlite3-shm|*.log)
      bad_files+=("$path")
      ;;
    .env|*/.env)
      bad_files+=("$path")
      ;;
    .env.*|*/.env.*)
      if [ "$base" != ".env.example" ]; then
        bad_files+=("$path")
      fi
      ;;
    frontend/public/data/*_raw.geojson|frontend/public/data/municipios_espana_raw.geojson|frontend/public/data/generated-*.json)
      bad_files+=("$path")
      ;;
  esac
done < <(git ls-files)

echo "== repo_guard: archivos prohibidos trackeados =="
if [ "${#bad_files[@]}" -gt 0 ]; then
  printf '%s\n' "${bad_files[@]}"
  echo "ERROR: hay archivos locales/prohibidos trackeados."
  fail=1
else
  echo "OK"
fi

echo
echo "== repo_guard: setToastTone fatal =="
if grep -R "setToastTone" -n frontend/src 2>/dev/null; then
  echo "ERROR: setToastTone no debe existir; ya causó pantalla negra."
  fail=1
else
  echo "OK"
fi

echo
echo "== repo_guard: versión consistente =="
VERSION_FILE="$(tr -d '\r\n' < VERSION)"
if grep -q "const APP_VERSION = '$VERSION_FILE'" frontend/src/App.jsx; then
  echo "OK VERSION=$VERSION_FILE"
else
  echo "ERROR: VERSION y APP_VERSION no coinciden."
  echo "VERSION=$VERSION_FILE"
  grep -n "APP_VERSION" frontend/src/App.jsx || true
  fail=1
fi

echo
echo "== repo_guard: sintaxis backend sin crear __pycache__ =="
python3 - <<'PY'
from pathlib import Path
source = Path("backend/app/main.py").read_text()
compile(source, "backend/app/main.py", "exec")
print("OK")
PY

if [ "$NO_BUILD" -eq 0 ]; then
  echo
  echo "== repo_guard: build frontend =="
  npm --prefix frontend run build
fi

exit "$fail"
