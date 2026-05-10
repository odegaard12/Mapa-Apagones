#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / "VERSION"
HTML_PATH = ROOT / "frontend" / "public" / "changelog.html"

MIN_UPDATED_DATE = date(2026, 5, 10)


def main() -> int:
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    html = HTML_PATH.read_text(encoding="utf-8")

    errors: list[str] = []

    if version not in html:
        errors.append(f"falta la versión actual en changelog público: {version}")

    h1_index = html.find("<h1")
    version_index = html.find(version)

    if h1_index == -1:
        errors.append("falta <h1> en changelog público")
    elif version_index != -1 and version_index < h1_index:
        errors.append("la versión actual aparece antes del encabezado del changelog")

    if h1_index != -1:
        prefix = html[:h1_index]
        if re.search(r"<h2>\s*v\d", prefix):
            errors.append("hay secciones de versión antes del encabezado principal")

    updated_match = re.search(r"Actualizado:\s*(\d{4}-\d{2}-\d{2})", html)

    if not updated_match:
        errors.append("falta línea 'Actualizado: YYYY-MM-DD' en changelog público")
    else:
        updated = date.fromisoformat(updated_match.group(1))
        if updated < MIN_UPDATED_DATE:
            errors.append(
                f"fecha de changelog público desfasada: {updated.isoformat()} "
                f"< {MIN_UPDATED_DATE.isoformat()}"
            )

    if errors:
        print("ERROR public changelog guard:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"OK public changelog current: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
