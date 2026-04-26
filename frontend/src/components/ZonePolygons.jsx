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

function featureStableKey(feature) {
  const props = feature?.properties || {}
  return props.zone_id || featureFallbackKey(props)
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

function pathOptionsForIncident(incident, selected, statusColor) {
  const baseColor = statusColor(incident.status)

  if (selected) {
    return {
      color: '#0f172a',
      fillColor: baseColor,
      fillOpacity: 0.32,
      weight: 4,
      opacity: 1,
      dashArray: '10 6',
    }
  }

  return {
    color: baseColor,
    fillColor: baseColor,
    fillOpacity: 0.14,
    weight: 2,
    opacity: 0.92,
  }
}

export default function ZonePolygons({
  municipiosGeoJson,
  activeVisible,
  selectedIncidentId,
  mode,
  focusIncident,
  statusColor,
}) {
  const { activeMunicipioGeoJson, incidentByFeatureKey, matchedIncidentIds, geoJsonRenderKey } = useMemo(() => {
    if (!municipiosGeoJson?.features?.length) {
      return {
        activeMunicipioGeoJson: null,
        incidentByFeatureKey: new Map(),
        matchedIncidentIds: new Set(),
        geoJsonRenderKey: `none::${mode || 'explore'}::${selectedIncidentId || 'none'}`,
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

      const featureKey = featureStableKey(feature)
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

    const stableKeys = resolvedFeatures.map(featureStableKey).sort().join(',')

    return {
      activeMunicipioGeoJson: resolvedFeatures.length
        ? { ...municipiosGeoJson, features: resolvedFeatures }
        : null,
      incidentByFeatureKey,
      matchedIncidentIds,
      geoJsonRenderKey: `${stableKeys}::${mode || 'explore'}::${selectedIncidentId || 'none'}`,
    }
  }, [municipiosGeoJson, activeVisible, selectedIncidentId, mode])

  const fallbackRectangles = useMemo(
    () => activeVisible.filter((incident) => !matchedIncidentIds.has(incident.id)),
    [activeVisible, matchedIncidentIds]
  )

  function getIncidentForFeature(feature) {
    return incidentByFeatureKey.get(featureStableKey(feature)) || null
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

    return pathOptionsForIncident(incident, selectedIncidentId === incident.id, statusColor)
  }

  return (
    <>
      {activeMunicipioGeoJson?.features?.length ? (
        <GeoJSON
          key={geoJsonRenderKey}
          data={activeMunicipioGeoJson}
          style={polygonStyle}
          onEachFeature={(feature, layer) => {
            const incident = getIncidentForFeature(feature)
            if (!incident) return

            if (selectedIncidentId === incident.id && typeof layer.bringToFront === 'function') {
              layer.bringToFront()
            }

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
            pathOptions={pathOptionsForIncident(incident, selected, statusColor)}
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
