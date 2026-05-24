#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

FILES = {
    "coverage": Path("frontend/public/cobertura-distribuidoras.html"),
    "reliability": Path("frontend/public/fiabilidad-distribuidoras.html"),
    "changelog": Path("frontend/public/changelog.html"),
}

REQUIRED = {
    "coverage": [
        "v0.10.7.7-static-public-pages-clean",
        "100% con pista no significa 100% verificación municipal fuerte",
        "regional_default",
        "no verificación municipal",
        "verified_partial",
        "Zonas con orientación/pista",
        "Zonas pendientes",
        "Las comunidades con cero pistas no faltan del mapa",
    ],
    "reliability": [
        "v0.10.7.7-static-public-pages-clean",
        "criterios vigentes a escala nacional",
        "Estado nacional por comunidad",
        "regional_default",
        "verified_partial",
        "No es verificación municipal fuerte",
    ],
    "changelog": [
        "v0.10.7.7",
        "Static public pages clean refresh",
        "v0.10.7.6",
        "v0.10.7.5",
        "v0.10.6.4-distributor-confidence-labels",
    ],
}

FORBIDDEN = [
    "gho_",
    "github_pat_",
    "-----BEGIN RSA PRIVATE KEY-----",
    "-----BEGIN OPENSSH PRIVATE KEY-----",
    "Historial técnico reciente desde Git",
    "4\ndatasets auditados en esta fase",
    "Actualizado: 2026-05-12",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    errors: list[str] = []

    for key, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue

        raw = read(path)
        low = raw.lower()

        for snippet in REQUIRED[key]:
            if snippet.lower() not in low:
                errors.append(f"{path}: missing snippet: {snippet}")

        for forbidden in FORBIDDEN:
            if forbidden.lower() in low:
                errors.append(f"{path}: forbidden stale/sensitive snippet: {forbidden}")

    changelog = read(FILES["changelog"]).lower() if FILES["changelog"].exists() else ""
    markers = [
        "v0.10.7.7",
        "v0.10.7.6",
        "v0.10.7.5",
        "v0.10.6.4-distributor-confidence-labels",
    ]
    positions = [changelog.find(m.lower()) for m in markers]

    if any(pos == -1 for pos in positions):
        errors.append(f"changelog: missing markers {markers}")
    elif positions != sorted(positions):
        errors.append(f"changelog: wrong order {positions}")

    if errors:
        print("FAIL public pages truthfulness")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK public pages truthfulness")
    return 0


if __name__ == "__main__":
    sys.exit(main())
