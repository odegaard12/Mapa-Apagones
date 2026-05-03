const geoJsonCache = new Map()

async function fetchGeoJson(path) {
  if (!path) return null

  if (!geoJsonCache.has(path)) {
    geoJsonCache.set(
      path,
      fetch(path).then((res) => {
        if (!res.ok) {
          throw new Error(`No se pudo cargar ${path}: HTTP ${res.status}`)
        }
        return res.json()
      })
    )
  }

  return geoJsonCache.get(path)
}

function pathsForDataset(dataset) {
  if (!dataset) return []

  if (Array.isArray(dataset.municipiosPaths) && dataset.municipiosPaths.length) {
    return dataset.municipiosPaths.filter(Boolean)
  }

  if (dataset.municipiosPath) {
    return [dataset.municipiosPath]
  }

  return []
}

export async function loadMunicipiosGeoJson(dataset) {
  const paths = pathsForDataset(dataset)

  if (!paths.length) return null

  if (paths.length === 1) {
    const data = await fetchGeoJson(paths[0])
    return { data, sources: paths }
  }

  const merged = {
    type: 'FeatureCollection',
    features: [],
  }

  const loadedSources = []

  for (const path of paths) {
    try {
      const data = await fetchGeoJson(path)
      const features = Array.isArray(data?.features) ? data.features : []

      if (features.length) {
        merged.features.push(...features)
        loadedSources.push(path)
      }
    } catch (err) {
      console.error('No se pudo cargar dataset municipal', path, err)
    }
  }

  if (!merged.features.length) return null

  return {
    data: merged,
    sources: loadedSources,
  }
}
