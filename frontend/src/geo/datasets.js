export const GEO_DATASETS = {
  all: {
    id: 'all',
    label: 'Toda España',
    municipiosPath: '/data/toda_espana_municipios.geojson',
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
  cantabria: {
    id: 'cantabria',
    label: 'Cantabria',
    municipiosPath: '/data/cantabria_municipios.geojson',
    defaultCenter: [43.13587, -4.00071],
    defaultZoom: 9,
    maxBounds: [
      [42.67805, -4.93178],
      [43.59369, -3.06963],
    ],
  },
  castilla_leon: {
    id: 'castilla_leon',
    label: 'Castilla y León',
    municipiosPath: '/data/castilla_leon_municipios.geojson',
    defaultCenter: [41.66007, -4.42622],
    defaultZoom: 7,
    maxBounds: [
      [39.93193, -7.22707],
      [43.3882, -1.62537],
    ],
  },
  aragon: {
    id: 'aragon',
    label: 'Aragón',
    municipiosPath: '/data/aragon_municipios.geojson',
    defaultCenter: [41.62, -0.88],
    defaultZoom: 8,
    maxBounds: [
      [39.70, -2.25],
      [42.95, 0.90],
    ],
  },
  madrid: {
    id: 'madrid',
    label: 'Comunidad de Madrid',
    municipiosPath: '/data/madrid_municipios.geojson',
    defaultCenter: [40.4168, -3.7038],
    defaultZoom: 9,
    maxBounds: [
      [39.88, -4.62],
      [41.20, -3.03],
    ],
  },
  navarra: {
    id: 'navarra',
    label: 'Navarra',
    municipiosPath: '/data/navarra_municipios.geojson',
    defaultCenter: [42.69539, -1.67607],
    defaultZoom: 9,
    maxBounds: [
      [41.85, -2.55],
      [43.35, -0.65],
    ],
  },

  la_rioja: {
    id: 'la_rioja',
    label: 'La Rioja',
    municipiosPath: '/data/la_rioja_municipios.geojson',
    defaultCenter: [42.29, -2.54],
    defaultZoom: 10,
    maxBounds: [
      [41.85, -3.20],
      [42.75, -1.65],
    ],
  },
  murcia: {
    id: 'murcia',
    label: 'Región de Murcia',
    municipiosPath: '/data/murcia_municipios.geojson',
    defaultCenter: [37.99, -1.13],
    defaultZoom: 9,
    maxBounds: [
      [37.30, -2.40],
      [38.45, -0.60],
    ],
  },
  ceuta: {
    id: 'ceuta',
    label: 'Ceuta',
    municipiosPath: '/data/ceuta_municipios.geojson',
    defaultCenter: [35.89, -5.32],
    defaultZoom: 12,
    maxBounds: [
      [35.84, -5.40],
      [35.93, -5.25],
    ],
  },
  melilla: {
    id: 'melilla',
    label: 'Melilla',
    municipiosPath: '/data/melilla_municipios.geojson',
    defaultCenter: [35.29, -2.94],
    defaultZoom: 12,
    maxBounds: [
      [35.25, -3.02],
      [35.33, -2.88],
    ],
  },

  comunitat_valenciana: {
    id: 'comunitat_valenciana',
    label: 'Comunitat Valenciana',
    municipiosPath: '/data/comunitat_valenciana_municipios.geojson',
    defaultCenter: [39.50, -0.75],
    defaultZoom: 8,
    maxBounds: [
      [37.75, -1.70],
      [40.95, 0.75],
    ],
  },
  illes_balears: {
    id: 'illes_balears',
    label: 'Illes Balears',
    municipiosPath: '/data/illes_balears_municipios.geojson',
    defaultCenter: [39.61, 2.98],
    defaultZoom: 8,
    maxBounds: [
      [38.55, 1.10],
      [40.10, 4.60],
    ],
  },
}

export const GEO_DATASET_LIST = Object.values(GEO_DATASETS)
export const DEFAULT_GEO_DATASET_ID = 'all'

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

/* Public initial map view: Spain-first */
if (GEO_DATASETS.all) {
  GEO_DATASETS.all.defaultCenter = [40.25, -3.7]
  GEO_DATASETS.all.defaultZoom = 6
  GEO_DATASETS.all.maxBounds = [[27.4, -19.5], [44.5, 5.0]]
}
