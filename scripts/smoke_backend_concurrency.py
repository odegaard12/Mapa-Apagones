#!/usr/bin/env python3
import concurrent.futures
import json
import os
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])

def request_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=8) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body or "{}")
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body or "{}")
        except Exception:
            parsed = {"raw": body}
        return exc.code, parsed

def wait_health(base_url: str) -> None:
    last_error = None
    for _ in range(60):
        try:
            status, body = request_json("GET", f"{base_url}/api/health")
            if status == 200 and body.get("ok") is True:
                return
            last_error = f"{status} {body}"
        except Exception as exc:
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"backend health timeout: {last_error}")

def post_report(base_url: str, index: int) -> tuple[int, dict]:
    payload = {
        "lat": 42.8782,
        "lng": -8.5448,
        "type": "sin_luz",
        "token": f"concurrency-token-{index:04d}-0000000000000000",
    }
    return request_json("POST", f"{base_url}/api/report", payload)

def active_incident_rows(db_path: Path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
            SELECT id, cell_key, report_count_active, unique_reporters_active, status
            FROM incidents
            WHERE report_count_active > 0
            ORDER BY report_count_active DESC
        """).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"

    with tempfile.TemporaryDirectory(prefix="apagones-concurrency-") as tmp:
        db_path = Path(tmp) / "app.db"
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": str(BACKEND),
            "DB_PATH": str(db_path),
            "IGN_WFS_ENABLED": "0",
            "TURNSTILE_ENABLED": "0",
            "TURNSTILE_REQUIRED": "0",
            "ANON_HASH_KEY": "concurrency-test-anon-hash-key-not-secret",
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

            workers = 8
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                results = list(executor.map(lambda idx: post_report(base_url, idx), range(workers)))

            bad = [(status, body) for status, body in results if status not in (200, 429)]
            if bad:
                raise RuntimeError(f"respuestas inesperadas: {bad}")

            rows = active_incident_rows(db_path)

            if len(rows) != 1:
                raise RuntimeError(f"se esperaba 1 incidencia activa agrupada, hay {len(rows)}: {rows}")

            row = rows[0]
            active_reports = int(row.get("report_count_active") or 0)
            unique_reporters = int(row.get("unique_reporters_active") or 0)

            if active_reports < 1 or unique_reporters < 1:
                raise RuntimeError(f"incidencia inválida: {row}")

            print("OK backend report concurrency smoke")
            print(f"active_incidents=1 active_reports={active_reports} unique_reporters={unique_reporters}")
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
