# Registro de despliegues — Mapa Apagones

## 2026-09-16

| Repo | Commit | Cloudflare Pages | Raspberry .103 | Raspberry .104 | Resultado |
|---|---|---|---|---|---|
| odegaard12/Mapa-Apagones | PR #222 `security: patch starlette/idna CVEs, add security headers` → `main` | Deploy automático disparado por push a main (confirmado por el check "Cloudflare Pages" en el PR) | **No aplicado** — requiere `git pull && docker compose up -d --build` manual en `.103`; sin acceso SSH desde este entorno | No confirmado si participa | Frontend en producción actualizado; backend en la Pi pendiente de que el usuario aplique el pull |
| odegaard12/Mapa-Apagones | PR #223 `docs: sync README/changelog with real version (v0.12.1)` → `main` | Deploy automático (preview URL confirmada antes del merge) | N/A (solo docs/versión) | N/A | OK |
| odegaard12/Mapa-Apagones | PR #224 `seo: add PWA manifest, fix missing canonical on /seguridad/` → `main` | Deploy automático (preview URL confirmada antes del merge) | N/A (solo frontend estático) | N/A | OK |
| odegaard12/Mapa-Apagones | Rama `fix/incident-timestamps-and-health` (pendiente de PR + merge) | Pendiente | **Pendiente** — este PR sí toca `backend/app/main.py` (fix de `/api/zones` y `/api/health`); tras mergear, el backend en `.103` necesita `git pull && docker compose up -d --build` para que el fix de "Detectado: sin datos" llegue a producción | No confirmado | Pendiente de merge y de aplicación manual en la Pi |

## Cómo aplicar un cambio de backend en la Raspberry `.103`

Este agente no tiene una clave SSH autorizada en `.103` desde este entorno (verificado: puerto 22 alcanzable, autenticación por clave rechazada). Hasta que se resuelva, el usuario debe ejecutar manualmente tras cada merge que toque `backend/`:

```bash
ssh srv-web-01-lan
cd /home/odegaard12/apagones-web   # o la ruta real si difiere
git pull origin main
docker compose up -d --build
docker compose ps
curl -s http://127.0.0.1:8098/api/health
```

## Cómo verificar que Cloudflare Pages sirvió el cambio real

```bash
curl -s https://mapa-apagones.es/ | grep -o 'v0\.[0-9]*\.[0-9]*' | head -1
curl -sI https://mapa-apagones.es/ | grep -i "content-security-policy\|strict-transport-security"
```

No se ha ejecutado esta verificación contra el dominio real en esta sesión (navegación externa bloqueada por el clasificador de permisos del entorno en el momento de intentarlo). Pendiente de confirmar en una sesión con acceso.
