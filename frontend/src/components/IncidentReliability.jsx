import React from 'react'

function ageHours(value) {
  if (!value) return Number.POSITIVE_INFINITY
  const stamp = new Date(value).getTime()
  return Number.isFinite(stamp) ? Math.max(0, (Date.now() - stamp) / 3600000) : Number.POSITIVE_INFINITY
}

export function incidentReliability(incident) {
  const confirmations = Number(incident?.report_count_active || 0)
  const age = ageHours(incident?.last_report_at)
  const recovering = ['degradandose', 'probablemente_resuelta', 'resuelta'].includes(incident?.status)
  if (incident?.status === 'resuelta') return { label: 'Cerrada', tone: 'recovering', recovering }
  if (recovering) return { label: 'En recuperación', tone: 'recovering', recovering }
  if (confirmations >= 3 && age <= 6) return { label: 'Alta', tone: 'high', recovering }
  if (confirmations >= 2 && age <= 12) return { label: 'Media', tone: 'medium', recovering }
  if (confirmations >= 1 && age <= 24) return { label: 'Limitada', tone: 'limited', recovering }
  return { label: 'Baja', tone: 'low', recovering }
}

export function ReliabilityBadge({ incident, compact = false }) {
  const value = incidentReliability(incident)
  return <span className={`reliability-badge reliability-${value.tone} ${compact ? 'compact' : ''}`} aria-label={`Fiabilidad ciudadana ${value.label}`}><span className="reliability-dot" aria-hidden="true" />{value.label}</span>
}

export default function IncidentReliability({ incident, formatTimeAgo, statusLabel }) {
  const value = incidentReliability(incident)
  return <section className="reliability-card" aria-labelledby="incident-reliability-title"><div className="reliability-heading"><div><span className="eyebrow">Señal ciudadana</span><h4 id="incident-reliability-title">Fiabilidad de la incidencia</h4></div><ReliabilityBadge incident={incident} /></div><div className="reliability-signals"><div><span>Ciclo de vida</span><strong>{statusLabel(incident?.status)}</strong></div><div><span>Confirmaciones activas</span><strong>{Number(incident?.report_count_active || 0)}</strong></div><div><span>Último aviso</span><strong>{formatTimeAgo(incident?.last_report_at)}</strong></div><div><span>Recuperación</span><strong>{value.recovering ? 'Con señales' : 'Sin señales suficientes'}</strong></div></div><p className="reliability-disclaimer">Estimación comunitaria agregada. No es una confirmación oficial ni garantiza que toda la zona esté afectada.</p></section>
}

export function DistributorReliability({ distributor }) {
  const known = Boolean(distributor?.name && distributor.name !== 'Sin determinar')
  return <section className="distributor-reliability" aria-labelledby="distributor-reliability-title"><span className="eyebrow">Pista de distribuidora</span><h4 id="distributor-reliability-title">{known ? distributor.name : 'Consultar distribuidora de la zona'}</h4><p>{known ? 'Pista basada en evidencia pública del dataset. Es independiente de la fiabilidad de la incidencia ciudadana.' : 'No existe una pista pública suficientemente fiable. No se infiere una empresa por presencia regional.'}</p></section>
}
