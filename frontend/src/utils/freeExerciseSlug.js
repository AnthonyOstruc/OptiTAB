export const slugifyText = (value) => {
  return String(value || '')
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

export const formatNiveauSlug = (value) => {
  if (!value) return ''
  const normalized = slugifyText(value)
  if (!normalized) return ''
  if (normalized.includes('terminale') || normalized.includes('terminal')) {
    return 'terminal-bac'
  }
  if (normalized.includes('premiere') || normalized.includes('premiere') || normalized.includes('1ere') || normalized.includes('1re')) {
    return 'premiere-1er'
  }
  if (normalized.includes('seconde') || normalized.includes('2nde') || normalized.includes('2de')) {
    return 'seconde'
  }
  return normalized
}

export const formatPaysSlug = (value) => {
  return slugifyText(value || '')
}

export const formatMatiereSlug = (value) => {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized.includes('math')) return 'maths'
  return normalized
}

export const buildExerciseChapterSlug = ({ niveauNom, niveau, name, title, notionNom } = {}) => {
  const levelSlug = formatNiveauSlug(niveauNom || niveau || '')
  const chapterSlug = slugifyText(name || title || notionNom || '')
  return [levelSlug, chapterSlug].filter(Boolean).join('-')
}

export const DEFAULT_PAYS_SLUG = 'france'
export const DEFAULT_MATIERE_SLUG = 'maths'

export const buildExerciseChapterRouteParams = ({ paysNom, matiereNom, niveauNom, name, title, notionNom, id } = {}) => {
  const paysSlug = formatPaysSlug(paysNom || '') || DEFAULT_PAYS_SLUG
  const matiereSlug = formatMatiereSlug(matiereNom || '') || DEFAULT_MATIERE_SLUG
  const slug = buildExerciseChapterSlug({ niveauNom, name, title, notionNom })
  return { pays: paysSlug, matiere: matiereSlug, slug, id: id ?? null }
}
