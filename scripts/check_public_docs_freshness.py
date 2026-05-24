#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

APP_VER = "v0.10.6.4-distributor-confidence-labels"

REQUIRED_FILES = [
    Path("README.md"),
    Path("CHANGELOG.md"),
    Path("frontend/public/changelog.html"),
    Path("docs/audit/andalucia-distributor-pending-audit-v1070.md"),
    Path("docs/audit/andalucia-geo-source-locator-v1071.md"),
    Path("docs/audit/andalucia-pending-review-queue-v1072.md"),
    Path("docs/audit/andalucia-v1072-closeout.md"),
    Path("docs/audit/andalucia-batch2-candidate-workbench-v1074.md"),
    Path("docs/audit/public-docs-national-validation-v1075.md"),
    Path("docs/audit/static-public-pages-clean-v1077.md"),
    Path("scripts/check_distributor_data_version.py"),
    Path("scripts/check_andalucia_pending_review_queue.py"),
    Path("scripts/check_andalucia_batch2_candidate_workbench.py"),
    Path("scripts/run_public_smoke_expected_version.sh"),
]

REQUIRED_TEXT_CASE_INSENSITIVE = {
    "README.md": [
        "versión actual visible: v0.10.6.4-distributor-confidence-labels",
        "andalucía",
        "scripts/post_merge_validate.sh",
        "check_public_docs_freshness.py",
    ],
    "CHANGELOG.md": [
        "andalucía",
        "batch 2",
        "532",
        "check_andalucia_batch2_candidate_workbench.py",
    ],
    "frontend/public/changelog.html": [
        "v0.10.7.7",
        "Static public pages clean refresh",
        "v0.10.7.6",
        "v0.10.7.5",
        "v0.10.6.4-distributor-confidence-labels",
    ],
    "scripts/post_merge_validate.sh": [
        "check_distributor_data_version.py",
        "check_andalucia_pending_review_queue.py",
        "check_andalucia_batch2_candidate_workbench.py",
        "check_public_docs_freshness.py",
    ],
    "docs/audit/public-docs-national-validation-v1075.md": [
        "2610",
        "786",
        "254",
        "532",
        "check_public_docs_freshness.py",
    ],
}

# Patrones de secretos reales. No bloquea variables documentadas vacías tipo
# TURNSTILE_SECRET_KEY= porque aparecen en README/.env.example como ejemplo.
FORBIDDEN_PATTERNS = [
    re.compile(r"gho_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required file: {path}")

    for file_name, snippets in REQUIRED_TEXT_CASE_INSENSITIVE.items():
        path = Path(file_name)
        if not path.exists():
            errors.append(f"missing text-check file: {path}")
            continue

        text = read(path).lower()
        for snippet in snippets:
            if snippet.lower() not in text:
                errors.append(f"{path}: missing snippet: {snippet}")

    for path in [
        Path("README.md"),
        Path("CHANGELOG.md"),
        Path("frontend/public/changelog.html"),
        Path("docs/audit/public-docs-national-validation-v1075.md"),
    Path("docs/audit/static-public-pages-clean-v1077.md"),
    ]:
        if not path.exists():
            continue

        text = read(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path}: forbidden sensitive pattern: {pattern.pattern}")

    version_path = Path("VERSION")
    if version_path.exists():
        version = read(version_path).strip()
        if version != APP_VER:
            errors.append(f"VERSION mismatch: {version} != {APP_VER}")

    if errors:
        print("FAIL public docs freshness")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK public docs freshness")
    return 0


if __name__ == "__main__":
    sys.exit(main())
