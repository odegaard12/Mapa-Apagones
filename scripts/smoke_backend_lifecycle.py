#!/usr/bin/env python3
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
    raise RuntimeError(f"backend lifecycle health timeout: {last_error}")

def db_rows(db_path: Path, query: str, params: tuple = ()) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def post_report(base_url: str, token: str, report_type: str, incident_id: str | None = None) -> tuple[int, dict]:
    payload = {
        "lat": 42.8782,
        "lng": -8.5448,
        "type": report_type,
        "token": token,
    }
    if incident_id:
        payload["incident_id"] = incident_id
    return request_json("POST", f"{base_url}/api/report", payload)

def active_incidents(db_path: Path) -> list[dict]:
    return db_rows(
        db_path,
        """
        SELECT id, cell_key, report_count_active, unique_reporters_active, status, primary_type
        FROM incidents
        WHERE report_count_active > 0
        ORDER BY report_count_active DESC, last_report_at DESC
        """,
    )

def incident_by_id(db_path: Path, incident_id: str) -> dict:
    rows = db_rows(
        db_path,
        """
        SELECT id, cell_key, report_count_active, unique_reporters_active, status, primary_type, resolved_at
        FROM incidents
        WHERE id = ?
        """,
        (incident_id,),
    )
    if not rows:
        raise RuntimeError(f"incidencia no encontrada: {incident_id}")
    return rows[0]

def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"

    with tempfile.TemporaryDirectory(prefix="apagones-lifecycle-") as tmp:
        db_path = Path(tmp) / "app.db"
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": str(BACKEND),
            "DB_PATH": str(db_path),
            "IGN_WFS_ENABLED": "0",
            "TURNSTILE_ENABLED": "0",
            "TURNSTILE_REQUIRED": "0",
            "ANON_HASH_KEY": "lifecycle-test-anon-hash-key-not-secret",
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

            # Errores básicos: tipo inválido y coordenada fuera de rango.
            status, body = post_report(base_url, "lifecycle-invalid-type-token-000000000000", "tipo_invalido")
            if status not in (400, 422):
                raise RuntimeError(f"tipo inválido debería fallar: {status} {body}")

            status, body = request_json("POST", f"{base_url}/api/report", {
                "lat": 99,
                "lng": -8.5448,
                "type": "sin_luz",
                "token": "lifecycle-invalid-lat-token-000000000000",
            })
            if status != 422:
                raise RuntimeError(f"lat inválida debería dar 422: {status} {body}")

            # Dos señales negativas cercanas deben quedar agrupadas en una incidencia.
            for idx, report_type in enumerate(("sin_luz", "microcortes"), start=1):
                status, body = post_report(
                    base_url,
                    f"lifecycle-negative-token-{idx:04d}-0000000000000000",
                    report_type,
                )
                if status != 200:
                    raise RuntimeError(f"reporte negativo falló: {status} {body}")

            rows = active_incidents(db_path)
            if len(rows) != 1:
                raise RuntimeError(f"se esperaba 1 incidencia activa agrupada, hay {len(rows)}: {rows}")

            incident = rows[0]
            incident_id = incident["id"]
            if int(incident["report_count_active"] or 0) < 2:
                raise RuntimeError(f"se esperaban al menos 2 reportes activos: {incident}")
            if int(incident["unique_reporters_active"] or 0) < 2:
                raise RuntimeError(f"se esperaban al menos 2 reporters únicos: {incident}")

            # /api/incidents debe responder después de reportar.
            status, body = request_json("GET", f"{base_url}/api/incidents")
            if status != 200:
                raise RuntimeError(f"/api/incidents falló: {status} {body}")

            # Bbox válido no debe romper el endpoint.
            status, body = request_json("GET", f"{base_url}/api/incidents?bbox=-9,42,-8,43")
            if status != 200:
                raise RuntimeError(f"/api/incidents bbox falló: {status} {body}")

            # Dos señales de "Ya volvió" deben neutralizar las dos señales negativas.
            for idx in range(1, 3):
                status, body = post_report(
                    base_url,
                    f"lifecycle-restore-token-{idx:04d}-0000000000000000",
                    "vuelve",
                    incident_id=incident_id,
                )
                if status != 200:
                    raise RuntimeError(f"reporte vuelve falló: {status} {body}")

            resolved = incident_by_id(db_path, incident_id)
            if resolved["status"] not in ("resuelta", "probablemente_resuelta"):
                raise RuntimeError(f"la incidencia debería quedar resuelta/probablemente resuelta: {resolved}")

            if int(resolved["report_count_active"] or 0) != 0:
                raise RuntimeError(f"la incidencia resuelta no debería mantener report_count_active > 0: {resolved}")

            print("OK backend report lifecycle smoke")
            print(f"incident_id={incident_id} final_status={resolved['status']}")
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
