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
        "100% con pista no significa 100% verificación municipal fuerte",
        "regional_default",
        "no es verificación municipal fuerte",
        "verified_partial",
        "entradas por confianza",
        "zonas con pista",
        "zonas pendientes",
        "distributor_hints v0.10.6.4-distributor-confidence-labels",
        "v0.10.7.6-public-pages-truthfulness",
    ],
    "reliability": [
        "criterios vigentes revisados: 2026-05-24",
        "documento histórico base",
        "cobertura global actual debe consultarse",
        "regional_default",
        "verified_partial",
    ],
    "changelog": [
        "v0.10.7.6",
        "public pages truthfulness",
        "v0.10.7.5",
        "v0.10.6.4-distributor-confidence-labels",
    ],
}

FORBIDDEN = [
    "gho_",
    "github_pat_",
    "-----BEGIN RSA PRIVATE KEY-----",
    "-----BEGIN OPENSSH PRIVATE KEY-----",
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
        text = raw.lower()

        for snippet in REQUIRED[key]:
            if snippet.lower() not in text:
                errors.append(f"{path}: missing snippet: {snippet}")

        for forbidden in FORBIDDEN:
            if forbidden.lower() in text:
                errors.append(f"{path}: forbidden sensitive snippet: {forbidden}")

    changelog = read(FILES["changelog"]).lower() if FILES["changelog"].exists() else ""
    pos_1076 = changelog.find("v0.10.7.6")
    pos_1075 = changelog.find("v0.10.7.5")
    pos_1064 = changelog.find("v0.10.6.4-distributor-confidence-labels")

    if pos_1076 == -1 or pos_1075 == -1 or pos_1064 == -1:
        errors.append("changelog: missing version ordering markers")
    elif not (pos_1076 < pos_1075 and pos_1076 < pos_1064):
        errors.append("changelog: v0.10.7.6 must appear before older entries")

    if errors:
        print("FAIL public pages truthfulness")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK public pages truthfulness")
    return 0


if __name__ == "__main__":
    sys.exit(main())
