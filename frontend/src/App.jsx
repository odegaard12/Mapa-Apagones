import React, { useEffect, useMemo, useRef, useState } from 'react'
import { MapContainer, Rectangle, TileLayer, useMapEvents } from 'react-leaflet'
import ZonePolygons from './components/ZonePolygons.jsx'
import {
  DEFAULT_GEO_DATASET_ID,
  GEO_DATASET_LIST,
  getGeoDataset,
  getInitialGeoDatasetId,
  syncGeoDatasetInUrl,
} from './geo/datasets'
import { loadMunicipiosGeoJson } from './geo/loadGeoDataset'
import { incidentBelongsToDataset } from './geo/incidentScope'

const APP_VERSION = 'v0.8.2-feedback-ready-close-fix'
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

function FeedbackOverlay({ open, title, subtitle, steps = [], activeStep = 0, done = false }) {
  if (!open) return null

  return (
    <>
      <style>{`
        @keyframes apagonesOverlayFade {
          from { opacity: 0; transform: translateY(12px) scale(0.98); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes apagonesSpinner {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes apagonesPulse {
          0% { transform: scale(0.9); opacity: 0.65; }
          50% { transform: scale(1.08); opacity: 1; }
          100% { transform: scale(0.9); opacity: 0.65; }
        }
        @keyframes apagonesToastIn {
          from { opacity: 0; transform: translate(-50%, 14px) scale(0.98); }
          to { opacity: 1; transform: translate(-50%, 0) scale(1); }
        }
      `}</style>

      <div
        style={{
          position: 'fixed',
          inset: 0,
          zIndex: 2500,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'rgba(7, 15, 28, 0.34)',
          backdropFilter: 'blur(6px)',
          padding: '20px',
        }}
      >
        <div
          style={{
            width: 'min(580px, calc(100vw - 28px))',
            borderRadius: '24px',
            padding: '22px',
            color: '#fff',
            background: 'linear-gradient(180deg, rgba(25,42,66,0.96), rgba(15,23,42,0.96))',
            boxShadow: '0 28px 80px rgba(0,0,0,0.34)',
            border: '1px solid rgba(255,255,255,0.08)',
            animation: 'apagonesOverlayFade 220ms ease-out',
          }}
        >
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <div
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '999px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: done ? 'none' : '4px solid rgba(255,255,255,0.14)',
                borderTopColor: done ? 'transparent' : '#60A5FA',
                background: done ? 'linear-gradient(180deg, #22C55E, #16A34A)' : 'transparent',
                animation: done ? 'none' : 'apagonesSpinner 1s linear infinite',
                boxShadow: done ? '0 12px 28px rgba(34,197,94,0.28)' : 'none',
                color: '#fff',
                fontSize: '26px',
                fontWeight: 800,
                flexShrink: 0,
              }}
            >
              {done ? '✓' : ''}
            </div>
            <div>
              <div style={{ fontSize: '29px', fontWeight: 800, lineHeight: 1.05 }}>{title}</div>
              <div style={{ marginTop: '7px', fontSize: '14px', lineHeight: 1.45, opacity: 0.88 }}>
                {subtitle}
              </div>
            </div>
          </div>

          {steps.length ? (
            <div style={{ marginTop: '18px', display: 'grid', gap: '10px' }}>
              {steps.map((step, idx) => {
                const done = idx < activeStep
                const active = idx === activeStep

                return (
                  <div
                    key={step}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '11px 13px',
                      borderRadius: '15px',
                      border: active
                        ? '1px solid rgba(96,165,250,0.38)'
                        : '1px solid rgba(255,255,255,0.07)',
                      background: active
                        ? 'rgba(96,165,250,0.14)'
                        : 'rgba(255,255,255,0.05)',
                      transition: 'all 180ms ease',
                    }}
                  >
                    <div
                      style={{
                        width: '26px',
                        height: '26px',
                        borderRadius: '999px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 800,
                        fontSize: '13px',
                        color: done || active ? '#fff' : 'rgba(255,255,255,0.78)',
                        background: done
                          ? 'linear-gradient(180deg, #22C55E, #16A34A)'
                          : active
                            ? 'linear-gradient(180deg, #60A5FA, #2563EB)'
                            : 'rgba(255,255,255,0.08)',
                        animation: active ? 'apagonesPulse 1.2s ease-in-out infinite' : 'none',
                        flexShrink: 0,
                      }}
                    >
                      {done ? '✓' : idx + 1}
                    </div>
                    <div style={{ fontSize: '14px', fontWeight: active ? 800 : 600, opacity: active ? 1 : 0.88 }}>
                      {step}
                    </div>
                  </div>
                )
              })}
            </div>
          ) : null}

          <div style={{ marginTop: '15px', fontSize: '13px', opacity: 0.76 }}>
            {done ? 'Listo. Cerrando aviso…' : 'No recargues la página ni cambies de ámbito hasta que desaparezca este aviso.'}
          </div>
        </div>
      </div>
    </>
  )
}

