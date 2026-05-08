#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

frontend_lock = ROOT / "frontend/package-lock.json"
backend_lock = ROOT / "backend/requirements.lock.txt"
backend_dockerfile = ROOT / "backend/Dockerfile"
frontend_dockerfile = ROOT / "frontend/Dockerfile"
ci = ROOT / ".github/workflows/ci.yml"

if not frontend_lock.exists():
    errors.append("Falta frontend/package-lock.json")

if not backend_lock.exists():
    errors.append("Falta backend/requirements.lock.txt")
else:
    lines = [
        line.strip()
        for line in backend_lock.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        errors.append("backend/requirements.lock.txt está vacío")

    for line in lines:
        lower = line.lower()
        if any(bad in lower for bad in ["git+", "file://", "../", "-e "]):
            errors.append(f"Dependencia no reproducible o local en backend lock: {line}")
        if "==" not in line and not line.startswith(("--", "-")):
            errors.append(f"Dependencia backend no fijada con ==: {line}")

    required = ["fastapi==", "uvicorn==", "starlette==", "pydantic=="]
    lock_text = "\n".join(lines).lower()
    for req in required:
        if req not in lock_text:
            errors.append(f"Falta dependencia esperada en backend lock: {req}")

if backend_dockerfile.exists():
    txt = backend_dockerfile.read_text(encoding="utf-8")
    if "requirements.lock.txt" not in txt:
        errors.append("backend/Dockerfile no usa requirements.lock.txt")
else:
    errors.append("Falta backend/Dockerfile")

if frontend_dockerfile.exists():
    txt = frontend_dockerfile.read_text(encoding="utf-8")
    if "npm ci" not in txt:
        errors.append("frontend/Dockerfile no usa npm ci")
else:
    errors.append("Falta frontend/Dockerfile")

if ci.exists():
    txt = ci.read_text(encoding="utf-8")
    if "backend/requirements.lock.txt" not in txt:
        errors.append("CI no instala backend/requirements.lock.txt")
    if "npm --prefix frontend ci" not in txt:
        errors.append("CI no usa npm ci para frontend")
    if "npm --prefix frontend install" in txt:
        errors.append("CI todavía usa npm install")
else:
    errors.append("Falta .github/workflows/ci.yml")

if errors:
    print("ERROR dependency locks guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK dependency locks guard")
