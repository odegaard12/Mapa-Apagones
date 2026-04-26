import { getGeoDataset } from './datasets'

export async function loadMunicipiosGeoJson(datasetId) {
  const dataset = getGeoDataset(datasetId)

  const res = await fetch(dataset.municipiosPath)
  if (!res.ok) {
    throw new Error(`No se pudo cargar ${dataset.id}: HTTP ${res.status}`)
  }

  const data = await res.json()

  if (!data || !Array.isArray(data.features)) {
    throw new Error(`GeoJSON inválido para ${dataset.id}`)
  }

  return { dataset, data }
}
