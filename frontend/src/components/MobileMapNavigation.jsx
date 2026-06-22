import React from 'react'

const NAV_ITEMS = [
  { id: 'map',     label: 'Mapa',     icon: '🗺️' },
  { id: 'zones',   label: 'Zonas',    icon: '📋' },
  { id: 'report',  label: 'Reportar', icon: '⚡' },
  { id: 'filters', label: 'Filtros',  icon: '⚙️' },
  { id: 'info',    label: 'Info',     icon: 'ℹ️' },
]

export default function MobileMapNavigation({ active, onMap, onZones, onReport, onFilters, onInfo }) {
  const handlers = {
    map:     onMap,
    zones:   onZones,
    report:  onReport,
    filters: onFilters,
    info:    onInfo,
  }

  return (
    <nav className="mobile-map-nav" aria-label="Navegación principal">
      {NAV_ITEMS.map(({ id, label, icon }) => (
        <button
          key={id}
          type="button"
          className={active === id ? 'active' : ''}
          aria-current={active === id ? 'page' : undefined}
          aria-label={label}
          onClick={handlers[id]}
        >
          <span className="mobile-map-nav-icon" aria-hidden="true">{icon}</span>
          <span>{label}</span>
        </button>
      ))}
    </nav>
  )
}
