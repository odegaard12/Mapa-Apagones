#!/usr/bin/env python3
import json
import os
import re
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

HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

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
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw or "{}")
    except HTTPError as exc:
        raw = exc.read().decode("utf-8")
        try:
            body = json.loads(raw or "{}")
        except Exception:
            body = {"raw": raw}
        return exc.code, body

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
    raise RuntimeError(f"backend privacy/abuse health timeout: {last_error}")

def post_report(base_url: str, token: str, idx: int) -> tuple[int, dict]:
    payload = {
        "lat": 42.8782 + (idx * 0.00001),
        "lng": -8.5448,
        "type": "sin_luz",
        "token": token,
    }
    return request_json("POST", f"{base_url}/api/report", payload)

def rows(db_path: Path, query: str) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(query).fetchall()]
    finally:
        conn.close()

def assert_hash_shape(value: str, label: str) -> None:
    if not isinstance(value, str) or not HEX64_RE.match(value):
        raise RuntimeError(f"{label} no parece hash hex64: {value!r}")

def assert_no_raw_values(db_path: Path, raw_values: list[str]) -> None:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        table_names = [
            row["name"]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        ]
        for table in table_names:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            text_cols = [
                col["name"]
                for col in cols
                if "TEXT" in str(col["type"]).upper()
            ]
            if not text_cols:
                continue

            selected = ", ".join(text_cols)
            for row in conn.execute(f"SELECT {selected} FROM {table}").fetchall():
                for col in text_cols:
                    value = row[col]
                    if value is None:
                        continue
                    value = str(value)
                    for raw in raw_values:
                        if raw and raw in value:
                            raise RuntimeError(f"valor raw encontrado en {table}.{col}: {raw!r}")
    finally:
        conn.close()

def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    abuse_limit = 16
    raw_ip = "127.0.0.1"
    tokens = [f"privacy-abuse-token-{idx:04d}-0000000000000000" for idx in range(abuse_limit + 1)]

    with tempfile.TemporaryDirectory(prefix="apagones-privacy-abuse-") as tmp:
        db_path = Path(tmp) / "app.db"
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": str(BACKEND),
            "DB_PATH": str(db_path),
            "IGN_WFS_ENABLED": "0",
            "TURNSTILE_ENABLED": "0",
            "TURNSTILE_REQUIRED": "0",
            "ANON_HASH_KEY": "privacy-abuse-test-anon-hash-key-not-secret",
            "ANON_HASH_KEY_REQUIRED": "1",
            "ANON_HASH_LEGACY_COMPAT": "0",
            "TRUST_PROXY_HEADERS": "1",
            "TRUSTED_PROXY_CIDRS": "127.0.0.1/32,::1/128",
            "DEBUG_ENDPOINTS": "0",
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

            for idx in range(abuse_limit):
                status, body = post_report(base_url, tokens[idx], idx)
                if status != 200:
                    raise RuntimeError(f"reporte {idx} debería pasar antes del límite: {status} {body}")

            status, body = post_report(base_url, tokens[abuse_limit], abuse_limit)
            if status != 429:
                raise RuntimeError(f"el reporte {abuse_limit + 1} debería rate-limitar por IP: {status} {body}")

            report_rows = rows(db_path, "SELECT reporter_token_hash, ip_hash FROM reports")
            action_rows = rows(db_path, "SELECT reporter_token_hash, ip_hash FROM action_log")

            if len(report_rows) < abuse_limit:
                raise RuntimeError(f"se esperaban reportes guardados antes del rate limit: {len(report_rows)}")

            if len(action_rows) != abuse_limit:
                raise RuntimeError(f"se esperaban {abuse_limit} action_log antes del rate limit: {len(action_rows)}")

            for idx, row in enumerate(report_rows):
                assert_hash_shape(row["reporter_token_hash"], f"reports[{idx}].reporter_token_hash")
                assert_hash_shape(row["ip_hash"], f"reports[{idx}].ip_hash")

            for idx, row in enumerate(action_rows):
                assert_hash_shape(row["reporter_token_hash"], f"action_log[{idx}].reporter_token_hash")
                assert_hash_shape(row["ip_hash"], f"action_log[{idx}].ip_hash")

            assert_no_raw_values(db_path, tokens + [raw_ip])

            print("OK backend privacy/abuse smoke")
            print(f"reports={len(report_rows)} action_log={len(action_rows)} rate_limit_status={status}")
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
