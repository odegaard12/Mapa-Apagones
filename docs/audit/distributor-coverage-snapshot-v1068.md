# Distributor hints coverage snapshot v0.10.6.8

Generated: 2026-05-22

## Scope

This report summarizes the public distributor hints dataset.

Privacy constraints:

- No CUPS.
- No addresses.
- No exact user coordinates.
- No private infrastructure inventory.
- No raw external API responses.

## Dataset summary

- JSON version: `v0.10.6.4-distributor-confidence-labels`
- Public hint zones: **2610**
- Dataset ids with hints: **15**

## Confidence distribution

| confidence | entries |
|---|---:|
| `regional_default` | 1800 |
| `verified_partial` | 967 |

## Coverage by dataset

| dataset_id | zones | regional_default | verified_partial | other/unknown |
|---|---:|---:|---:|---:|
| `andalucia` | 254 | 0 | 254 | 0 |
| `asturias` | 78 | 78 | 2 | 0 |
| `canarias` | 88 | 87 | 1 | 0 |
| `cantabria` | 103 | 103 | 0 | 0 |
| `ceuta` | 1 | 0 | 1 | 0 |
| `comunitat_valenciana` | 544 | 533 | 11 | 0 |
| `euskadi` | 255 | 252 | 3 | 0 |
| `extremadura` | 388 | 0 | 530 | 0 |
| `galicia` | 313 | 172 | 154 | 0 |
| `illes_balears` | 68 | 67 | 1 | 0 |
| `la_rioja` | 175 | 175 | 0 | 0 |
| `madrid` | 9 | 0 | 9 | 0 |
| `melilla` | 1 | 0 | 1 | 0 |
| `murcia` | 45 | 45 | 0 | 0 |
| `navarra` | 288 | 288 | 0 | 0 |

## Top public distributor names

| distributor | entries |
|---|---:|
| i-DE Redes Eléctricas Inteligentes, S.A.U. | 1293 |
| I-DE Redes Eléctricas Inteligentes, S.A.U. | 255 |
| E-Distribución Redes Digitales, S.L.U. | 254 |
| UFD Distribución Electricidad, S.A. | 177 |
| e-distribución Redes Digitales, S.L.U. | 154 |
| Viesgo Distribución | 103 |
| Edistribución Redes Digitales, S.L.U. | 100 |
| E-REDES Distribución | 78 |
| Barras Eléctricas Galaico-Asturianas, S.A. (BEGASA) | 66 |
| Eléctrica del Oeste Distribución, S.L.U. | 52 |
| Eléctricas Pitarch Distribución, S.L.U. | 30 |
| Unión Distribuidores Electricidad S.A. (Udesa) | 17 |
| Hijos de Jacinto Guillén, D.E., S.L. | 10 |
| Distribuidora Eléctrica Monesterio, S.L. | 9 |
| Eléctrica Santa Marta y Villalba, S.L. | 8 |
| Eléctrica San Serván, S.L. | 8 |
| Energía de Miajadas, S.A. | 8 |
| Fuentes y Compañía, S.L. | 7 |
| Distribuidora Eléctrica Carrión, S.L. | 6 |
| Electra de Cabalar, S.L. | 6 |
| Electra del Narahío S.A. | 6 |
| Hijos de Francisco Escaso, S.L. | 5 |
| Distribución de Electricidad Valle de Santa Ana, S.L. | 5 |
| Eléctrica de Moscoso, S.L. | 5 |
| Sociedad Electricista de Tui S.A. | 5 |
| Energética de Alcocer, S.L. | 4 |
| Industrial Barcalesa, S.L. | 4 |
| Eléctrica de Cantoña, S.L. | 4 |
| San Miguel 2000, Distribuición S.L. | 4 |
| Luis Rangel y Hermanos, S.A. | 3 |

## Recommended next work

Priority should favor conservative, source-backed improvements:

1. Expand `verified_partial` only where strong public evidence exists.
2. Avoid converting broad regional defaults into municipal claims without evidence.
3. Keep local distributors visible only when supported by public sources.
4. Prefer research/audit PRs before data import PRs for large communities.

Suggested next data targets:

- Andalucía: continue pending municipal review after the strong E-Distribución import.
- Extremadura: continue municipal review queue before importing further hints.
- Madrid: review remaining mixed/local distributor cases.
- Castilla y León / Castilla-La Mancha: start with research PRs, not direct import.

