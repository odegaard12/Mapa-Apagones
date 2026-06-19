# Dependency hygiene v0.10.7.8

## Included

- FastAPI patch update to 0.136.3.
- Vite patch update to 8.0.16.
- React plugin patch update to 6.0.2.
- Dependabot groups split between runtime and tooling.
- Automatic React, React DOM and React-Leaflet major updates disabled.
- Dependency policy guard integrated into post-merge validation.

## Deliberately not included

- React 19.
- React-Leaflet 5.
- Standalone pydantic-core update.
- Unvalidated Click, httptools or Starlette minor upgrades.

Those updates require a dedicated compatibility migration.

## Safety

No application data, distributor hints, geographic datasets, reports, secrets,
CUPS, addresses or coordinates are modified.
