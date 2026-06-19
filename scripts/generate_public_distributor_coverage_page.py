#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "research" / "distributor_coverage_matrix.md"
VERSION_FILE = ROOT / "VERSION"
CHANGELOG_HTML = ROOT / "frontend" / "public" / "changelog.html"
OUTPUT = ROOT / "frontend" / "public" / "cobertura-distribuidoras.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract(pattern: str, text: str, default: str = "—") -> str:
    m = re.search(pattern, text, flags=re.I | re.M)
    return m.group(1).strip() if m else default


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_matrix(text: str) -> tuple[dict[str, str], list[dict[str, str]]]:
    summary = {
        "datasets": extract(r"Datasets geográficos autonómicos:\s+\*\*([^*]+)\*\*", text),
        "geo_total": extract(r"Municipios/zonas normalizadas en GeoJSON:\s+\*\*([^*]+)\*\*", text),
        "with_hint": extract(r"Municipios/zonas con pista pública de distribuidora:\s+\*\*([^*]+)\*\*", text),
        "pending": extract(r"Municipios/zonas pendientes de pista pública:\s+\*\*([^*]+)\*\*", text),
        "coverage": extract(r"Cobertura actual de pistas públicas:\s+\*\*([^*]+)\*\*", text),
    }

    rows: list[dict[str, str]] = []
    in_table = False

    for line in text.splitlines():
        if line.startswith("| Zona | Dataset | GeoJSON |"):
            in_table = True
            continue

        if not in_table:
            continue

        if not line.startswith("|"):
            break

        if line.startswith("|---"):
            continue

        cells = split_md_row(line)
        if len(cells) < 10:
            continue

        rows.append(
            {
                "zone": cells[0],
                "dataset": cells[1].strip("`"),
                "geojson": cells[2],
                "with_hint": cells[3],
                "pending": cells[4],
                "coverage": cells[5],
                "status": cells[6],
                "confidence": cells[7],
                "with_date": cells[8],
                "with_source": cells[9],
            }
        )

    if not rows:
        raise SystemExit("ERROR: no se encontraron filas de matriz de cobertura")

    return summary, rows


def status_class(row: dict[str, str]) -> str:
    if row["pending"] == "0":
        return "complete"
    if row["with_hint"] != "0":
        return "partial"
    return "pending"


