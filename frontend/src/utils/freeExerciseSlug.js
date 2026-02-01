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
    return 'terminale-bac'
  }
  if (normalized.includes('premiere') || normalized.includes('premiere') || normalized.includes('1ere') || normalized.includes('1re')) {
    return 'premiere-bac'
  }
  if (normalized.includes('seconde') || normalized.includes('2nde') || normalized.includes('2de')) {
    return 'seconde'
  }
  return normalized
}

export const formatPaysSlug = (value) => {
  return slugifyText(value || '')
}

export const buildExerciseChapterSlug = ({ niveauNom, niveau, name, title, notionNom } = {}) => {
  const levelSlug = formatNiveauSlug(niveauNom || niveau || '')
  const chapterSlug = slugifyText(name || title || notionNom || '')
  return [levelSlug, chapterSlug].filter(Boolean).join('-')
}

export const DEFAULT_PAYS_SLUG = 'france'

export const buildExerciseChapterRouteParams = ({ paysNom, niveauNom, name, title, notionNom, id } = {}) => {
  const paysSlug = formatPaysSlug(paysNom || '') || DEFAULT_PAYS_SLUG
  const slug = buildExerciseChapterSlug({ niveauNom, name, title, notionNom })
  return { pays: paysSlug, slug, id: id ?? null }
}
