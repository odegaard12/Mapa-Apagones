#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
DIST = FRONTEND / "dist"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

errors = []

def require_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        errors.append(f"Falta fichero: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8", errors="replace")

index = require_file(DIST / "index.html")
if index:
    if "<div id=\"root\"" not in index and "<div id='root'" not in index:
        errors.append("dist/index.html no contiene root React")
    if "/assets/" not in index and "assets/" not in index:
        errors.append("dist/index.html no referencia assets")
    if VERSION not in index:
        # Vite puede no incrustar literal de versión en index, así que no fallamos aquí.
        pass

assets_dir = DIST / "assets"
if not assets_dir.exists():
    errors.append("Falta dist/assets")
else:
    js_assets = list(assets_dir.glob("*.js"))
    css_assets = list(assets_dir.glob("*.css"))
    if not js_assets:
        errors.append("No hay JS en dist/assets")
    if not css_assets:
        errors.append("No hay CSS en dist/assets")

    app_version_found = False
    for js in js_assets:
        txt = js.read_text(encoding="utf-8", errors="replace")
        if VERSION in txt:
            app_version_found = True
            break
    if not app_version_found:
        errors.append(f"No se encontró VERSION actual en JS construido: {VERSION}")

changelog = require_file(DIST / "changelog.html")
if changelog:
    if VERSION not in changelog:
        errors.append(f"dist/changelog.html no contiene VERSION actual: {VERSION}")
    if "Historial público" not in changelog:
        errors.append("dist/changelog.html no parece el changelog público esperado")

robots = require_file(DIST / "robots.txt")
if robots and "Sitemap:" not in robots:
    errors.append("dist/robots.txt no contiene Sitemap")

sitemap = require_file(DIST / "sitemap.xml")
if sitemap and "mapa-apagones.es" not in sitemap:
    errors.append("dist/sitemap.xml no contiene dominio público")

dist_hints = DIST / "data/distributor_hints.json"
src_hints = FRONTEND / "public/data/distributor_hints.json"

if not dist_hints.exists():
    errors.append("Falta dist/data/distributor_hints.json")
else:
    try:
        dist_data = json.loads(dist_hints.read_text(encoding="utf-8"))
        src_data = json.loads(src_hints.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"JSON distributor_hints inválido: {exc}")
    else:
        if dist_data != src_data:
            errors.append("dist/data/distributor_hints.json difiere de frontend/public/data/distributor_hints.json")
        items = dist_data.get("items", [])
        if len(items) < 1000:
            errors.append(f"distributor_hints dist tiene pocos items: {len(items)}")
        for item in items[:20]:
            if "zone_id" not in item or "dataset_id" not in item or "distributors" not in item:
                errors.append("distributor_hints contiene item sin zone_id/dataset_id/distributors")
                break

# Evitar que aparezcan rutas locales o artefactos típicos en el build público.
for path in DIST.rglob("*"):
    if not path.is_file():
        continue
    rel = str(path.relative_to(DIST))
    if path.suffix.lower() in {".map", ".bak", ".tmp", ".orig", ".rej"}:
        errors.append(f"Artefacto no deseado en dist: {rel}")

    if path.suffix.lower() in {".html", ".js", ".css", ".json", ".txt", ".xml"}:
        txt = path.read_text(encoding="utf-8", errors="replace")
        for forbidden in [
            "/home/odegaard12",
            "192.168.",

            "BEGIN RSA PRIVATE KEY",
            "BEGIN OPENSSH PRIVATE KEY",
        ]:
            if forbidden in txt:
                errors.append(f"Contenido sensible o local en dist/{rel}: {forbidden}")

        secret_patterns = [
            (r"TURNSTILE_SECRET_KEY\\s*=\\s*(?!$|\\.\\.\\.|<|[\\'\\\"]|\\n)(0x[A-Za-z0-9_-]{12,})", "TURNSTILE_SECRET_KEY con valor real"),
            (r"ANON_HASH_KEY\\s*=\\s*(?!$|\\.\\.\\.|<|[\\'\\\"]|\\n)([A-Fa-f0-9]{32,}|[A-Za-z0-9_./+=-]{32,})", "ANON_HASH_KEY con valor real"),
        ]
        for pattern, label in secret_patterns:
            if re.search(pattern, txt):
                errors.append(f"Posible secreto real en dist/{rel}: {label}")

if errors:
    print("ERROR frontend static smoke")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK frontend static smoke")
print(f"version={VERSION}")
print(f"assets_js={len(list(assets_dir.glob('*.js')))} assets_css={len(list(assets_dir.glob('*.css')))}")
print(f"distributor_hints_items={len(json.loads(dist_hints.read_text(encoding='utf-8')).get('items', []))}")
