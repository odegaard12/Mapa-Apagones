import { GEO_DATASET_LIST, getGeoDataset } from './datasets'

const datasetPromiseCache = new Map()

async function fetchGeoJson(path, datasetId) {
  const res = await fetch(path)
  if (!res.ok) {
    throw new Error(`No se pudo cargar ${datasetId}: HTTP ${res.status}`)
  }

  const data = await res.json()

  if (!data || !Array.isArray(data.features)) {
    throw new Error(`GeoJSON inválido para ${datasetId}`)
  }

  return data
}

function withDatasetId(dataset, data) {
  return {
    ...data,
    features: (data.features || []).map((feature) => ({
      ...feature,
      properties: {
        ...(feature?.properties || {}),
        dataset_id: feature?.properties?.dataset_id || dataset.id,
      },
    })),
  }
}

async function loadSingleDatasetData(dataset) {
  if (!dataset?.municipiosPath) {
    return { dataset, data: null }
  }

  if (!datasetPromiseCache.has(dataset.id)) {
    datasetPromiseCache.set(
      dataset.id,
      fetchGeoJson(dataset.municipiosPath, dataset.id).then((data) =>
        withDatasetId(dataset, data)
      )
    )
  }

  const data = await datasetPromiseCache.get(dataset.id)
  return { dataset, data }
}

function mergeCollections(collections) {
  return {
    type: 'FeatureCollection',
    features: collections.flatMap((item) => item?.features || []),
  }
}

export async function loadMunicipiosGeoJson(datasetId) {
  const dataset = getGeoDataset(datasetId)

  if (dataset.id !== 'all') {
    return loadSingleDatasetData(dataset)
  }

  const polygonDatasets = GEO_DATASET_LIST.filter(
    (item) => item.id !== 'all' && item.municipiosPath
  )

  const loaded = []
  for (const item of polygonDatasets) {
    const { data } = await loadSingleDatasetData(item)
    if (data) loaded.push(data)
  }

  return {
    dataset,
    data: mergeCollections(loaded),
  }
}
