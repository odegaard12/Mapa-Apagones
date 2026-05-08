#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")

errors = []

for snippet in [
    "def begin_report_write_transaction(",
    "BEGIN IMMEDIATE",
    '@app.post("/api/report")',
    "begin_report_write_transaction(conn)",
]:
    if snippet not in main:
        errors.append(f"Falta snippet esperado: {snippet}")

pos_route = main.find('@app.post("/api/report")')
pos_call = main.find("begin_report_write_transaction(conn)", pos_route)

if pos_route == -1:
    errors.append("No se encuentra endpoint /api/report")
elif pos_call == -1:
    errors.append("/api/report no llama a begin_report_write_transaction(conn)")
else:
    pos_cleanup = main.find("cleanup_old(conn)", pos_route)
    if pos_cleanup == -1:
        errors.append("/api/report no contiene cleanup_old(conn)")
    elif not (pos_cleanup < pos_call < pos_cleanup + 200):
        errors.append("begin_report_write_transaction no está justo después de cleanup_old(conn) en /api/report")

if errors:
    print("ERROR report transaction guard")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK report transaction guard")
