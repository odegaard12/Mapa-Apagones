export const GEO_DATASETS = {
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
}

export const DEFAULT_GEO_DATASET_ID = 'galicia'

export function getGeoDataset(datasetId = DEFAULT_GEO_DATASET_ID) {
  return GEO_DATASETS[datasetId] || GEO_DATASETS[DEFAULT_GEO_DATASET_ID]
}
