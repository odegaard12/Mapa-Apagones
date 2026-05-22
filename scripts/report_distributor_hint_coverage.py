#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


DATA_PATH = Path("frontend/src/data/distributor_hints.json")
OUT_PATH = Path("docs/audit/distributor-coverage-snapshot-v1068.md")


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    items = data["items"]

    by_dataset = defaultdict(list)
    confidence_counter = Counter()
    dataset_conf = defaultdict(Counter)
    distributor_counter = Counter()

    for item in items:
        dataset_id = item.get("dataset_id", "unknown")
        by_dataset[dataset_id].append(item)

        for dist in item.get("distributors", []):
            confidence = dist.get("confidence", "unknown")
            confidence_counter[confidence] += 1
            dataset_conf[dataset_id][confidence] += 1
            name = dist.get("name", "unknown")
            distributor_counter[name] += 1

    lines = []
    lines.append("# Distributor hints coverage snapshot v0.10.6.8")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This report summarizes the public distributor hints dataset.")
    lines.append("")
    lines.append("Privacy constraints:")
    lines.append("")
    lines.append("- No CUPS.")
    lines.append("- No addresses.")
    lines.append("- No exact user coordinates.")
    lines.append("- No private infrastructure inventory.")
    lines.append("- No raw external API responses.")
    lines.append("")
    lines.append("## Dataset summary")
    lines.append("")
    lines.append(f"- JSON version: `{data.get('version')}`")
    lines.append(f"- Public hint zones: **{len(items)}**")
    lines.append(f"- Dataset ids with hints: **{len(by_dataset)}**")
    lines.append("")
    lines.append("## Confidence distribution")
    lines.append("")
    lines.append("| confidence | entries |")
    lines.append("|---|---:|")
    for confidence, count in sorted(confidence_counter.items()):
        lines.append(f"| `{confidence}` | {count} |")
    lines.append("")
    lines.append("## Coverage by dataset")
    lines.append("")
    lines.append("| dataset_id | zones | regional_default | verified_partial | other/unknown |")
    lines.append("|---|---:|---:|---:|---:|")

    for dataset_id in sorted(by_dataset):
        conf = dataset_conf[dataset_id]
        total_zones = len(by_dataset[dataset_id])
        regional = conf.get("regional_default", 0)
        verified = conf.get("verified_partial", 0)
        other = sum(conf.values()) - regional - verified
        lines.append(
            f"| `{dataset_id}` | {total_zones} | {regional} | {verified} | {other} |"
        )

    lines.append("")
    lines.append("## Top public distributor names")
    lines.append("")
    lines.append("| distributor | entries |")
    lines.append("|---|---:|")
    for name, count in distributor_counter.most_common(30):
        safe_name = str(name).replace("|", "\\|")
        lines.append(f"| {safe_name} | {count} |")

    lines.append("")
    lines.append("## Recommended next work")
    lines.append("")
    lines.append("Priority should favor conservative, source-backed improvements:")
    lines.append("")
    lines.append("1. Expand `verified_partial` only where strong public evidence exists.")
    lines.append("2. Avoid converting broad regional defaults into municipal claims without evidence.")
    lines.append("3. Keep local distributors visible only when supported by public sources.")
    lines.append("4. Prefer research/audit PRs before data import PRs for large communities.")
    lines.append("")
    lines.append("Suggested next data targets:")
    lines.append("")
    lines.append("- Andalucía: continue pending municipal review after the strong E-Distribución import.")
    lines.append("- Extremadura: continue municipal review queue before importing further hints.")
    lines.append("- Madrid: review remaining mixed/local distributor cases.")
    lines.append("- Castilla y León / Castilla-La Mancha: start with research PRs, not direct import.")
    lines.append("")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OK wrote {OUT_PATH}")
    print(f"items={len(items)}")
    print(f"datasets={len(by_dataset)}")
    print("confidence=", dict(sorted(confidence_counter.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
