import React, { useEffect, useMemo, useState } from 'react'
import { MapContainer, Rectangle, TileLayer, useMapEvents } from 'react-leaflet'

const APP_VERSION = 'v0.7.0-zones-wip'
const GRID_SIZE_M = 1600
const EARTH_R = 6378137
const DEFAULT_CENTER = [42.67, -8.71]
const DEFAULT_ZOOM = 9

function normalizeText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}

function fallbackUuid() {
  const bytes = new Uint8Array(16)
  if (typeof globalThis !== 'undefined' && globalThis.crypto && globalThis.crypto.getRandomValues) {
    globalThis.crypto.getRandomValues(bytes)
  } else {
    for (let i = 0; i < bytes.length; i += 1) bytes[i] = Math.floor(Math.random() * 256)
  }
  bytes[6] = (bytes[6] & 0x0f) | 0x40
  bytes[8] = (bytes[8] & 0x3f) | 0x80
  const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('')
  return [hex.slice(0, 8), hex.slice(8, 12), hex.slice(12, 16), hex.slice(16, 20), hex.slice(20, 32)].join('-')
}

function getToken() {
  const key = 'apagones_token'
  let token = localStorage.getItem(key)
  if (!token) {
    token =
      typeof globalThis !== 'undefined' &&
      globalThis.crypto &&
      typeof globalThis.crypto.randomUUID === 'function'
        ? globalThis.crypto.randomUUID()
        : fallbackUuid()
    localStorage.setItem(key, token)
  }
  return token
}

function typeLabel(type) {
  return {
    sin_luz: 'Sin luz',
    microcortes: 'Microcortes',
    baja_tension: 'Baja tensión',
    vuelve: 'Ya volvió',
  }[type] || type
}

function statusLabel(status) {
  return {
    senal_debil: 'Débil',
    probable: 'Probable',
    activa: 'Activa',
    degradandose: 'Degradándose',
    probablemente_resuelta: 'Casi resuelta',
    resuelta: 'Resuelta',
  }[status] || status
}

function statusColor(status) {
  return {
    senal_debil: '#D4A938',
    probable: '#F58A4B',
    activa: '#EB6343',
    degradandose: '#8D73F6',
    probablemente_resuelta: '#6CCB83',
    resuelta: '#7A879B',
  }[status] || '#4F8CFF'
}

function reportWord(n) {
  return Number(n) === 1 ? 'confirmación' : 'confirmaciones'
}

function formatTimeAgo(isoValue) {
  if (!isoValue) return 'sin datos'
  const then = new Date(isoValue)
  const now = new Date()
  const diff = Math.max(1, Math.floor((now - then) / 1000))
  if (diff < 60) return `Hace ${diff}s`
  if (diff < 3600) return `Hace ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} h`
  return `Hace ${Math.floor(diff / 86400)} d`
}

function latlngToMercator(lat, lng) {
  const x = EARTH_R * (lng * Math.PI / 180)
  const clampedLat = Math.max(Math.min(lat, 85.05112878), -85.05112878)
  const y = EARTH_R * Math.log(Math.tan(Math.PI / 4 + (clampedLat * Math.PI / 180) / 2))
  return [x, y]
}

function mercatorToLatlng(x, y) {
  const lng = (x / EARTH_R) * 180 / Math.PI
  const lat = (2 * Math.atan(Math.exp(y / EARTH_R)) - Math.PI / 2) * 180 / Math.PI
  return [lat, lng]
}

function gridBoundsForPoint(lat, lng, sizeM = GRID_SIZE_M) {
  const [x, y] = latlngToMercator(lat, lng)
  const ix = Math.floor(x / sizeM)
  const iy = Math.floor(y / sizeM)

  const minX = ix * sizeM
  const maxX = (ix + 1) * sizeM
  const minY = iy * sizeM
  const maxY = (iy + 1) * sizeM

  const [latA, lngA] = mercatorToLatlng(minX, minY)
  const [latB, lngB] = mercatorToLatlng(maxX, maxY)

  return [
    [Math.min(latA, latB), Math.min(lngA, lngB)],
    [Math.max(latA, latB), Math.max(lngA, lngB)],
  ]
}

function zoneCenterText(point) {
  if (!point) return ''
  return `${point[0].toFixed(4)}, ${point[1].toFixed(4)}`
}

function incidentBounds(incident) {
  return [
    [incident.lat_min, incident.lng_min],
    [incident.lat_max, incident.lng_max],
  ]
}

function zoneTitle(incident) {
  return incident.display_zone || incident.municipio || 'Zona comunitaria agrupada'
}

