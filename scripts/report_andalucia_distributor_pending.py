#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

DATA_PATH = Path("frontend/src/data/distributor_hints.json")
OUT_PATH = Path("docs/audit/andalucia-distributor-pending-audit-v1070.md")

ANDALUCIA_TOTAL_EXPECTED = 786


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    items = data["items"]

    andalucia = [
        item for item in items
        if item.get("dataset_id") == "andalucia"
    ]

    conf = Counter()
    distributors = Counter()

    for item in andalucia:
        for dist in item.get("distributors", []):
            conf[dist.get("confidence", "unknown")] += 1
            distributors[dist.get("name", "unknown")] += 1

    covered = len(andalucia)
    pending = max(ANDALUCIA_TOTAL_EXPECTED - covered, 0)

    lines = []
    lines.append("# Andalucía distributor pending audit v0.10.7.0")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This is a research/audit scaffold for the next Andalucía distributor work.")
    lines.append("")
    lines.append("It does not import distributor hints and does not modify public data.")
    lines.append("")
    lines.append("## Current Andalucía baseline")
    lines.append("")
    lines.append(f"- Expected Andalucía municipalities/zones: **{ANDALUCIA_TOTAL_EXPECTED}**")
    lines.append(f"- Current Andalucía public hint zones: **{covered}**")
    lines.append(f"- Pending review estimate: **{pending}**")
    lines.append("")
    lines.append("## Confidence distribution in current Andalucía hints")
    lines.append("")
    lines.append("| confidence | entries |")
    lines.append("|---|---:|")
    for key, value in sorted(conf.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("## Current public distributor names in Andalucía")
    lines.append("")
    lines.append("| distributor | entries |")
    lines.append("|---|---:|")
    for name, value in distributors.most_common():
        lines.append(f"| {str(name).replace('|', '\\|')} | {value} |")
    lines.append("")
    lines.append("## Recommended next audit method")
    lines.append("")
    lines.append("Future Andalucía imports should be split into small batches.")
    lines.append("")
    lines.append("For every candidate municipality:")
    lines.append("")
    lines.append("1. Require public, source-backed evidence.")
    lines.append("2. Import only as `verified_partial`.")
    lines.append("3. Do not assert exclusivity.")
    lines.append("4. Do not use `regional_default` for municipal claims.")
    lines.append("5. Exclude Red Eléctrica as a distribution-company hint.")
    lines.append("6. Exclude generic labels such as `Pequeña distribuidora`.")
    lines.append("")
    lines.append("## Privacy and safety constraints")
    lines.append("")
    lines.append("- No CUPS.")
    lines.append("- No addresses.")
    lines.append("- No exact coordinates.")
    lines.append("- No customer data.")
    lines.append("- No raw external API responses.")
    lines.append("- No private grid inventory.")
    lines.append("- No substations, transformers, lines or internal network geometry.")
    lines.append("")
    lines.append("## Proposed next PR sequence")
    lines.append("")
    lines.append("1. Build a sanitized local review queue for Andalucía pending zones.")
    lines.append("2. Manually classify only strong public candidates.")
    lines.append("3. Import a small batch of `verified_partial` hints.")
    lines.append("4. Re-run public smoke, version guard and distributor hint guard.")
    lines.append("")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OK wrote {OUT_PATH}")
    print(f"andalucia_covered={covered}")
    print(f"andalucia_pending_estimate={pending}")
    print("confidence=", dict(sorted(conf.items())))
    print("distributors=", dict(distributors.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
