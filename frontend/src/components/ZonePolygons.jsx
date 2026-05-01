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

function incidentSelectionKeys(incident) {
  return [incident?.zone_id, incident?.id, incident?.incident_id].filter(Boolean).map(String)
}

function incidentMatchesSelected(incident, selectedKey) {
  if (!incident || !selectedKey) return false
  return incidentSelectionKeys(incident).includes(String(selectedKey))
}

function featureStableKey(feature) {
  const props = feature?.properties || {}
  const datasetKey = normalizeText(props.dataset_id) || 'default'
  const localKey = props.zone_id || featureFallbackKey(props)
  return `${datasetKey}::${localKey}`
}

function featureMatchesIncident(feature, incident) {
  const props = feature?.properties || {}

  const featureMunicipio = normalizeText(props.municipio)
  const featureProvince = normalizeText(props.province)
  const incidentMunicipio = normalizeText(incident?.municipio)
  const incidentProvince = normalizeText(incident?.province)

  if (!featureMunicipio || !featureProvince || !incidentMunicipio || !incidentProvince) {
    return false
  }

  return featureMunicipio === incidentMunicipio && featureProvince === incidentProvince
}

function shouldReplaceIncident(current, candidate, selectedIncidentId) {
  if (!current) return true

  const currentSelected = incidentMatchesSelected(current, selectedIncidentId)
  const candidateSelected = incidentMatchesSelected(candidate, selectedIncidentId)

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

function selectFeatureForIncident(incident, byZoneId, byMunicipioProvince) {
  const zoneCandidates = incident?.zone_id
    ? byZoneId.get(String(incident.zone_id)) || []
    : []

  const exactZoneMatch = zoneCandidates.find((feature) =>
    featureMatchesIncident(feature, incident)
  )
  if (exactZoneMatch) return exactZoneMatch

  const fallbackKey = incidentFallbackKey(incident)
  if (fallbackKey !== '|' && byMunicipioProvince.has(fallbackKey)) {
    return byMunicipioProvince.get(fallbackKey)
  }

  if (zoneCandidates.length === 1) {
    return zoneCandidates[0]
  }

  return null
}

export default function ZonePolygons({
  municipiosGeoJson,
  activeVisible,
  selectedIncidentId,
  mode,
  focusIncident,
  statusColor,
  geoDatasetId,
}) {
  const { activeMunicipioGeoJson, incidentByFeatureKey, matchedIncidentIds, geoJsonRenderKey } = useMemo(() => {
    if (!municipiosGeoJson?.features?.length) {
      return {
        activeMunicipioGeoJson: null,
        incidentByFeatureKey: new Map(),
        matchedIncidentIds: new Set(),
        geoJsonRenderKey: `${geoDatasetId || 'unknown'}::none::${mode || 'explore'}::${selectedIncidentId || 'none'}`,
      }
    }

    const byZoneId = new Map()
    const byMunicipioProvince = new Map()

    for (const feature of municipiosGeoJson.features) {
      const props = feature?.properties || {}

      if (props.zone_id) {
        const zoneKey = String(props.zone_id)
        const list = byZoneId.get(zoneKey) || []
        list.push(feature)
        byZoneId.set(zoneKey, list)
      }

      const fallbackKey = featureFallbackKey(props)
      if (fallbackKey !== '|' && !byMunicipioProvince.has(fallbackKey)) {
        byMunicipioProvince.set(fallbackKey, feature)
      }
    }

    const resolvedFeatures = []
    const seenFeatureKeys = new Set()
    const incidentByFeatureKey = new Map()
    const matchedIncidentIds = new Set()

    for (const incident of activeVisible) {
      const feature = selectFeatureForIncident(incident, byZoneId, byMunicipioProvince)
      if (!feature) continue

      incidentSelectionKeys(incident).forEach((key) => matchedIncidentIds.add(key))

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
      geoJsonRenderKey: `${geoDatasetId || 'unknown'}::${stableKeys}::${mode || 'explore'}::${selectedIncidentId || 'none'}`,
    }
  }, [municipiosGeoJson, activeVisible, selectedIncidentId, mode, geoDatasetId])

  const fallbackRectangles = useMemo(
    () => activeVisible.filter((incident) => !incidentSelectionKeys(incident).some((key) => matchedIncidentIds.has(key))),
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

    return pathOptionsForIncident(incident, incidentMatchesSelected(incident, selectedIncidentId), statusColor)
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

            if (incidentMatchesSelected(incident, selectedIncidentId) && typeof layer.bringToFront === 'function') {
              layer.bringToFront()
            }

            layer.on({
              click: (event) => { if (event?.originalEvent?.stopPropagation) event.originalEvent.stopPropagation(); focusIncident(incident) },
            })
          }}
        />
      ) : null}

      {fallbackRectangles.map((incident) => {
        const selected = incidentMatchesSelected(incident, selectedIncidentId)

        return (
          <Rectangle
            key={incident.id}
            bounds={incidentBounds(incident)}
            pathOptions={pathOptionsForIncident(incident, selected, statusColor)}
            eventHandlers={{
              click: (event) => { if (event?.originalEvent?.stopPropagation) event.originalEvent.stopPropagation(); focusIncident(incident) },
            }}
          />
        )
      })}
    </>
  )
}
