import React, { useMemo } from 'react'
import { GeoJSON, Rectangle } from 'react-leaflet'

function incidentBounds(incident) {
  return [
    [incident.lat_min, incident.lng_min],
    [incident.lat_max, incident.lng_max],
  ]
}

function normalizeText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}

function featureFallbackKey(props) {
  return `${normalizeText(props?.municipio)}|${normalizeText(props?.province)}`
}

function incidentFallbackKey(incident) {
  return `${normalizeText(incident?.municipio)}|${normalizeText(incident?.province)}`
}

function shouldReplaceIncident(current, candidate, selectedIncidentId) {
  if (!current) return true

  const currentSelected = current.id === selectedIncidentId
  const candidateSelected = candidate.id === selectedIncidentId

  if (candidateSelected && !currentSelected) return true
  if (currentSelected && !candidateSelected) return false

  const currentReports = Number(current.report_count_active || 0)
  const candidateReports = Number(candidate.report_count_active || 0)

  if (candidateReports !== currentReports) {
    return candidateReports > currentReports
  }

  const currentTs = new Date(current.last_report_at || 0).getTime()
  const candidateTs = new Date(candidate.last_report_at || 0).getTime()

  return candidateTs > currentTs
}

export default function ZonePolygons({
  municipiosGeoJson,
  activeVisible,
  selectedIncidentId,
  mode,
  focusIncident,
  statusColor,
}) {
  const { activeMunicipioGeoJson, incidentByFeatureKey, matchedIncidentIds } = useMemo(() => {
    if (!municipiosGeoJson?.features?.length) {
      return {
        activeMunicipioGeoJson: null,
        incidentByFeatureKey: new Map(),
        matchedIncidentIds: new Set(),
      }
    }

    const byZoneId = new Map()
    const byMunicipioProvince = new Map()

    for (const feature of municipiosGeoJson.features) {
      const props = feature?.properties || {}

      if (props.zone_id) {
        byZoneId.set(props.zone_id, feature)
      }

      const fallbackKey = featureFallbackKey(props)
      if (fallbackKey !== '|') {
        byMunicipioProvince.set(fallbackKey, feature)
      }
    }

    const resolvedFeatures = []
    const seenFeatureKeys = new Set()
    const incidentByFeatureKey = new Map()
    const matchedIncidentIds = new Set()

    for (const incident of activeVisible) {
      let feature = null

      if (incident.zone_id && byZoneId.has(incident.zone_id)) {
        feature = byZoneId.get(incident.zone_id)
      }

      if (!feature) {
        const fallbackKey = incidentFallbackKey(incident)
        if (fallbackKey !== '|' && byMunicipioProvince.has(fallbackKey)) {
          feature = byMunicipioProvince.get(fallbackKey)
        }
      }

      if (!feature) continue

      matchedIncidentIds.add(incident.id)

      const props = feature?.properties || {}
      const featureKey = props.zone_id || featureFallbackKey(props)
      if (!featureKey) continue

      if (!seenFeatureKeys.has(featureKey)) {
        seenFeatureKeys.add(featureKey)
        resolvedFeatures.push(feature)
      }

      const current = incidentByFeatureKey.get(featureKey)
      if (shouldReplaceIncident(current, incident, selectedIncidentId)) {
        incidentByFeatureKey.set(featureKey, incident)
      }
    }

    return {
      activeMunicipioGeoJson: resolvedFeatures.length
        ? { ...municipiosGeoJson, features: resolvedFeatures }
        : null,
      incidentByFeatureKey,
      matchedIncidentIds,
    }
  }, [municipiosGeoJson, activeVisible, selectedIncidentId])

  const fallbackRectangles = useMemo(
    () => activeVisible.filter((incident) => !matchedIncidentIds.has(incident.id)),
    [activeVisible, matchedIncidentIds]
  )

  function getIncidentForFeature(feature) {
    const props = feature?.properties || {}
    const key = props.zone_id || featureFallbackKey(props)
    return incidentByFeatureKey.get(key) || null
  }

  function polygonStyle(feature) {
    const incident = getIncidentForFeature(feature)

    if (!incident) {
      return {
        color: 'transparent',
        weight: 0,
        fillOpacity: 0,
      }
    }

    const selected = selectedIncidentId === incident.id

    return {
      color: statusColor(incident.status),
      fillColor: statusColor(incident.status),
      fillOpacity: selected ? 0.24 : 0.14,
      weight: selected ? 3 : 2,
    }
  }

  return (
    <>
      {activeMunicipioGeoJson?.features?.length ? (
        <GeoJSON
          data={activeMunicipioGeoJson}
          style={polygonStyle}
          onEachFeature={(feature, layer) => {
            const incident = getIncidentForFeature(feature)
            if (!incident) return

            layer.on({
              click: () => {
                if (mode === 'explore') focusIncident(incident)
              },
            })
          }}
        />
      ) : null}

      {fallbackRectangles.map((incident) => {
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
    </>
  )
}
