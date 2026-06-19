#!/usr/bin/env python3
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
checks={'frontend/src/App.jsx':['v0.11.0.0-map-ux-reliability','MobileMapNavigation','IncidentReliability','incidentsError','incidentsUpdatedAt','Reintentar','Yo también','Ya volvió'],'frontend/src/components/IncidentReliability.jsx':['Ciclo de vida','Confirmaciones activas','Último aviso','Recuperación','independiente'],'frontend/src/components/MobileMapNavigation.jsx':['Mapa','Zonas','Reportar','Filtros','Navegación principal'],'frontend/src/styles.css':[':focus-visible','prefers-reduced-motion','.mobile-map-nav','.reliability-card'],'VERSION':['v0.11.0.0-map-ux-reliability'],'CHANGELOG.md':['v0.11.0.0','Mapa 2.0'],'frontend/public/changelog.html':['v0.11.0.0','Mapa 2.0: diseño móvil y fiabilidad pública']}
e=[]
for f,needles in checks.items():
    p=R/f
    if not p.exists(): e.append(f'Falta {f}'); continue
    s=p.read_text(encoding='utf-8')
    for n in needles:
        if n not in s: e.append(f'{f}: falta {n!r}')
m=[]
for p in R.rglob('*.json'):
    if any(x in {'.git','node_modules','dist','build'} for x in p.parts) or 'distribut' not in p.name.lower(): continue
    try: d=json.loads(p.read_text(encoding='utf-8'))
    except Exception: continue
    seq=[d] if isinstance(d,list) else [v for v in d.values() if isinstance(v,list)] if isinstance(d,dict) else []
    for rows in seq:
        if len(rows)==2610: m.append((p,rows))
if len(m)!=2:
    e.append(f'Se esperaban dos copias espejo de 2610 hints y hay {len(m)}')
elif len({__import__('hashlib').sha256(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest() for _,rows in m})!=1:
    e.append('Las dos copias productivas de hints no son idénticas')
if e:
    print('Map UX reliability guard: FAIL',file=sys.stderr)
    [print('- '+x,file=sys.stderr) for x in e]
    raise SystemExit(1)
print('Map UX reliability guard: OK; hints=2610')
