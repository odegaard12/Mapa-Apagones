#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

EXPECTED_VERSION="${EXPECTED_DISTRIBUTOR_VERSION:-$(cat VERSION)}"
MAX_ATTEMPTS="${PUBLIC_SMOKE_MAX_ATTEMPTS:-18}"
SLEEP_SECONDS="${PUBLIC_SMOKE_SLEEP_SECONDS:-10}"

echo "=== run_public_smoke_expected_version ==="
echo "expected_distributor_version=${EXPECTED_VERSION}"
echo "max_attempts=${MAX_ATTEMPTS}"
echo "sleep_seconds=${SLEEP_SECONDS}"

LAST_STATUS=0

for ATTEMPT in $(seq 1 "$MAX_ATTEMPTS"); do
  echo
  echo "--- intento ${ATTEMPT}/${MAX_ATTEMPTS} ---"

  set +e
  EXPECTED_DISTRIBUTOR_VERSION="$EXPECTED_VERSION" \
    python3 scripts/check_public_deploy_smoke.py "$@"
  LAST_STATUS=$?
  set -e

  if [[ "$LAST_STATUS" -eq 0 ]]; then
    echo
    echo "OK: smoke público con versión esperada pasado"
    exit 0
  fi

  if [[ "$ATTEMPT" -lt "$MAX_ATTEMPTS" ]]; then
    echo "INFO: puede estar propagándose/caché; reintentando..."
    sleep "$SLEEP_SECONDS"
  fi
done

echo
echo "FAIL: smoke público con versión esperada no pasó"
exit "$LAST_STATUS"
