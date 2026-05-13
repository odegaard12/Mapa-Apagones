# Fiabilidad de pistas de distribuidoras

Fecha: `2026-05-13`.

Esta carpeta documenta la auditoría de fiabilidad de pistas de distribuidora para Galicia, Asturias, Cantabria y La Rioja.

## Resultado

No se añaden nuevas pistas `verified_partial` en esta fase.

El avance real es separar mejor dos niveles que no deben verse igual:

- `verified_partial`: pista pública municipal/parcial con fuente fuerte.
- `regional_default`: orientación regional o corporativa; útil, pero no verificación municipal fuerte.

## Hallazgos principales

| Dataset | Zonas | Pistas actuales | Fuertes actuales | Orientativas regionales | Decisión |
|---|---:|---:|---:|---:|---|
| `galicia` | 313 | 313 | 141 | 172 | Mantener fuertes; aclarar orientación regional |
| `asturias` | 78 | 78 | 2 | 76 | Mantener Electra de Carbayín; E-REDES como orientación |
| `cantabria` | 103 | 103 | 0 | 103 | Viesgo como orientación regional |
| `la_rioja` | 175 | 175 | 0 | 175 | No subir desde mapa i-DE interactivo |

## Por qué esto sí aporta

- Evita vender como “verificado municipal” lo que solo es orientación regional.
- Conserva las distribuidoras locales ya verificadas en Galicia.
- Deja documentada la decisión técnica de no importar La Rioja 175/175 desde el mapa i-DE.
- Prepara una mejora de UX para que el usuario entienda la calidad de cada pista.

## Archivos

- `north_west_knowledge_audit.md`
- `north_west_knowledge_by_dataset.csv`
- `north_west_knowledge_by_zone.csv`
- `north_west_knowledge_sources.csv`
- `north_west_reliability_refined.md`
- `la_rioja_ide_final_decision.md`
- `north_west_reliability_summary.json`

## Privacidad y seguridad

No se publican CUPS, direcciones, coordenadas exactas, capturas, respuestas raw, tokens, claves ni geometrías de red.
