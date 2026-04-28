import hashlib
import json
import math
import os
import sqlite3
import uuid
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import unicodedata

from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.zones import ensure_zone_tables, sync_zone_for_incident, refresh_all_zones, get_zone_items

DB_PATH = os.getenv("DB_PATH", "/data/app.db")

def env_bool(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}

def env_csv(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]

DEFAULT_ALLOWED_ORIGINS = ",".join([
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8098",
    "http://127.0.0.1:8098",
    "http://192.168.68.103:8098",
    "https://mapaapagones.es",
    "https://www.mapaapagones.es",
])

ALLOWED_ORIGINS = env_csv("ALLOWED_ORIGINS", DEFAULT_ALLOWED_ORIGINS)
DEBUG_ENDPOINTS = env_bool("DEBUG_ENDPOINTS", "0")

TURNSTILE_ENABLED = os.getenv("TURNSTILE_ENABLED", "0") == "1"
TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY", "")
TURNSTILE_VERIFY_URL = os.getenv("TURNSTILE_VERIFY_URL", "https://challenges.cloudflare.com/turnstile/v0/siteverify")
TURNSTILE_TIMEOUT = float(os.getenv("TURNSTILE_TIMEOUT", "5"))

GRID_SIZE_M = 1600
MATCH_INCIDENT_RADIUS_M = 1600
USER_NEARBY_LOCK_M = 2200
REPORT_TTL_HOURS = 3
RESTORE_TTL_MINUTES = 20
SAME_TYPE_COOLDOWN_SEC = 10 * 60
TYPE_CHANGE_COOLDOWN_SEC = 20
NEW_ZONE_COOLDOWN_SEC = 180
NEW_INCIDENT_COOLDOWN_SEC = 180
ABUSE_LIMIT_PER_HOUR = 16
INCIDENT_LOOKBACK_HOURS = 8
MAX_API_HOURS = 48
DEFAULT_API_LIMIT = 250
MAX_API_LIMIT = 500

IGN_WFS_URL = os.getenv("IGN_WFS_URL", "https://www.ign.es/wfs-inspire/unidades-administrativas")
IGN_WFS_TIMEOUT = float(os.getenv("IGN_WFS_TIMEOUT", "12"))
IGN_WFS_USER_AGENT = os.getenv("IGN_WFS_USER_AGENT", "ApagonesCiudadanos/0.5")
IGN_WFS_ENABLED = os.getenv("IGN_WFS_ENABLED", "1") == "1"

ALLOWED_TYPES = {"sin_luz", "microcortes", "baja_tension", "vuelve"}
EARTH_R = 6378137.0

app = FastAPI(title="Apagones Ciudadanos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=False,
)

class ReportIn(BaseModel):
    lat: float = Field(ge=27.0, le=45.0)
    lng: float = Field(ge=-19.0, le=5.0)
    type: str
    token: str = Field(min_length=16, max_length=128)
    turnstile_token: Optional[str] = Field(default=None, max_length=4096)

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()

def parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value)

def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def configure_sqlite_connection(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA foreign_keys = ON")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    configure_sqlite_connection(conn)
    return conn

def client_ip(request: FastAPIRequest) -> str:
    forwarded = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    if forwarded:
        return forwarded
    if request.client and request.client.host:
        return request.client.host
    return "unknown"

def verify_turnstile_or_403(turnstile_token: Optional[str], request: FastAPIRequest) -> None:
    if not TURNSTILE_ENABLED:
        return

    if not TURNSTILE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Turnstile no está configurado.")

    if not turnstile_token or not turnstile_token.strip():
        raise HTTPException(status_code=403, detail="Verificación anti-abuso requerida.")

    form = urlencode(
        {
            "secret": TURNSTILE_SECRET_KEY,
            "response": turnstile_token.strip(),
            "remoteip": client_ip(request),
        }
    ).encode("utf-8")

    req = Request(
        TURNSTILE_VERIFY_URL,
        data=form,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "ApagonesCiudadanos/turnstile",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=TURNSTILE_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=403, detail="No se pudo validar la verificación anti-abuso.")

    if not result.get("success"):
        raise HTTPException(status_code=403, detail="Verificación anti-abuso fallida.")

def haversine_m(lat1, lng1, lat2, lng2):
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(a))

