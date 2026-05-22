#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

OUT = Path("docs/audit/andalucia-geo-source-locator-v1071.md")

TEXT_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".json", ".geojson", ".md",
    ".html", ".csv", ".txt", ".py"
}

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".venv", "venv",
    "__pycache__", ".pytest_cache"
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        yield path


def safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def count_geojson_features(path: Path, text: str) -> int | None:
    if path.suffix.lower() not in {".json", ".geojson"}:
        return None
    try:
        data = json.loads(text)
    except Exception:
        return None

    if isinstance(data, dict) and isinstance(data.get("features"), list):
        return len(data["features"])
    if isinstance(data, list):
        return len(data)
    return None


def main() -> int:
    root = Path(".")
    hits = []

    patterns = [
        re.compile(r"andalucia", re.IGNORECASE),
        re.compile(r"andalucía", re.IGNORECASE),
        re.compile(r"dataset_id['\"]?\s*[:=]\s*['\"]andalucia['\"]", re.IGNORECASE),
    ]

    for path in iter_files(root):
        text = safe_read(path)
        if text is None:
            continue

        lower = text.lower()
        if "andalucia" not in lower and "andalucía" not in lower:
            continue

        matched = []
        for pat in patterns:
            if pat.search(text):
                matched.append(pat.pattern)

        dataset_mentions = len(re.findall(r"dataset_id", text, flags=re.IGNORECASE))
        zone_mentions = len(re.findall(r"zone_id", text, flags=re.IGNORECASE))
        feature_count = count_geojson_features(path, text)

        hits.append({
            "path": str(path),
            "size": path.stat().st_size,
            "matched": matched,
            "dataset_mentions": dataset_mentions,
            "zone_mentions": zone_mentions,
            "feature_count": feature_count,
        })

    hits.sort(key=lambda h: (0 if "frontend" in h["path"] else 1, h["path"]))

    by_ext = Counter(Path(h["path"]).suffix.lower() or "(none)" for h in hits)

    lines = []
    lines.append("# Andalucía geo source locator v0.10.7.1")
    lines.append("")
    lines.append("This research report locates repository files that mention Andalucía/andalucia.")
    lines.append("")
    lines.append("It does not import distributor data and does not modify datasets.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Candidate files found: **{len(hits)}**")
    lines.append("")
    lines.append("## Candidate files by extension")
    lines.append("")
    lines.append("| extension | files |")
    lines.append("|---|---:|")
    for ext, count in sorted(by_ext.items()):
        lines.append(f"| `{ext}` | {count} |")
    lines.append("")
    lines.append("## Candidate files")
    lines.append("")
    lines.append("| file | bytes | dataset_id mentions | zone_id mentions | parsed feature/list count |")
    lines.append("|---|---:|---:|---:|---:|")

    for h in hits[:200]:
        fc = "" if h["feature_count"] is None else str(h["feature_count"])
        lines.append(
            f"| `{h['path']}` | {h['size']} | {h['dataset_mentions']} | "
            f"{h['zone_mentions']} | {fc} |"
        )

    lines.append("")
    lines.append("## Next step")
    lines.append("")
    lines.append("Use this locator to identify the real Andalucía municipal source file before")
    lines.append("building a sanitized pending review CSV.")
    lines.append("")
    lines.append("A future queue builder must only use repository-local public geography and")
    lines.append("must keep these constraints:")
    lines.append("")
    lines.append("- No CUPS.")
    lines.append("- No addresses.")
    lines.append("- No exact coordinates in the generated review queue.")
    lines.append("- No customer data.")
    lines.append("- No private grid inventory.")
    lines.append("- No raw external API responses.")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK wrote {OUT}")
    print(f"candidate_files={len(hits)}")
    for h in hits[:30]:
        print(f"- {h['path']} size={h['size']} dataset_id={h['dataset_mentions']} zone_id={h['zone_mentions']} features={h['feature_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
