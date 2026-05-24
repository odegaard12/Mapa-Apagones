#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

DOC_VERSION = "v0.10.7.7-static-public-pages-clean"
APP_VERSION = Path("VERSION").read_text(encoding="utf-8").strip()
TODAY = "2026-05-24"

DATA_DIR = Path("frontend/public/data")
HINTS_PATH = Path("frontend/src/data/distributor_hints.json")

OUT_CHANGELOG = Path("frontend/public/changelog.html")
OUT_COVERAGE = Path("frontend/public/cobertura-distribuidoras.html")
OUT_RELIABILITY = Path("frontend/public/fiabilidad-distribuidoras.html")
OUT_AUDIT = Path("docs/audit/static-public-pages-clean-v1077.md")

LABELS = {
    "galicia": "Galicia",
    "asturias": "Asturias",
    "cantabria": "Cantabria",
    "castilla_leon": "Castilla y León",
    "aragon": "Aragón",
    "madrid": "Comunidad de Madrid",
    "navarra": "Navarra",
    "la_rioja": "La Rioja",
    "murcia": "Región de Murcia",
    "ceuta": "Ceuta",
    "melilla": "Melilla",
    "comunitat_valenciana": "Comunitat Valenciana",
    "illes_balears": "Illes Balears",
    "canarias": "Canarias",
    "euskadi": "Euskadi",
    "extremadura": "Extremadura",
    "castilla_la_mancha": "Castilla-La Mancha",
    "andalucia": "Andalucía",
    "catalunya": "Catalunya",
}

