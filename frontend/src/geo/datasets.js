export const GEO_DATASETS = {
  all: {
    id: 'all',
    label: 'Toda España',
    defaultCenter: [40.25, -3.70],
    defaultZoom: 6,
    maxBounds: null,
  },
  galicia: {
    id: 'galicia',
    label: 'Galicia',
    municipiosPath: '/data/galicia_municipios.geojson',
    defaultCenter: [42.67, -8.71],
    defaultZoom: 9,
    maxBounds: [
      [41.75, -9.60],
      [43.95, -6.70],
    ],
  },
  asturias: {
    id: 'asturias',
    label: 'Asturias',
    municipiosPath: '/data/asturias_municipios.geojson',
    defaultCenter: [43.36, -5.85],
    defaultZoom: 9,
    maxBounds: [
      [42.85, -7.35],
      [44.40, -4.50],
    ],
  },
}

export const GEO_DATASET_LIST = Object.values(GEO_DATASETS)
export const DEFAULT_GEO_DATASET_ID = 'galicia'

export function getGeoDataset(datasetId = DEFAULT_GEO_DATASET_ID) {
  return GEO_DATASETS[datasetId] || GEO_DATASETS[DEFAULT_GEO_DATASET_ID]
}

export function getInitialGeoDatasetId() {
  if (typeof window === 'undefined') return DEFAULT_GEO_DATASET_ID
  const params = new URLSearchParams(window.location.search)
  const requested = params.get('geo')
  return getGeoDataset(requested).id
}

export function syncGeoDatasetInUrl(datasetId = DEFAULT_GEO_DATASET_ID) {
  if (typeof window === 'undefined') return

  const url = new URL(window.location.href)

  if (!datasetId || datasetId === DEFAULT_GEO_DATASET_ID) {
    url.searchParams.delete('geo')
  } else {
    url.searchParams.set('geo', datasetId)
  }

  const next =
    url.pathname +
    (url.searchParams.toString() ? `?${url.searchParams.toString()}` : '') +
    url.hash

  window.history.replaceState({}, '', next)
}
