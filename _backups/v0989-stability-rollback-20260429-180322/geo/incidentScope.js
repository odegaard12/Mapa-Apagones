function isFiniteNumber(value) {
  return Number.isFinite(Number(value))
}

function getIncidentBox(incident) {
  const latMin = isFiniteNumber(incident?.lat_min) ? Number(incident.lat_min) : null
  const latMax = isFiniteNumber(incident?.lat_max) ? Number(incident.lat_max) : null
  const lngMin = isFiniteNumber(incident?.lng_min) ? Number(incident.lng_min) : null
  const lngMax = isFiniteNumber(incident?.lng_max) ? Number(incident.lng_max) : null

  if (
    latMin !== null &&
    latMax !== null &&
    lngMin !== null &&
    lngMax !== null
  ) {
    return { latMin, latMax, lngMin, lngMax }
  }

  const centerLat = isFiniteNumber(incident?.center_lat) ? Number(incident.center_lat) : null
  const centerLng = isFiniteNumber(incident?.center_lng) ? Number(incident.center_lng) : null

  if (centerLat !== null && centerLng !== null) {
    return {
      latMin: centerLat,
      latMax: centerLat,
      lngMin: centerLng,
      lngMax: centerLng,
    }
  }

  return null
}

export function incidentBelongsToDataset(incident, dataset) {
  if (!dataset?.maxBounds) return true

  const box = getIncidentBox(incident)
  if (!box) return true

  const [[regionLatMin, regionLngMin], [regionLatMax, regionLngMax]] = dataset.maxBounds

  const noOverlap =
    box.latMax < regionLatMin ||
    box.latMin > regionLatMax ||
    box.lngMax < regionLngMin ||
    box.lngMin > regionLngMax

  return !noOverlap
}
