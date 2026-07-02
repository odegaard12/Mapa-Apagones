import hashlib
import hmac
from typing import Tuple

from fastapi import HTTPException

from app.settings import (
    ANON_HASH_ALLOW_DEV_FALLBACK,
    ANON_HASH_DEV_FALLBACK,
    ANON_HASH_KEY,
    ANON_HASH_KEY_REQUIRED,
    ANON_HASH_LEGACY_COMPAT,
)


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def anonymization_secret() -> str:
    if ANON_HASH_KEY:
        return ANON_HASH_KEY

    if ANON_HASH_ALLOW_DEV_FALLBACK and not ANON_HASH_KEY_REQUIRED:
        return ANON_HASH_DEV_FALLBACK

    raise HTTPException(status_code=500, detail="Anonimización no configurada.")


def anon_hash(value: str) -> str:
    secret = anonymization_secret()
    message = f"mapa-apagones-anon-v1:{value}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


def normalize_hash_values(values) -> Tuple[str, ...]:
    if isinstance(values, str):
        return (values,)
    return tuple(str(value) for value in values if value)


def anon_hash_candidates(value: str) -> Tuple[str, ...]:
    normalized = str(value or "").strip()
    current = anon_hash(normalized)

    if not ANON_HASH_LEGACY_COMPAT:
        return (current,)

    legacy = sha256(normalized)
    if legacy == current:
        return (current,)

    return (current, legacy)


def sql_in_clause(column: str, values: Tuple[str, ...]) -> Tuple[str, list[str]]:
    values = normalize_hash_values(values)
    if not values:
        raise HTTPException(status_code=500, detail="Hash anónimo inválido.")

    placeholders = ", ".join(["?"] * len(values))
    return f"{column} IN ({placeholders})", list(values)