def latlng_to_mercator(lat: float, lng: float) -> Tuple[float, float]:
    x = EARTH_R * math.radians(lng)
    lat = max(min(lat, 85.05112878), -85.05112878)
    y = EARTH_R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y

def mercator_to_latlng(x: float, y: float) -> Tuple[float, float]:
    lng = math.degrees(x / EARTH_R)
    lat = math.degrees(2 * math.atan(math.exp(y / EARTH_R)) - math.pi / 2)
    return lat, lng

def grid_for_point(lat: float, lng: float, size_m: int = GRID_SIZE_M):
    x, y = latlng_to_mercator(lat, lng)
    ix = math.floor(x / size_m)
    iy = math.floor(y / size_m)

    min_x = ix * size_m
    max_x = (ix + 1) * size_m
    min_y = iy * size_m
    max_y = (iy + 1) * size_m

    lat_a, lng_a = mercator_to_latlng(min_x, min_y)
    lat_b, lng_b = mercator_to_latlng(max_x, max_y)
    center_lat, center_lng = mercator_to_latlng((min_x + max_x) / 2, (min_y + max_y) / 2)

    return {
        "cell_key": f"{ix}:{iy}:{size_m}",
        "lat_min": min(lat_a, lat_b),
        "lat_max": max(lat_a, lat_b),
        "lng_min": min(lng_a, lng_b),
        "lng_max": max(lng_a, lng_b),
        "center_lat": center_lat,
        "center_lng": center_lng,
    }

def table_columns(conn, table_name: str):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}

def ensure_column(conn, table_name: str, col_name: str, col_def: str):
    cols = table_columns(conn, table_name)
    if col_name not in cols:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def}")

