import React from 'react'
const items = [['map','Mapa','⌖'],['zones','Zonas','▤'],['report','Reportar','+'],['filters','Filtros','◫']]
export default function MobileMapNavigation({ active, onMap, onZones, onReport, onFilters }) {
  const actions = { map:onMap, zones:onZones, report:onReport, filters:onFilters }
  return <nav className="mobile-map-nav" aria-label="Navegación principal" aria-label="Navegación principal">{items.map(([id,label,icon]) => <button key={id} type="button" className={active===id?'active':''} aria-current={active===id?'page':undefined} aria-label={label} onClick={actions[id]}><span className="mobile-map-nav-icon" aria-hidden="true">{icon}</span><span>{label}</span></button>)}</nav>
}
