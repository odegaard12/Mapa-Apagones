#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_PATH="${DB_PATH:-$ROOT_DIR/data/app.db}"
BACKUP_DIR="${BACKUP_DIR:-$ROOT_DIR/backups/sqlite}"
KEEP_DAYS="${KEEP_DAYS:-14}"

if [ ! -f "$DB_PATH" ]; then
  echo "ERROR: no existe la base de datos: $DB_PATH" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
TMP_BACKUP="$BACKUP_DIR/app-$TS.sqlite3"
GZ_BACKUP="$TMP_BACKUP.gz"
SHA_FILE="$GZ_BACKUP.sha256"

python3 - "$DB_PATH" "$TMP_BACKUP" <<'PY'
import sqlite3
import sys
from pathlib import Path

src_path = Path(sys.argv[1])
dst_path = Path(sys.argv[2])

src = sqlite3.connect(str(src_path), timeout=30)
dst = sqlite3.connect(str(dst_path), timeout=30)

try:
    src.execute("PRAGMA busy_timeout = 5000")
    src.execute("PRAGMA wal_checkpoint(PASSIVE)")
    src.backup(dst)
    check = dst.execute("PRAGMA integrity_check").fetchone()[0]
    if check != "ok":
        raise SystemExit(f"integrity_check failed: {check}")
finally:
    dst.close()
    src.close()
PY

gzip -9 "$TMP_BACKUP"
sha256sum "$GZ_BACKUP" > "$SHA_FILE"

find "$BACKUP_DIR" -type f \( -name 'app-*.sqlite3.gz' -o -name 'app-*.sqlite3.gz.sha256' \) -mtime +"$KEEP_DAYS" -delete

echo "Backup creado:"
echo "  $GZ_BACKUP"
echo "  $SHA_FILE"
