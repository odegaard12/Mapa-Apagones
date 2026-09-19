# Investigación de fuentes de distribuidoras — España

Búsqueda de fuentes públicas verificables para 4 regiones (4,901 municipios sin pista).

## Política del proyecto
- ✅ Fuentes públicas documentadas
- ✅ Acceso sin CAPTCHA/bypass
- ✅ Descarga manual de archivos
- ❌ Scraping agresivo o evasión de protecciones
- ❌ Almacenamiento de PII (coordenadas exactas, direcciones)

---

## Fuentes encontradas

### 1. Castilla y León (2,298 municipios)

**Distribuidoras principales:**
- **E-REDES Distribución** (Endesa) — cubre mayoría de la región
  - Fuente oficial: https://www.eredesdistribucion.es/
  - Listado de municipios: NO público (verificado 2026-09-17)
  - Alternativa: Mapa interactivo con filtro por código postal (requiere entrada manual)
  
- **Distribuidoras municipales / cooperativas** — información dispersa
  - No hay registro centralizado público

**Conclusión:** Sin acceso a listado municipal verificable. La página de E-REDES tiene mapa pero no permite descarga.

---

### 2. Catalunya (948 municipios)

**Distribuidoras principales:**
- **Endesa Distribution** — principal
- **E-REDES** — zona pequeña
- **Distribuidoras municipales** — dispersas

**Fuentes investigadas:**
- Dept. de Política Territorial i Sostenibilitat: NO ofrece listado de distribuidoras por municipio (2026-09-17, verificado)
- Endesa: Mapa interactivo sin API pública

**Conclusión:** Información pública disponible principalmente a través de mapas interactivos, no descargables en bulk.

---

### 3. Castilla-La Mancha (921 municipios)

**Distribuidoras principales:**
- **E-REDES Distribución** — cubre casi toda la región

**Fuentes investigadas:**
- Consejería de Hacienda y Administración Pública: NO tiene registro público de distribuidoras
- E-REDES: Mapa con acceso interactivo solamente

**Conclusión:** Información disponible solo mediante consulta interactiva en web de distribuidoras.

---

### 4. Aragón (734 municipios)

**Distribuidoras principales:**
- **Endesa Distribution** — principal
- **E-REDES** — zona pequeña

**Fuentes investigadas:**
- Generalidad de Aragón: NO ofrece listado de distribuidoras por municipio
- Endesa: Acceso interactivo solamente

**Conclusión:** Sin listado público bulk descargable.

---

## Opciones disponibles

| Opción | Esfuerzo | Verificabilidad | Notas |
|--------|----------|-----------------|-------|
| **A. Usar solo acceso interactivo de distribuidoras** | Alto | Alta | Manual por municipio o código postal |
| **B. Solicitar datos a distribuidoras** | Muy alto | Alta | Requiere contacto administrativo formal |
| **C. Usar estimación regional** | Muy bajo | Media | Asumir distribuidora principal por región (ya en datos) |
| **D. Dejar como "unknown"** | Nulo | Máxima | Honesto: no hay fuente pública verificable |

---

## Recomendación

**Opción D (mantener como unknown) es la más correcta:**
- Sin fuentes públicas verificables y descargables, no hay forma de poblar sin CAPTCHA/scraping agresivo
- La política del proyecto prohíbe scraping y CAPTCHA-bypass
- Mantener "unknown" es honesto y evita datos incorrectos

**Alternativa**: Agregar nota en la interfaz:
> "Estas regiones no tienen fuentes públicas verificables de distribuidoras disponibles. Puedes consultar directamente a E-REDES, Endesa o tu comercializadora."

---

## Próximos pasos

- [ ] Confirmar con usuario si acepta dejar como "unknown"
- [ ] O solicitar autorización para contacto administrativo con distribuidoras
- [ ] O implementar formulario de crowdsourcing ("¿Tu distribuidora es...?")

---

## ACTUALIZACIÓN 2026-09-19 — Fuente real encontrada

**Se encontró y explotó una fuente pública real**, corrigiendo la conclusión anterior de "sin fuentes públicas descargables".

### Fuente: CNMC (regulador nacional) — Mapa de capacidad de acceso en redes de distribución

- Portal: https://www.cnmc.es/prensa/mapas-capacidad-redes-electricas-20260415
- API subyacente (ArcGIS FeatureServer, pública, sin autenticación, sin CAPTCHA):
  `https://services9.arcgis.com/F9FmuOlj5xjEjPRZ/arcgis/rest/services/Demanda_en_Distribucion/FeatureServer/4`
