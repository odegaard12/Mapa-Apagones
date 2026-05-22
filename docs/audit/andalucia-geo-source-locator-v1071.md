# Andalucía geo source locator v0.10.7.1

This research report locates repository files that mention Andalucía/andalucia.

It does not import distributor data and does not modify datasets.

## Summary

- Candidate files found: **33**

## Candidate files by extension

| extension | files |
|---|---:|
| `.csv` | 8 |
| `.geojson` | 1 |
| `.html` | 2 |
| `.js` | 1 |
| `.json` | 2 |
| `.md` | 9 |
| `.py` | 7 |
| `.txt` | 3 |

## Candidate files

| file | bytes | dataset_id mentions | zone_id mentions | parsed feature/list count |
|---|---:|---:|---:|---:|
| `frontend/public/changelog.html` | 68096 | 2 | 7 |  |
| `frontend/public/cobertura-distribuidoras.html` | 14273 | 0 | 0 |  |
| `frontend/public/data/andalucia_municipios.geojson` | 7989369 | 786 | 786 | 786 |
| `frontend/public/data/distributor_hints.json` | 2625218 | 2610 | 2610 |  |
| `frontend/src/data/distributor_hints.json` | 2625218 | 2610 | 2610 |  |
| `frontend/src/geo/datasets.js` | 6515 | 6 | 0 |  |
| `CHANGELOG.md` | 54870 | 3 | 9 |  |
| `README.md` | 9069 | 1 | 1 |  |
| `docs/audit/andalucia-distributor-pending-audit-v1070.md` | 1586 | 0 | 0 |  |
| `docs/audit/distributor-coverage-snapshot-v1068.md` | 3345 | 1 | 0 |  |
| `docs/audit/distributor-next-targets-v1069.md` | 3341 | 0 | 0 |  |
| `docs/audit/distributor_hint_quality_audit.md` | 1742 | 0 | 0 |  |
| `docs/research/distributor_coverage_matrix.md` | 4083 | 0 | 0 |  |
| `docs/research/distributor_import_batches/andalucia_edistribucion_strong_lineowner_import.md` | 1638 | 0 | 0 |  |
| `docs/research/distributor_import_batches/next_batches_plan.md` | 1751 | 0 | 0 |  |
| `docs/research/distributor_regional_audits/edistribucion_coverage_candidates.csv` | 2381181 | 1 | 0 |  |
| `docs/research/distributor_regional_audits/edistribucion_local_exception_hunt_by_dataset/andalucia.csv` | 479192 | 1 | 1 |  |
| `docs/research/distributor_regional_audits/edistribucion_local_exception_hunt_by_province_v1024.csv` | 1782 | 1 | 0 |  |
| `docs/research/distributor_regional_audits/edistribucion_local_exception_hunt_v1024.csv` | 1755408 | 1 | 1 |  |
| `docs/research/distributor_regional_audits/edistribucion_local_exception_hunt_v1024_summary.txt` | 764 | 0 | 0 |  |
| `docs/research/distributor_regional_audits/edistribucion_local_exception_search_queries_v1024.csv` | 28083 | 1 | 0 |  |
| `docs/research/distributor_regional_audits/edistribucion_review_queue_by_dataset/andalucia.csv` | 349374 | 1 | 0 |  |
| `docs/research/distributor_regional_audits/edistribucion_review_summary.txt` | 812 | 0 | 0 |  |
| `docs/research/distributor_regional_audits/remaining_regional_distributor_candidates_v1023.csv` | 3323720 | 1 | 1 |  |
| `docs/research/distributor_regional_audits/remaining_regional_distributor_candidates_v1023_summary.txt` | 1464 | 0 | 0 |  |
| `docs/research/distributor_regional_audits/remaining_regional_review_queue_by_dataset/andalucia.csv` | 391875 | 1 | 1 |  |
| `scripts/audit_geo_datasets.py` | 6221 | 18 | 16 |  |
| `scripts/check_geo_dataset_provinces.py` | 4100 | 5 | 0 |  |
| `scripts/check_spain_geo_coverage.py` | 6133 | 13 | 18 |  |
| `scripts/generate_distributor_coverage_matrix.py` | 15919 | 23 | 6 |  |
| `scripts/locate_andalucia_geo_sources.py` | 4842 | 4 | 3 |  |
| `scripts/report_andalucia_distributor_pending.py` | 4160 | 1 | 0 |  |
| `scripts/report_distributor_hint_coverage.py` | 4526 | 9 | 0 |  |

## Next step

Use this locator to identify the real Andalucía municipal source file before
building a sanitized pending review CSV.

A future queue builder must only use repository-local public geography and
must keep these constraints:

- No CUPS.
- No addresses.
- No exact coordinates in the generated review queue.
- No customer data.
- No private grid inventory.
- No raw external API responses.
