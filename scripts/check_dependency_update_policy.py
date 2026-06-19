#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


def lock_versions() -> dict[str, str]:
    result: dict[str, str] = {}
    text = Path("backend/requirements.lock.txt").read_text(encoding="utf-8")
    for line in text.splitlines():
        if "==" in line:
            name, version = line.split("==", 1)
            result[name.strip().lower()] = version.strip()
    return result


def major(spec: str) -> int:
    match = re.search(r"(\d+)", spec)
    if not match:
        raise ValueError(f"No major version in {spec!r}")
    return int(match.group(1))


def main() -> int:
    backend = lock_versions()
    frontend = json.loads(
        Path("frontend/package.json").read_text(encoding="utf-8")
    )

    deps = frontend["dependencies"]
    dev = frontend["devDependencies"]

    assert backend["fastapi"] == "0.136.3"
    assert backend["pydantic"] == "2.13.4"
    assert backend["pydantic_core"] == "2.46.4"

    assert major(deps["react"]) == 18
    assert major(deps["react-dom"]) == 18
    assert major(deps["react-leaflet"]) == 4
    assert major(dev["vite"]) == 8
    assert major(dev["@vitejs/plugin-react"]) == 6

    dependabot = Path(".github/dependabot.yml").read_text(encoding="utf-8")
    required = [
        "frontend-runtime-minor-patch",
        "frontend-tooling-minor-patch",
        "backend-patches",
        "version-update:semver-major",
    ]
    for value in required:
        assert value in dependabot, f"Dependabot policy missing {value}"

    print("OK dependency update policy")
    print("fastapi=0.136.3")
    print("pydantic_core=2.46.4")
    print("react_major=18")
    print("react_leaflet_major=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
