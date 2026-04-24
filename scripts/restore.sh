#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DB="$BASE_DIR/data/app.db"

if [ $# -ne 1 ]; then
  echo "Uso: $0 /ruta/al/backup.sqlite3"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "No existe el backup: $BACKUP_FILE"
  exit 1
fi

cd "$BASE_DIR"
docker compose stop backend >/dev/null 2>&1 || true
cp "$BACKUP_FILE" "$TARGET_DB"
docker compose start backend >/dev/null 2>&1 || true

echo "Restore completado desde: $BACKUP_FILE"
