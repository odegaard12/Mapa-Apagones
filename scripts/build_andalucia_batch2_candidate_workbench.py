#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

csv.field_size_limit(sys.maxsize)

PENDING_CSV = Path("docs/audit/andalucia_pending_review_queue_v1072.csv")
HINTS_PATH = Path("frontend/src/data/distributor_hints.json")

OUT_CSV = Path("docs/audit/andalucia_batch2_candidate_workbench_v1074.csv")
OUT_MD = Path("docs/audit/andalucia-batch2-candidate-workbench-v1074.md")

EXPECTED_PENDING = 532
EXPECTED_COVERED = 254

SOURCE_CSVS = [
    Path("docs/research/distributor_regional_audits/edistribucion_review_queue_by_dataset/andalucia.csv"),
    Path("docs/research/distributor_regional_audits/edistribucion_local_exception_hunt_by_dataset/andalucia.csv"),
    Path("docs/research/distributor_regional_audits/remaining_regional_review_queue_by_dataset/andalucia.csv"),
    Path("docs/research/distributor_regional_audits/edistribucion_coverage_candidates.csv"),
    Path("docs/research/distributor_regional_audits/remaining_regional_distributor_candidates_v1023.csv"),
]

CANONICAL_DISTRIBUTOR = "E-Distribución Redes Digitales, S.L.U."


