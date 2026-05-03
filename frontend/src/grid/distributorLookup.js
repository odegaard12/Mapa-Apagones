function normalizeText(value = '') {
  return String(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
}

function slug(value = '') {
  return normalizeText(value).replace(/\s+/g, '_')
}

export const DISTRIBUTORS = {
  electrica_catoira: {
    id: 'electrica_catoira',
    name: 'Eléctrica de Catoira',
    legalName: 'Eléctrica de Catoira, S.L. / Distribuidora Eléctrica de Catoira',
    type: 'distribuidora',
    incidentsPhone: '900 373 685',
    customerPhone: '986 523 100',
    website: 'https://electricadecatoira.es/',
    confidence: 'alta',
    sourceLabel: 'Web pública / CNMC',
    note: 'Dato orientativo. Confirma siempre con la distribuidora o canales oficiales.',
  },
}

export const MUNICIPALITY_DISTRIBUTORS = {
  'municipality:pontevedra::catoira': ['electrica_catoira'],
}

export function municipalityDistributorKey(incident) {
  if (!incident) return null

  if (incident.zone_id && MUNICIPALITY_DISTRIBUTORS[incident.zone_id]) {
    return incident.zone_id
  }

  if (incident.id && MUNICIPALITY_DISTRIBUTORS[incident.id]) {
    return incident.id
  }

  const province = slug(incident.province || '')
  const municipio = slug(incident.municipio || incident.display_zone || '')

  if (!province || !municipio) return null

  return `municipality:${province}::${municipio}`
}

export function getDistributorCandidates(incident) {
  const key = municipalityDistributorKey(incident)
  const ids = key ? MUNICIPALITY_DISTRIBUTORS[key] || [] : []

  return ids
    .map((id) => DISTRIBUTORS[id])
    .filter(Boolean)
}
