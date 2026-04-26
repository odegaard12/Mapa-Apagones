export const GEO_DATASETS = {
  galicia: {
    id: 'galicia',
    label: 'Galicia',
    municipiosPath: '/data/galicia_municipios.geojson',
  },
}

export const DEFAULT_GEO_DATASET_ID = 'galicia'

export function getGeoDataset(datasetId = DEFAULT_GEO_DATASET_ID) {
  return GEO_DATASETS[datasetId] || GEO_DATASETS[DEFAULT_GEO_DATASET_ID]
}
