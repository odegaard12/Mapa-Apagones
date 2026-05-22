#!/usr/bin/env python3
"""
Verifica sincronía entre:
- VERSION
- frontend/src/App.jsx APP_VERSION
- frontend/src/data/distributor_hints.json["version"]
- frontend/public/data/distributor_hints.json["version"]

También verifica que los dos distributor_hints.json sean byte-a-byte idénticos.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "VERSION").exists() and (candidate / "frontend").exists():
            return candidate
    raise FileNotFoundError(f"No se encontró raíz del repo desde {start}")


def read_repo_version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def read_app_version(root: Path) -> str:
    path = root / "frontend" / "src" / "App.jsx"
    text = path.read_text(encoding="utf-8")
    matches = re.findall(
        r"\b(?:const|let|var)\s+APP_VERSION\s*=\s*['\"]([^'\"]+)['\"]",
        text,
    )
    if not matches:
        raise ValueError(f"APP_VERSION no encontrado en {path.relative_to(root)}")
    if len(matches) > 1:
        raise ValueError(f"APP_VERSION ambiguo en {path.relative_to(root)}: {matches}")
    return matches[0]


def read_json_version(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "version" not in data:
        raise KeyError(f"Campo 'version' ausente en {path}")
    if not isinstance(data["version"], str):
        raise TypeError(f"Campo 'version' no es string en {path}: {data['version']!r}")
    return data["version"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=None)
    args = parser.parse_args()

    root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path(__file__).resolve())

    sources: list[tuple[str, str | None]] = []
    errors: list[str] = []

    try:
        sources.append(("VERSION", read_repo_version(root)))
    except Exception as exc:
        sources.append(("VERSION", None))
        errors.append(f"[VERSION] ERROR: {exc}")

    try:
        sources.append(("frontend/src/App.jsx APP_VERSION", read_app_version(root)))
    except Exception as exc:
        sources.append(("frontend/src/App.jsx APP_VERSION", None))
        errors.append(f"[App.jsx] ERROR: {exc}")

    json_paths = [
        root / "frontend" / "src" / "data" / "distributor_hints.json",
        root / "frontend" / "public" / "data" / "distributor_hints.json",
    ]

    for path in json_paths:
        rel = str(path.relative_to(root))
        try:
            sources.append((f'{rel} ["version"]', read_json_version(path)))
        except Exception as exc:
            sources.append((f'{rel} ["version"]', None))
            errors.append(f"[{rel}] ERROR: {exc}")

    print("=== check_distributor_data_version ===")
    for name, value in sources:
        print(f"{name:<62} {value}")

    values = [value for _, value in sources if value is not None]
    if len(set(values)) > 1:
        errors.append(f"Versiones divergentes: {sorted(set(values))}")

    try:
        src_hash = sha256(json_paths[0])
        public_hash = sha256(json_paths[1])
        print(f"{str(json_paths[0].relative_to(root)):<62} sha256={src_hash}")
        print(f"{str(json_paths[1].relative_to(root)):<62} sha256={public_hash}")
        if src_hash != public_hash:
            errors.append("Los dos distributor_hints.json no son byte-a-byte idénticos")
    except Exception as exc:
        errors.append(f"ERROR comparando SHA256 de JSON: {exc}")

    if errors:
        print()
        print("ERRORES DETECTADOS:")
        for err in errors:
            print(f"  - {err}")
        print()
        print("FAIL: distributor_hints metadata/version desincronizada")
        return 1

    print()
    print("OK: VERSION, APP_VERSION y distributor_hints.json version están sincronizados")
    print("OK: distributor_hints.json src/public son byte-a-byte idénticos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