def changelog_date() -> str:
    if not CHANGELOG_HTML.exists():
        return "2026-05-11"
    text = read(CHANGELOG_HTML)
    return extract(r"Actualizado:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text, "2026-05-11")


def build_html() -> str:
    matrix_text = read(MATRIX)
    version = read(VERSION_FILE).strip()
    updated = changelog_date()
    summary, rows = parse_matrix(matrix_text)

    row_html = []
    for row in rows:
        cls = status_class(row)
        row_html.append(
            f"""
            <tr class="{cls}">
              <td>{html.escape(row["zone"])}</td>
              <td><code>{html.escape(row["dataset"])}</code></td>
              <td>{html.escape(row["geojson"])}</td>
              <td>{html.escape(row["with_hint"])}</td>
              <td>{html.escape(row["pending"])}</td>
              <td>{html.escape(row["coverage"])}</td>
              <td>{html.escape(row["status"])}</td>
              <td>{html.escape(row["confidence"])}</td>
              <td>{html.escape(row["with_source"])}</td>
            </tr>"""
        )

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Cobertura pública de distribuidoras · Mapa Apagones</title>
  <meta name="description" content="Cobertura orientativa de pistas públicas de distribuidora eléctrica por comunidad en Mapa Apagones. No pedimos CUPS, direcciones ni datos personales." />
  <meta name="robots" content="index,follow" />
  <meta property="og:title" content="Cobertura pública de distribuidoras · Mapa Apagones" />
  <meta property="og:description" content="Estado de cobertura de pistas públicas de distribuidora eléctrica por zona, sin CUPS ni datos personales." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://mapa-apagones.es/cobertura-distribuidoras.html" />
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7fb;
      --card: #ffffff;
      --text: #172033;
      --muted: #657084;
      --border: #dce2ec;
      --ok: #e6f7ed;
      --warn: #fff7df;
      --pending: #f3f5f9;
      --accent: #0b63ce;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background: radial-gradient(circle at top left, #eef5ff, var(--bg) 42%);
      line-height: 1.5;
    }}
    main {{
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 28px 0 48px;
    }}
    .top {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 22px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.8);
      padding: 8px 12px;
      border-radius: 999px;
      color: var(--text);
    }}
    .hero {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 26px;
      box-shadow: 0 18px 50px rgba(31, 45, 70, 0.08);
      margin-bottom: 18px;
    }}
    h1 {{
      font-size: clamp(2rem, 6vw, 4.2rem);
      line-height: 0.95;
      letter-spacing: -0.06em;
      margin: 0 0 16px;
    }}
    h2 {{ margin-top: 0; letter-spacing: -0.02em; }}
    .lead {{
      color: var(--muted);
      font-size: 1.08rem;
      max-width: 820px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}
    .metric {{
      border: 1px solid var(--border);
      border-radius: 18px;
      background: #fbfcff;
      padding: 14px;
    }}
    .metric strong {{
      display: block;
      font-size: 1.55rem;
      letter-spacing: -0.04em;
    }}
    .metric span {{ color: var(--muted); font-size: 0.9rem; }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin: 18px 0;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 20px;
      box-shadow: 0 12px 34px rgba(31, 45, 70, 0.06);
    }}
    ul {{ padding-left: 1.2rem; }}
    .table-wrap {{
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: var(--card);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 980px;
      font-size: 0.94rem;
    }}
    th, td {{
      padding: 12px 10px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f8fafc;
      color: #3b4658;
      position: sticky;
      top: 0;
      z-index: 1;
    }}
    tr.complete {{ background: var(--ok); }}
    tr.partial {{ background: var(--warn); }}
    tr.pending {{ background: var(--pending); }}
    code {{
      background: rgba(11, 99, 206, 0.08);
      padding: 2px 6px;
      border-radius: 8px;
    }}
    .note {{
      color: var(--muted);
      font-size: 0.95rem;
    }}
    @media (max-width: 860px) {{
      main {{ width: min(100% - 20px, 1120px); padding-top: 18px; }}
      .hero {{ padding: 20px; border-radius: 20px; }}
      .metrics {{ grid-template-columns: 1fr 1fr; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="top">
      <a class="pill" href="/">← Volver al mapa</a>
      <span>Actualizado: {html.escape(updated)} · {html.escape(version)}</span>
    </div>

    <section class="hero">
      <h1>Cobertura pública de distribuidoras</h1>
      <p class="lead">
        Esta página resume las pistas públicas de distribuidora eléctrica cargadas en Mapa Apagones.
        Son datos orientativos para ayudar a identificar posibles distribuidoras por zona.
        No afirma exclusividad de red y no sustituye una comprobación oficial con comercializadora o distribuidora.
      </p>

      <div class="metrics" aria-label="Resumen de cobertura">
        <div class="metric"><strong>{html.escape(summary["datasets"])}</strong><span>datasets geográficos</span></div>
        <div class="metric"><strong>{html.escape(summary["geo_total"])}</strong><span>zonas normalizadas</span></div>
        <div class="metric"><strong>{html.escape(summary["with_hint"])}</strong><span>Zonas con orientación/pista</span></div>
        <div class="metric"><strong>{html.escape(summary["pending"])}</strong><span>zonas pendientes</span></div>
        <div class="metric"><strong>{html.escape(summary["coverage"])}</strong><span>cobertura actual</span></div>
      </div>
    </section>

    <section class="card">
      <h2>Lectura correcta de la cobertura</h2>
      <p><strong>100% con pista no significa 100% verificación municipal fuerte.</strong></p>
      <p><code>regional_default</code> es orientación regional, no verificación municipal.</p>
      <p><code>verified_partial</code> es una pista pública parcial o municipal, no una garantía de exclusividad.</p>
      <p>Las comunidades con cero pistas no faltan del mapa: tienen geografía municipal, pero siguen pendientes de una pista pública suficientemente segura.</p>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Cómo leer estos datos</h2>
        <ul>
          <li><strong>regional_default</strong>: pista regional orientativa, no exclusividad.</li>
          <li><strong>verified_partial</strong>: presencia pública razonablemente verificada, no cobertura total exclusiva.</li>
          <li>Las zonas pendientes siguen usando fallback seguro hasta tener revisión pública suficiente.</li>
        </ul>
      </article>

      <article class="card">
        <h2>Privacidad</h2>
        <ul>
          <li>No pedimos CUPS.</li>
          <li>No pedimos dirección exacta.</li>
          <li>No pedimos cuentas, contratos, facturas ni datos de contador.</li>
          <li>No publicamos coordenadas privadas ni inventario de infraestructura crítica.</li>
        </ul>
      </article>
    </section>

    <section class="card">
      <h2>Matriz por comunidad</h2>
      <p class="note">
        Generada desde la matriz real del repositorio. Si cambian los GeoJSON o las pistas públicas,
        esta página debe regenerarse con <code>scripts/generate_public_distributor_coverage_page.py</code>.
      </p>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Zona</th>
              <th>Dataset</th>
              <th>GeoJSON</th>
              <th>Con pista</th>
              <th>Pendiente</th>
              <th>Cobertura</th>
              <th>Estado</th>
              <th>Confianza</th>
              <th>Con fuente</th>
            </tr>
          </thead>
          <tbody>
            {''.join(row_html)}
          </tbody>
        </table>
      </div>
    </section>

    <p class="note">
      También puedes consultar el <a href="/changelog.html">changelog público</a>.
    </p>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    raw_html = build_html()
    html_text = "\n".join(line.rstrip() for line in raw_html.splitlines()) + "\n"

    if args.check:
        if not OUTPUT.exists():
            print(f"ERROR: falta {OUTPUT.relative_to(ROOT)}")
            return 1
        current = read(OUTPUT)
        if current != html_text:
            print(f"ERROR: {OUTPUT.relative_to(ROOT)} no está actualizada")
            print("Ejecuta: python3 scripts/generate_public_distributor_coverage_page.py")
            return 1
        print("OK public distributor coverage page actualizada")
        return 0

    OUTPUT.write_text(html_text, encoding="utf-8")
    print(f"OK página generada: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
