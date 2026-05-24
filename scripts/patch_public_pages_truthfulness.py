#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

COVERAGE = Path("frontend/public/cobertura-distribuidoras.html")
RELIABILITY = Path("frontend/public/fiabilidad-distribuidoras.html")
CHANGELOG = Path("frontend/public/changelog.html")

APP_VERSION = "v0.10.6.4-distributor-confidence-labels"
DOC_VERSION = "v0.10.7.6-public-pages-truthfulness"


def patch_changelog() -> None:
    text = CHANGELOG.read_text(encoding="utf-8")

    section = """
<section class="release-card">
  <h2>v0.10.7.6 — Public pages truthfulness and ordering refresh</h2>
  <p>
    Corrige el orden del changelog público y aclara la lectura de las páginas
    públicas de cobertura y fiabilidad de distribuidoras.
  </p>
  <ul>
    <li>La cobertura pública distingue mejor entre zonas, pistas y entradas de confianza.</li>
    <li>Se aclara que 100% con pista no significa 100% verificación municipal fuerte.</li>
    <li>Se aclara que regional_default es orientación regional, no comprobación municipal.</li>
    <li>La página de fiabilidad queda marcada como criterios vigentes e histórico de auditoría.</li>
    <li>Sin importación de nuevas distribuidoras.</li>
  </ul>
  <p>
    Privacidad: sin CUPS, sin direcciones, sin coordenadas exactas, sin datos de
    clientes y sin inventario privado de red.
  </p>
</section>
"""

    # Elimina una versión previa de esta misma entrada si existe.
    text = re.sub(
        r"\n?<section class=\"release-card\">\s*<h2>v0\.10\.7\.6.*?</section>\s*",
        "\n",
        text,
        flags=re.DOTALL,
    )

    # Si la entrada v0.10.7.5 quedó al final, no la borra; la nueva v0.10.7.6 debe ir arriba.
    marker = "v0.10.6.4-distributor-confidence-labels"

    if section.strip() not in text:
        idx = text.find(marker)
        if idx != -1:
            sec_start = text.rfind("<section", 0, idx)
            if sec_start != -1:
                text = text[:sec_start] + section + "\n" + text[sec_start:]
            elif "<main" in text:
                main_end = text.find(">", text.find("<main")) + 1
                text = text[:main_end] + "\n" + section + "\n" + text[main_end:]
            else:
                text = section + "\n" + text
        elif "</main>" in text:
            text = text.replace("</main>", section + "\n</main>", 1)
        else:
            text = section + "\n" + text

    CHANGELOG.write_text(text, encoding="utf-8")
    print(f"OK patched {CHANGELOG}")


def patch_coverage() -> None:
    text = COVERAGE.read_text(encoding="utf-8")

    replacements = {
        "Actualizado: 2026-05-12 · v0.10.6.4-distributor-confidence-labels":
            f"Datos: distributor_hints {APP_VERSION} · Página revisada: 2026-05-24 · {DOC_VERSION}",
        "<th>Con pista</th>": "<th>Zonas con pista</th>",
        "<th>Pendiente</th>": "<th>Zonas pendientes</th>",
        "<th>Confianza</th>": "<th>Entradas por confianza</th>",
        "<th>Con fuente</th>": "<th>Zonas con fuente</th>",
        "con pista en todas las zonas": "todas las zonas tienen orientación o pista pública",
        "regional_default: pista regional orientativa, no exclusividad.":
            "regional_default: orientación regional. No es verificación municipal fuerte ni exclusividad.",
        "verified_partial: presencia pública razonablemente verificada, no cobertura total exclusiva.":
            "verified_partial: presencia pública razonablemente verificada, parcial o municipal. No afirma cobertura total exclusiva.",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    note = """
<div class="notice">
  <strong>Lectura importante:</strong>
  100% con pista no significa 100% verificación municipal fuerte.
  Puede significar que todas las zonas tienen una orientación regional
  <code>regional_default</code>. Las entradas por confianza cuentan pistas de
  distribuidora, no necesariamente zonas únicas; por eso una zona con varias
  distribuidoras puede sumar más de una entrada.
</div>
"""

    if "100% con pista no significa 100% verificación municipal fuerte" not in text:
        if "Cómo leer estos datos" in text:
            text = text.replace("Cómo leer estos datos", "Cómo leer estos datos\n" + note, 1)
        elif "</main>" in text:
            text = text.replace("</main>", note + "\n</main>", 1)
        else:
            text += "\n" + note

    # Aclaración específica para Extremadura si aparece la fila.
    extremadura_note = """
<p class="small-note">
  Nota: en comunidades con varias distribuidoras por zona, las entradas
  <code>verified_partial</code> pueden superar el número de zonas porque cuentan
  pistas de distribuidora, no municipios únicos.
</p>
"""

    if "las entradas <code>verified_partial</code> pueden superar el número de zonas" not in text:
        if "Matriz por comunidad" in text:
            text = text.replace("Matriz por comunidad", "Matriz por comunidad\n" + extremadura_note, 1)
        elif "</main>" in text:
            text = text.replace("</main>", extremadura_note + "\n</main>", 1)

    COVERAGE.write_text(text, encoding="utf-8")
    print(f"OK patched {COVERAGE}")


def patch_reliability() -> None:
    text = RELIABILITY.read_text(encoding="utf-8")

    text = text.replace(
        "Actualizado: 2026-05-13 · v0.10.6.3-distributor-reliability-audit-ui",
        "Criterios vigentes revisados: 2026-05-24 · Documento histórico base: v0.10.6.3-distributor-reliability-audit-ui",
    )

    note = """
<div class="notice">
  <strong>Nota de vigencia:</strong>
  esta página explica los criterios de fiabilidad y conserva una auditoría
  histórica de Galicia, Asturias, Cantabria y La Rioja. La cobertura global
  actual debe consultarse en la página de cobertura de distribuidoras.
</div>
"""

    if "esta página explica los criterios de fiabilidad" not in text:
        if "Fiabilidad de pistas de distribuidoras" in text:
            text = text.replace("Fiabilidad de pistas de distribuidoras", "Fiabilidad de pistas de distribuidoras\n" + note, 1)
        elif "</main>" in text:
            text = text.replace("</main>", note + "\n</main>", 1)
        else:
            text += "\n" + note

    text = text.replace(
        "4\ndatasets auditados en esta fase",
        "4\ndatasets auditados en esta fase histórica",
    )

    RELIABILITY.write_text(text, encoding="utf-8")
    print(f"OK patched {RELIABILITY}")


def main() -> int:
    patch_changelog()
    patch_coverage()
    patch_reliability()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
