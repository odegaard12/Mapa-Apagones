#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_BIN = os.environ.get("SMOKE_PYTHON") or sys.executable

PHASES = [
    ("backend_api", "scripts/smoke_backend_api.py", 20.0),
    ("report_lifecycle", "scripts/smoke_backend_lifecycle.py", 25.0),
    ("report_concurrency", "scripts/smoke_backend_concurrency.py", 25.0),
    ("privacy_abuse", "scripts/smoke_backend_privacy_abuse.py", 30.0),
]


def run_phase(name: str, script: str, threshold: float) -> tuple[bool, float]:
    cmd = [PYTHON_BIN, script]
    start = time.perf_counter()

    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
        check=False,
    )

    elapsed = time.perf_counter() - start
    ok = completed.returncode == 0 and elapsed <= threshold

    print(f"{name}: elapsed={elapsed:.3f}s threshold={threshold:.3f}s returncode={completed.returncode}")

    if not ok:
        print("---- output tail ----")
        print("\n".join((completed.stdout or "").splitlines()[-40:]))
        print("---------------------")

    return ok, elapsed


def main() -> int:
    print("== Mapa Apagones · reporting timing smoke ==")
    print(f"Repo: {ROOT}")
    print(f"Python: {PYTHON_BIN}")
    print()

    errors: list[str] = []
    total_start = time.perf_counter()

    for name, script, threshold in PHASES:
        ok, elapsed = run_phase(name, script, threshold)
        if not ok:
            errors.append(f"{name} failed or exceeded threshold ({elapsed:.3f}s > {threshold:.3f}s)")

    total_elapsed = time.perf_counter() - total_start

    print()
    print(f"total_elapsed={total_elapsed:.3f}s")

    if errors:
        print("ERROR reporting timing smoke:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("OK reporting timing smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
