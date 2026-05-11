#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "frontend" / "src" / "App.jsx"
SITEMAP = ROOT / "frontend" / "public" / "sitemap.xml"
PAGE = ROOT / "frontend" / "public" / "cobertura-distribuidoras.html"

REQUIRED = [
    (APP, "/cobertura-distribuidoras.html"),
    (APP, "Cobertura distribuidoras"),
    (SITEMAP, "https://mapa-apagones.es/cobertura-distribuidoras.html"),
    (PAGE, "Cobertura pública de distribuidoras"),
]

def main() -> int:
    errors: list[str] = []

    for path, token in REQUIRED:
        if not path.exists():
            errors.append(f"falta archivo: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if token not in text:
            errors.append(f"falta token en {path.relative_to(ROOT)}: {token}")

    if errors:
        print("ERROR public coverage linking guard:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("OK public coverage linking guard")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
