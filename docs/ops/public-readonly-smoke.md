# Smoke público read-only

Este smoke comprueba producción pública sin crear reportes.

## Qué valida

- Web pública `/`.
- Changelog público con versión y fecha.
- Página pública de cobertura de distribuidoras.
- JSON público `/data/distributor_hints.json`.
- API pública `/api/health`.
- API pública `/api/status` segura.
- API pública `/api/incidents?limit=5`.

## Qué no hace

- No envía reportes.
- No llama a `/api/report`.
- No pide CUPS.
- No usa cuentas.
- No envía texto libre.
- No sube fotos.
- No publica direcciones exactas ni coordenadas privadas.
- No toca la base de datos real.
- No expone secretos, rutas privadas, IPs privadas ni CIDRs reales desde `/api/status`.

## Uso

    EXPECTED_VERSION="v0.10.5.4-public-status-readonly-smoke" \
    EXPECTED_DISTRIBUTOR_HINTS_ITEMS=1959 \
    scripts/smoke_public_readonly.sh

También se puede usar contra preview o entornos alternativos:

    PUBLIC_BASE_URL="https://mapa-apagones.es" \
    PUBLIC_API_BASE_URL="https://api.mapa-apagones.es" \
    EXPECTED_DISTRIBUTOR_HINTS_ITEMS=1959 \
    scripts/smoke_public_readonly.sh

## Nota

Este smoke no debe ser obligatorio en CI normal porque depende de red externa y de producción. Es un runbook manual post-despliegue.
