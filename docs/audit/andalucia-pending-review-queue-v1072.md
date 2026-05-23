# Andalucía pending distributor review queue v0.10.7.2

Generated: 2026-05-23

## Summary

- Andalucía municipal GeoJSON features: **786**
- Already covered by distributor hints: **254**
- Pending municipal review rows: **532**
- CSV: `docs/audit/andalucia_pending_review_queue_v1072.csv`

## Pending rows by province

| province | pending rows |
|---|---:|
| Almería | 73 |
| Cádiz | 29 |
| Córdoba | 44 |
| Granada | 129 |
| Huelva | 53 |
| Jaén | 50 |
| Málaga | 70 |
| Sevilla | 84 |

## Intended use

This queue is a sanitized working list for future Andalucía distributor research.

It does not import new distributor hints.

Future imports must only promote rows from this queue when there is
strong public, source-backed evidence for a `verified_partial` hint.

## Safety constraints

- No CUPS.
- No addresses.
- No exact coordinates.
- No customer data.
- No private grid inventory.
- No raw external API responses.
- No unsupported exclusivity claims.
- No Red Eléctrica distributor hint.
- No generic `Pequeña distribuidora` placeholder.
