# MAPA APAGONES — Guía de Operación

**Versión**: v0.12.1 | **Última actualización**: 2026-09-18

---

## ARQUITECTURA

```
GitHub (odegaard12/Mapa-Apagones, main branch)
  ├─ Push → Cloudflare Pages (automático)
  │   └─ Frontend estático: frontend/dist/ con _headers (CSP, HSTS, etc.)
  │
  └─ Push → (manual deploy necesario en .103)
      └─ Raspberry .103 (srv-web-01-lan): docker-compose up -d --build
          ├─ apagones_backend (FastAPI en :8000)
          ├─ apagones_web (nginx proxy /api/ a :8000)
          └─ SQLite: /app/data/apagones.db

Frontend: React 18 + Leaflet + Vite
Backend: FastAPI + SQLite + HMAC-SHA256 hashing (anónimo, sin PII)
```

---

## REGLAS ESTRICTAS

1. **Responde ÚNICAMENTE con código/comando solicitado. Cero explicaciones.**
2. **Lee ÚNICAMENTE archivos explícitos.**
3. **No repitas trabajo ya mergeado** a main.
4. **Políticas de datos**:
   - No CUPS, no direcciones exactas, no fotos, no nombres reales
   - Hashing anónimo (HMAC-SHA256) para token/IP
   - Agregación por zona aproximada
5. **Distribuidoras**: solo fuentes públicas verificables. Sin CAPTCHA-bypass, sin scraping agresivo.
6. **Despliegue a .103**: requiere `git pull && docker compose up -d --build` manual (sin SSH autorizado).

---

## COMANDOS CRÍTICOS

### Build & Test (local)
```bash
# Frontend
cd frontend && npm install && npm run build
npm run dev                          # Vite dev server :5173

# Backend (sin Docker)
cd backend && pip install -r requirements.txt
DB_PATH=/tmp/test.db TURNSTILE_SECRET="" uvicorn app.main:app --reload

# Smoke tests (verifican que app levanta correctamente)
python scripts/smoke_backend_api.py
python scripts/smoke_backend_schema.py
python scripts/smoke_frontend_static.py
```

### Git (flujo local)
```bash
git checkout -b <feature-branch>     # Nueva rama
git add <file>; git commit -m "..."  # Commit con Co-Authored-By
git push -u origin <feature-branch>  # Push
# Luego: crear PR manualmente en GitHub (main está protegida)
```

### Deploy a .103 (manual, post-merge)
```bash
ssh srv-web-01-lan
cd /home/odegaard12/apagones-web
git pull origin main
docker compose up -d --build
docker compose ps
curl -s http://127.0.0.1:8098/api/health
```

---

## ESTADO ACTUAL (2026-09-18)

### main (HEAD: 1b53168)
- ✅ PR #225 mergeado: timestamps de incidencia + refresco manual
- ✅ PR #224: PWA manifest + canonical tag en /seguridad/
- ✅ PR #223: README/changelog sync (v0.12.1)
- ✅ PR #222: CVE fixes (starlette, idna) + security headers en Cloudflare
- ✅ PR #221: 5 Dependabot PRs merged
- ✅ PR #220: Auto-detección de cortes (5+ reports en 10 min)

### Frontend estático
- ✅ Cloudflare Pages: despliega automáticamente en push a main
- ✅ CSP/HSTS/Referrer-Policy/X-Frame-Options vía `frontend/public/_headers`
- ✅ CORS: `ALLOWED_ORIGINS` restringido, `allow_credentials=False`
- ✅ PWA: manifest.json + service worker ready

