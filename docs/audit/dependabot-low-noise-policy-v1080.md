# Dependabot low-noise policy v0.10.8.0

## Policy

- Frontend runtime and tooling receive grouped minor/patch proposals.
- Frontend major migrations are ignored automatically.
- Backend automatic proposals are limited to patch releases.
- Backend minor/major upgrades require a curated compatibility PR.
- GitHub Actions major migrations require manual review.
- Open automatic PR counts are limited.

## Reason

FastAPI, Starlette, Uvicorn, React, React-Leaflet and GitHub Actions major or
minor migrations can contain compatibility or behavior changes. They should not
be merged individually without complete backend/frontend validation.

## Safety

This policy changes dependency automation only. It does not modify public data,
geographic datasets, distributor hints or user reports.
