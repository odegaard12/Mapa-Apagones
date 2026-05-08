import os


def env_bool(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def env_csv(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


DB_PATH = os.getenv("DB_PATH", "/data/app.db")

DEFAULT_ALLOWED_ORIGINS = ",".join([
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8098",
    "http://127.0.0.1:8098",
    "https://mapa-apagones.es",
    "https://www.mapa-apagones.es",
])

ALLOWED_ORIGINS = env_csv("ALLOWED_ORIGINS", DEFAULT_ALLOWED_ORIGINS)
DEBUG_ENDPOINTS = env_bool("DEBUG_ENDPOINTS", "0")

TURNSTILE_ENABLED = os.getenv("TURNSTILE_ENABLED", "0") == "1"
TURNSTILE_REQUIRED = os.getenv("TURNSTILE_REQUIRED", "1") == "1"
TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY", "")
TURNSTILE_VERIFY_URL = os.getenv(
    "TURNSTILE_VERIFY_URL",
    "https://challenges.cloudflare.com/turnstile/v0/siteverify",
)
TURNSTILE_TIMEOUT = float(os.getenv("TURNSTILE_TIMEOUT", "5"))

ANON_HASH_KEY = os.getenv("ANON_HASH_KEY", "").strip()
ANON_HASH_LEGACY_COMPAT = env_bool("ANON_HASH_LEGACY_COMPAT", "1")
ANON_HASH_KEY_REQUIRED = env_bool(
    "ANON_HASH_KEY_REQUIRED",
    "1" if TURNSTILE_ENABLED and TURNSTILE_REQUIRED else "0",
)
ANON_HASH_DEV_FALLBACK = "dev-only-mapa-apagones-anon-hash-key"

TRUST_PROXY_HEADERS = env_bool("TRUST_PROXY_HEADERS", "1")
TRUSTED_PROXY_CIDRS = env_csv(
    "TRUSTED_PROXY_CIDRS",
    "127.0.0.1/32,::1/128,172.16.0.0/12,10.0.0.0/8,192.168.0.0/16",
)

GRID_SIZE_M = 1600
MATCH_INCIDENT_RADIUS_M = 1600
USER_NEARBY_LOCK_M = 2200
REPORT_TTL_HOURS = 3
RESTORE_TTL_MINUTES = REPORT_TTL_HOURS * 60
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
