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
  // Más comunidades añadidas en v0.9.8.4
  andalucia: {
    id: "andalucia",
    label: "Andalucía",
    municipiosPath: "/data/andalucia_municipios.geojson",
    defaultCenter: [37.333367, -4.576585],
    defaultZoom: 7,
    maxBounds: [[35.937646, -7.523047], [38.729087, -1.630124]],
  },
  aragon: {
    id: "aragon",
    label: "Aragón",
    municipiosPath: "/data/aragon_municipios.geojson",
    defaultCenter: [41.385582, -0.701182],
    defaultZoom: 7,
    maxBounds: [[39.846778, -2.173671], [42.924386, 0.771307]],
  },
  castilla_la_mancha: {
    id: "castilla_la_mancha",
    label: "Castilla-La Mancha",
    municipiosPath: "/data/castilla_la_mancha_municipios.geojson",
    defaultCenter: [39.674735, -3.160988],
    defaultZoom: 7,
    maxBounds: [[38.021838, -5.406184], [41.327632, -0.915793]],
  },
  cataluna: {
    id: "cataluna",
    label: "Cataluña",
    municipiosPath: "/data/cataluna_municipios.geojson",
    defaultCenter: [41.692248, 1.745806],
    defaultZoom: 7,
    maxBounds: [[40.523047, 0.159070], [42.861450, 3.332541]],
  },
  comunitat_valenciana: {
    id: "comunitat_valenciana",
    label: "Comunitat Valenciana",
    municipiosPath: "/data/comunitat_valenciana_municipios.geojson",
    defaultCenter: [39.316230, -0.419244],
    defaultZoom: 8,
    maxBounds: [[37.843828, -1.528799], [40.788631, 0.690311]],
  },
  extremadura: {
    id: "extremadura",
    label: "Extremadura",
    municipiosPath: "/data/extremadura_municipios.geojson",
    defaultCenter: [39.213839, -6.094455],
    defaultZoom: 7,
    maxBounds: [[37.941026, -7.541332], [40.486651, -4.647577]],
  },
  illes_balears: {
    id: "illes_balears",
    label: "Illes Balears",
    municipiosPath: "/data/illes_balears_municipios.geojson",
    defaultCenter: [39.367455, 2.743197],
    defaultZoom: 8,
    maxBounds: [[38.640388, 1.158655], [40.094521, 4.327739]],
  },
  la_rioja: {
    id: "la_rioja",
    label: "La Rioja",
    municipiosPath: "/data/la_rioja_municipios.geojson",
    defaultCenter: [42.281649, -2.406486],
    defaultZoom: 8,
    maxBounds: [[41.919034, -3.134271], [42.644265, -1.678701]],
  },
  madrid: {
    id: "madrid",
    label: "Comunidad de Madrid",
    municipiosPath: "/data/madrid_municipios.geojson",
    defaultCenter: [40.525282, -3.816030],
    defaultZoom: 8,
    maxBounds: [[39.884719, -4.579076], [41.165845, -3.052983]],
  },
  murcia: {
    id: "murcia",
    label: "Región de Murcia",
    municipiosPath: "/data/murcia_municipios.geojson",
    defaultCenter: [38.064418, -1.496084],
    defaultZoom: 8,
    maxBounds: [[37.373753, -2.344184], [38.755084, -0.647983]],
  },
  navarra: {
    id: "navarra",
    label: "Navarra",
    municipiosPath: "/data/navarra_municipios.geojson",
    defaultCenter: [42.612343, -1.612076],
    defaultZoom: 8,
    maxBounds: [[41.909894, -2.500083], [43.314792, -0.724070]],
  },
  pais_vasco: {
    id: "pais_vasco",
    label: "País Vasco / Euskadi",
    municipiosPath: "/data/pais_vasco_municipios.geojson",
    defaultCenter: [42.964658, -2.589836],
    defaultZoom: 8,
    maxBounds: [[42.472361, -3.450329], [43.456955, -1.729343]],
  },
  canarias: {
    id: "canarias",
    label: "Canarias",
    municipiosPath: "/data/canarias_municipios.geojson",
    defaultCenter: [28.527093, -15.747884],
    defaultZoom: 7,
    maxBounds: [[27.637734, -18.160809], [29.416452, -13.334958]],
  },
  ceuta: {
    id: "ceuta",
    label: "Ceuta",
    municipiosPath: "/data/ceuta_municipios.geojson",
    defaultCenter: [35.894343, -5.330180],
    defaultZoom: 11,
    maxBounds: [[35.870738, -5.382061], [35.917947, -5.278299]],
  },
  melilla: {
    id: "melilla",
    label: "Melilla",
    municipiosPath: "/data/melilla_municipios.geojson",
    defaultCenter: [35.292894, -2.946731],
    defaultZoom: 11,
    maxBounds: [[35.265489, -2.970296], [35.320300, -2.923167]],
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
