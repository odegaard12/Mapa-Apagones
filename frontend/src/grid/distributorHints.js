import rawDistributorHints from '../data/distributor_hints.json'

export const UNKNOWN_DISTRIBUTOR_LABEL = 'Consultar distribuidora de la zona'

export const DISTRIBUTOR_CONFIDENCE_LABELS = {
  verified_municipal: 'Distribuidora verificada',
  verified_partial: 'Varias distribuidoras posibles',
  regional_default: 'Distribuidora probable',
  unknown: 'Consultar distribuidora',
}

export const DISTRIBUTOR_HINTS = Array.isArray(rawDistributorHints?.items)
  ? rawDistributorHints.items
  : []

function normalizeText(value = '') {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
}

function zoneKeyFromParts(province, municipio) {
  const provinceSlug = normalizeText(province)
  const municipioSlug = normalizeText(municipio)

  if (!provinceSlug || !municipioSlug) return null
  return `municipality:${provinceSlug}::${municipioSlug}`
}

function itemMatchesIncident(item, incident) {
  if (!item || !incident) return false

  const itemZoneId = item.zone_id ? String(item.zone_id) : null
  const incidentZoneId = incident.zone_id ? String(incident.zone_id) : null

  if (itemZoneId && incidentZoneId && itemZoneId === incidentZoneId) {
    return true
  }

  const itemKey = zoneKeyFromParts(item.province, item.municipio)
  const incidentKey = zoneKeyFromParts(incident.province, incident.municipio)

  return Boolean(itemKey && incidentKey && itemKey === incidentKey)
}

function uniqueDistributors(distributors) {
  const seen = new Set()
  const result = []

  for (const distributor of distributors) {
    const name = String(distributor?.name || '').trim()
    if (!name) continue

    const key = [
      normalizeText(name),
      normalizeText(distributor?.r1_code || ''),
      normalizeText(distributor?.coverage_note || ''),
    ].join('|')

    if (seen.has(key)) continue

    seen.add(key)
    result.push(distributor)
  }

  return result
}

function formatDistributor(distributor) {
  const name = String(distributor?.name || '').trim()
  const confidence = distributor?.confidence || 'unknown'
  const label = DISTRIBUTOR_CONFIDENCE_LABELS[confidence] || DISTRIBUTOR_CONFIDENCE_LABELS.unknown

  if (!name) return UNKNOWN_DISTRIBUTOR_LABEL
  return `${name} (${label})`
}

export function getDistributorHintItemsForIncident(incident) {
  if (!incident) return []

  return DISTRIBUTOR_HINTS.filter((item) => itemMatchesIncident(item, incident))
}

export function getDistributorCandidatesForIncident(incident) {
  return uniqueDistributors(
    getDistributorHintItemsForIncident(incident).flatMap((item) =>
      Array.isArray(item.distributors) ? item.distributors : []
    )
  )
}

export function findDistributorHint(incident) {
  const distributors = getDistributorCandidatesForIncident(incident)

  if (!distributors.length) {
    return UNKNOWN_DISTRIBUTOR_LABEL
  }

  if (distributors.length === 1) {
    return formatDistributor(distributors[0])
  }

  return `Varias distribuidoras posibles: ${distributors
    .map((distributor) => String(distributor?.name || '').trim())
    .filter(Boolean)
    .slice(0, 4)
    .join(', ')}`
}