def setup_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id TEXT PRIMARY KEY,
            cell_key TEXT NOT NULL,
            status TEXT NOT NULL,
            primary_type TEXT NOT NULL,
            center_lat REAL NOT NULL,
            center_lng REAL NOT NULL,
            lat_min REAL NOT NULL,
            lat_max REAL NOT NULL,
            lng_min REAL NOT NULL,
            lng_max REAL NOT NULL,
            report_count_active INTEGER NOT NULL DEFAULT 0,
            unique_reporters_active INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            last_report_at TEXT NOT NULL,
            resolved_at TEXT
        );

        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            incident_id TEXT NOT NULL,
            reporter_token_hash TEXT NOT NULL,
            ip_hash TEXT NOT NULL,
            report_type TEXT NOT NULL,
            status TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS action_log (
            id TEXT PRIMARY KEY,
            reporter_token_hash TEXT NOT NULL,
            ip_hash TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS geocode_cache (
            cell_key TEXT PRIMARY KEY,
            municipio TEXT,
            province TEXT,
            country TEXT,
            display_zone TEXT,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_incidents_last_report_at ON incidents(last_report_at);
        CREATE INDEX IF NOT EXISTS idx_incidents_cell_key ON incidents(cell_key);
        CREATE INDEX IF NOT EXISTS idx_reports_incident ON reports(incident_id);
        CREATE INDEX IF NOT EXISTS idx_reports_token ON reports(reporter_token_hash);
        CREATE INDEX IF NOT EXISTS idx_action_log_created ON action_log(created_at);
        """
    )

    ensure_column(conn, "incidents", "municipio", "TEXT")
    ensure_column(conn, "incidents", "province", "TEXT")
    ensure_column(conn, "incidents", "country", "TEXT")
    ensure_column(conn, "incidents", "display_zone", "TEXT")
    ensure_column(conn, "incidents", "zone_id", "TEXT")
    ensure_column(conn, "reports", "zone_id", "TEXT")
    ensure_zone_tables(conn)

    conn.commit()
    conn.close()

@app.on_event("startup")
def on_startup():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    setup_db()

def cleanup_old(conn):
    now = utcnow()
    conn.execute(
        "DELETE FROM action_log WHERE created_at < ?",
        (iso(now - timedelta(days=2)),),
    )
    conn.execute(
        "UPDATE reports SET status='inactive' WHERE status='active' AND expires_at < ?",
        (iso(now),),
    )
    conn.commit()

def record_action(conn, token_hash: str, ip_hash: str, action: str):
    conn.execute(
        "INSERT INTO action_log (id, reporter_token_hash, ip_hash, action, created_at) VALUES (?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), token_hash, ip_hash, action, iso(utcnow())),
    )

def assert_not_rate_limited(conn, token_hash: str, ip_hash: str):
    cutoff = iso(utcnow() - timedelta(hours=1))
    row = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM action_log
        WHERE created_at >= ?
          AND (reporter_token_hash = ? OR ip_hash = ?)
        """,
        (cutoff, token_hash, ip_hash),
    ).fetchone()
    if row["c"] >= ABUSE_LIMIT_PER_HOUR:
        raise HTTPException(status_code=429, detail="Límite temporal alcanzado. Espera un poco y vuelve a intentarlo.")

def clamp_int(value: int, default: int, min_value: int, max_value: int) -> int:
    try:
        parsed = int(value)
    except Exception:
        parsed = default
    return max(min_value, min(parsed, max_value))

def parse_bbox_query(value: Optional[str]) -> Optional[Tuple[float, float, float, float]]:
    if not value:
        return None

    try:
        parts = [float(item.strip()) for item in value.split(",")]
    except Exception:
        raise HTTPException(status_code=400, detail="bbox inválido. Usa minLng,minLat,maxLng,maxLat.")

    if len(parts) != 4:
        raise HTTPException(status_code=400, detail="bbox inválido. Usa minLng,minLat,maxLng,maxLat.")

    min_lng, min_lat, max_lng, max_lat = parts

    if not (-180 <= min_lng <= 180 and -180 <= max_lng <= 180 and -90 <= min_lat <= 90 and -90 <= max_lat <= 90):
        raise HTTPException(status_code=400, detail="bbox fuera de rango.")

    if min_lng >= max_lng or min_lat >= max_lat:
        raise HTTPException(status_code=400, detail="bbox inválido: min debe ser menor que max.")

    return min_lng, min_lat, max_lng, max_lat

def bbox_overlaps(
    item_lat_min: Optional[float],
    item_lat_max: Optional[float],
    item_lng_min: Optional[float],
    item_lng_max: Optional[float],
    bbox: Optional[Tuple[float, float, float, float]],
) -> bool:
    if not bbox:
        return True

    if None in (item_lat_min, item_lat_max, item_lng_min, item_lng_max):
        return True

    min_lng, min_lat, max_lng, max_lat = bbox

    return not (
        float(item_lng_max) < min_lng
        or float(item_lng_min) > max_lng
        or float(item_lat_max) < min_lat
        or float(item_lat_min) > max_lat
    )

def build_display_zone(municipio: Optional[str], province: Optional[str]) -> str:
    if municipio and province:
        return f"{municipio} · {province}"
    if municipio:
        return municipio
    if province:
        return province
    return "Zona comunitaria agrupada"

def normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return value.lower().strip()

def localname(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag

def first_text_descendant(elem) -> Optional[str]:
    for child in elem.iter():
        if localname(child.tag) == "text" and child.text and child.text.strip():
            return child.text.strip()
    return None

def nested_text_of_localname(elem, wanted: str) -> Optional[str]:
    for child in elem.iter():
        if localname(child.tag) == wanted:
            parts = [t.strip() for t in child.itertext() if t and t.strip()]
            if parts:
                return " ".join(parts)
    return None

def fetch_admin_features_bbox(lat: float, lng: float, delta: float):
    params = {
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "REQUEST": "GetFeature",
        "TYPENAMES": "au:AdministrativeUnit",
        "COUNT": "50",
        "srsName": "EPSG:4326",
        "bbox": f"{lng - delta},{lat - delta},{lng + delta},{lat + delta},EPSG:4326",
    }

    req = Request(
        f"{IGN_WFS_URL}?{urlencode(params)}",
        headers={
            "User-Agent": IGN_WFS_USER_AGENT,
            "Accept": "application/xml,text/xml;q=0.9,*/*;q=0.8",
        },
    )

    with urlopen(req, timeout=IGN_WFS_TIMEOUT) as resp:
        raw = resp.read()

    root = ET.fromstring(raw)
    features = []

    for elem in root.iter():
        if localname(elem.tag) != "AdministrativeUnit":
            continue

        name = first_text_descendant(elem)
        level = nested_text_of_localname(elem, "nationalLevelName") or nested_text_of_localname(elem, "nationalLevel")
        country = nested_text_of_localname(elem, "country")

        if name:
            features.append(
                {
                    "name": name,
                    "level": level or "",
                    "country": country or "",
                }
            )

    return features

def resolve_zone_via_ign(lat: float, lng: float):
    if not IGN_WFS_ENABLED:
        return {
            "municipio": None,
            "province": None,
            "country": None,
            "display_zone": "Zona comunitaria agrupada",
        }

    municipio = None
    province = None
    country = None

    for delta in (0.0005, 0.002, 0.01):
        try:
            features = fetch_admin_features_bbox(lat, lng, delta)
        except Exception:
            features = []

        if not features:
            continue

        for feat in features:
            level = normalize_text(feat.get("level"))
            name = feat.get("name")

            if not municipio and "municipio" in level:
                municipio = name
            elif not province and "provincia" in level:
                province = name
            elif not country and ("pais" in level or "country" in level or "estado" in level):
                country = name or feat.get("country")

        if municipio or province:
            break

    return {
        "municipio": municipio,
        "province": province,
        "country": country,
        "display_zone": build_display_zone(municipio, province),
    }

def get_cached_geocode(conn, cell_key: str):
    row = conn.execute(
        "SELECT municipio, province, country, display_zone FROM geocode_cache WHERE cell_key = ?",
        (cell_key,),
    ).fetchone()
    if row:
        return dict(row)
    return None

def cache_geocode(conn, cell_key: str, data: dict):
    conn.execute(
        """
        INSERT OR REPLACE INTO geocode_cache (cell_key, municipio, province, country, display_zone, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            cell_key,
            data.get("municipio"),
            data.get("province"),
            data.get("country"),
            data.get("display_zone"),
            iso(utcnow()),
        ),
    )

def resolve_geodata_for_cell(conn, cell_key: str, lat: float, lng: float):
    cached = get_cached_geocode(conn, cell_key)
    if cached:
        return cached

    data = resolve_zone_via_ign(lat, lng)
    cache_geocode(conn, cell_key, data)
    return data

def fill_incident_geodata_if_missing(conn, incident_id: str):
    incident = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    if not incident:
        return

    if incident["display_zone"]:
        return

    data = resolve_geodata_for_cell(conn, incident["cell_key"], incident["center_lat"], incident["center_lng"])
    conn.execute(
        """
        UPDATE incidents
        SET municipio = ?, province = ?, country = ?, display_zone = ?
        WHERE id = ?
        """,
        (
            data.get("municipio"),
            data.get("province"),
            data.get("country"),
            data.get("display_zone"),
            incident_id,
        ),
    )

def compute_incident_status(active_negative_unique: int, last_negative_at: Optional[datetime], has_restore_signal: bool) -> str:
    if active_negative_unique <= 0:
        return "resuelta"

    now = utcnow()
    if not last_negative_at:
        return "resuelta"

    age_min = (now - last_negative_at).total_seconds() / 60

    if age_min <= 45:
        if active_negative_unique >= 4:
            return "activa"
        if active_negative_unique >= 2:
            return "probable"
        return "senal_debil"

    if age_min <= 90:
        return "degradandose"

    if has_restore_signal:
        return "probablemente_resuelta"

    if age_min <= 180:
        return "probablemente_resuelta"

    return "resuelta"

def recompute_incident(conn, incident_id: str):
    now = utcnow()

    conn.execute(
        "UPDATE reports SET status='inactive' WHERE incident_id = ? AND status='active' AND expires_at < ?",
        (incident_id, iso(now)),
    )

    rows = conn.execute(
        "SELECT * FROM reports WHERE incident_id = ? ORDER BY updated_at DESC",
        (incident_id,),
    ).fetchall()

    active_rows = [r for r in rows if r["status"] == "active" and parse_dt(r["expires_at"]) and parse_dt(r["expires_at"]) >= now]
    negative_rows = [r for r in active_rows if r["report_type"] != "vuelve"]
    restore_rows = [r for r in active_rows if r["report_type"] == "vuelve"]

    active_negative_unique = len({r["reporter_token_hash"] for r in negative_rows})
    active_restore_unique = len({r["reporter_token_hash"] for r in restore_rows})
    last_negative_at = max((parse_dt(r["updated_at"]) for r in negative_rows), default=None)
    last_any_at = max((parse_dt(r["updated_at"]) for r in rows), default=None)

    status = compute_incident_status(
        active_negative_unique=active_negative_unique,
        last_negative_at=last_negative_at,
        has_restore_signal=active_restore_unique > 0,
    )

    counter = Counter([r["report_type"] for r in negative_rows])
    primary_type = counter.most_common(1)[0][0] if counter else "sin_luz"

    incident = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    last_report_at = last_any_at or parse_dt(incident["last_report_at"]) or now
    resolved_at = iso(now) if status == "resuelta" else None

    conn.execute(
        """
        UPDATE incidents
        SET status = ?,
            primary_type = ?,
            report_count_active = ?,
            unique_reporters_active = ?,
            last_report_at = ?,
            resolved_at = ?
        WHERE id = ?
        """,
        (
            status,
            primary_type,
            len(negative_rows),
            active_negative_unique,
            iso(last_report_at),
            resolved_at,
            incident_id,
        ),
    )

    fill_incident_geodata_if_missing(conn, incident_id)
    sync_zone_for_incident(conn, incident_id)

def refresh_all_incidents(conn):
    cleanup_old(conn)
    rows = conn.execute("SELECT id FROM incidents").fetchall()
    for row in rows:
        recompute_incident(conn, row["id"])
    refresh_all_zones(conn)
    conn.commit()

def find_recent_incident_in_same_cell(conn, cell_key: str) -> Optional[sqlite3.Row]:
    cutoff = iso(utcnow() - timedelta(hours=INCIDENT_LOOKBACK_HOURS))
    return conn.execute(
        """
        SELECT *
        FROM incidents
        WHERE cell_key = ?
          AND last_report_at >= ?
          AND report_count_active > 0
        ORDER BY last_report_at DESC
        LIMIT 1
        """,
        (cell_key, cutoff),
    ).fetchone()

def find_nearest_recent_incident(conn, lat: float, lng: float) -> Optional[sqlite3.Row]:
    cutoff = iso(utcnow() - timedelta(hours=INCIDENT_LOOKBACK_HOURS))
    rows = conn.execute(
        """
        SELECT *
        FROM incidents
        WHERE last_report_at >= ?
          AND report_count_active > 0
        ORDER BY last_report_at DESC
        """,
        (cutoff,),
    ).fetchall()

    best = None
    best_d = None
    for row in rows:
        d = haversine_m(lat, lng, row["center_lat"], row["center_lng"])
        if d <= MATCH_INCIDENT_RADIUS_M and (best_d is None or d < best_d):
            best = row
            best_d = d
    return best

def find_user_nearby_active_report(conn, token_hash: str, lat: float, lng: float) -> Optional[sqlite3.Row]:
    rows = conn.execute(
        """
        SELECT r.*, i.center_lat, i.center_lng
        FROM reports r
        JOIN incidents i ON i.id = r.incident_id
        WHERE r.reporter_token_hash = ?
          AND r.status = 'active'
          AND r.report_type != 'vuelve'
          AND i.report_count_active > 0
        ORDER BY r.updated_at DESC
        """,
        (token_hash,),
    ).fetchall()

    best = None
    best_d = None
    for row in rows:
        d = haversine_m(lat, lng, row["center_lat"], row["center_lng"])
        if d <= USER_NEARBY_LOCK_M and (best_d is None or d < best_d):
            best = row
            best_d = d
    return best

def create_incident(conn, lat: float, lng: float, base_type: str) -> str:
    grid = grid_for_point(lat, lng)
    geodata = resolve_geodata_for_cell(conn, grid["cell_key"], grid["center_lat"], grid["center_lng"])
    incident_id = str(uuid.uuid4())
    now = utcnow()

    conn.execute(
        """
        INSERT INTO incidents (
            id, cell_key, status, primary_type, center_lat, center_lng,
            lat_min, lat_max, lng_min, lng_max,
            report_count_active, unique_reporters_active,
            created_at, last_report_at, resolved_at,
            municipio, province, country, display_zone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            incident_id,
            grid["cell_key"],
            "senal_debil",
            base_type,
            grid["center_lat"],
            grid["center_lng"],
            grid["lat_min"],
            grid["lat_max"],
            grid["lng_min"],
            grid["lng_max"],
            0,
            0,
            iso(now),
            iso(now),
            None,
            geodata.get("municipio"),
            geodata.get("province"),
            geodata.get("country"),
            geodata.get("display_zone"),
        ),
    )
    return incident_id

def get_or_create_incident_id(conn, lat: float, lng: float, report_type: str) -> str:
    if report_type == "vuelve":
        nearby = find_nearest_recent_incident(conn, lat, lng)
        if not nearby:
            raise HTTPException(status_code=400, detail="No hay una incidencia activa cercana para marcar como resuelta.")
        return nearby["id"]

    grid = grid_for_point(lat, lng)
    same_cell = find_recent_incident_in_same_cell(conn, grid["cell_key"])
    if same_cell:
        return same_cell["id"]

    nearby = find_nearest_recent_incident(conn, lat, lng)
    if nearby:
        return nearby["id"]

    return create_incident(conn, lat, lng, report_type)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/debug/incidents")
def debug_incidents():
    if not DEBUG_ENDPOINTS:
        raise HTTPException(status_code=404, detail="Not found")

    conn = get_db()
    refresh_all_incidents(conn)
    rows = conn.execute(
        """
        SELECT id, display_zone, municipio, province, country, report_count_active, status, last_report_at
        FROM incidents
        ORDER BY last_report_at DESC
        LIMIT 20
        """
    ).fetchall()
    out = [dict(r) for r in rows]

    visible_ids = [r["id"] for r in rows if int(r["report_count_active"] or 0) > 0]
    unique_reporters_visible = 0
    active_reports_visible = 0

    if visible_ids:
        placeholders = ",".join("?" for _ in visible_ids)
        stats_row = conn.execute(
            f"""
            SELECT
                COUNT(*) AS active_reports_visible,
                COUNT(DISTINCT reporter_token_hash) AS unique_reporters_visible
            FROM reports
            WHERE status = 'active'
              AND incident_id IN ({placeholders})
            """,
            visible_ids,
        ).fetchone()

        active_reports_visible = int(stats_row["active_reports_visible"] or 0)
        unique_reporters_visible = int(stats_row["unique_reporters_visible"] or 0)

    summary = {
        "active_incidents_visible": len(visible_ids),
        "active_reports_visible": active_reports_visible,
        "unique_reporters_visible": unique_reporters_visible,
    }

    conn.close()
    return {"items": out, "summary": summary}

@app.get("/api/incidents")
def incidents(hours: int = 24, include_resolved: int = 0, bbox: Optional[str] = None, limit: int = DEFAULT_API_LIMIT):
    hours = clamp_int(hours, 24, 1, MAX_API_HOURS)
    limit = clamp_int(limit, DEFAULT_API_LIMIT, 1, MAX_API_LIMIT)
    bbox_filter = parse_bbox_query(bbox)

    conn = get_db()
    refresh_all_incidents(conn)
    cutoff = iso(utcnow() - timedelta(hours=hours))

    where = ["last_report_at >= ?"]
    params: list[object] = [cutoff]

    if include_resolved:
        where.append("(report_count_active > 0 OR status = 'resuelta')")
    else:
        where.append("report_count_active > 0")

    if bbox_filter:
        min_lng, min_lat, max_lng, max_lat = bbox_filter
        where.append("lng_max >= ? AND lng_min <= ? AND lat_max >= ? AND lat_min <= ?")
        params.extend([min_lng, max_lng, min_lat, max_lat])

    params.append(limit)

    rows = conn.execute(
        f"""
        SELECT *
        FROM incidents
        WHERE {' AND '.join(where)}
        ORDER BY report_count_active DESC, last_report_at DESC
        LIMIT ?
        """,
        params,
    ).fetchall()

    out = [dict(r) for r in rows]
    conn.close()
    return {"items": out, "limit": limit, "hours": hours}

@app.get("/api/zones")
def zones(hours: int = 24, include_resolved: int = 0, bbox: Optional[str] = None, limit: int = DEFAULT_API_LIMIT):
    hours = clamp_int(hours, 24, 1, MAX_API_HOURS)
    limit = clamp_int(limit, DEFAULT_API_LIMIT, 1, MAX_API_LIMIT)
    bbox_filter = parse_bbox_query(bbox)

    conn = get_db()
    refresh_all_incidents(conn)

    raw_items = get_zone_items(conn, hours=hours, include_resolved=bool(include_resolved))
    items = []

    for z in raw_items:
        if not bbox_overlaps(
            z["bbox_min_lat"],
            z["bbox_max_lat"],
            z["bbox_min_lng"],
            z["bbox_max_lng"],
            bbox_filter,
        ):
            continue

        latest_incident = conn.execute(
            """
            SELECT primary_type, status, last_report_at
            FROM incidents
            WHERE zone_id = ?
            ORDER BY report_count_active DESC, last_report_at DESC
            LIMIT 1
            """,
            (z["id"],),
        ).fetchone()

        primary_type = latest_incident["primary_type"] if latest_incident else "sin_luz"

        items.append({
            "id": z["id"],
            "display_zone": z["display_name"],
            "municipio": z["municipio"],
            "province": z["province"],
            "center_lat": z["center_lat"],
            "center_lng": z["center_lng"],
            "lat_min": z["bbox_min_lat"],
            "lat_max": z["bbox_max_lat"],
            "lng_min": z["bbox_min_lng"],
            "lng_max": z["bbox_max_lng"],
            "status": z["status"],
            "primary_type": primary_type,
            "report_count_active": z["confirmations_active"],
            "unique_reporters_active": z["confirmations_active"],
            "last_report_at": z["last_report_at"],
            "resolved_at": z["resolved_at"],
            "zone_id": z["id"],
        })

        if len(items) >= limit:
            break

    summary = {
        "active_zones": sum(1 for i in items if int(i.get("report_count_active", 0)) > 0),
        "confirmations": sum(int(i.get("report_count_active", 0)) for i in items),
    }

    conn.close()
    return {"items": items, "summary": summary, "limit": limit, "hours": hours}


@app.post("/api/report")
def report(payload: ReportIn, request: FastAPIRequest):
    if payload.type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Tipo de reporte inválido")

    verify_turnstile_or_403(payload.turnstile_token, request)

    conn = get_db()
    cleanup_old(conn)

    token_hash = sha256(payload.token.strip())
    ip_hash = sha256(client_ip(request))
    assert_not_rate_limited(conn, token_hash, ip_hash)

    now = utcnow()
    previous_incident_to_recompute = None
    moved_zone = False

    nearby_user_report = find_user_nearby_active_report(conn, token_hash, payload.lat, payload.lng)

    current_active_negative = conn.execute(
        """
        SELECT *
        FROM reports
        WHERE reporter_token_hash = ?
          AND status = 'active'
          AND report_type != 'vuelve'
        ORDER BY updated_at DESC
        LIMIT 1
        """,
        (token_hash,),
    ).fetchone()

    if payload.type == "vuelve":
        incident_id = get_or_create_incident_id(conn, payload.lat, payload.lng, payload.type)
    elif nearby_user_report:
        incident_id = nearby_user_report["incident_id"]
    else:
        if current_active_negative:
            last_dt = parse_dt(current_active_negative["updated_at"]) or now
            elapsed = (now - last_dt).total_seconds()

            if elapsed < NEW_ZONE_COOLDOWN_SEC:
                conn.close()
                wait_sec = int(NEW_ZONE_COOLDOWN_SEC - elapsed)
                raise HTTPException(
                    status_code=429,
                    detail=f"Ya tienes una incidencia activa. Márcala como resuelta o espera {wait_sec}s antes de abrir otra zona."
                )

            previous_incident_to_recompute = current_active_negative["incident_id"]
            conn.execute(
                "UPDATE reports SET status = 'inactive', expires_at = ? WHERE id = ?",
                (iso(now), current_active_negative["id"]),
            )
            moved_zone = True

        incident_id = get_or_create_incident_id(conn, payload.lat, payload.lng, payload.type)

    incident_before = conn.execute(
        "SELECT report_count_active FROM incidents WHERE id = ?",
        (incident_id,),
    ).fetchone()

    incident_for_storage = conn.execute(
        "SELECT center_lat, center_lng FROM incidents WHERE id = ?",
        (incident_id,),
    ).fetchone()
    stored_lat = incident_for_storage["center_lat"] if incident_for_storage else payload.lat
    stored_lng = incident_for_storage["center_lng"] if incident_for_storage else payload.lng

    existing = conn.execute(
        """
        SELECT *
        FROM reports
        WHERE incident_id = ?
          AND reporter_token_hash = ?
          AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 1
        """,
        (incident_id, token_hash),
    ).fetchone()

    action = "created_new_zone"

    if existing:
        last_update = parse_dt(existing["updated_at"]) or now
        cooldown = SAME_TYPE_COOLDOWN_SEC if existing["report_type"] == payload.type else TYPE_CHANGE_COOLDOWN_SEC
        elapsed = (now - last_update).total_seconds()

        if elapsed < cooldown:
            conn.close()
            wait_sec = int(cooldown - elapsed)
            raise HTTPException(status_code=429, detail=f"Espera {wait_sec}s antes de volver a actualizar esta zona.")

        expires_at = now + (timedelta(minutes=RESTORE_TTL_MINUTES) if payload.type == "vuelve" else timedelta(hours=REPORT_TTL_HOURS))
        conn.execute(
            """
            UPDATE reports
            SET report_type = ?, lat = ?, lng = ?, updated_at = ?, expires_at = ?, status = 'active'
            WHERE id = ?
            """,
            (
                payload.type,
                stored_lat,
                stored_lng,
                iso(now),
                iso(expires_at),
                existing["id"],
            ),
        )
        action = "updated_own_report"
    else:
        expires_at = now + (timedelta(minutes=RESTORE_TTL_MINUTES) if payload.type == "vuelve" else timedelta(hours=REPORT_TTL_HOURS))
        conn.execute(
            """
            INSERT INTO reports (
                id, incident_id, reporter_token_hash, ip_hash, report_type, status,
                lat, lng, created_at, updated_at, expires_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                incident_id,
                token_hash,
                ip_hash,
                payload.type,
                "active",
                stored_lat,
                stored_lng,
                iso(now),
                iso(now),
                iso(expires_at),
            ),
        )

        if moved_zone:
            action = "moved_to_new_zone"
        elif incident_before and int(incident_before["report_count_active"] or 0) > 0:
            action = "confirmed_existing_zone"
        else:
            action = "created_new_zone"

    record_action(conn, token_hash, ip_hash, action)

    if previous_incident_to_recompute and previous_incident_to_recompute != incident_id:
        recompute_incident(conn, previous_incident_to_recompute)

    recompute_incident(conn, incident_id)
    conn.commit()

    incident = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    conn.close()

    return {
        "ok": True,
        "action": action,
        "incident_id": incident_id,
        "incident": dict(incident),
    }
