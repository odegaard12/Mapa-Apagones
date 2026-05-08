#!/usr/bin/env python3
import fnmatch
import subprocess
import sys

FORBIDDEN_PATTERNS = [
    "*.bak",
    "*.bak.*",
    "*.orig",
    "*.rej",
    "*.tmp",
    "*~",
    "backend/app/*.bak",
    "backend/app/*.bak.*",
    "backend/app/*backup*",
]

ALLOWLIST = {
}

def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]

bad = []

for path in tracked_files():
    if path in ALLOWLIST:
        continue

    for pattern in FORBIDDEN_PATTERNS:
        if fnmatch.fnmatch(path, pattern):
            bad.append(path)
            break

if bad:
    print("ERROR: artefactos backup/temporales trackeados:")
    for path in bad:
        print(f"- {path}")
    sys.exit(1)

print("OK no tracked backup/editor artifacts")
