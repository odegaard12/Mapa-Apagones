#!/usr/bin/env bash
set -euo pipefail

SMOKE_PYTHON="${SMOKE_PYTHON:-python3}"
SMOKE_WEB_PORT="${SMOKE_WEB_PORT:-18098}"

echo "============================================================"
echo " Mapa Apagones · post-merge validation"
echo "============================================================"
echo "Repo: $(pwd)"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"
echo

echo "== 1) Git limpio =="
git status --short
test -z "$(git status --short)"

echo
echo "== 2) Versión pública =="
cat VERSION
grep -n "APP_VERSION" frontend/src/App.jsx | head

echo
echo "== 3) Guardias estáticas =="
python3 scripts/check_public_version_mentions.py
python3 scripts/check_no_tracked_backup_artifacts.py
python3 scripts/check_anonymous_hashing.py
python3 scripts/check_backend_privacy_module.py
python3 scripts/check_trusted_proxy_ip.py
python3 scripts/check_report_transaction.py
python3 scripts/check_dependency_locks.py
python3 scripts/check_docker_compose_smoke.py
python3 scripts/check_backend_lifecycle_smoke.py
python3 scripts/check_backend_privacy_abuse_smoke.py
python3 scripts/check_architecture_docs.py
python3 scripts/check_audit_closeout.py
python3 scripts/check_distributor_data_safety.py
python3 scripts/check_frontend_static_smoke.py
python3 scripts/check_public_changelog_current.py
python3 scripts/check_public_readonly_smoke.py
python3 scripts/check_safe_status_endpoint.py
python3 scripts/check_sqlite_schema_hardening.py
python3 scripts/check_distributor_hints.py
echo '--- check_distributor_data_version ---'
python3 scripts/check_distributor_data_version.py --repo-root .
echo '--- check_andalucia_pending_review_queue ---'
python3 scripts/check_andalucia_pending_review_queue.py
echo '--- check_andalucia_batch2_candidate_workbench ---'
python3 scripts/check_andalucia_batch2_candidate_workbench.py
echo '--- check_public_docs_freshness ---'
python3 scripts/check_public_docs_freshness.py
echo '--- check_public_pages_truthfulness ---'
python3 scripts/check_public_pages_truthfulness.py
echo '--- check_clean_static_public_pages ---'
python3 scripts/check_clean_static_public_pages.py
echo '--- check_dependency_update_policy ---'
python3 scripts/check_dependency_update_policy.py
python3 scripts/generate_distributor_coverage_matrix.py --check
python3 scripts/check_public_distributor_coverage_page.py
python3 scripts/check_public_coverage_linking.py
python3 scripts/generate_public_distributor_coverage_page.py --check
python3 scripts/generate_madrid_distributor_deep_review.py --check
python3 scripts/generate_extremadura_distributor_deep_audit.py --check
python3 scripts/generate_reporting_runtime_health_audit.py --check
python3 scripts/check_reporting_timing_smoke.py
python3 scripts/generate_distributor_hint_quality_audit.py --check

echo
echo "== 4) Repo guard completo =="
bash scripts/repo_guard.sh --no-build

echo
echo "== 5) Geografía y cobertura =="
node --check frontend/src/geo/datasets.js
node --check frontend/src/grid/distributorHints.js
python3 scripts/check_all_scope_datasets.py
python3 scripts/audit_geo_datasets.py
python3 scripts/check_geo_dataset_provinces.py
python3 scripts/check_spain_geo_coverage.py

echo
echo "== 6) Build frontend + smoke estático =="
NODE_OPTIONS=--max-old-space-size=1536 npm --prefix frontend run build
python3 scripts/smoke_frontend_static.py

echo
echo "== 7) Backend runtime smokes =="
"$SMOKE_PYTHON" scripts/smoke_backend_status.py
"$SMOKE_PYTHON" scripts/smoke_backend_schema.py
"$SMOKE_PYTHON" scripts/smoke_backend_api.py
"$SMOKE_PYTHON" scripts/smoke_backend_concurrency.py
"$SMOKE_PYTHON" scripts/smoke_backend_lifecycle.py
"$SMOKE_PYTHON" scripts/smoke_backend_privacy_abuse.py
"$SMOKE_PYTHON" scripts/smoke_reporting_timing.py

echo
echo "== 8) Docker Compose smoke aislado =="
SMOKE_WEB_PORT="$SMOKE_WEB_PORT" bash scripts/smoke_docker_compose.sh

echo
echo "============================================================"
echo " OK post-merge validation completa"
echo "============================================================"
