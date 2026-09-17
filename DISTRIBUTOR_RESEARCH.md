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
