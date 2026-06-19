#!/usr/bin/env python3
from pathlib import Path

path = Path(".github/dependabot.yml")
text = path.read_text(encoding="utf-8")

required = [
    'package-ecosystem: "npm"',
    'package-ecosystem: "pip"',
    'package-ecosystem: "github-actions"',
    "frontend-runtime-minor-patch",
    "frontend-tooling-minor-patch",
    "backend-patches",
    "github-actions-minor-patch",
    "version-update:semver-major",
    "version-update:semver-minor",
    "open-pull-requests-limit: 2",
]

for value in required:
    if value not in text:
        raise SystemExit(f"ERROR: falta política Dependabot: {value}")

pip_pos = text.find('package-ecosystem: "pip"')
actions_pos = text.find('package-ecosystem: "github-actions"')

if not (0 <= pip_pos < actions_pos):
    raise SystemExit("ERROR: estructura Dependabot inesperada")

pip_block = text[pip_pos:actions_pos]
for value in [
    "backend-patches",
    '"version-update:semver-major"',
    '"version-update:semver-minor"',
]:
    if value not in pip_block:
        raise SystemExit(f"ERROR: falta en bloque pip: {value}")

print("OK Dependabot low-noise policy")
print("npm: majors ignorados")
print("pip: solo parches automáticos")
print("github-actions: majors ignorados")