### Backend (en .103)
- ⚠️ **PENDIENTE**: aplicar `git pull && docker compose up -d --build` (PR #225 fixes)
- ✅ `/api/health`: valida conexión real a SQLite
- ✅ `/api/zones`: incluye `created_at` de incidencias (bug fixed en PR #225)
- ✅ Rate limiting: `ABUSE_LIMIT_PER_HOUR` (escritura), `PUBLIC_READ_LIMIT_PER_MINUTE` (lectura)

### Cobertura de distribuidoras
- ✅ 15 regiones: Asturias, Cantabria, Galicia, Euskadi, Navarra, La Rioja, Aragón, Cataluña, Comunitat Valenciana, Murcia, Andalucía, Extremadura, Castilla-La Mancha, Madrid, Illes Balears, Canarias, Ceuta, Melilla
- ❌ 4 regiones: **0% pista de distribuidora** (2,298 + 948 + 921 + 734 = 4,901 municipios)
  - Castilla y León
  - Catalunya
  - Castilla-La Mancha
  - Aragón
  - **Hallazgo (2026-09-18)**: No hay fuentes públicas descargables sin scraping/CAPTCHA. Opción: dejar como "unknown", o implementar crowdsourcing.

---

## TRABAJO PENDIENTE

### BLOQUEADO (requiere decisión/acción usuario)
- [ ] Mergear PR #225 en GitHub (main está protegida)
- [ ] Aplicar `git pull && docker compose up -d --build` en .103 para que fixes lleguen a producción
- [ ] Estrategia para 4 regiones sin distribuidoras:
  - A) Dejar como "unknown" (honesto, sin datos falsos)
  - B) Usar distribuidora regional default (menos preciso)
  - C) Implementar crowdsourcing (formulario "¿Tu distribuidora es...?")

### RAMAS LISTAS PARA PR (2026-09-18)
```
fix/mobile-responsive-design   ← CSS fixes (map 100% ancho, panels respetan nav)
feat/distributor-sources-spain ← Investigación (documento DISTRIBUTOR_RESEARCH.md)
audit/mobile-ux-complete       ← Auditoría UX (documento AUDIT_UX_MOBILE.md)
```

### RAMAS ANTIGUAS (considerar cerrar)
```
docs/reconcile-pr225-state     ← Reconciliation de docs (no mergeada)
chore/dependabot-batch-sept    ← Viejos, ya merged
docs/readme-changelog-sync     ← Ya merged como PR #223
security/headers-and-cve-fixes ← Ya merged como PR #222
seo/*                          ← Ya merged
feat/auto-outage-detection     ← Ya merged como PR #220
```

---

## DECISIONES TOMADAS (que no repetir)

1. **No revertir PR #225**: está merged, documentado. Siguiente sesión continúa desde ahí.
2. **Diseño móvil**: CSS fixes no rompen desktop. Testear en 375×812.
3. **Distribuidoras**: sin fuentes públicas = documentar el bloqueo en lugar de inventar datos.
4. **UX**: todos los botones funcionan (MAPA/ZONAS/REPORTAR/FILTROS/INFO). No hay bloqueadores.

---

## PUNTOS FRÁGILES (precaución)

- **Raspberry .103**: SSH no autorizado. Requiere user manual `git pull && docker compose up -d --build`.
- **React 18→19**: PRs #217/#218 rompen Cloudflare Pages build. No mergear hasta resolver.
- **Dependabot**: 5 PRs viejos abiertos (#216/#215/#213/#212/#211). Se cerrarán solos cuando Dependabot los rescane.
- **Scroll en paneles mobile**: scrollbar es pequeño (4px). En pantallas muy pequeñas podría ser poco visible.

---

## PRÓXIMOS PASOS (recomendación)

1. Mergear `fix/mobile-responsive-design` (impacto visual, ya testeado)
2. Decidir estrategia para 4 regiones sin distribuidoras (A/B/C arriba)
3. Implementar si es C (crowdsourcing)
4. Auditoría de performance (Lighthouse, Core Web Vitals real)
5. Considerar dark mode refinement

---

## CÓMO CONTINUAMOS

**Próxima sesión:**
1. `git fetch origin && git log main -5` — confirmar estado de main
2. Revisar si PRs nuevas fueron mergeadas en GitHub
3. Aplicar fixes en .103 si fue necesario
4. Continuar desde "Trabajo Pendiente" arriba

**Graphify**: el grafo existe en `graphify-out/`. Usar `graphify query "<pregunta>"` antes de explorar código.

---

## CONTACTO / LOGS

- **User email**: oscarandroid2000@gmail.com
- **Repo**: https://github.com/odegaard12/Mapa-Apagones
- **Cloudflare Pages**: mapa-apagones.es
- **Backend**: .103 (srv-web-01-lan)

---

**Última revisión**: 2026-09-18 por Claude Haiku 4.5
