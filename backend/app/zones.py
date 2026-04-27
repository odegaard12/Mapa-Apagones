import re
import sqlite3
import unicodedata


def _slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", (value or "").strip().lower())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
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


def _status_rank(status: str | None) -> int:
    order = {
        "activa": 5,
        "probable": 4,
        "senal_debil": 3,
        "degradandose": 2,
        "probablemente_resuelta": 1,
        "resuelta": 0,
    }
    return order.get(status or "", 0)


def _worst_status(rows) -> str:
    if not rows:
        return "resuelta"
    return max(rows, key=lambda r: _status_rank(r["status"]))["status"]


def sync_zone_for_incident(conn: sqlite3.Connection, incident_id: str) -> str | None:
    incident = conn.execute(
        """
        SELECT id, cell_key, municipio, province, display_zone, center_lat, center_lng,
               lat_min, lat_max, lng_min, lng_max, status, report_count_active,
               created_at, last_report_at, resolved_at
        FROM incidents
        WHERE id = ?
        """,
        (incident_id,),
    ).fetchone()

    if not incident:
        return None

    ensure_zone_tables(conn)

    zone_id = build_zone_id(incident["municipio"], incident["province"], incident["cell_key"])
    display_name = build_display_name(incident["municipio"], incident["province"], incident["display_zone"])

    conn.execute("UPDATE incidents SET zone_id = ? WHERE id = ?", (zone_id, incident_id))
    conn.execute("UPDATE reports SET zone_id = ? WHERE incident_id = ?", (zone_id, incident_id))

    rows = conn.execute(
        """
        SELECT id, municipio, province, display_zone, center_lat, center_lng,
               lat_min, lat_max, lng_min, lng_max, status, report_count_active,
               created_at, last_report_at, resolved_at
        FROM incidents
        WHERE zone_id = ?
        """,
        (zone_id,),
    ).fetchall()

    if not rows:
        return zone_id

    active_rows = [r for r in rows if int(r["report_count_active"] or 0) > 0]
    base_rows = active_rows if active_rows else rows
    pick = sorted(base_rows, key=lambda r: r["last_report_at"] or "", reverse=True)[0]

    confirmations_active = sum(int(r["report_count_active"] or 0) for r in active_rows)
    status = _worst_status(active_rows) if active_rows else "resuelta"

    created_at = min((r["created_at"] for r in rows if r["created_at"]), default=None)
    last_report_at = max((r["last_report_at"] for r in rows if r["last_report_at"]), default=None)
    resolved_at = None if active_rows else max((r["resolved_at"] for r in rows if r["resolved_at"]), default=None)

    bbox_min_lat = min(r["lat_min"] for r in base_rows)
    bbox_max_lat = max(r["lat_max"] for r in base_rows)
    bbox_min_lng = min(r["lng_min"] for r in base_rows)
    bbox_max_lng = max(r["lng_max"] for r in base_rows)

    conn.execute(
        """
        INSERT INTO zones (
            id, source, source_ref, name, municipio, province, display_name,
            center_lat, center_lng, bbox_min_lat, bbox_max_lat, bbox_min_lng, bbox_max_lng,
            status, confirmations_active, created_at, last_report_at, resolved_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            source = excluded.source,
            source_ref = excluded.source_ref,
            name = excluded.name,
            municipio = excluded.municipio,
            province = excluded.province,
            display_name = excluded.display_name,
            center_lat = excluded.center_lat,
            center_lng = excluded.center_lng,
            bbox_min_lat = excluded.bbox_min_lat,
            bbox_max_lat = excluded.bbox_max_lat,
            bbox_min_lng = excluded.bbox_min_lng,
            bbox_max_lng = excluded.bbox_max_lng,
            status = excluded.status,
            confirmations_active = excluded.confirmations_active,
            created_at = excluded.created_at,
            last_report_at = excluded.last_report_at,
            resolved_at = excluded.resolved_at
        """,
        (
            zone_id,
            "municipality" if incident["municipio"] else "cell",
            zone_id,
            incident["municipio"] or display_name,
            incident["municipio"],
            incident["province"],
            display_name,
            pick["center_lat"],
            pick["center_lng"],
            bbox_min_lat,
            bbox_max_lat,
            bbox_min_lng,
            bbox_max_lng,
            status,
            confirmations_active,
            created_at,
            last_report_at,
            resolved_at,
        ),
    )

    return zone_id


def refresh_all_zones(conn: sqlite3.Connection) -> int:
    ensure_zone_tables(conn)
    rows = conn.execute("SELECT id FROM incidents").fetchall()
    seen = set()
    for row in rows:
        zone_id = sync_zone_for_incident(conn, row["id"])
        if zone_id:
            seen.add(zone_id)
    return len(seen)


def get_zone_items(conn: sqlite3.Connection, hours: int = 24, include_resolved: bool = False):
    from datetime import datetime, timedelta, timezone

    hours = max(1, min(hours, 48))
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).replace(microsecond=0).isoformat()

    if include_resolved:
        rows = conn.execute(
            """
            SELECT *
            FROM zones
            WHERE last_report_at >= ?
            ORDER BY confirmations_active DESC, last_report_at DESC
            """,
            (cutoff,),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT *
            FROM zones
            WHERE last_report_at >= ?
              AND confirmations_active > 0
            ORDER BY confirmations_active DESC, last_report_at DESC
            """,
            (cutoff,),
        ).fetchall()

    return [dict(r) for r in rows]
