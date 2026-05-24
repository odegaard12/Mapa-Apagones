#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PAGES = [
    Path("frontend/public/changelog.html"),
    Path("frontend/public/cobertura-distribuidoras.html"),
    Path("frontend/public/fiabilidad-distribuidoras.html"),
]

REQUIRED = {
    "frontend/public/changelog.html": [
        "v0.10.7.7",
        "v0.10.7.6",
        "v0.10.7.5",
        "v0.10.6.4-distributor-confidence-labels",
        "Historial público curado",
    ],
    "frontend/public/cobertura-distribuidoras.html": [
        "v0.10.7.7-static-public-pages-clean",
        "19</strong><span>datasets geográficos",
        "8.215</strong><span>zonas normalizadas",
        "100% con pista no significa 100% verificación municipal fuerte",
        "Castilla y León",
        "Catalunya",
        "Aragón",
        "Andalucía",
        "Las comunidades con cero pistas no faltan del mapa",
    ],
    "frontend/public/fiabilidad-distribuidoras.html": [
        "v0.10.7.7-static-public-pages-clean",
        "criterios vigentes a escala nacional",
        "19 datasets geográficos",
        "Estado nacional por comunidad",
        "regional_default",
        "verified_partial",
    ],
}

FORBIDDEN = [
    "gho_",
    "github_pat_",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "Historial técnico reciente desde Git",
    "Lectura importante:",
    "4\ndatasets auditados en esta fase",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    errors: list[str] = []

    for page in PAGES:
        if not page.exists():
            errors.append(f"missing page: {page}")
            continue

        text = read(page)
        lower = text.lower()

        for snippet in REQUIRED[str(page)]:
            if snippet.lower() not in lower:
                errors.append(f"{page}: missing snippet: {snippet}")

        for forbidden in FORBIDDEN:
            if forbidden.lower() in lower:
                errors.append(f"{page}: forbidden stale snippet: {forbidden}")

    changelog = read(Path("frontend/public/changelog.html")).lower()
    positions = [
        changelog.find("v0.10.7.7"),
        changelog.find("v0.10.7.6"),
        changelog.find("v0.10.7.5"),
        changelog.find("v0.10.6.4-distributor-confidence-labels"),
    ]

    if any(pos == -1 for pos in positions):
        errors.append("changelog: missing ordered version markers")
    elif positions != sorted(positions):
        errors.append(f"changelog: version order is wrong: {positions}")

    if errors:
        print("FAIL clean static public pages")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK clean static public pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
