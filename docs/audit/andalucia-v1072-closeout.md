# Andalucía distributor pending queue closeout v0.10.7.3

## Summary

This closeout records the Andalucía distributor research work completed through v0.10.7.2 and the post-merge validation integration added in v0.10.7.3.

## Completed work

The repository now has:

- Andalucía geography source locator.
- Andalucía pending audit scaffold.
- Andalucía pending review queue.
- Andalucía queue builder.
- Andalucía queue validator.
- Post-merge validation integration for the queue validator.

## Current Andalucía distributor baseline

- Geography source: frontend/public/data/andalucia_municipios.geojson
- GeoJSON features: 786
- Existing public distributor hints: 254
- Pending municipal review rows: 532
- Current imported confidence: verified_partial
- Current imported public distributor: E-Distribución Redes Digitales, S.L.U.

## Added queue files

- scripts/build_andalucia_pending_review_queue.py
- scripts/check_andalucia_pending_review_queue.py
- docs/audit/andalucia_pending_review_queue_v1072.csv
- docs/audit/andalucia-pending-review-queue-v1072.md

## Post-merge guard

post_merge_validate.sh now runs:

python3 scripts/check_andalucia_pending_review_queue.py

This protects these invariants:

- 786 Andalucía GeoJSON features.
- 254 already-covered public distributor hints.
- 532 pending municipal review rows.
- No duplicated pending zone_id.
- No pending row already covered by current hints.
- No pre-filled candidate distributor.
- No pre-filled source URL.
- No sensitive columns or high-risk sensitive markers.

## Privacy and safety constraints

The queue and validator avoid:

- No CUPS.
- No addresses.
- No exact coordinates.
- No customer data.
- No private grid inventory.
- No raw external API responses.
- No unsupported exclusivity claims.
- No Red Eléctrica distributor hint.
- No generic Pequeña distribuidora placeholder.

## Next safe data step

The next data PR should select a small source-backed Andalucía subset from the pending queue and import only strong public candidates as verified_partial.

Required checks for future imports:

- python3 scripts/check_distributor_hints.py
- python3 scripts/check_distributor_data_version.py --repo-root .
- python3 scripts/check_andalucia_pending_review_queue.py
- scripts/run_public_smoke_expected_version.sh

## Non-goals

This closeout does not:

- Import distributor hints.
- Modify distributor_hints.json.
- Change frontend behavior.
- Add private or sensitive data.