function distributorHint(incident) {
  const province = normalizeText(incident.province)
  const municipio = normalizeText(incident.municipio)

  if (province.includes('a coruna') || province.includes('coruna') || province.includes('pontevedra')) {
    return { name: 'UFD (probable)' }
  }
  if (province.includes('lugo')) {
    return { name: 'Begasa / i-DE' }
  }
  if (province.includes('ourense') || province.includes('orense')) {
    return { name: 'UFD / i-DE' }
  }
  if (municipio) {
    return { name: 'Consultar distribuidora de la zona' }
  }
  return { name: 'Sin determinar' }
}

function MapClickSelector({ mode, onPick }) {
  useMapEvents({
    click(e) {
      if (mode === 'report') onPick([e.latlng.lat, e.latlng.lng])
    },
  })
  return null
}

export default function App() {
  const [hours, setHours] = useState(24)
  const [incidents, setIncidents] = useState([])
  const [mode, setMode] = useState('explore')
  const [leftTab, setLeftTab] = useState('incidents')
  const [reportType, setReportType] = useState('sin_luz')
  const [reportPoint, setReportPoint] = useState(null)
  const [selectedIncidentId, setSelectedIncidentId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [query, setQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [mapInstance, setMapInstance] = useState(null)

  async function loadIncidents() {
    const includeResolved = statusFilter === 'resuelta' ? 1 : 0
    const res = await fetch(`/api/zones?hours=${hours}&include_resolved=${includeResolved}`)
    const data = await res.json()
    setIncidents(Array.isArray(data.items) ? data.items : [])
  }

  useEffect(() => {
    loadIncidents()
    const id = setInterval(loadIncidents, 30000)
    return () => clearInterval(id)
  }, [hours, statusFilter])

  const filteredIncidents = useMemo(() => {
    let rows = [...incidents]

    if (statusFilter !== 'all') {
      rows = rows.filter((i) => i.status === statusFilter)
    }

    if (query.trim()) {
      const q = normalizeText(query)
      rows = rows.filter((i) => {
        const text = normalizeText([
          typeLabel(i.primary_type),
          statusLabel(i.status),
          i.display_zone,
          i.municipio,
          i.province
        ].join(' '))
        return text.includes(q)
      })
    }

    rows.sort((a, b) => {
      const ra = Number(a.report_count_active || 0)
      const rb = Number(b.report_count_active || 0)
      if (rb !== ra) return rb - ra
      return new Date(b.last_report_at) - new Date(a.last_report_at)
    })

    return rows
  }, [incidents, statusFilter, query])

  const activeVisible = useMemo(
    () => filteredIncidents.filter((i) => Number(i.report_count_active || 0) > 0),
    [filteredIncidents]
  )

  const selectedIncident = useMemo(
    () => filteredIncidents.find((i) => i.id === selectedIncidentId) || null,
    [filteredIncidents, selectedIncidentId]
  )

  const reportBounds = useMemo(() => {
    if (!reportPoint) return null
    return gridBoundsForPoint(reportPoint[0], reportPoint[1])
  }, [reportPoint])

  const stats = useMemo(() => {
    return activeVisible.reduce(
      (acc, item) => {
        acc.incidents += 1
        acc.reports += Number(item.report_count_active || 0)
        return acc
      },
      { incidents: 0, reports: 0 }
    )
  }, [activeVisible])

  function focusIncident(incident) {
    setSelectedIncidentId(incident.id)
    setMode('explore')
    setReportPoint(null)
    setMessage('')
    if (mapInstance) {
      mapInstance.fitBounds(incidentBounds(incident), {
        padding: [56, 56],
        maxZoom: 13,
      })
    }
  }

  async function sendReport(pointOverride = null, typeOverride = null) {
    const point = pointOverride || reportPoint
    const type = typeOverride || reportType

    if (!point) {
      setMessage('Selecciona una zona del mapa.')
      return
    }

    setLoading(true)
    setMessage('')

    try {
      const res = await fetch('/api/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lat: point[0],
          lng: point[1],
          type,
          token: getToken(),
        }),
      })

      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'No se pudo enviar el reporte')

      if (type === 'vuelve' && Number(data.incident.report_count_active || 0) === 0) {
        setMessage('Zona marcada como resuelta.')
        setSelectedIncidentId(null)
      } else {
        const actionMessage = {
          created_new_zone: 'Nueva incidencia enviada.',
          confirmed_existing_zone: 'Confirmación añadida.',
          updated_own_report: 'Reporte actualizado.',
          moved_to_new_zone: 'Tu reporte se movió a la nueva zona.',
          created: 'Reporte enviado.',
          updated: 'Reporte actualizado.',
        }[data.action] || 'Reporte enviado.'

        setMessage(actionMessage)
        setSelectedIncidentId(data.incident_id)
      }

      setReportPoint([data.incident.center_lat, data.incident.center_lng])
      setMode('explore')
      await loadIncidents()
    } catch (err) {
      setMessage(err.message || 'Error enviando el reporte')
    } finally {
      setLoading(false)
    }
  }

  function enterExplore() {
    setMode('explore')
    setReportPoint(null)
  }

  function enterReport() {
    setMode('report')
    setSelectedIncidentId(null)
    setMessage('')
  }

  const selectedDistributor = selectedIncident ? distributorHint(selectedIncident) : null

  return (
    <div className="app">
      <header className="topbar glass">
        <div className="brand-block">
          <div className="brand-logo">⚡</div>
          <div>
            <div className="brand-title">Apagones Ciudadanos</div>
            <div className="brand-subtitle">Mapa ciudadano de zonas con incidencias eléctricas</div>
          </div>
        </div>

        <div className="search-box glass-soft">
          <span className="search-icon">⌕</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar municipio o incidencia..."
          />
        </div>

        <div className="top-controls">
          <div className="mode-switch glass-soft">
            <button className={mode === 'explore' ? 'mode-btn active' : 'mode-btn'} onClick={enterExplore}>
              Explorar
            </button>
            <button className={mode === 'report' ? 'mode-btn active' : 'mode-btn'} onClick={enterReport}>
              Reportar
            </button>
          </div>
        </div>
      </header>

      <aside className="left-panel glass">
        <div className="left-tabs">
          <button className={leftTab === 'incidents' ? 'tab-btn active' : 'tab-btn'} onClick={() => setLeftTab('incidents')}>
            Zonas
          </button>
          <button className={leftTab === 'filters' ? 'tab-btn active' : 'tab-btn'} onClick={() => setLeftTab('filters')}>
            Filtros
          </button>
        </div>

        {leftTab === 'incidents' ? (
          <>
            <div className="summary-grid two">
              <div className="summary-card">
                <strong>{stats.incidents}</strong>
                <span>Activas</span>
              </div>
              <div className="summary-card">
                <strong>{stats.reports}</strong>
                <span>Confirmaciones</span>
              </div>
            </div>

            <div className="incident-list">
              {activeVisible.length === 0 ? (
                <div className="empty-state">
                  <strong>Sin zonas activas</strong>
                  <span>Prueba otra ventana temporal o cambia el filtro.</span>
                </div>
              ) : (
                activeVisible.map((incident) => {
                  const selected = selectedIncidentId === incident.id
                  return (
                    <button
                      key={incident.id}
                      className={`incident-item ${selected ? 'selected' : ''}`}
                      onClick={() => focusIncident(incident)}
                    >
                      <div className="incident-item-top">
                        <span className="status-pill" style={{ background: statusColor(incident.status) }}>
                          {statusLabel(incident.status)}
                        </span>
                      </div>

                      <div className="incident-item-title">{zoneTitle(incident)}</div>
                      <div className="incident-item-sub">{typeLabel(incident.primary_type)}</div>

                      <div className="incident-item-meta">
                        <span>{incident.report_count_active} {reportWord(incident.report_count_active)}</span>
                        <span>{formatTimeAgo(incident.last_report_at)}</span>
                      </div>
                    </button>
                  )
                })
              )}
            </div>
          </>
        ) : (
          <div className="filters-wrap">
            <div className="filter-group">
              <label>Ventana temporal</label>
              <div className="chip-row">
                {[2, 6, 24].map((h) => (
                  <button key={h} className={`chip ${hours === h ? 'active' : ''}`} onClick={() => setHours(h)}>
                    {h}h
                  </button>
                ))}
              </div>
            </div>

            <div className="filter-group">
              <label>Estado</label>
              <div className="chip-row">
                {['all', 'activa', 'probable', 'senal_debil', 'probablemente_resuelta', 'resuelta'].map((s) => (
                  <button key={s} className={`chip ${statusFilter === s ? 'active' : ''}`} onClick={() => setStatusFilter(s)}>
                    {s === 'all' ? 'Todas activas' : statusLabel(s)}
                  </button>
                ))}
              </div>
            </div>

            <div className="filter-group">
              <label>Tipo al reportar</label>
              <div className="chip-row">
                {['sin_luz', 'microcortes', 'baja_tension', 'vuelve'].map((t) => (
                  <button key={t} className={`chip ${reportType === t ? 'active' : ''}`} onClick={() => setReportType(t)}>
                    {typeLabel(t)}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="left-footer">
          <a href="/privacy.html" target="_blank" rel="noreferrer">Privacidad</a>
          <a href="/legal.html" target="_blank" rel="noreferrer">Aviso legal</a>
          <a href="/cookies.html" target="_blank" rel="noreferrer">Cookies</a>
          <a href="/changelog.html" target="_blank" rel="noreferrer">{APP_VERSION}</a>
        </div>
      </aside>

      <main className="map-stage">
        <MapContainer
          center={DEFAULT_CENTER}
          zoom={DEFAULT_ZOOM}
          minZoom={6}
          zoomControl={false}
          className="map"
          whenCreated={setMapInstance}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapClickSelector
            mode={mode}
            onPick={(point) => {
              setSelectedIncidentId(null)
              setReportPoint(point)
              setMessage('')
            }}
          />

          {filteredIncidents.map((incident) => {
            const selected = selectedIncidentId === incident.id
            return (
              <Rectangle
                key={incident.id}
                bounds={incidentBounds(incident)}
                pathOptions={{
                  color: statusColor(incident.status),
                  fillColor: statusColor(incident.status),
                  fillOpacity: selected ? 0.24 : 0.12,
                  weight: selected ? 3 : 2,
                }}
                eventHandlers={{
                  click: () => {
                    if (mode === 'explore') focusIncident(incident)
                  },
                }}
              />
            )
          })}

          {mode === 'report' && reportBounds && (
            <Rectangle
              bounds={reportBounds}
              pathOptions={{
                color: '#4F8CFF',
                fillColor: '#4F8CFF',
                fillOpacity: 0.13,
                weight: 2.5,
                dashArray: '6 6',
              }}
            />
          )}
        </MapContainer>

        {mode === 'report' ? (
          <section className="right-panel glass">
            <div className="panel-head">
              <span className="panel-chip blue">Reportar</span>
            </div>

            <h3>{reportPoint ? 'Zona seleccionada' : 'Selecciona una zona'}</h3>
            <div className="panel-subtitle">
              {reportPoint
                ? `Centro aprox.: ${zoneCenterText(reportPoint)}`
                : 'Pulsa en el mapa para seleccionar la zona'}
            </div>

            <div className="simple-grid">
              {['sin_luz', 'microcortes', 'baja_tension', 'vuelve'].map((t) => (
                <button
                  key={t}
                  className={`type-btn ${reportType === t ? 'active' : ''}`}
                  onClick={() => setReportType(t)}
                >
                  {typeLabel(t)}
                </button>
              ))}
            </div>

            <div className="action-row">
              <button className="btn-secondary" onClick={enterExplore}>Cancelar</button>
              <button className="btn-primary" onClick={() => sendReport()} disabled={loading || !reportPoint}>
                {loading ? 'Enviando...' : 'Confirmar'}
              </button>
            </div>

            {message ? <div className="inline-msg">{message}</div> : null}
          </section>
        ) : selectedIncident ? (
          <section className="right-panel glass">
            <div className="panel-head">
              <span className="panel-chip" style={{ background: statusColor(selectedIncident.status) }}>
                {statusLabel(selectedIncident.status)}
              </span>
            </div>

            <h3>{typeLabel(selectedIncident.primary_type)}</h3>
            <div className="panel-subtitle">{zoneTitle(selectedIncident)}</div>

            <div className="info-list">
              <div className="info-row">
                <span>Concello / municipio</span>
                <strong>{selectedIncident.municipio || 'sin resolver todavía'}</strong>
              </div>
              <div className="info-row">
                <span>Provincia</span>
                <strong>{selectedIncident.province || 'sin resolver todavía'}</strong>
              </div>
              <div className="info-row">
                <span>Distribuidora probable</span>
                <strong>{selectedDistributor?.name || 'Sin determinar'}</strong>
              </div>
            </div>

            <div className="stats-strip two">
              <div>
                <span>Confirmaciones</span>
                <strong>{selectedIncident.report_count_active}</strong>
              </div>
              <div>
                <span>Actualización</span>
                <strong>{formatTimeAgo(selectedIncident.last_report_at)}</strong>
              </div>
            </div>

            <div className="action-row">
              <button
                className="btn-primary"
                onClick={() => {
                  setMode('report')
                  setReportType('sin_luz')
                  setReportPoint([selectedIncident.center_lat, selectedIncident.center_lng])
                  setSelectedIncidentId(null)
                }}
              >
                Yo también
              </button>
              <button
                className="btn-green"
                onClick={() => sendReport([selectedIncident.center_lat, selectedIncident.center_lng], 'vuelve')}
              >
                Ya volvió
              </button>
            </div>

            {message ? <div className="inline-msg">{message}</div> : null}
          </section>
        ) : (
          <section className="right-panel glass empty">
            <div className="panel-head">
              <span className="panel-chip blue">{mode === 'explore' ? 'Explorar' : 'Reportar'}</span>
            </div>
            <h3>{mode === 'explore' ? 'Selecciona una zona' : 'Selecciona una zona'}</h3>
            <div className="panel-subtitle">
              {mode === 'explore'
                ? 'Usa la lista lateral o pulsa una zona activa.'
                : 'Pulsa una zona del mapa para reportar.'}
            </div>
            {message ? <div className="inline-msg">{message}</div> : null}
          </section>
        )}
      </main>
    </div>
  )
}
