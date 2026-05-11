#!/usr/bin/env bash
set -euo pipefail

SCRIPT="scripts/post_merge_validate.sh"
README="README.md"

if [ ! -f "$SCRIPT" ]; then
  echo "ERROR: falta $SCRIPT"
  exit 1
fi

required=(
  "check_public_version_mentions.py"
  "check_no_tracked_backup_artifacts.py"
  "check_anonymous_hashing.py"
  "check_backend_privacy_module.py"
  "check_trusted_proxy_ip.py"
  "check_report_transaction.py"
  "check_dependency_locks.py"
  "check_docker_compose_smoke.py"
  "check_backend_lifecycle_smoke.py"
  "check_backend_privacy_abuse_smoke.py"
  "check_architecture_docs.py"
  "check_audit_closeout.py"
  "check_frontend_static_smoke.py"
  "check_safe_status_endpoint.py"
  "check_sqlite_schema_hardening.py"
  "check_distributor_hints.py"
  "check_all_scope_datasets.py"
  "audit_geo_datasets.py"
  "check_spain_geo_coverage.py"
  "smoke_frontend_static.py"
  "smoke_backend_status.py"
  "smoke_backend_schema.py"
  "smoke_backend_api.py"
  "smoke_backend_concurrency.py"
  "smoke_backend_lifecycle.py"
  "smoke_backend_privacy_abuse.py"
  "smoke_docker_compose.sh"
)

for item in "${required[@]}"; do
  if ! grep -q "$item" "$SCRIPT"; then
    echo "ERROR: $SCRIPT no contiene $item"
    exit 1
  fi
done

if ! grep -q "scripts/post_merge_validate.sh" "$README"; then
  echo "ERROR: README no menciona scripts/post_merge_validate.sh"
  exit 1
fi

echo "OK post-merge validation guard"

python3 scripts/check_distributor_data_safety.py
python3 scripts/generate_distributor_coverage_matrix.py --check
python3 scripts/check_public_distributor_coverage_page.py
python3 scripts/check_public_coverage_linking.py
python3 scripts/generate_public_distributor_coverage_page.py --check
python3 scripts/generate_reporting_runtime_health_audit.py --check
python3 scripts/check_reporting_timing_smoke.py
python3 scripts/generate_distributor_hint_quality_audit.py --check
python3 scripts/check_geo_dataset_provinces.py
python3 scripts/check_public_changelog_current.py
python3 scripts/check_public_readonly_smoke.py
