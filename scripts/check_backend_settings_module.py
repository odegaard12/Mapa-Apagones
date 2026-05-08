#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
settings = (ROOT / "backend/app/settings.py").read_text(encoding="utf-8")

errors = []

required_settings = [
    "DB_PATH",
    "ALLOWED_ORIGINS",
    "TURNSTILE_ENABLED",
    "ANON_HASH_KEY",
    "TRUST_PROXY_HEADERS",
    "TRUSTED_PROXY_CIDRS",
    "GRID_SIZE_M",
    "IGN_WFS_ENABLED",
    "ALLOWED_TYPES",
]

for item in required_settings:
    if item not in settings:
        errors.append(f"settings.py no contiene {item}")

required_main = [
    "from app.settings import (",
    "DB_PATH",
    "TURNSTILE_ENABLED",
    "ANON_HASH_KEY",
    "TRUST_PROXY_HEADERS",
]

for item in required_main:
    if item not in main:
        errors.append(f"main.py no importa/usa {item}")

for forbidden in [
    'DB_PATH = os.getenv("DB_PATH"',
    'DEFAULT_ALLOWED_ORIGINS = ",".join',
    'TURNSTILE_ENABLED = os.getenv',
    'ANON_HASH_KEY = os.getenv',
    'TRUST_PROXY_HEADERS = env_bool',
]:
    if forbidden in main:
        errors.append(f"configuración duplicada en main.py: {forbidden}")

if errors:
    print("ERROR backend settings module guard")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("OK backend settings module guard")
