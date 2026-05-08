#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")

errors = []

required = [
    "def apply_schema_hardening(",
    "uq_reports_active_incident_reporter",
    "WHERE status = 'active'",
    "idx_reports_status_expires",
    "idx_reports_token_status_updated",
    "idx_reports_zone_status",
    "idx_action_log_token_ip_created",
    "apply_schema_hardening(conn)",
]

for snippet in required:
    if snippet not in main:
        errors.append(f"Falta snippet esperado: {snippet}")

pos_setup = main.find("def setup_db():")
pos_call = main.find("apply_schema_hardening(conn)", pos_setup)
pos_commit = main.find("conn.commit()", pos_setup)

if pos_setup == -1:
    errors.append("No se encuentra setup_db")
elif pos_call == -1:
    errors.append("setup_db no llama a apply_schema_hardening")
elif pos_commit != -1 and pos_call > pos_commit:
    errors.append("apply_schema_hardening debe ejecutarse antes de conn.commit()")

if errors:
    print("ERROR sqlite schema hardening guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK sqlite schema hardening guard")