- Campos relevantes: `PROVINCIA`, `MUNICIPIO`, `DESCRIPCION` (nombre legal de la distribuidora), `GESTOR_RED` (código R1-xxx)
- Los gestores de red están **obligados por regulación** (RDC/DE/001/25) a reportar esta información mensualmente a la CNMC
- Consulta vía API REST estándar (GET con parámetros de query), sin scraping de HTML ni evasión de protecciones

### Cómo se descubrió

1. Se revisó cómo se obtuvieron los datos ya existentes de Andalucía (`distributor_hints.json`) → llevó a un WFS de la Junta de Andalucía
2. Búsqueda del patrón equivalente para las 4 regiones faltantes → no había WFS regional útil (Aragón: capa sin nombre de distribuidora)
3. Búsqueda de fuente **nacional** en vez de regional → CNMC publica mapas de capacidad de acceso desde abril 2026
4. Las apps son ArcGIS Experience Builder → se localizó el FeatureServer real inspeccionando la config del item de ArcGIS Online
5. El FeatureServer expone datos estructurados por municipio, consultables sin restricciones

### Resultado de la importación (2026-09-19)

| Región | Municipios cubiertos | Total región | % |
|---|---:|---:|---:|
| Aragón | 138 | 734 | 18.8% |
| Catalunya | 157 | 948 | 16.6% |
| Castilla-La Mancha | 154 | 921 | 16.7% |
| Castilla y León | 251 | 2.298 | 10.9% |
| **Total** | **700** | **4.901** | **14.3%** |

37 municipios tienen múltiples distribuidoras detectadas (zonas con más de una subestación de distinto operador) — se listan todas, sin afirmar exclusividad.

7 municipios de Catalunya no matchearon por variantes de artículo catalán no estándar (Les, L', Els, Es) — pendiente de fix menor de normalización.

**Confidence asignado**: `verified_partial` — es dato real de un operador con subestación en el municipio, pero no confirma cobertura del 100% del término municipal (municipios grandes pueden tener varios operadores en distintas zonas).

### Por qué el hallazgo previo (0% viable) no era incorrecto, solo incompleto

Las auditorías previas (`docs/audit/aragon-wave2-candidate-gate-v1083.md`, etc.) buscaban fuentes **regionales** (DOGC, DOCM, boletines autonómicos) y confirmaron correctamente que ninguna tenía datos descargables a nivel municipal. Nadie había buscado a nivel **nacional** (CNMC como regulador, no las comunidades autónomas). Ese fue el gap.

### Próximos pasos posibles

- Aplicar el mismo método a Madrid (actualmente 9/181, 5%) y otras regiones con cobertura parcial
- Arreglar el matching de los 7 municipios catalanes con artículo no estándar
- Revisar si el FeatureServer de generación (`Capacidad_Periodo`) aporta datos adicionales
- Considerar automatizar la re-sincronización mensual (CNMC publica actualizaciones mensuales)

---

## ACTUALIZACIÓN 2026-09-19 (parte 2) — Expansión nacional completa

Tras el hallazgo inicial (700 municipios en las 4 regiones objetivo), se amplió la consulta al FeatureServer
de CNMC a **todo el territorio nacional** (6.186 filas totales), no solo las 4 regiones sin cobertura.

**Bug encontrado y corregido durante el proceso**: Extremadura (ya al 100%) usa una convención de `zone_id`
distinta a la del resto (`municipality:extremadura::xxx` en vez de `municipality:{provincia}::xxx`). Al
matchear contra el `zone_id` canónico del GeoJSON se generaron 91 duplicados reales (mismo municipio, dos
entradas). Se detectó comparando pares (municipio, provincia) duplicados y se eliminaron las entradas nuevas
redundantes, conservando las originales. **Cero duplicados** confirmado tras la limpieza.

### Resultado final combinado (ambas pasadas)

| Región | Antes sesión | Ahora | Municipios nuevos |
|---|---:|---:|---:|
| Madrid | 5,0% (9/181) | **34,3%** (62/181) | +53 |
| Andalucía | 32,3% (254/786) | **47,2%** (371/786) | +117 |
| Aragón | 0% | **18,8%** (138/734) | +138 |
| Catalunya | 0% | **17,2%** (163/948) | +163 |
| Castilla-La Mancha | 0% | **16,7%** (154/921) | +154 |
| Castilla y León | 0% | **10,9%** (251/2.298) | +251 |
| **Total nacional** | 31,8% | **42,4%** (3.486/8.215) | **+876** |

Extremadura se mantuvo en 100% (388/388) tras la limpieza de duplicados — no se tocó, solo se evitó
contaminarla con entradas redundantes.
