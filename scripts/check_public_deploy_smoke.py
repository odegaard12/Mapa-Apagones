#!/usr/bin/env python3
"""
Smoke test público para Mapa Apagones.

Valida, sin imprimir respuestas raw:
- Web pública carga por HTTPS
- API health responde
- distributor_hints.json público existe, es JSON válido y mantiene estructura mínima

Importante:
- La policy pública puede mencionar términos como CUPS para explicar que NO se publican.
- Por eso el chequeo sensible se aplica sobre items/datos operativos, no sobre el texto bruto completo.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_SITE_URL = "https://mapa-apagones.es/"
DEFAULT_API_HEALTH_URL = "https://api.mapa-apagones.es/api/health"
DEFAULT_DISTRIBUTOR_JSON_URL = "https://mapa-apagones.es/data/distributor_hints.json"

FORBIDDEN_ITEM_KEYS = {
    "cups",
    "cup",
    "token",
    "secret",
    "password",
    "private_key",
    "api_key",
    "authorization",
}

# Patrón conservador para evitar códigos CUPS españoles obvios en datos operativos.
CUPS_LIKE_RE = re.compile(r"\bES[0-9A-Z]{18,24}\b", re.IGNORECASE)


@dataclass
class FetchResult:
    url: str
    status: int
    content_type: str
    body: bytes


def fetch(url: str, timeout: float) -> FetchResult:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mapa-Apagones-public-smoke/1.1",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.1",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return FetchResult(
                url=url,
                status=int(resp.status),
                content_type=resp.headers.get("Content-Type", ""),
                body=resp.read(8_000_000),
            )
    except urllib.error.HTTPError as exc:
        return FetchResult(
            url=url,
            status=int(exc.code),
            content_type=exc.headers.get("Content-Type", ""),
            body=exc.read(4096),
        )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def smoke_site(url: str, timeout: float) -> None:
    result = fetch(url, timeout)

    require(200 <= result.status < 400, f"web pública status inesperado: {result.status}")
    require(len(result.body) > 100, "web pública respondió cuerpo demasiado pequeño")

    text_head = result.body[:20_000].decode("utf-8", errors="ignore").lower()
    require("<html" in text_head or "<!doctype html" in text_head, "web pública no parece HTML")

    print(
        f"OK web pública: status={result.status} "
        f"content_type={result.content_type!r} bytes={len(result.body)}"
    )


def smoke_api_health(url: str, timeout: float) -> None:
    result = fetch(url, timeout)

    require(200 <= result.status < 500, f"API health status inesperado: {result.status}")
    require(len(result.body) > 0, "API health respondió vacío")

    parsed_keys: list[str] = []

    if "json" in result.content_type.lower():
        try:
            data = json.loads(result.body.decode("utf-8"))
            if isinstance(data, dict):
                parsed_keys = sorted(str(k) for k in data.keys())[:20]
        except Exception as exc:
            raise AssertionError(f"API health declara JSON pero no parsea: {exc}") from exc

    require(result.status < 400, f"API health no OK: status={result.status}")

    suffix = f" keys={parsed_keys}" if parsed_keys else ""
    print(
        f"OK API health: status={result.status} "
        f"content_type={result.content_type!r} bytes={len(result.body)}{suffix}"
    )


def scan_items_for_sensitive_markers(items: list[Any]) -> None:
    """
    Escanea solo items/datos operativos.

    No escanea policy porque policy puede mencionar CUPS/tokens/etc. precisamente
    como prohibiciones documentales.
    """
    problems: list[str] = []

    def walk(value: Any, path: str) -> None:
        if len(problems) >= 20:
            return

        if isinstance(value, dict):
            for key, nested in value.items():
                key_s = str(key)
                key_l = key_s.lower()

                if key_l in FORBIDDEN_ITEM_KEYS:
                    problems.append(f"clave prohibida en {path}.{key_s}")

                walk(nested, f"{path}.{key_s}")

        elif isinstance(value, list):
            for idx, nested in enumerate(value):
                walk(nested, f"{path}[{idx}]")

        elif isinstance(value, str):
            if CUPS_LIKE_RE.search(value):
                problems.append(f"valor con patrón CUPS-like en {path}")

    walk(items, "items")

    if problems:
        sample = "; ".join(problems[:5])
        raise AssertionError(f"marcadores sensibles en datos operativos: {sample}")


def smoke_distributor_json(
    url: str,
    timeout: float,
    expected_version: str | None,
    min_items: int,
) -> None:
    result = fetch(url, timeout)

    require(result.status == 200, f"distributor_hints.json status inesperado: {result.status}")
    require(len(result.body) > 1000, "distributor_hints.json demasiado pequeño")

    text = result.body.decode("utf-8", errors="strict")

    try:
        data: Any = json.loads(text)
    except Exception as exc:
        raise AssertionError(f"distributor_hints.json no es JSON válido: {exc}") from exc

    require(isinstance(data, dict), "distributor_hints.json raíz no es objeto")
    require(isinstance(data.get("version"), str), "campo version ausente o no string")
    require(isinstance(data.get("policy"), dict), "campo policy ausente o no objeto")
    require(isinstance(data.get("items"), list), "campo items ausente o no lista")
    require(len(data["items"]) >= min_items, f"items insuficientes: {len(data['items'])} < {min_items}")

    if expected_version:
        require(
            data["version"] == expected_version,
            f"version pública inesperada: {data['version']!r} != {expected_version!r}",
        )

    scan_items_for_sensitive_markers(data["items"])

    print(
        f"OK distributor_hints público: status={result.status} "
        f"version={data['version']} items={len(data['items'])} bytes={len(result.body)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-url", default=os.getenv("PUBLIC_SITE_URL", DEFAULT_SITE_URL))
    parser.add_argument("--api-health-url", default=os.getenv("PUBLIC_API_HEALTH_URL", DEFAULT_API_HEALTH_URL))
    parser.add_argument(
        "--distributor-json-url",
        default=os.getenv("PUBLIC_DISTRIBUTOR_JSON_URL", DEFAULT_DISTRIBUTOR_JSON_URL),
    )
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument(
        "--expected-distributor-version",
        default=os.getenv("EXPECTED_DISTRIBUTOR_VERSION"),
    )
    parser.add_argument(
        "--min-distributor-items",
        type=int,
        default=int(os.getenv("MIN_DISTRIBUTOR_ITEMS", "2500")),
    )
    args = parser.parse_args()

    print("=== check_public_deploy_smoke ===")
    print(f"site_url={args.site_url}")
    print(f"api_health_url={args.api_health_url}")
    print(f"distributor_json_url={args.distributor_json_url}")
    print(f"min_distributor_items={args.min_distributor_items}")
    if args.expected_distributor_version:
        print(f"expected_distributor_version={args.expected_distributor_version}")

    try:
        smoke_site(args.site_url, args.timeout)
        smoke_api_health(args.api_health_url, args.timeout)
        smoke_distributor_json(
            args.distributor_json_url,
            args.timeout,
            args.expected_distributor_version,
            args.min_distributor_items,
        )
    except Exception as exc:
        print()
        print(f"FAIL: public deploy smoke failed: {exc}")
        return 1

    print()
    print("OK: public deploy smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
