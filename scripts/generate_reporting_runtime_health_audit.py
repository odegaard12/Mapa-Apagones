#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "audit" / "reporting_runtime_health_audit.md"

REQUIRED_FILES = [
    "scripts/smoke_backend_api.py",
    "scripts/smoke_backend_lifecycle.py",
    "scripts/smoke_backend_concurrency.py",
    "scripts/smoke_backend_privacy_abuse.py",
    "scripts/smoke_docker_compose.sh",
    "scripts/post_merge_validate.sh",
]

REQUIRED_POST_MERGE_TOKENS = [
    "smoke_backend_api.py",
    "smoke_backend_lifecycle.py",
    "smoke_backend_concurrency.py",
    "smoke_backend_privacy_abuse.py",
    "smoke_docker_compose.sh",
]

FLOW_EXPECTATIONS = {
    "scripts/smoke_backend_api.py": [
        "/api/health",
        "/api/report",
        "/api/incidents",
    ],
    "scripts/smoke_backend_lifecycle.py": [
        "/api/report",
        "/api/incidents",
    ],
    "scripts/smoke_backend_concurrency.py": [
        "/api/report",
    ],
    "scripts/smoke_backend_privacy_abuse.py": [
        "429",
        "ip_hash",
        "reporter_token_hash",
    ],
    "scripts/smoke_docker_compose.sh": [
        "/api/health",
        "/api/report",
        "/api/incidents",
        "/data/distributor_hints.json",
    ],
}


def render() -> tuple[str, list[str]]:
    errors: list[str] = []

    post_merge_path = ROOT / "scripts" / "post_merge_validate.sh"
    post_merge_text = post_merge_path.read_text(encoding="utf-8") if post_merge_path.exists() else ""

    lines: list[str] = []
    lines.append("# Auditoría de salud runtime de reportes")
    lines.append("")
    lines.append("Esta auditoría documenta las comprobaciones automáticas que protegen el flujo de reportes ciudadanos.")
    lines.append("")
    lines.append("## Cobertura esperada")
    lines.append("")
    lines.append("- Crear reportes mediante `/api/report`.")
    lines.append("- Ver incidencias recién creadas mediante `/api/incidents`.")
    lines.append("- Validar ciclo de vida de reportes, agrupación y resolución.")
    lines.append("- Validar concurrencia para evitar incidencias duplicadas.")
    lines.append("- Validar privacidad: hashes HMAC y ausencia de IP/token raw en SQLite temporal.")
    lines.append("- Validar anti-abuso con respuesta `429`.")
    lines.append("- Validar Docker Compose real con frontend, backend, proxy `/api` y JSON público de distribuidoras.")
    lines.append("")
    lines.append("## Scripts requeridos")
    lines.append("")
    lines.append("| Script | Existe | Incluido en post-merge |")
    lines.append("|---|---:|---:|")

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        exists = path.exists()
        included = rel.split("/")[-1] in post_merge_text

        if not exists:
            errors.append(f"Falta script requerido: {rel}")

        if rel != "scripts/post_merge_validate.sh" and not included:
            errors.append(f"Script no incluido en post_merge_validate.sh: {rel}")

        lines.append(f"| `{rel}` | {'sí' if exists else 'no'} | {'sí' if included else 'no'} |")

    lines.append("")
    lines.append("## Tokens funcionales revisados")
    lines.append("")
    lines.append("| Script | Token esperado | Estado |")
    lines.append("|---|---|---|")

    for rel, tokens in FLOW_EXPECTATIONS.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8") if path.exists() else ""

        for token in tokens:
            ok = token in text
            if not ok:
                errors.append(f"{rel}: no contiene token esperado {token}")
            lines.append(f"| `{rel}` | `{token}` | {'OK' if ok else 'FALTA'} |")

    lines.append("")
    lines.append("## Lectura operativa")
    lines.append("")
    lines.append("- La comprobación fuerte se ejecuta con `scripts/post_merge_validate.sh`.")
    lines.append("- El smoke de lifecycle cubre que un reporte se vea en incidencias y que el estado cambie al resolver.")
    lines.append("- El smoke de concurrencia cubre reportes simultáneos en la misma zona.")
    lines.append("- El smoke de privacidad/abuso cubre HMAC, ausencia de datos raw y rate limit.")
    lines.append("- El smoke Docker Compose cubre el camino frontend/proxy/backend de forma aislada.")
    lines.append("")
    lines.append("## Seguridad y privacidad")
    lines.append("")
    lines.append("Esta auditoría no introduce CUPS, cuentas, texto libre, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, logs, bases de datos reales ni inventario de infraestructura crítica.")
    lines.append("")

    if errors:
        lines.append("## Errores bloqueantes")
        lines.append("")
        for error in errors:
            lines.append(f"- {error}")
        lines.append("")

    return "\n".join(lines), errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered, errors = render()

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"ERROR: falta {OUTPUT_PATH.relative_to(ROOT)}")
            return 1

        current = OUTPUT_PATH.read_text(encoding="utf-8")
        if current != rendered:
            tmp = Path("/tmp/reporting_runtime_health_audit.generated.md")
            tmp.write_text(rendered, encoding="utf-8")
            print("ERROR: auditoría runtime de reportes desactualizada.")
            print(f"Generado esperado en: {tmp}")
            print("Ejecuta: python3 scripts/generate_reporting_runtime_health_audit.py")
            return 1

        if errors:
            print(f"ERROR: auditoría runtime con {len(errors)} errores bloqueantes")
            return 1

        print("OK reporting runtime health audit actualizada")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")

    if errors:
        print(f"WARN auditoría generada con {len(errors)} errores bloqueantes: {OUTPUT_PATH.relative_to(ROOT)}")
        return 1

    print(f"OK auditoría generada: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
