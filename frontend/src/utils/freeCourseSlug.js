import { slugifyText, formatNiveauSlug, formatPaysSlug, formatMatiereSlug, formatNiveauGroupSlug } from './freeExerciseSlug'

const COMPLEX_NIVEAU_PREFIXES = ['terminal-bac', 'premiere-1er']
const SIMPLE_NIVEAU_PREFIXES = new Set([
  'terminale',
  'terminal',
  'seconde',
  '2nde',
  '2de',
  'premiere',
  '1ere',
  '1re',
  '6e',
  '5e',
  '4e',
  '3e',
  'mpsi',
  'mp2i',
  'pcsi',
  'mp',
  'psi'
])

export const extractCourseSlugParts = (rawSlug) => {
  const normalized = slugifyText(rawSlug || '')
  if (!normalized) return { niveauSlug: '', titleSlug: '' }

  for (const prefix of COMPLEX_NIVEAU_PREFIXES) {
    if (normalized === prefix) {
      return { niveauSlug: prefix, titleSlug: '' }
    }
    if (normalized.startsWith(`${prefix}-`)) {
      return { niveauSlug: prefix, titleSlug: normalized.slice(prefix.length + 1) }
    }
  }

  const dashIndex = normalized.indexOf('-')
  if (dashIndex === -1) {
    return { niveauSlug: normalized, titleSlug: '' }
  }

  const firstPart = normalized.slice(0, dashIndex)
  if (SIMPLE_NIVEAU_PREFIXES.has(firstPart)) {
    return { niveauSlug: firstPart, titleSlug: normalized.slice(dashIndex + 1) }
  }

  return { niveauSlug: '', titleSlug: normalized }
}

export const normalizeNiveauFromSlug = (value) => {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized === 'terminal-bac' || normalized === 'terminal' || normalized === 'terminale') {
    return 'terminale'
  }
  if (normalized === 'premiere-1er' || normalized === 'premiere' || normalized === '1ere' || normalized === '1re') {
    return 'premiere'
  }
  if (normalized === 'seconde' || normalized === '2nde' || normalized === '2de') {
    return 'seconde'
  }
  return normalized
}

export const normalizeMatiereFromSlug = (value) => {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized === 'math' || normalized === 'maths' || normalized === 'mathematique' || normalized === 'mathematiques') {
    return 'mathematiques'
  }
  return normalized
}

export const buildCoursePathSlug = ({ niveauNom, titre } = {}) => {
  const levelSlug = formatNiveauSlug(niveauNom || '')
  const titleSlug = slugifyText(titre || '')
  if (!levelSlug) return titleSlug
  if (!titleSlug) return levelSlug
  if (titleSlug === levelSlug || titleSlug.startsWith(`${levelSlug}-`)) return titleSlug
  return `${levelSlug}-${titleSlug}`
}

export const buildCourseRouteParams = ({ paysNom, matiereNom, niveauNom, titre, id } = {}) => {
  const paysSlug = formatPaysSlug(paysNom || '')
  const matiereSlug = formatMatiereSlug(matiereNom || '')
  const niveauGroupSlug = formatNiveauGroupSlug(niveauNom || '')
  const slug = buildCoursePathSlug({ niveauNom, titre })
  const safeId = id != null ? String(id) : ''
  if (!paysSlug || !matiereSlug || !slug || !safeId) return null
  return { pays: paysSlug, niveauGroup: niveauGroupSlug, matiere: matiereSlug, slug, id: safeId }
}

export const buildCourseApiSlug = ({ id, pays, niveau, matiere, titre } = {}) => {
  const safeId = String(id || '').replace(/\D/g, '')
  if (!safeId) return ''
  const base = `cours-gratuit-${safeId}`
  const paysSlug = slugifyText(pays || '')
  const niveauSlug = slugifyText(niveau || '')
  const matiereSlug = slugifyText(matiere || '')
  const titreSlug = slugifyText(titre || '')

  const parts = [paysSlug, niveauSlug, matiereSlug, titreSlug].filter(Boolean)
  if (parts.length === 0) return base

  const deduped = []
  for (const part of parts) {
    if (!deduped.includes(part)) deduped.push(part)
  }

  return `${base}-${deduped.join('-')}`
}

export const buildCourseApiSlugFromRoute = ({ id, pays, matiere, slug } = {}) => {
  const safeId = String(id || '').replace(/\D/g, '')
  if (!safeId) return ''

  const { niveauSlug, titleSlug } = extractCourseSlugParts(slug)
  const normalizedNiveau = normalizeNiveauFromSlug(niveauSlug)
  const normalizedMatiere = normalizeMatiereFromSlug(matiere)

  return buildCourseApiSlug({
    id: safeId,
    pays: pays,
    niveau: normalizedNiveau,
    matiere: normalizedMatiere,
    titre: titleSlug
  })
}
