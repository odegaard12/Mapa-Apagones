# Auditoría grande de conocimiento/fiabilidad · Galicia, Asturias, Cantabria y La Rioja

## Seguridad

- No modifica el repositorio.
- No guarda geometrías ni coordenadas.
- No guarda CUPS, direcciones, teléfonos ni emails.
- Solo guarda metadatos saneados de fuentes y recomendaciones por municipio/zona.

## Resultado por dataset

| Dataset | Zonas | Con pista | Faltan | Verificar mapa interactivo | Revisar fuente fuerte | Mantener verified_partial | Mantener orientación regional | Manual | Duplicados |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `galicia` | 313 | 313 | 0 | 0 | 0 | 141 | 172 | 0 | 0 |
| `asturias` | 78 | 78 | 0 | 0 | 0 | 2 | 76 | 0 | 0 |
| `cantabria` | 103 | 103 | 0 | 0 | 0 | 0 | 103 | 0 | 0 |
| `la_rioja` | 175 | 175 | 0 | 175 | 0 | 0 | 0 | 0 | 0 |

## Lectura

- `candidate_verify_interactive_map`: candidato interesante, pero no importable sin comprobación reproducible/manual.
- `candidate_source_upgrade_review`: posible subida a `verified_partial` si la fuente prueba municipio/zona.
- `keep_verified_partial`: ya está en buen nivel.
- `keep_regional_orientation`: no vender como verificación municipal fuerte.

## Siguientes PR posibles

1. PR UX: mostrar claramente orientación regional vs pista parcial verificada.
2. PR datos La Rioja si se verifica municipio a municipio contra fuente reproducible.
3. PR datos puntuales Galicia/Asturias si aparece fuente municipal/zonal fuerte adicional.

## Archivos

- `<artefacto-local-temporal>`
- `<artefacto-local-temporal>`
- `<artefacto-local-temporal>`
