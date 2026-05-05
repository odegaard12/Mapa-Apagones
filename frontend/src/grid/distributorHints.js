export const UNKNOWN_DISTRIBUTOR_LABEL = 'Consultar distribuidora de la zona'

export const DISTRIBUTOR_CONFIDENCE_LABELS = {
  verified_municipal: 'Verificada',
  verified_partial: 'Varias distribuidoras posibles',
  regional_default: 'Confirmar con comercializadora/distribuidora',
  unknown: 'Consultar distribuidora',
}

export const DISTRIBUTOR_DISPLAY_LABELS = {
  verified_municipal: 'Distribuidora verificada',
  verified_partial: 'Distribuidora probable',
  regional_default: 'Distribuidora orientativa',
  unknown: 'Distribuidora',
}

export const DISTRIBUTOR_HINTS_PUBLIC_PATH = '/data/distributor_hints.json'

export const DISTRIBUTOR_HINTS = []

let distributorHintsLoadPromise = null
let distributorHintsLoaded = false

function setDistributorHints(items) {
  DISTRIBUTOR_HINTS.splice(0, DISTRIBUTOR_HINTS.length, ...items)
  distributorHintsLoaded = true
}

export function areDistributorHintsLoaded() {
  return distributorHintsLoaded
}

export async function loadDistributorHints({ force = false } = {}) {
  if (distributorHintsLoaded && !force) {
    return DISTRIBUTOR_HINTS
  }

  if (distributorHintsLoadPromise && !force) {
    return distributorHintsLoadPromise
  }

  distributorHintsLoadPromise = fetch(DISTRIBUTOR_HINTS_PUBLIC_PATH, {
    headers: { Accept: 'application/json' },
    cache: 'no-cache',
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`No se pudo cargar ${DISTRIBUTOR_HINTS_PUBLIC_PATH}: HTTP ${response.status}`)
      }

      return response.json()
    })
    .then((payload) => {
      const items = Array.isArray(payload?.items) ? payload.items : []
      setDistributorHints(items)
      return DISTRIBUTOR_HINTS
    })
    .catch((error) => {
      distributorHintsLoadPromise = null
      throw error
    })

  return distributorHintsLoadPromise
}

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
      normalizeText(distributor?.confidence || ''),
    ].join('|')

    if (seen.has(key)) continue
    seen.add(key)
    result.push(distributor)
  }

  return result
}

function getDistributorConfidence(distributor) {
  return distributor?.confidence || 'unknown'
}

function formatDistributor(distributor) {
  const name = String(distributor?.name || '').trim()
  const confidence = getDistributorConfidence(distributor)
  const label = DISTRIBUTOR_CONFIDENCE_LABELS[confidence] || DISTRIBUTOR_CONFIDENCE_LABELS.unknown

  if (!name) return UNKNOWN_DISTRIBUTOR_LABEL
  return `${name} (${label})`
}

function displayLabelForConfidence(confidence) {
  return DISTRIBUTOR_DISPLAY_LABELS[confidence] || DISTRIBUTOR_DISPLAY_LABELS.unknown
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

export function getDistributorHintDisplay(incident) {
  const distributors = getDistributorCandidatesForIncident(incident)

  if (!distributors.length) {
    return {
      confidence: 'unknown',
      label: DISTRIBUTOR_DISPLAY_LABELS.unknown,
      name: UNKNOWN_DISTRIBUTOR_LABEL,
    }
  }

  if (distributors.length === 1) {
    const confidence = getDistributorConfidence(distributors[0])

    return {
      confidence,
      label: displayLabelForConfidence(confidence),
      name: formatDistributor(distributors[0]),
    }
  }

  return {
    confidence: 'verified_partial',
    label: 'Distribuidoras posibles',
    name: `Varias distribuidoras posibles: ${distributors
      .map((distributor) => String(distributor?.name || '').trim())
      .filter(Boolean)
      .slice(0, 4)
      .join(', ')}`,
  }
}

export function findDistributorHint(incident) {
  return getDistributorHintDisplay(incident).name
}
