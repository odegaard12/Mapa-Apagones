#!/usr/bin/env python3
import json
import os
import socket
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

    with tempfile.TemporaryDirectory(prefix="apagones-status-") as tmp:
        db_path = Path(tmp) / "app.db"
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": str(BACKEND),
            "DB_PATH": str(db_path),
            "IGN_WFS_ENABLED": "0",
            "TURNSTILE_ENABLED": "0",
            "TURNSTILE_REQUIRED": "0",
            "ANON_HASH_KEY": "status-test-anon-hash-key-not-secret",
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
            status, body = request_json(f"{base_url}/api/status")

            if status != 200:
                raise RuntimeError(f"/api/status devolvió HTTP {status}: {body}")

            if body.get("service") != "mapa-apagones-api":
                raise RuntimeError(f"service inesperado: {body}")

            if body.get("ok") is not True:
                raise RuntimeError(f"status ok no es true: {body}")

            db = body.get("database") or {}
            if db.get("engine") != "sqlite" or db.get("ok") is not True:
                raise RuntimeError(f"database status inválido: {body}")

            tables = db.get("required_tables") or {}
            for table in ["incidents", "reports", "action_log", "geocode_cache"]:
                if tables.get(table) is not True:
                    raise RuntimeError(f"tabla requerida ausente en status: {table} -> {body}")

            privacy = body.get("privacy") or {}
            if privacy.get("anonymous_hashing") != "hmac-sha256":
                raise RuntimeError(f"anonymous_hashing inválido: {body}")
            if privacy.get("anonymous_hashing_configured") is not True:
                raise RuntimeError(f"anonymous_hashing_configured debería ser true en smoke: {body}")
            if privacy.get("stores_raw_ip") is not False or privacy.get("stores_raw_token") is not False:
                raise RuntimeError(f"status declara almacenamiento raw inesperado: {body}")

            network = body.get("network") or {}
            if network.get("trust_proxy_headers") is not True:
                raise RuntimeError(f"trust_proxy_headers debería ser true en smoke: {body}")
            if network.get("trusted_proxy_cidrs_configured") is not True:
                raise RuntimeError(f"trusted_proxy_cidrs_configured debería ser true en smoke: {body}")

            serialized = json.dumps(body, sort_keys=True)
            forbidden_values = [
                "status-test-anon-hash-key-not-secret",
                str(db_path),
                "TURNSTILE_SECRET_KEY",
                "ANON_HASH_KEY=",
                "127.0.0.1/32",
                "::1/128",
            ]
            for value in forbidden_values:
                if value in serialized:
                    raise RuntimeError(f"/api/status expone valor interno: {value}")

            print("OK backend status smoke")
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
