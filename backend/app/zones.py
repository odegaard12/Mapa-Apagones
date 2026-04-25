import re
import sqlite3


def _slug(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def build_zone_id(municipio: str | None, province: str | None, fallback_cell_key: str | None = None) -> str:
    if municipio and province:
        return f"municipality:{_slug(province)}::{_slug(municipio)}"
    if municipio:
        return f"municipality:{_slug(municipio)}"
    if fallback_cell_key:
        return f"cell:{fallback_cell_key}"
    return "unknown"


def build_display_name(municipio: str | None, province: str | None, display_zone: str | None) -> str:
    if display_zone:
        return display_zone
    if municipio and province:
        return f"{municipio} · {province}"
    if municipio:
        return municipio
    if province:
        return province
    return "Zona comunitaria agrupada"


def ensure_zone_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS zones (
            id TEXT PRIMARY KEY,
            source TEXT,
            source_ref TEXT,
            name TEXT,
            municipio TEXT,
            province TEXT,
            display_name TEXT,
            center_lat REAL,
            center_lng REAL,
            bbox_min_lat REAL,
            bbox_max_lat REAL,
            bbox_min_lng REAL,
            bbox_max_lng REAL,
            status TEXT NOT NULL DEFAULT 'resuelta',
            confirmations_active INTEGER NOT NULL DEFAULT 0,
            created_at TEXT,
            last_report_at TEXT,
            resolved_at TEXT
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_zones_last_report_at ON zones(last_report_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_zones_status ON zones(status)")