PREFERRED_ORDER = [
    "castilla_leon",
    "catalunya",
    "castilla_la_mancha",
    "aragon",
    "andalucia",
    "madrid",
    "extremadura",
    "galicia",
    "comunitat_valenciana",
    "euskadi",
    "navarra",
    "la_rioja",
    "asturias",
    "cantabria",
    "canarias",
    "illes_balears",
    "murcia",
    "ceuta",
    "melilla",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def fmt_int(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def pct(covered: int, total: int) -> str:
    if total <= 0:
        return "0,0%"
    return f"{(covered / total) * 100:.1f}%".replace(".", ",")


def css() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f4f7fb;
  --card: #ffffff;
  --text: #172033;
  --muted: #667085;
  --border: #d9e2ef;
  --accent: #0f766e;
  --accent-soft: #e6fffb;
  --warn: #92400e;
  --warn-soft: #fff7ed;
  --bad: #991b1b;
  --bad-soft: #fef2f2;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
}
main {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  padding: 28px 0 56px;
}
a { color: var(--accent); }
.back {
  display: inline-block;
  margin-bottom: 18px;
  text-decoration: none;
  font-weight: 700;
}
.eyebrow {
  color: var(--muted);
  font-size: .95rem;
  margin: 0 0 6px;
}
h1 {
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.05;
  margin: 0 0 12px;
}
h2 { margin-top: 34px; }
.lead {
  max-width: 860px;
  color: var(--muted);
  font-size: 1.08rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin: 24px 0;
}
.card, .release, .notice {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 12px 26px rgba(16, 24, 40, .06);
}
.metric strong {
  display: block;
  font-size: 1.8rem;
}
.metric span { color: var(--muted); }
.notice {
  background: var(--accent-soft);
  border-color: #99f6e4;
}
.notice.warn {
  background: var(--warn-soft);
  border-color: #fed7aa;
}
.notice.bad {
  background: var(--bad-soft);
  border-color: #fecaca;
}
.table-wrap {
  overflow-x: auto;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: 0 12px 26px rgba(16, 24, 40, .06);
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 860px;
}
th, td {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  text-align: left;
  vertical-align: top;
}
th {
  background: #eef4fb;
  font-size: .9rem;
}
tr:last-child td { border-bottom: 0; }
.badge {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: .82rem;
  font-weight: 700;
  background: #eef2ff;
}
.badge.pending { background: var(--bad-soft); color: var(--bad); }
.badge.partial { background: var(--warn-soft); color: var(--warn); }
.badge.full { background: var(--accent-soft); color: var(--accent); }
code {
  background: #eef4fb;
  padding: 2px 5px;
  border-radius: 6px;
}
.release + .release { margin-top: 14px; }
.release h2 { margin-top: 0; }
.small { color: var(--muted); font-size: .92rem; }
footer { margin-top: 34px; color: var(--muted); }
"""


def load_geo_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in sorted(DATA_DIR.glob("*_municipios.geojson")):
        data = json.loads(path.read_text(encoding="utf-8"))
        features = data.get("features", [])
        if not features:
            continue

        props = features[0].get("properties", {})
        dataset_id = props.get("dataset_id") or path.name.replace("_municipios.geojson", "")
        counts[str(dataset_id)] = len(features)

    return counts


def load_hint_stats() -> tuple[dict[str, set[str]], dict[str, Counter]]:
    data = json.loads(HINTS_PATH.read_text(encoding="utf-8"))

    covered: dict[str, set[str]] = defaultdict(set)
    conf: dict[str, Counter] = defaultdict(Counter)

    for item in data.get("items", []):
        dataset_id = str(item.get("dataset_id") or "")
        zone_id = str(item.get("zone_id") or item.get("municipio") or item.get("name") or "")
        if not dataset_id or not zone_id:
            continue

        distributors = item.get("distributors") or []
        if distributors:
            covered[dataset_id].add(zone_id)

        for dist in distributors:
            confidence = str(dist.get("confidence") or "unknown")
            conf[dataset_id][confidence] += 1

    return covered, conf


def status_for(total: int, covered: int) -> tuple[str, str]:
    if covered == 0:
        return "Pendiente", "pending"
    if covered < total:
        return "Parcial", "partial"
    return "Con orientación/pista en todas las zonas", "full"


def build_matrix():
    geo = load_geo_counts()
    covered, conf = load_hint_stats()

    rows = []
    for dataset_id, total in geo.items():
        cov = len(covered.get(dataset_id, set()))
        pending = total - cov
        label, badge = status_for(total, cov)
        confidence = conf.get(dataset_id, Counter())
        confidence_text = ", ".join(
            f"{k}: {v}" for k, v in sorted(confidence.items())
        ) or "—"

        rows.append({
            "dataset_id": dataset_id,
            "label": LABELS.get(dataset_id, dataset_id),
            "total": total,
            "covered": cov,
            "pending": pending,
            "coverage": pct(cov, total),
            "status": label,
            "badge": badge,
            "confidence": confidence_text,
        })

    order_index = {ds: i for i, ds in enumerate(PREFERRED_ORDER)}
    rows.sort(key=lambda r: (order_index.get(r["dataset_id"], 999), r["label"]))
    return rows


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · Mapa Apagones</title>
  <style>{css()}</style>
</head>
<body>
<main>
  <a class="back" href="/">← Volver al mapa</a>
{body}
  <footer>
    Mapa Apagones · páginas estáticas desplegadas por Cloudflare Pages desde el repositorio público.
  </footer>
</main>
</body>
</html>
"""


def write_coverage(rows) -> None:
    total_geo = sum(r["total"] for r in rows)
    total_covered = sum(r["covered"] for r in rows)
    total_pending = sum(r["pending"] for r in rows)
    full = sum(1 for r in rows if r["badge"] == "full")
    partial = sum(1 for r in rows if r["badge"] == "partial")
    pending_ds = sum(1 for r in rows if r["badge"] == "pending")

    table = []
    for r in rows:
        table.append(
            "<tr>"
            f"<td>{esc(r['label'])}</td>"
            f"<td><code>{esc(r['dataset_id'])}</code></td>"
            f"<td>{fmt_int(r['total'])}</td>"
            f"<td>{fmt_int(r['covered'])}</td>"
            f"<td>{fmt_int(r['pending'])}</td>"
            f"<td>{esc(r['coverage'])}</td>"
            f"<td><span class=\"badge {esc(r['badge'])}\">{esc(r['status'])}</span></td>"
            f"<td>{esc(r['confidence'])}</td>"
            "</tr>"
        )

    body = f"""
  <p class="eyebrow">Datos: distributor_hints {esc(APP_VERSION)} · Página revisada: {TODAY} · {DOC_VERSION}</p>
  <h1>Cobertura pública de distribuidoras</h1>
  <p class="lead">
    Esta página resume las pistas públicas de distribuidora eléctrica cargadas en Mapa Apagones.
    Son datos orientativos: ayudan a identificar posibles distribuidoras por zona, pero no sustituyen
    la confirmación oficial de la comercializadora o distribuidora.
  </p>

  <section class="grid">
    <div class="card metric"><strong>{len(rows)}</strong><span>datasets geográficos</span></div>
    <div class="card metric"><strong>{fmt_int(total_geo)}</strong><span>zonas normalizadas</span></div>
    <div class="card metric"><strong>{fmt_int(total_covered)}</strong><span>zonas con orientación/pista</span></div>
    <div class="card metric"><strong>{fmt_int(total_pending)}</strong><span>zonas pendientes</span></div>
    <div class="card metric"><strong>{pct(total_covered, total_geo)}</strong><span>cobertura orientativa actual</span></div>
  </section>

  <section class="notice warn">
    <strong>Lectura correcta:</strong>
    100% con pista no significa 100% verificación municipal fuerte.
    <code>regional_default</code> es orientación regional, no verificación municipal.
    <code>verified_partial</code> es una pista pública parcial o municipal, no una garantía de exclusividad.
    Las entradas por confianza cuentan pistas de distribuidora; una zona puede tener más de una entrada.
  </section>

  <section class="grid">
    <div class="card metric"><strong>{full}</strong><span>datasets con orientación/pista en todas las zonas</span></div>
    <div class="card metric"><strong>{partial}</strong><span>datasets parciales</span></div>
    <div class="card metric"><strong>{pending_ds}</strong><span>datasets pendientes de distribuidora</span></div>
  </section>

  <h2>Matriz por comunidad</h2>
  <p class="small">
    Ordenada por prioridad de revisión y tamaño. Las comunidades con cero pistas no faltan del mapa:
    tienen geografía municipal, pero aún no tienen una pista pública de distribuidora suficientemente segura.
  </p>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Zona</th>
          <th>Dataset</th>
          <th>Zonas GeoJSON</th>
          <th>Zonas con orientación/pista</th>
          <th>Zonas pendientes</th>
          <th>Cobertura</th>
          <th>Estado</th>
          <th>Entradas por confianza</th>
        </tr>
      </thead>
      <tbody>
        {''.join(table)}
      </tbody>
    </table>
  </div>

  <h2>Privacidad</h2>
  <div class="notice">
    No pedimos CUPS, dirección exacta, cuentas, contratos, facturas ni datos de contador.
    No publicamos coordenadas privadas ni inventario de infraestructura crítica.
  </div>

  <p class="small">
    También puedes consultar el <a href="/fiabilidad-distribuidoras.html">criterio de fiabilidad</a>
    y el <a href="/changelog.html">changelog público</a>.
  </p>
"""
    OUT_COVERAGE.write_text(page("Cobertura pública de distribuidoras", body), encoding="utf-8")


def write_reliability(rows) -> None:
    table = []
    for r in rows:
        table.append(
            "<tr>"
            f"<td>{esc(r['label'])}</td>"
            f"<td>{fmt_int(r['total'])}</td>"
            f"<td>{fmt_int(r['covered'])}</td>"
            f"<td>{fmt_int(r['pending'])}</td>"
            f"<td><span class=\"badge {esc(r['badge'])}\">{esc(r['status'])}</span></td>"
            f"<td>{esc(r['confidence'])}</td>"
            "</tr>"
        )

    body = f"""
  <p class="eyebrow">Criterios vigentes revisados: {TODAY} · {DOC_VERSION}</p>
  <h1>Fiabilidad de pistas de distribuidoras</h1>
  <p class="lead">
    Mapa Apagones usa pistas públicas para orientar al usuario sobre posibles distribuidoras por municipio o zona.
    Estas pistas no sustituyen a la confirmación oficial.
  </p>

  <section class="notice warn">
    Esta página resume criterios vigentes a escala nacional. La auditoría histórica de Galicia, Asturias,
    Cantabria y La Rioja queda integrada como antecedente, pero la tabla actual cubre los 19 datasets geográficos.
  </section>

  <h2>Niveles de fiabilidad</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>Nivel</th><th>Cómo debe leerse</th><th>Qué no significa</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><code>verified_partial</code></td>
          <td>Pista pública fuerte para una presencia municipal, parcial o local.</td>
          <td>No afirma exclusividad ni cobertura total del municipio.</td>
        </tr>
        <tr>
          <td><code>regional_default</code></td>
          <td>Orientación regional cuando no hay prueba municipal fuerte.</td>
          <td>No es verificación municipal fuerte.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>Estado nacional por comunidad</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Zona</th>
          <th>Zonas</th>
          <th>Con orientación/pista</th>
          <th>Pendientes</th>
          <th>Estado</th>
          <th>Entradas por confianza</th>
        </tr>
      </thead>
      <tbody>
        {''.join(table)}
      </tbody>
    </table>
  </div>

  <h2>Qué falta para mejorar datos</h2>
  <div class="notice">
    Para subir más municipios a <code>verified_partial</code> hace falta una fuente pública más fuerte:
    listado municipal oficial, capa pública descargable saneable o documentación pública por municipio/zona.
    No se automatizan consultas protegidas por CAPTCHA y no se guardan coordenadas, direcciones, capturas ni respuestas raw.
  </div>
"""
    OUT_RELIABILITY.write_text(page("Fiabilidad de pistas de distribuidoras", body), encoding="utf-8")


def write_changelog() -> None:
    releases = [
        (
            "v0.10.7.7 — Static public pages clean refresh",
            "2026-05-24",
            [
                "Reordena el changelog público con una entrada actual arriba.",
                "Regenera las páginas estáticas de cobertura y fiabilidad con diseño limpio.",
                "Actualiza la lectura pública de comunidades completas, parciales y pendientes.",
                "Aclara que faltan pistas de distribuidora verificadas, no comunidades geográficas.",
                "No importa nuevas distribuidoras.",
            ],
        ),
        (
            "v0.10.7.6 — Public pages truthfulness and ordering refresh",
            "2026-05-24",
            [
                "Corrige el orden del changelog público.",
                "Aclara que 100% con pista no significa 100% verificación municipal fuerte.",
                "Aclara regional_default y verified_partial.",
                "Añade guard de verdad pública para páginas estáticas.",
            ],
        ),
        (
            "v0.10.7.5 — Public docs, changelog and national validation refresh",
            "2026-05-24",
            [
                "Actualiza documentación pública tras el trabajo de Andalucía.",
                "Andalucía batch 2: 532 candidatos en modo revisión manual.",
                "Añade guard de frescura documental.",
            ],
        ),
        (
            "v0.10.7.4 — Andalucía batch 2 candidate workbench",
            "2026-05-24",
            [
                "Crea un workbench de 532 candidatos Andalucía batch 2 en modo revisión manual.",
                "No importa datos automáticamente.",
                "Integra validador en post-merge.",
            ],
        ),
        (
            "v0.10.7.2 — Andalucía pending review queue",
            "2026-05-23",
            [
                "Genera cola saneada de 532 zonas pendientes de revisión en Andalucía.",
                "Valida 786 features GeoJSON y 254 hints ya cubiertos.",
            ],
        ),
        (
            "v0.10.6.4-distributor-confidence-labels",
            "2026-05-13",
            [
                "Mejora etiquetas públicas de fiabilidad de pistas de distribuidora.",
                "verified_partial se presenta como pista parcial verificada.",
                "regional_default se presenta como orientación regional.",
            ],
        ),
        (
            "v0.10.6.3-distributor-reliability-audit-ui",
            "2026-05-13",
            [
                "Añade auditoría pública saneada de fiabilidad para Galicia, Asturias, Cantabria y La Rioja.",
                "Añade página pública de fiabilidad de distribuidoras.",
            ],
        ),
        (
            "v0.10.6.2-andalucia-edistribucion-strong-lineowner-hints",
            "2026-05-13",
            [
                "Importa 254 pistas públicas parciales para Andalucía como verified_partial.",
                "Usa solo candidatos fuertes de E-Distribución Redes Digitales, S.L.U.",
            ],
        ),
        (
            "v0.10.6.1-extremadura-verified-partial-hints",
            "2026-05-12",
            [
                "Importa 388 zonas de Extremadura con pistas públicas verified_partial.",
                "Mantiene municipios multi-distribuidora con varias pistas.",
            ],
        ),
        (
            "v0.10.5.9-madrid-ufd-partial-hints",
            "2026-05-11",
            [
                "Importa 9 pistas públicas de UFD para Comunidad de Madrid.",
                "Mantiene el resto de Madrid pendiente.",
            ],
        ),
        (
            "v0.10.5.6-public-distributor-coverage-page",
            "2026-05-11",
            [
                "Añade página pública de cobertura de pistas de distribuidoras.",
                "Añade generador y guardia automática.",
            ],
        ),
        (
            "v0.10.1.0-geo-complete-spain-audit",
            "2026-05-04",
            [
                "Verifica cobertura geográfica completa de España.",
                "Comprueba 17 comunidades autónomas y Ceuta/Melilla.",
            ],
        ),
        (
            "v0.9.1-public-legal",
            "2026-04-28",
            [
                "Dominio público activo.",
                "Páginas legales, SEO básico y correos públicos.",
            ],
        ),
    ]

    cards = []
    for title, release_date, bullets in releases:
        cards.append(
            '<section class="release">'
            f"<h2>{esc(title)}</h2>"
            f"<p class=\"eyebrow\">{esc(release_date)}</p>"
            "<ul>"
            + "".join(f"<li>{esc(b)}</li>" for b in bullets)
            + "</ul>"
            "</section>"
        )

    body = f"""
  <p class="eyebrow">Actualizado: {TODAY} · {DOC_VERSION}</p>
  <h1>Changelog</h1>
  <p class="lead">
    Historial público curado de cambios importantes. El historial técnico completo está disponible en GitHub.
  </p>
  {''.join(cards)}
"""
    OUT_CHANGELOG.write_text(page("Changelog", body), encoding="utf-8")


def write_audit(rows) -> None:
    total_geo = sum(r["total"] for r in rows)
    total_covered = sum(r["covered"] for r in rows)
    total_pending = sum(r["pending"] for r in rows)

    OUT_AUDIT.write_text(
        "\n".join([
            "# Static public pages clean refresh v0.10.7.7",
            "",
            "## Summary",
            "",
            "Regenerates static public pages served by Cloudflare Pages from the repository.",
            "",
            "## Pages regenerated",
            "",
            "- frontend/public/changelog.html",
            "- frontend/public/cobertura-distribuidoras.html",
            "- frontend/public/fiabilidad-distribuidoras.html",
            "",
            "## Current public data summary",
            "",
            f"- Geographic datasets: {len(rows)}",
            f"- Normalized zones: {total_geo}",
            f"- Zones with distributor orientation/hint: {total_covered}",
            f"- Pending distributor-review zones: {total_pending}",
            "",
            "## Safety",
            "",
            "No distributor hints are imported.",
            "No CUPS, addresses, exact coordinates, customer data, private grid inventory, raw external API responses, secrets, backups or logs are added.",
            "",
        ]) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    rows = build_matrix()

    if len(rows) != 19:
        raise SystemExit(f"ERROR expected 19 geographic datasets, got {len(rows)}")
    if sum(r["total"] for r in rows) != 8215:
        raise SystemExit("ERROR expected 8215 normalized zones")

    write_coverage(rows)
    write_reliability(rows)
    write_changelog()
    write_audit(rows)

    print("OK regenerated clean static public pages")
    print(f"datasets={len(rows)}")
    print(f"zones={sum(r['total'] for r in rows)}")
    print(f"covered={sum(r['covered'] for r in rows)}")
    print(f"pending={sum(r['pending'] for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
