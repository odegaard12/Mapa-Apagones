# Public docs and national validation refresh v0.10.7.5

## Summary

This document records the public documentation refresh and validation state after the Andalucía distributor research pipeline work.

## Current public version

- VERSION: v0.10.7.7-static-public-pages-clean
- Public distributor JSON version expected: v0.10.7.7-static-public-pages-clean
- Public distributor hint zones: 2610

## Andalucía distributor research baseline

- Andalucía municipal GeoJSON source: frontend/public/data/andalucia_municipios.geojson
- Andalucía GeoJSON features: 786
- Existing public Andalucía distributor hints: 254
- Pending municipal review queue rows: 532
- Batch 2 candidate workbench rows: 532

## Current Andalucía guard scripts

- scripts/check_andalucia_pending_review_queue.py
- scripts/check_andalucia_batch2_candidate_workbench.py

## Current public/version guard scripts

- scripts/check_distributor_data_version.py
- scripts/check_public_deploy_smoke.py
- scripts/run_public_smoke_expected_version.sh
- scripts/check_public_docs_freshness.py

## National coverage checks to keep running

- node --check frontend/src/geo/datasets.js
- python3 scripts/check_all_scope_datasets.py
- python3 scripts/audit_geo_datasets.py
- python3 scripts/check_spain_geo_coverage.py
- bash scripts/repo_guard.sh --no-build
- npm --prefix frontend run build

## Safety constraints

The refreshed docs and guards must not add:

- CUPS.
- Addresses.
- Exact user coordinates.
- Customer data.
- Private grid inventory.
- Raw external API responses.
- Secrets, tokens, logs or backups.

## Next safe data step

The next data step should select a small, source-backed Andalucía subset from the batch 2 workbench and manually review it before any import.

No automatic import should be performed from the workbench.
