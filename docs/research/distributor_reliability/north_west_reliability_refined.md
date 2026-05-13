# Auditoría refinada de fiabilidad · Galicia, Asturias, Cantabria y La Rioja

Fecha: `2026-05-13`.

## Resultado corregido

| Dataset | Zonas | Con pista | Pendientes | Regional default | Verified partial | Fuertes | Orientativas regionales | Revisión | Multi | Problemas reales | Riesgo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `galicia` | 313 | 313 | 0 | 172 | 154 | 141 | 172 | 0 | 12 | 0 | `MIXED_RELIABILITY_UI_REQUIRED` |
| `asturias` | 78 | 78 | 0 | 78 | 2 | 2 | 78 | 0 | 2 | 0 | `MIXED_RELIABILITY_UI_REQUIRED` |
| `cantabria` | 103 | 103 | 0 | 103 | 0 | 0 | 103 | 0 | 0 | 0 | `UI_RELIABILITY_DOWNGRADE_REQUIRED` |
| `la_rioja` | 175 | 175 | 0 | 175 | 0 | 0 | 175 | 0 | 0 | 0 | `UI_RELIABILITY_DOWNGRADE_REQUIRED` |

## Diagnóstico

### galicia
- Riesgo: `MIXED_RELIABILITY_UI_REQUIRED`.
- Clases: C_REGIONAL_DEFAULT_CORPORATE=172 | A_VERIFIED_PARTIAL_STRONG=154.
- Top distribuidoras: UFD Distribución Electricidad, S.A.=168 | Barras Eléctricas Galaico-Asturianas, S.A. (BEGASA)=66 | Unión Distribuidores Electricidad S.A. (Udesa)=17 | Electra de Cabalar, S.L.=6 | Electra del Narahío S.A.=6 | Eléctrica de Moscoso, S.L.=5 | Sociedad Electricista de Tui S.A.=5 | Industrial Barcalesa, S.L.=4 | Eléctrica de Cantoña, S.L.=4 | San Miguel 2000, Distribuición S.L.=4 | Hidroeléctrica de Laracha S.L.=3 | Central Eléctrica Industrial, S.L.U.=3.
- Top fuentes: UFD/Naturgy presencia regional Galicia=106 | APYDE ficha pública=84 | BEGASA información pública distribuidora Lugo=66 | CNMC C/1436/24 Grupo EHR/Moscoso=4 | DOG 9/2024 UFD en A Coruña=1 | DOG 220/2024 UFD en A Pobra do Caramiñal=1 | DOG 51/2026 UFD en Aranga=1 | DOG 52/2026 UFD en Ares=1 | DOG 66/2026 UFD en Bergondo=1 | DOG 156/2025 UFD en Betanzos=1 | DOG 52/2026 UFD en Boimorto=1 | DOG 80/2026 UFD en Boiro=1.

### asturias
- Riesgo: `MIXED_RELIABILITY_UI_REQUIRED`.
- Clases: C_REGIONAL_DEFAULT_CORPORATE=78 | A_VERIFIED_PARTIAL_STRONG=2.
- Top distribuidoras: E-REDES Distribución=78 | Electra de Carbayín, S.A.U.=2.
- Top fuentes: E-REDES — información pública distribuidora=78 | Electra de Carbayín — área de distribución=2.

### cantabria
- Riesgo: `UI_RELIABILITY_DOWNGRADE_REQUIRED`.
- Clases: C_REGIONAL_DEFAULT_CORPORATE=103.
- Top distribuidoras: Viesgo Distribución=103.
- Top fuentes: Viesgo Distribución — información pública distribuidora=103.

### la_rioja
- Riesgo: `UI_RELIABILITY_DOWNGRADE_REQUIRED`.
- Clases: C_REGIONAL_DEFAULT_PRIVATE_MAP=175.
- Top distribuidoras: i-DE Redes Eléctricas Inteligentes, S.A.U.=175.
- Top fuentes: i-DE — mapa oficial de distribuidoras=175.

## Recomendación

- No abrir PR de importación de nuevas pistas con esta auditoría.
- Abrir PR de fiabilidad/UX: mostrar `regional_default` como orientación regional, no como pista municipal fuerte.
- Mantener `verified_partial` fuerte como pista municipal/parcial.
- Galicia necesita separar claramente sus 154 entradas fuertes de sus 172 regionales orientativas.
- Asturias, Cantabria y La Rioja no deberían verse como 100% verificadas, sino como 100% con orientación regional.

## Archivos

- `<artefacto-local-temporal>`
- `<artefacto-local-temporal>`
- `<artefacto-local-temporal>`
- `<artefacto-local-temporal>`
- `<artefacto-local-temporal>`
