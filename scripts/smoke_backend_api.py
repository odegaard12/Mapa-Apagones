#!/usr/bin/env python3
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
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
        with urlopen(req, timeout=5) as resp:
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
    for _ in range(40):
        try:
            status, body = request_json("GET", f"{base_url}/api/health")
            if status == 200 and body.get("ok") is True:
                return
            last_error = f"{status} {body}"
        except Exception as exc:
            last_error = exc
        time.sleep(0.25)
    raise RuntimeError(f"backend smoke health timeout: {last_error}")

def post_first_existing(base_url: str, candidate_paths: list[str], payload: dict) -> tuple[str | None, int, dict]:
    last_status = None
    last_body = None

    for path in candidate_paths:
        status, body = request_json("POST", f"{base_url}{path}", payload)
        if status != 404:
            return path, status, body
        last_status = status
        last_body = body

    return None, int(last_status or 404), dict(last_body or {"detail": "Not Found"})

def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"

    with tempfile.TemporaryDirectory(prefix="apagones-smoke-") as tmp:
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": str(BACKEND),
            "DB_PATH": str(Path(tmp) / "app.db"),
            "IGN_WFS_ENABLED": "0",
            "TURNSTILE_ENABLED": "0",
            "TURNSTILE_REQUIRED": "0",
            "ANON_HASH_KEY": "smoke-test-anon-hash-key-not-secret",
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

            payload = {
                "lat": 42.8782,
                "lng": -8.5448,
                "type": "sin_luz",
                "token": "smoke-token-0000000000001",
            }

            preflight_path, preflight_status, preflight_body = post_first_existing(
                base_url,
                [
                    "/api/report-preflight",
                    "/api/report/preflight",
                    "/api/report_preflight",
                    "/api/preflight/report",
                ],
                payload,
            )

            if preflight_path:
                if preflight_status != 200 or preflight_body.get("ok") is not True:
                    raise RuntimeError(f"preflight inesperado en {preflight_path}: {preflight_status} {preflight_body}")
                print(f"OK backend preflight smoke: {preflight_path}")
            else:
                print("WARN backend preflight smoke: no hay endpoint preflight público; se valida flujo /api/report directo")

            status, report = request_json("POST", f"{base_url}/api/report", payload)
            if status != 200:
                raise RuntimeError(f"report inesperado: {status} {report}")

            status, incidents = request_json("GET", f"{base_url}/api/incidents?hours=24&include_resolved=1")
            if status != 200:
                raise RuntimeError(f"incidents inesperado: {status} {incidents}")

            if not isinstance(incidents, list) and "items" not in incidents and "incidents" not in incidents:
                raise RuntimeError(f"incidents formato inesperado: {incidents}")

            print("OK backend API smoke")
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
