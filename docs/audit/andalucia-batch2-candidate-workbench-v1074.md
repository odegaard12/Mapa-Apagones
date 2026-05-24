# Andalucía batch 2 candidate workbench v0.10.7.4

Generated: 2026-05-24

## Summary

- Pending queue rows available: **532**
- Already covered Andalucía hints: **254**
- Source CSV rows scanned: **15048**
- Source rows matched before scoring: **9111**
- Candidate workbench rows: **532**
- CSV: `docs/audit/andalucia_batch2_candidate_workbench_v1074.csv`

## Source files scanned

| source file | rows |
|---|---:|
| `docs/research/distributor_regional_audits/edistribucion_coverage_candidates.csv` | 5629 |
| `docs/research/distributor_regional_audits/edistribucion_local_exception_hunt_by_dataset/andalucia.csv` | 786 |
| `docs/research/distributor_regional_audits/edistribucion_review_queue_by_dataset/andalucia.csv` | 786 |
| `docs/research/distributor_regional_audits/remaining_regional_distributor_candidates_v1023.csv` | 7061 |
| `docs/research/distributor_regional_audits/remaining_regional_review_queue_by_dataset/andalucia.csv` | 786 |

## Candidates by province

| province | candidates |
|---|---:|
| Almería | 73 |
| Cádiz | 29 |
| Córdoba | 44 |
| Granada | 129 |
| Huelva | 53 |
| Jaén | 50 |
| Málaga | 70 |
| Sevilla | 84 |

## Match methods

| match method | rows |
|---|---:|
| `zone_id` | 532 |

## Safety

This workbench is not an import file.

- Every row remains `manual_review_only`.
- Every candidate confidence remains `manual_review_required`.
- No distributor hint is imported by this script.
- No CUPS, addresses, exact coordinates, secrets or raw API responses are added.
- Future data imports must manually review evidence before promoting any row to `verified_partial`.
