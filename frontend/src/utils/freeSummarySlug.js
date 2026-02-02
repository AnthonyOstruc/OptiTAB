import {
  slugifyText,
  formatPaysSlug,
  formatMatiereSlug,
  formatNiveauGroupSlug
} from './freeExerciseSlug'
import {
  buildCoursePathSlug,
  extractCourseSlugParts,
  normalizeNiveauFromSlug,
  normalizeMatiereFromSlug
} from './freeCourseSlug'

export const buildSummaryPathSlug = ({ niveauNom, titre } = {}) => {
  return buildCoursePathSlug({ niveauNom, titre })
}

export const buildSummaryRouteParams = ({ paysNom, matiereNom, niveauNom, titre, id } = {}) => {
  const paysSlug = formatPaysSlug(paysNom || '')
  const matiereSlug = formatMatiereSlug(matiereNom || '')
  const niveauGroupSlug = formatNiveauGroupSlug(niveauNom || '')
  const slug = buildSummaryPathSlug({ niveauNom, titre })
  const safeId = id != null ? String(id) : ''
  if (!paysSlug || !matiereSlug || !slug || !safeId) return null
  return { pays: paysSlug, niveauGroup: niveauGroupSlug, matiere: matiereSlug, slug, id: safeId }
}

export const buildSummaryApiSlug = ({ id, pays, niveau, matiere, titre } = {}) => {
  const safeId = String(id || '').replace(/\D/g, '')
  if (!safeId) return ''
  const base = `synthese-gratuite-${safeId}`
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

export const buildSummaryApiSlugFromRoute = ({ id, pays, matiere, slug } = {}) => {
  const safeId = String(id || '').replace(/\D/g, '')
  if (!safeId) return ''

  const { niveauSlug, titleSlug } = extractCourseSlugParts(slug)
  const normalizedNiveau = normalizeNiveauFromSlug(niveauSlug)
  const normalizedMatiere = normalizeMatiereFromSlug(matiere)

  return buildSummaryApiSlug({
    id: safeId,
    pays: pays,
    niveau: normalizedNiveau,
    matiere: normalizedMatiere,
    titre: titleSlug
  })
}