def norm(value: object) -> str:
    text = str(value or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def compact(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", norm(value))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
        return list(csv.DictReader(fh))


def load_pending() -> list[dict[str, str]]:
    rows = read_csv(PENDING_CSV)
    if len(rows) != EXPECTED_PENDING:
        raise SystemExit(f"ERROR pending queue rows={len(rows)} expected={EXPECTED_PENDING}")

    seen: set[str] = set()
    for row in rows:
        zone_id = row.get("zone_id", "")
        if not zone_id:
            raise SystemExit(f"ERROR pending row without zone_id: {row}")
        if zone_id in seen:
            raise SystemExit(f"ERROR duplicated pending zone_id={zone_id}")
        seen.add(zone_id)

    return rows


def load_covered_zone_ids() -> set[str]:
    data = json.loads(HINTS_PATH.read_text(encoding="utf-8"))
    covered: set[str] = set()

    for item in data.get("items", []):
        if item.get("dataset_id") != "andalucia":
            continue
        zone_id = str(item.get("zone_id") or "").strip()
        if not zone_id:
            raise SystemExit(f"ERROR Andalucía hint without zone_id: {item}")
        covered.add(zone_id)

    if len(covered) != EXPECTED_COVERED:
        raise SystemExit(f"ERROR covered={len(covered)} expected={EXPECTED_COVERED}")

    return covered


def first_by_col_terms(row: dict[str, str], terms: list[str]) -> str:
    exact = {k.lower(): k for k in row}
    for term in terms:
        if term in exact and str(row.get(exact[term]) or "").strip():
            return str(row.get(exact[term]) or "").strip()

    for key, value in row.items():
        key_l = key.lower()
        if any(term in key_l for term in terms):
            v = str(value or "").strip()
            if v:
                return v

    return ""


def http_urls(row: dict[str, str]) -> list[str]:
    text = " ".join(str(v or "") for v in row.values())
    urls = re.findall(r"https?://[^\s,;\"')]+", text)
    cleaned = []
    for url in urls:
        if url not in cleaned:
            cleaned.append(url)
    return cleaned[:3]


def source_row_text(row: dict[str, str], source: Path) -> str:
    return f"{source} " + " ".join(str(v or "") for v in row.values())


def is_bad_candidate(text_norm: str) -> bool:
    bad = [
        "red electrica",
        "ree",
        "pequena distribuidora",
        "pequeña distribuidora",
        "sin identificar",
        "generica",
        "generic",
    ]
    return any(token in text_norm for token in bad)


def is_edistribucion_candidate(text_norm: str, source: Path) -> bool:
    source_norm = norm(source)
    tokens = [
        "edistribucion",
        "e distribucion",
        "e distribucion redes digitales",
        "endesa distribucion",
    ]
    return any(token in text_norm for token in tokens) or "edistribucion" in source_norm


def build_indexes(pending_rows: list[dict[str, str]]):
    by_zone = {row["zone_id"]: row for row in pending_rows}
    by_name_prov: dict[tuple[str, str], dict[str, str]] = {}
    by_name: dict[str, list[dict[str, str]]] = {}

    for row in pending_rows:
        name = norm(row.get("municipality"))
        prov = norm(row.get("province"))
        if name and prov:
            by_name_prov[(name, prov)] = row
        if name:
            by_name.setdefault(name, []).append(row)

    return by_zone, by_name_prov, by_name


def match_pending(
    source_row: dict[str, str],
    source: Path,
    by_zone: dict[str, dict[str, str]],
    by_name_prov: dict[tuple[str, str], dict[str, str]],
    by_name: dict[str, list[dict[str, str]]],
) -> tuple[dict[str, str] | None, str]:
    zone_id = first_by_col_terms(source_row, ["zone_id", "zone", "municipio", "mun_code", "ine", "id"])
    if zone_id in by_zone:
        return by_zone[zone_id], "zone_id"

    municipality = first_by_col_terms(
        source_row,
        ["municipality", "municipio", "mun_name", "nombre_municipio", "localidad", "name"],
    )
    province = first_by_col_terms(
        source_row,
        ["province", "provincia", "prov_name", "nombre_provincia"],
    )

    name_n = norm(municipality)
    prov_n = norm(province)

    if name_n and prov_n and (name_n, prov_n) in by_name_prov:
        return by_name_prov[(name_n, prov_n)], "municipality_province"

    if name_n and name_n in by_name and len(by_name[name_n]) == 1:
        return by_name[name_n][0], "unique_municipality"

    # Fallback: some old research CSVs may not have clean columns.
    # Search compact municipality tokens in the source row text.
    text_c = compact(source_row_text(source_row, source))
    matches = []
    for name_key, rows in by_name.items():
        if len(name_key) < 4:
            continue
        if compact(name_key) and compact(name_key) in text_c:
            matches.extend(rows)

    unique_by_zone = {r["zone_id"]: r for r in matches}
    if len(unique_by_zone) == 1:
        return next(iter(unique_by_zone.values())), "text_unique_municipality"

    return None, ""


def score_candidate(source: Path, row: dict[str, str], match_method: str) -> int:
    text_n = norm(source_row_text(row, source))
    score = 0

    if match_method == "zone_id":
        score += 60
    elif match_method == "municipality_province":
        score += 45
    elif match_method == "unique_municipality":
        score += 35
    elif match_method == "text_unique_municipality":
        score += 25

    if is_edistribucion_candidate(text_n, source):
        score += 30

    if http_urls(row):
        score += 10

    for key in row:
        key_l = key.lower()
        if any(token in key_l for token in ["score", "confidence", "percent", "pct", "share", "match"]):
            value = str(row.get(key) or "")
            if re.search(r"\b(9[5-9]|100)\b", value):
                score += 15
            elif re.search(r"\b(8[5-9]|9[0-4])\b", value):
                score += 8

    if is_bad_candidate(text_n):
        score -= 200

    return score


def short_evidence(row: dict[str, str]) -> str:
    preferred_terms = [
        "reason",
        "evidence",
        "source",
        "label",
        "match",
        "score",
        "confidence",
        "notes",
        "candidate",
    ]

    parts = []
    for key, value in row.items():
        v = str(value or "").strip()
        if not v:
            continue
        key_l = key.lower()
        if any(term in key_l for term in preferred_terms):
            snippet = v.replace("\n", " ").replace("\r", " ")
            if len(snippet) > 180:
                snippet = snippet[:177] + "..."
            parts.append(f"{key}={snippet}")
        if len(parts) >= 6:
            break

    return " | ".join(parts)


def assert_safe_output(rows: list[dict[str, str]]) -> None:
    forbidden_columns = {
        "cups",
        "token",
        "password",
        "secret",
        "private_key",
        "api_key",
        "authorization",
        "lat",
        "latitude",
        "lon",
        "longitude",
        "coord",
        "coordinates",
        "address",
        "direccion",
        "dirección",
    }

    for row in rows:
        for key in row:
            if str(key).lower() in forbidden_columns:
                raise SystemExit(f"ERROR forbidden column {key!r}")

        joined = " ".join(str(v or "") for v in row.values()).lower()
        for marker in ["cups", "token", "password", "secret", "private_key", "api_key", "authorization"]:
            if marker in joined:
                raise SystemExit(f"ERROR forbidden marker {marker!r} in row {row.get('zone_id')}")

        if row.get("proposed_import_action") != "manual_review_only":
            raise SystemExit(f"ERROR row is not manual_review_only: {row}")

        if row.get("candidate_confidence") != "manual_review_required":
            raise SystemExit(f"ERROR candidate confidence must stay manual_review_required: {row}")


def main() -> int:
    pending_rows = load_pending()
    covered = load_covered_zone_ids()
    by_zone, by_name_prov, by_name = build_indexes(pending_rows)

    candidates: dict[str, dict[str, str]] = {}
    source_file_counts = Counter()
    scanned_rows = 0
    matched_rows = 0

    for source in SOURCE_CSVS:
        if not source.exists():
            continue

        rows = read_csv(source)
        source_file_counts[str(source)] = len(rows)

        for source_row in rows:
            scanned_rows += 1
            text_n = norm(source_row_text(source_row, source))

            if not is_edistribucion_candidate(text_n, source):
                continue
            if is_bad_candidate(text_n):
                continue

            pending, method = match_pending(source_row, source, by_zone, by_name_prov, by_name)
            if not pending:
                continue

            if pending["zone_id"] in covered:
                continue

            matched_rows += 1
            score = score_candidate(source, source_row, method)

            if score < 45:
                continue

            urls = http_urls(source_row)
            candidate = {
                "dataset_id": "andalucia",
                "zone_id": pending["zone_id"],
                "municipality": pending["municipality"],
                "province": pending["province"],
                "candidate_distributor": CANONICAL_DISTRIBUTOR,
                "candidate_confidence": "manual_review_required",
                "proposed_import_action": "manual_review_only",
                "score": str(score),
                "match_method": method,
                "source_file": str(source),
                "source_url_1": urls[0] if len(urls) > 0 else "",
                "source_url_2": urls[1] if len(urls) > 1 else "",
                "source_url_3": urls[2] if len(urls) > 2 else "",
                "evidence_summary": short_evidence(source_row),
                "review_notes": "",
            }

            old = candidates.get(pending["zone_id"])
            if old is None or int(candidate["score"]) > int(old["score"]):
                candidates[pending["zone_id"]] = candidate

    output_rows = sorted(
        candidates.values(),
        key=lambda r: (r["province"], r["municipality"], -int(r["score"]), r["zone_id"]),
    )

    assert_safe_output(output_rows)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "dataset_id",
        "zone_id",
        "municipality",
        "province",
        "candidate_distributor",
        "candidate_confidence",
        "proposed_import_action",
        "score",
        "match_method",
        "source_file",
        "source_url_1",
        "source_url_2",
        "source_url_3",
        "evidence_summary",
        "review_notes",
    ]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    by_province = Counter(row["province"] for row in output_rows)
    by_method = Counter(row["match_method"] for row in output_rows)

    lines = []
    lines.append("# Andalucía batch 2 candidate workbench v0.10.7.4")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Pending queue rows available: **{len(pending_rows)}**")
    lines.append(f"- Already covered Andalucía hints: **{len(covered)}**")
    lines.append(f"- Source CSV rows scanned: **{scanned_rows}**")
    lines.append(f"- Source rows matched before scoring: **{matched_rows}**")
    lines.append(f"- Candidate workbench rows: **{len(output_rows)}**")
    lines.append(f"- CSV: `{OUT_CSV}`")
    lines.append("")
    lines.append("## Source files scanned")
    lines.append("")
    lines.append("| source file | rows |")
    lines.append("|---|---:|")
    for path, count in sorted(source_file_counts.items()):
        lines.append(f"| `{path}` | {count} |")
    lines.append("")
    lines.append("## Candidates by province")
    lines.append("")
    lines.append("| province | candidates |")
    lines.append("|---|---:|")
    for province, count in sorted(by_province.items()):
        lines.append(f"| {province or 'unknown'} | {count} |")
    lines.append("")
    lines.append("## Match methods")
    lines.append("")
    lines.append("| match method | rows |")
    lines.append("|---|---:|")
    for method, count in sorted(by_method.items()):
        lines.append(f"| `{method}` | {count} |")
    lines.append("")
    lines.append("## Safety")
    lines.append("")
    lines.append("This workbench is not an import file.")
    lines.append("")
    lines.append("- Every row remains `manual_review_only`.")
    lines.append("- Every candidate confidence remains `manual_review_required`.")
    lines.append("- No distributor hint is imported by this script.")
    lines.append("- No CUPS, addresses, exact coordinates, secrets or raw API responses are added.")
    lines.append("- Future data imports must manually review evidence before promoting any row to `verified_partial`.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK wrote {OUT_CSV}")
    print(f"OK wrote {OUT_MD}")
    print(f"pending_rows={len(pending_rows)}")
    print(f"covered={len(covered)}")
    print(f"source_rows_scanned={scanned_rows}")
    print(f"matched_rows={matched_rows}")
    print(f"candidate_rows={len(output_rows)}")
    print("candidates_by_province=", dict(sorted(by_province.items())))
    print("match_methods=", dict(sorted(by_method.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
