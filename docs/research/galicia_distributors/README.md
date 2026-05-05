# Auditoría de distribuidoras eléctricas por concello — Galicia

Objetivo: revisar los 313 concellos de Galicia antes de ampliar `frontend/src/data/distributor_hints.json`.

Reglas:

- No publicar CUPS.
- No publicar datos personales.
- No publicar direcciones exactas de usuarios.
- No publicar coordenadas privadas.
- No publicar subestaciones, líneas, tendidos, cables, centros de transformación ni inventario de infraestructura crítica.
- No usar una distribuidora por comunidad autónoma como verdad municipal.
- CNMC censo confirma existencia de distribuidora, pero no cobertura municipal.
- DOG/Xunta con solicitante + ayuntamiento es fuente fuerte.
- APYDE con "Zonas de distribución" es fuente pública útil para pequeñas distribuidoras gallegas.
- Web oficial de distribuidora con zona/municipio es fuente válida.
- Si hay duda, marcar `pending_review` o `conflict`, no añadir a producción.

Estados:

- `verified_municipal`: fuente pública permite asignación municipal fuerte.
- `verified_partial`: fuente pública verifica actividad/zona, sin afirmar exclusividad ni cobertura total.
- `regional_default_candidate`: distribuidora mayoritaria/regional, pendiente de comprobación municipal.
- `pending_review`: falta revisar.
- `conflict`: hay fuentes contradictorias.
- `unknown`: sin fuente fiable encontrada.
