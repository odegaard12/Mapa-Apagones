#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

REQUIRED_FILES = [
    Path("SECURITY.md"),
    Path("MAINTENANCE.md"),
    Path("CONTRIBUTING.md"),
    Path("README.md"),
    Path("CHANGELOG.md"),
    Path(".github/ISSUE_TEMPLATE/config.yml"),
    Path("frontend/public/seguridad/index.html"),
    Path("frontend/public/sitemap.xml"),
    Path("frontend/src/App.jsx"),
    Path("docs/maintenance/repo-health-roadmap-v1084.md"),
]

errors: list[str] = []


def require(path: Path, snippets: list[str]) -> None:
    if not path.exists():
        errors.append(f"{path}: missing file")
        return

    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )
    folded = text.casefold()

    for snippet in snippets:
        if snippet.casefold() not in folded:
            errors.append(
                f"{path}: missing snippet: {snippet}"
            )


for path in REQUIRED_FILES:
    if not path.exists():
        errors.append(f"{path}: missing file")

require(
    Path("SECURITY.md"),
    [
        "privacidad@mapa-apagones.es",
        "no abras una issue pública",
        "5 días laborables",
        "10 días laborables",
        "divulgación coordinada",
    ],
)

require(
    Path("MAINTENANCE.md"),
    [
        "no abrir PRs mínimos",
        "Dependabot",
        "actualizaciones automáticas de parche",
        "watcher privado",
        "revisión de dependencias",
    ],
)

require(
    Path("README.md"),
    [
        "repo-health-badges:start",
        "actions/workflows",
        "SECURITY.md",
        "MAINTENANCE.md",
        "mapa-apagones.es/seguridad/",
    ],
)

require(
    Path("CONTRIBUTING.md"),
    [
        "security-reporting:start",
        "privacidad@mapa-apagones.es",
        "No abras una issue",
    ],
)

require(
    Path("frontend/public/seguridad/index.html"),
    [
        "Comunicación privada",
        "No lo publiques en una issue",
        "privacidad@mapa-apagones.es",
        "5 días laborables",
    ],
)

require(
    Path("frontend/public/sitemap.xml"),
    [
        "https://mapa-apagones.es/seguridad/",
    ],
)

require(
    Path("frontend/src/App.jsx"),
    [
        'href="/seguridad/"',
        "Seguridad",
    ],
)

require(
    Path(".github/ISSUE_TEMPLATE/config.yml"),
    [
        "mapa-apagones.es/seguridad/",
        "Vulnerabilidad o problema de privacidad",
    ],
)

require(
    Path("CHANGELOG.md"),
    [
        "Security and repository governance",
    ],
)

public_paths = [
    Path("SECURITY.md"),
    Path("MAINTENANCE.md"),
    Path("README.md"),
    Path("CONTRIBUTING.md"),
    Path("frontend/public/seguridad/index.html"),
    Path("docs/maintenance/repo-health-roadmap-v1084.md"),
]

for path in public_paths:
    if not path.exists():
        continue

    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    for pattern in [
        r"(?i)\bTODO\b",
        r"(?i)\bPLACEHOLDER\b",
        r"(?i)security@example\.com",
        r"(?i)api[_-]?key\s*=\s*['\"][^'\"]+",
        r"(?i)password\s*=\s*['\"][^'\"]+",
        r"(?i)private[_-]?key\s*=\s*['\"][^'\"]+",
    ]:
        if re.search(pattern, text):
            errors.append(
                f"{path}: forbidden pattern: {pattern}"
            )

if errors:
    print("FAIL repository governance")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK repository governance")
print("security_policy=present")
print("maintenance_policy=present")
print("ci_badges=present")
print("public_security_page=present")
print("private_reporting_channel=present")
