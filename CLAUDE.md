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
6. **Despliegue a .103**: `git pull && docker compose up -d --build` en `/home/odegaard12/apagones-web`. Requiere acceso a la Raspberry (el operador humano gestiona sus propias credenciales fuera de este repo).

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

### main — todo mergeado y desplegado en producción
- ✅ PR #225: timestamps de incidencia + refresco manual
- ✅ PR #226: mobile responsive design (map 100% ancho, panels respetan nav)
- ✅ PR #227: investigación distribuidoras (documentado, sin fuentes públicas viables)
- ✅ PR #228: auditoría UX completa + CLAUDE.md inicial
- ✅ PR #229: fix contraste barra inferior móvil
- ✅ Backend en `.103` actualizado y verificado healthy en producción

### Frontend estático
- ✅ Cloudflare Pages: despliega automáticamente en push a main
- ✅ CSP/HSTS/Referrer-Policy/X-Frame-Options vía `frontend/public/_headers`
- ✅ CORS: `ALLOWED_ORIGINS` restringido, `allow_credentials=False`
- ✅ PWA: manifest.webmanifest presente

### Backend (en .103) — desplegado y verificado 2026-09-18
- ✅ `/api/health`: valida conexión real a SQLite — confirmado en producción
- ✅ `/api/zones`: incluye `created_at` de incidencias — confirmado en producción
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

### Decisión de usuario pendiente
- [ ] Estrategia para 4 regiones sin distribuidoras:
  - A) Dejar como "unknown" (honesto, sin datos falsos)
  - B) Usar distribuidora regional default (menos preciso)
  - C) Implementar crowdsourcing (formulario "¿Tu distribuidora es...?")

### Ramas
Sin ramas locales huérfanas al cierre de esta sesión. Revisar `gh pr list --state open` por PRs de Dependabot que puedan seguir abiertos aunque su contenido ya esté en main (se cierran solos al siguiente escaneo).

---

## DECISIONES TOMADAS (que no repetir)

1. **No revertir nada mergeado** — main es la fuente de verdad.
2. **Diseño móvil**: CSS fixes no rompen desktop. Testear en 375×812 y desktop.
3. **Distribuidoras**: sin fuentes públicas = documentar el bloqueo en lugar de inventar datos.
4. **UX**: todos los botones funcionan (MAPA/ZONAS/REPORTAR/FILTROS/INFO). No hay bloqueadores.
5. **Barra inferior móvil**: contraste corregido tras feedback de usuario (color inactivo alineado con `--muted`).

---

## PUNTOS FRÁGILES (precaución)

- **React 18→19**: PRs de Dependabot rompen Cloudflare Pages build. No mergear hasta investigar la causa.
- **Scroll en paneles mobile**: scrollbar es pequeño (4px). En pantallas muy pequeñas podría ser poco visible.

---

## PRÓXIMOS PASOS (recomendación)

1. Decidir estrategia para 4 regiones sin distribuidoras (A/B/C arriba)
2. Implementar si es C (crowdsourcing)
3. Auditoría de performance (Lighthouse, Core Web Vitals real)
4. Investigar por qué React 19 rompe el build de Cloudflare Pages
5. Seguir recogiendo feedback de UX real de usuarios

---

## CÓMO CONTINUAMOS

**Próxima sesión:**
1. `git fetch origin && git log main -5` — confirmar estado de main
2. Revisar `gh pr list --state open` por PRs pendientes
3. Continuar desde "Trabajo Pendiente" arriba

**Graphify**: el grafo existe en `graphify-out/`. Usar `graphify query "<pregunta>"` antes de explorar código.

---

## CONTACTO / LOGS

- **Repo**: https://github.com/odegaard12/Mapa-Apagones
- **Cloudflare Pages**: mapa-apagones.es
- **Backend**: Raspberry en red local, acceso gestionado por el operador fuera de este repo

---

**Última revisión**: 2026-09-18
