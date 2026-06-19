# Distributor hints next targets v0.10.6.9

## Context

Current public distributor hints baseline:

- Public hint zones: 2610
- Confidence entries:
  - `regional_default`: 1800
  - `verified_partial`: 967
- Current metadata version: `v0.10.6.4-distributor-confidence-labels`

This document does not import new data. It defines a conservative next-work plan.

## Rules

Any future distributor import must keep these constraints:

- No CUPS.
- No addresses.
- No exact user coordinates.
- No private grid geometry.
- No substation / transformer / line inventory.
- No raw external API dumps.
- No unsupported exclusivity claims.
- No regional default promoted to municipal evidence without source.

## Priority 1 — Andalucía pending review

Andalucía is the best next large target because a first strong import already exists.

Known state:

- Strong E-Distribución line-owner hints already imported where confidence was high.
- Remaining municipalities should stay pending until reviewed.
- Next work should be a research/audit PR before any data import PR.

Recommended next PRs:

1. `research(distributors): audit andalucia pending municipalities`
2. `data(distributors): add andalucia verified partial hints batch 2`

Acceptance criteria for future import:

- Only `verified_partial`.
- Only municipalities with strong public support.
- No regional blanket.
- No Red Eléctrica as distributor hint.
- No generic “Pequeña distribuidora” labels.

## Priority 2 — Extremadura municipal review queue

Extremadura already has a review queue and should continue with conservative municipal checks.

Recommended next PRs:

1. `research(distributors): review extremadura municipal queue batch 1`
2. `data(distributors): add extremadura verified partial hints batch 1`

Acceptance criteria:

- Keep unresolved municipalities pending.
- Import only source-backed local/municipal hints.
- Avoid inferring exclusivity.

## Priority 3 — Madrid mixed/local distributor cases

Madrid already has partial work and is useful because users may benefit from clearer local distributor guidance.

Recommended next PRs:

1. `research(distributors): review madrid remaining distributor cases`
2. `data(distributors): add madrid verified partial local hints`

Acceptance criteria:

- Preserve UFD partial semantics.
- Add local distributors only with source-backed municipal evidence.
- Avoid blanket claims.

## Priority 4 — Castilla y León / Castilla-La Mancha

Large territories, likely mixed evidence.

Recommended approach:

- Research PR first.
- No direct import until clear public sources are found.
- Split by province if needed.

## Priority 5 — Smaller controlled communities

Good candidates for smaller, safer batches:

- La Rioja
- Región de Murcia
- Navarra
- Aragón
- Illes Balears
- Canarias

These should be easier to review in small PRs.

## Recommended sequence

1. Andalucía pending audit.
2. Andalucía verified partial batch 2.
3. Extremadura queue audit.
4. Extremadura verified partial batch 1.
5. Madrid remaining cases audit.
6. Madrid verified partial batch 2.
7. Castilla y León research.
8. Castilla-La Mancha research.

## Non-goals

This roadmap intentionally does not:

- Add distributor data.
- Modify `distributor_hints.json`.
- Change frontend behavior.
- Change confidence labels.
- Add sensitive data.

## National next-wave follow-up v0.10.8.1

A sanitized 4,901-row research queue now covers the four geographic datasets
that currently have no public distributor hints:

- Aragón: 734
- Castilla-La Mancha: 921
- Catalunya: 948
- Castilla y León: 2,298

The queue is research-only. Candidate distributor and source fields remain
empty until reproducible public evidence is reviewed.

## Aragón wave 2 candidate gate v0.10.8.3

Aragón now has a 734-row candidate matrix with a strict evidence gate.

- 733 municipalities remain regional-context only.
- Barbastro is a strong secondary candidate.
- Barbastro still lacks primary operator/regulator confirmation.
- Current import-eligible municipalities: 0.
- Wave 1 repository references are explicitly separated from real
  distributor evidence.

No productive distributor hints are changed by this phase.