function FloatingToast({ message, tone = 'success' }) {
  if (!message) return null

  const isError = tone === 'error'
  const icon = isError ? '⚠️' : '✅'

  return (
    <>
      <style>{`
        @keyframes apagonesToastIn {
          from { opacity: 0; transform: translate(-50%, 16px) scale(0.98); }
          to { opacity: 1; transform: translate(-50%, 0) scale(1); }
        }
      `}</style>

      <div
        style={{
          position: 'fixed',
          left: '50%',
          bottom: '24px',
          transform: 'translateX(-50%)',
          zIndex: 2600,
          minWidth: 'min(520px, calc(100vw - 28px))',
          maxWidth: 'min(620px, calc(100vw - 28px))',
          padding: '14px 18px',
          borderRadius: '16px',
          color: '#fff',
          background: isError
            ? 'linear-gradient(180deg, rgba(127,29,29,0.96), rgba(69,10,10,0.96))'
            : 'linear-gradient(180deg, rgba(17,94,89,0.96), rgba(15,23,42,0.96))',
          border: isError
            ? '1px solid rgba(248,113,113,0.34)'
            : '1px solid rgba(74,222,128,0.24)',
          boxShadow: '0 20px 48px rgba(0,0,0,0.28)',
          fontSize: '14px',
          fontWeight: 700,
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          animation: 'apagonesToastIn 220ms ease-out',
          pointerEvents: 'none',
        }}
      >
        <span>{icon}</span>
        <span>{message}</span>
      </div>
    </>
  )
}

