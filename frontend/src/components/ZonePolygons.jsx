import React, { useMemo } from 'react'
import { GeoJSON, Rectangle } from 'react-leaflet'

function incidentBounds(incident) {
  return [
    [incident.lat_min, incident.lng_min],
    [incident.lat_max, incident.lng_max],
  ]
}

export default function ZonePolygons({
  municipiosGeoJson,
  activeVisible,
  selectedIncidentId,
  mode,
  focusIncident,
  statusColor,
}) {
  const activeZoneMap = useMemo(() => {
    const m = new Map()
    for (const item of activeVisible) {
      if (item.zone_id) m.set(item.zone_id, item)
    }
    return m
  }, [activeVisible])

  const activeMunicipioGeoJson = useMemo(() => {
    if (!municipiosGeoJson?.features) return null
    return {
      ...municipiosGeoJson,
      features: municipiosGeoJson.features.filter((ft) => activeZoneMap.has(ft?.properties?.zone_id)),
    }
  }, [municipiosGeoJson, activeZoneMap])

  const polygonRenderedZoneIds = useMemo(
    () => new Set((activeMunicipioGeoJson?.features || []).map((ft) => ft?.properties?.zone_id).filter(Boolean)),
    [activeMunicipioGeoJson]
  )

  const fallbackRectangles = useMemo(
    () => activeVisible.filter((item) => !polygonRenderedZoneIds.has(item.zone_id)),
    [activeVisible, polygonRenderedZoneIds]
  )

  function polygonStyle(feature) {
    const zone = activeZoneMap.get(feature?.properties?.zone_id)
    if (!zone) {
      return {
        color: 'transparent',
        weight: 0,
        fillOpacity: 0,
      }
    }

    const selected = selectedIncidentId === zone.id
    return {
      color: statusColor(zone.status),
      fillColor: statusColor(zone.status),
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
            const zone = activeZoneMap.get(feature?.properties?.zone_id)
            if (!zone) return
            layer.on({
              click: () => {
                if (mode === 'explore') focusIncident(zone)
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
