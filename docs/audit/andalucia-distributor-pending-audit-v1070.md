# Andalucía distributor pending audit v0.10.7.0

Generated: 2026-05-22

## Scope

This is a research/audit scaffold for the next Andalucía distributor work.

It does not import distributor hints and does not modify public data.

## Current Andalucía baseline

- Expected Andalucía municipalities/zones: **786**
- Current Andalucía public hint zones: **254**
- Pending review estimate: **532**

## Confidence distribution in current Andalucía hints

| confidence | entries |
|---|---:|
| `verified_partial` | 254 |

## Current public distributor names in Andalucía

| distributor | entries |
|---|---:|
| E-Distribución Redes Digitales, S.L.U. | 254 |

## Recommended next audit method

Future Andalucía imports should be split into small batches.

For every candidate municipality:

1. Require public, source-backed evidence.
2. Import only as `verified_partial`.
3. Do not assert exclusivity.
4. Do not use `regional_default` for municipal claims.
5. Exclude Red Eléctrica as a distribution-company hint.
6. Exclude generic labels such as `Pequeña distribuidora`.

## Privacy and safety constraints

- No CUPS.
- No addresses.
- No exact coordinates.
- No customer data.
- No raw external API responses.
- No private grid inventory.
- No substations, transformers, lines or internal network geometry.

## Proposed next PR sequence

1. Build a sanitized local review queue for Andalucía pending zones.
2. Manually classify only strong public candidates.
3. Import a small batch of `verified_partial` hints.
4. Re-run public smoke, version guard and distributor hint guard.

