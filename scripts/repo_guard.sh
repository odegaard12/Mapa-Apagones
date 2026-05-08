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

echo
echo "== repo_guard: tamaño máximo de assets Cloudflare Pages =="
BIG_ASSETS="$(find frontend/public -type f -size +24M -print 2>/dev/null || true)"
if [ -n "$BIG_ASSETS" ]; then
  echo "$BIG_ASSETS"
  echo "ERROR: hay assets mayores de 24 MiB. Cloudflare Pages rechaza archivos individuales de más de 25 MiB."
  exit 1
fi
echo "OK"

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

echo "== repo_guard: Toda España incluye todos los datasets municipales =="
python3 scripts/check_all_scope_datasets.py
echo
echo "== repo_guard: cobertura geográfica completa España =="
python3 scripts/check_spain_geo_coverage.py
echo
echo "== repo_guard: distributor hints seguros =="
python3 scripts/check_distributor_hints.py

echo
echo "== repo_guard: versión pública sincronizada =="
python3 scripts/check_public_version_mentions.py

echo
echo "== repo_guard: backups/temporales trackeados =="
python3 scripts/check_no_tracked_backup_artifacts.py

echo
echo "== repo_guard: hashes anónimos HMAC =="
python3 scripts/check_anonymous_hashing.py

echo
echo "== repo_guard: IP real solo desde proxy confiable =="
python3 scripts/check_trusted_proxy_ip.py

echo
echo "== repo_guard: transacción de reportes concurrentes =="
python3 scripts/check_report_transaction.py

echo
echo "== repo_guard: lockfiles reproducibles =="
python3 scripts/check_dependency_locks.py

echo
echo "== repo_guard: Docker Compose smoke cableado en CI =="
python3 scripts/check_docker_compose_smoke.py

echo
echo "== repo_guard: smoke ciclo de vida backend cableado en CI =="
python3 scripts/check_backend_lifecycle_smoke.py

echo
echo "== repo_guard: smoke privacidad/anti-abuso backend cableado en CI =="
python3 scripts/check_backend_privacy_abuse_smoke.py