export default function App() {
  const [hours, setHours] = useState(24)
  const [incidents, setIncidents] = useState([])
  const [municipiosGeoJson, setMunicipiosGeoJson] = useState(null)
  const [geoLoading, setGeoLoading] = useState(false)
  const [geoDatasetId, setGeoDatasetId] = useState(() => getInitialGeoDatasetId())
  const currentGeoDataset = useMemo(() => getGeoDataset(geoDatasetId), [geoDatasetId])
  const incidentsLoadSeqRef = useRef(0)
  const [mode, setMode] = useState('explore')
  const [leftTab, setLeftTab] = useState('incidents')
  const [reportType, setReportType] = useState('sin_luz')
  const [reportPoint, setReportPoint] = useState(null)
  const [selectedIncidentId, setSelectedIncidentId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [toastMessage, setToastMessage] = useState('')
  const [feedbackStage, setFeedbackStage] = useState(null)
  const [query, setQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [mapInstance, setMapInstance] = useState(null)

  async function loadIncidents() {
    const seq = ++incidentsLoadSeqRef.current
    const includeResolved = statusFilter === 'resuelta' ? 1 : 0
    const res = await fetch(`/api/zones?hours=${hours}&include_resolved=${includeResolved}`)
    const data = await res.json()
    if (seq !== incidentsLoadSeqRef.current) return
    setIncidents(Array.isArray(data.items) ? data.items : [])
  }

  useEffect(() => {
    let cancelled = false

    setGeoLoading(true)
    setMunicipiosGeoJson(null)

    loadMunicipiosGeoJson(geoDatasetId)
      .then(({ data }) => {
        if (!cancelled) setMunicipiosGeoJson(data)
      })
      .catch((err) => {
        console.error(`No se pudo cargar el dataset geográfico ${geoDatasetId}`, err)
        if (!cancelled) setMunicipiosGeoJson(null)
      })
      .finally(() => {
        if (!cancelled) setGeoLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [geoDatasetId])

  useEffect(() => {
    setSelectedIncidentId(null)
    setReportPoint(null)
    setMessage('')
    setMode('explore')
    setLeftTab('incidents')

    if (!mapInstance) return

    if (currentGeoDataset?.maxBounds) {
      mapInstance.fitBounds(currentGeoDataset.maxBounds, { padding: [24, 24] })
      return
    }

    if (currentGeoDataset?.defaultCenter && Number.isFinite(currentGeoDataset?.defaultZoom)) {
      mapInstance.setView(currentGeoDataset.defaultCenter, currentGeoDataset.defaultZoom)
    }
  }, [geoDatasetId, currentGeoDataset, mapInstance])

  useEffect(() => {
    loadIncidents()
    const id = setInterval(loadIncidents, 30000)
    return () => clearInterval(id)
  }, [hours, statusFilter])

  useEffect(() => {
    if (loading || geoLoading || feedbackStage) {
      setToastMessage('')
      return
    }

    if (!message) return

    setToastMessage(message)
    const id = setTimeout(() => setToastMessage(''), 3200)
    return () => clearTimeout(id)
  }, [message, loading, geoLoading, feedbackStage])

  useEffect(() => {
    if (loading) {
      setFeedbackStage('report-loading')
      return
    }

    if (geoLoading) {
      setFeedbackStage('geo-loading')
      return
    }

    setFeedbackStage((current) => {
      if (current === 'report-loading') return 'report-ready'
      if (current === 'geo-loading') return 'geo-ready'
      return current
    })
  }, [loading, geoLoading])

  useEffect(() => {
    if (feedbackStage !== 'report-ready' && feedbackStage !== 'geo-ready') return

    const readyStage = feedbackStage
    const id = setTimeout(() => {
      setFeedbackStage((current) => (current === readyStage ? null : current))
    }, 1000)

    return () => clearTimeout(id)
  }, [feedbackStage])

  const scopedIncidents = useMemo(
    () => incidents.filter((incident) => incidentBelongsToDataset(incident, currentGeoDataset)),
    [incidents, currentGeoDataset]
  )

  const filteredIncidents = useMemo(() => {
    let rows = [...scopedIncidents]

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
  }, [scopedIncidents, statusFilter, query])

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
    setLeftTab('incidents')
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
        setLeftTab('incidents')
      }

      setReportPoint([data.incident.center_lat, data.incident.center_lng])
      setMode('explore')
      setLeftTab('incidents')

      if (
        mapInstance &&
        data.incident &&
        Number.isFinite(Number(data.incident.lat_min)) &&
        Number.isFinite(Number(data.incident.lat_max)) &&
        Number.isFinite(Number(data.incident.lng_min)) &&
        Number.isFinite(Number(data.incident.lng_max))
      ) {
        mapInstance.fitBounds(incidentBounds(data.incident), {
          padding: [56, 56],
          maxZoom: 13,
        })
      } else if (
        mapInstance &&
        data.incident &&
        Number.isFinite(Number(data.incident.center_lat)) &&
        Number.isFinite(Number(data.incident.center_lng))
      ) {
        mapInstance.setView(
          [Number(data.incident.center_lat), Number(data.incident.center_lng)],
          12
        )
      }

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

  const overlayConfig = useMemo(() => {
    const label = currentGeoDataset?.label || 'ámbito seleccionado'

    if (feedbackStage === 'report-loading') {
      return {
        title: 'Reportando incidencia',
        subtitle: 'Estamos guardando el reporte, detectando el ayuntamiento y actualizando el mapa.',
        steps: ['Guardando reporte', 'Detectando ayuntamiento', 'Actualizando mapa'],
        activeStep: 1,
        done: false,
      }
    }

    if (feedbackStage === 'report-ready') {
      return {
        title: 'Listo',
        subtitle: 'Incidencia enviada y mapa actualizado.',
        steps: ['Guardando reporte', 'Detectando ayuntamiento', 'Mapa actualizado'],
        activeStep: 3,
        done: true,
      }
    }

    if (feedbackStage === 'geo-loading') {
      return {
        title: 'Apagones Ciudadanos',
        subtitle: `Preparando mapa y polígonos de ${label}.`,
        steps: ['Cargando datos geográficos', 'Preparando contornos', 'Pintando mapa'],
        activeStep: 2,
        done: false,
      }
    }

    if (feedbackStage === 'geo-ready') {
      return {
        title: 'Listo',
        subtitle: `Mapa de ${label} preparado.`,
        steps: ['Cargando datos geográficos', 'Preparando contornos', 'Mapa listo'],
        activeStep: 3,
        done: true,
      }
    }

    return null
  }, [feedbackStage, currentGeoDataset])

  const toastTone = useMemo(() => {
    return /error|no se pudo|selecciona/i.test(toastMessage) ? 'error' : 'success'
  }, [toastMessage])

  return (
    <div className="app">
      <FeedbackOverlay
        open={Boolean(overlayConfig)}
        title={overlayConfig?.title}
        subtitle={overlayConfig?.subtitle}
        steps={overlayConfig?.steps || []}
        activeStep={overlayConfig?.activeStep || 0}
        done={Boolean(overlayConfig?.done)}
      />
      <FloatingToast message={toastMessage} tone={toastTone} />
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

            <div className="filter-group">
              <label>Ámbito geográfico</label>
              <div className="chip-row">
                {GEO_DATASET_LIST.map((dataset) => (
                  <button
                    key={dataset.id}
                    className={`chip ${geoDatasetId === dataset.id ? 'active' : ''}`}
                    onClick={() => setGeoDatasetId(dataset.id)}
                  >
                    {dataset.label}
                  </button>
                ))}
              </div>
            <div style={{ marginTop: 8, fontSize: 12, opacity: 0.78, lineHeight: 1.4 }}>
              “Toda España” te deja mover el mapa libremente. Seguimos añadiendo más comunidades y provincias con polígonos reales.
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
          key={`map::${geoDatasetId}`}
          center={currentGeoDataset.defaultCenter || DEFAULT_CENTER}
          zoom={currentGeoDataset.defaultZoom ?? DEFAULT_ZOOM}
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

          <ZonePolygons
            municipiosGeoJson={municipiosGeoJson}
            activeVisible={activeVisible}
            selectedIncidentId={selectedIncidentId}
            mode={mode}
            focusIncident={focusIncident}
            statusColor={statusColor}
            geoDatasetId={geoDatasetId}
          />

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
                {loading ? 'Enviando…' : 'Confirmar'}
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
