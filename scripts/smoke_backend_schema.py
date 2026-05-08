#!/usr/bin/env python3
import json
import os
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])

def request_json(url: str) -> tuple[int, dict]:
    req = Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body or "{}")
        except Exception:
            parsed = {"raw": body}
        return exc.code, parsed

def wait_health(base_url: str) -> None:
    last = None
    for _ in range(60):
        try:
            status, body = request_json(f"{base_url}/api/health")
            if status == 200 and body.get("ok") is True:
                return
            last = f"{status} {body}"
        except Exception as exc:
            last = exc
        time.sleep(0.2)
    raise RuntimeError(f"backend health timeout: {last}")

def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"

    with tempfile.TemporaryDirectory(prefix="apagones-schema-") as tmp:
        db_path = Path(tmp) / "app.db"
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": str(BACKEND),
            "DB_PATH": str(db_path),
            "IGN_WFS_ENABLED": "0",
            "TURNSTILE_ENABLED": "0",
            "TURNSTILE_REQUIRED": "0",
            "ANON_HASH_KEY": "schema-test-anon-hash-key-not-secret",
            "ANON_HASH_KEY_REQUIRED": "1",
            "ANON_HASH_LEGACY_COMPAT": "0",
            "TRUST_PROXY_HEADERS": "1",
            "TRUSTED_PROXY_CIDRS": "127.0.0.1/32,::1/128",
        })

        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)],
            cwd=str(BACKEND),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        try:
            wait_health(base_url)

            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            try:
                indexes = {
                    row["name"]: row["sql"] or ""
                    for row in conn.execute(
                        "SELECT name, sql FROM sqlite_master WHERE type = 'index'"
                    ).fetchall()
                }

                required_indexes = [
                    "uq_reports_active_incident_reporter",
                    "idx_reports_status_expires",
                    "idx_reports_token_status_updated",
                    "idx_reports_zone_status",
                    "idx_action_log_token_ip_created",
                ]

                for index_name in required_indexes:
                    if index_name not in indexes:
                        raise RuntimeError(f"falta índice requerido: {index_name}")

                uq_sql = indexes["uq_reports_active_incident_reporter"].lower()
                if "unique" not in uq_sql or "where status = 'active'" not in uq_sql:
                    raise RuntimeError(f"índice único parcial mal definido: {indexes['uq_reports_active_incident_reporter']}")

                now = datetime.now(timezone.utc).replace(microsecond=0)
                now_s = now.isoformat()
                exp_s = (now + timedelta(hours=3)).isoformat()

                conn.execute(
                    """
                    INSERT INTO incidents (
                        id, cell_key, status, primary_type,
                        center_lat, center_lng,
                        lat_min, lat_max, lng_min, lng_max,
                        report_count_active, unique_reporters_active,
                        created_at, last_report_at, resolved_at,
                        municipio, province, country, display_zone, zone_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "schema-incident-1", "schema-cell-1", "senal_debil", "sin_luz",
                        42.8782, -8.5448,
                        42.87, 42.89, -8.55, -8.53,
                        1, 1,
                        now_s, now_s, None,
                        None, None, None, "Zona test", "schema-zone-1",
                    ),
                )

                conn.execute(
                    """
                    INSERT INTO reports (
                        id, incident_id, reporter_token_hash, ip_hash,
                        report_type, status, lat, lng,
                        created_at, updated_at, expires_at, zone_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "schema-report-1", "schema-incident-1",
                        "a" * 64, "b" * 64,
                        "sin_luz", "active", 42.8782, -8.5448,
                        now_s, now_s, exp_s, "schema-zone-1",
                    ),
                )

                try:
                    conn.execute(
                        """
                        INSERT INTO reports (
                            id, incident_id, reporter_token_hash, ip_hash,
                            report_type, status, lat, lng,
                            created_at, updated_at, expires_at, zone_id
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            "schema-report-2", "schema-incident-1",
                            "a" * 64, "c" * 64,
                            "microcortes", "active", 42.8783, -8.5449,
                            now_s, now_s, exp_s, "schema-zone-1",
                        ),
                    )
                    raise RuntimeError("el índice único parcial no bloqueó duplicado activo por reporter/incidencia")
                except sqlite3.IntegrityError:
                    pass

                conn.execute(
                    """
                    INSERT INTO reports (
                        id, incident_id, reporter_token_hash, ip_hash,
                        report_type, status, lat, lng,
                        created_at, updated_at, expires_at, zone_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        "schema-report-3", "schema-incident-1",
                        "a" * 64, "d" * 64,
                        "microcortes", "inactive", 42.8784, -8.5450,
                        now_s, now_s, exp_s, "schema-zone-1",
                    ),
                )

                conn.commit()
            finally:
                conn.close()

            print("OK backend schema smoke")
            return 0
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

            if proc.returncode not in (0, -15, 143, None):
                output = proc.stdout.read() if proc.stdout else ""
                print(output[-4000:])
                raise RuntimeError(f"uvicorn terminó con código {proc.returncode}")

if __name__ == "__main__":
    raise SystemExit(main())
