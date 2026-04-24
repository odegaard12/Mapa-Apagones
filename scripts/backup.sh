#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB_PATH="$BASE_DIR/data/app.db"
BACKUP_DIR="$BASE_DIR/backups"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$BACKUP_DIR/apagones-$STAMP.sqlite3"

mkdir -p "$BACKUP_DIR"

if [ ! -f "$DB_PATH" ]; then
  echo "No existe la base de datos en: $DB_PATH"
  exit 1
fi

python3 - <<PY
import sqlite3
src = sqlite3.connect(r"$DB_PATH")
dst = sqlite3.connect(r"$OUT")
with dst:
    src.backup(dst)
src.close()
dst.close()
print("Backup creado:", r"$OUT")
PY
