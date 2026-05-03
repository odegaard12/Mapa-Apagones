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
    .replace(/[^a-z0-9]+/g, ' ')
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
  const featureMunicipio = normalizeText(props.municipio || props.mun_name || props.name)
  const featureProvince = normalizeText(props.province || props.prov_name)
  const incidentMunicipio = normalizeText(incident?.municipio)
  const incidentProvince = normalizeText(incident?.province)

  if (!featureMunicipio || !featureProvince || !incidentMunicipio || !incidentProvince) {
    return false
  }

  return featureMunicipio === incidentMunicipio && featureProvince === incidentProvince
}

function featureProvinceMatchesIncident(feature, incident) {
  const props = feature?.properties || {}
  const featureProvince = normalizeText(props.province || props.prov_name)
  const incidentProvince = normalizeText(incident?.province)

  return Boolean(featureProvince && incidentProvince && featureProvince === incidentProvince)
}

function incidentCenterPoint(incident) {
  const centerLat = Number(incident?.center_lat)
  const centerLng = Number(incident?.center_lng)

  if (Number.isFinite(centerLat) && Number.isFinite(centerLng)) {
    return { lat: centerLat, lng: centerLng }
  }

  const latMin = Number(incident?.lat_min)
  const latMax = Number(incident?.lat_max)
  const lngMin = Number(incident?.lng_min)
  const lngMax = Number(incident?.lng_max)

  if ([latMin, latMax, lngMin, lngMax].every(Number.isFinite)) {
    return {
      lat: (latMin + latMax) / 2,
      lng: (lngMin + lngMax) / 2,
    }
  }

  return null
}

function pointInRing(point, ring) {
  if (!Array.isArray(ring) || ring.length < 4) return false

  let inside = false
  const x = point.lng
  const y = point.lat

  for (let i = 0, j = ring.length - 1; i < ring.length; j = i, i += 1) {
    const xi = Number(ring[i]?.[0])
    const yi = Number(ring[i]?.[1])
    const xj = Number(ring[j]?.[0])
    const yj = Number(ring[j]?.[1])

    if (![xi, yi, xj, yj].every(Number.isFinite)) continue

    const intersects =
      yi > y !== yj > y &&
      x < ((xj - xi) * (y - yi)) / ((yj - yi) || Number.EPSILON) + xi

    if (intersects) inside = !inside
  }

  return inside
}

function pointInPolygon(point, polygonCoordinates) {
  if (!Array.isArray(polygonCoordinates) || !polygonCoordinates.length) return false

  const [outerRing, ...holes] = polygonCoordinates

  if (!pointInRing(point, outerRing)) return false

  return !holes.some((hole) => pointInRing(point, hole))
}

function featureContainsPoint(feature, point) {
  if (!feature || !point) return false

  const geometry = feature.geometry || {}

  if (geometry.type === 'Polygon') {
    return pointInPolygon(point, geometry.coordinates)
  }

  if (geometry.type === 'MultiPolygon') {
    return Array.isArray(geometry.coordinates) &&
      geometry.coordinates.some((polygon) => pointInPolygon(point, polygon))
  }

  return false
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

function selectFeatureForIncident(incident, byZoneId, byMunicipioProvince, features) {
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

  // v0.10.0.5: último recurso robusto.
  // Si nombre/zone_id no coinciden por variantes oficiales, bilingües o normalizaciones,
  // usamos el punto central de la incidencia y buscamos el polígono municipal que lo contiene.
  const point = incidentCenterPoint(incident)

  if (point && Array.isArray(features)) {
    const containing = features.filter((feature) => featureContainsPoint(feature, point))

    if (containing.length === 1) return containing[0]

    const sameName = containing.find((feature) => featureMatchesIncident(feature, incident))
    if (sameName) return sameName

    const sameProvince = containing.find((feature) => featureProvinceMatchesIncident(feature, incident))
    if (sameProvince) return sameProvince

    if (containing.length) return containing[0]
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
    const features = Array.isArray(municipiosGeoJson?.features) ? municipiosGeoJson.features : []

    if (!features.length) {
      return {
        activeMunicipioGeoJson: null,
        incidentByFeatureKey: new Map(),
        matchedIncidentIds: new Set(),
        geoJsonRenderKey: `${geoDatasetId || 'unknown'}::none::${mode || 'explore'}::${selectedIncidentId || 'none'}`,
      }
    }

    const byZoneId = new Map()
    const byMunicipioProvince = new Map()

    for (const feature of features) {
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
      const feature = selectFeatureForIncident(incident, byZoneId, byMunicipioProvince, features)
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
    () => activeVisible.filter(
      (incident) => !incidentSelectionKeys(incident).some((key) => matchedIncidentIds.has(key))
    ),
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
              click: (event) => {
                if (event?.originalEvent?.stopPropagation) event.originalEvent.stopPropagation()
                focusIncident(incident)
              },
            })
          }}
        />
      ) : null}

      {fallbackRectangles.map((incident) => {
        const selected = incidentMatchesSelected(incident, selectedIncidentId)

        return (
          <Rectangle
            key={incidentSelectionKey(incident)}
            bounds={incidentBounds(incident)}
            pathOptions={pathOptionsForIncident(incident, selected, statusColor)}
            eventHandlers={{
              click: (event) => {
                if (event?.originalEvent?.stopPropagation) event.originalEvent.stopPropagation()
                focusIncident(incident)
              },
            }}
          />
        )
      })}
    </>
  )
}

function incidentSelectionKey(incident) {
  return incident?.zone_id || incident?.id || incident?.incident_id || 'incident'
}
