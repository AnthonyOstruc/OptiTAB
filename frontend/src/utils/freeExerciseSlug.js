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

export const formatNiveauGroupSlug = (value) => {
  const normalized = slugifyText(value || '')
  if (!normalized) return ''
  if (normalized.includes('bases-methodes')) {
    return 'lycee'
  }
  if (normalized.includes('lycee') || normalized.includes('terminale') || normalized.includes('terminal') || normalized.includes('premiere') || normalized.includes('1ere') || normalized.includes('1re') || normalized.includes('seconde') || normalized.includes('2nde') || normalized.includes('2de') || normalized.includes('bac')) {
    return 'lycee'
  }
  if (normalized.includes('college') || normalized.includes('3e') || normalized.includes('4e') || normalized.includes('5e') || normalized.includes('6e') || normalized.includes('brevet')) {
    return 'college'
  }
  if (normalized.includes('prepa') || normalized.includes('mpsi') || normalized.includes('mp2i') || normalized.includes('pcsi') || normalized.includes('psi') || normalized.includes('mp') || normalized.includes('ecole') || normalized.includes('grandes-ecoles')) {
    return 'prepa'
  }
  return ''
}

export const buildExerciseChapterSlug = ({ niveauNom, niveau, name, title, notionNom } = {}) => {
  const levelSlug = formatNiveauSlug(niveauNom || niveau || '')
  const chapterSlug = slugifyText(name || title || notionNom || '')
  return [levelSlug, chapterSlug].filter(Boolean).join('-')
}

export const DEFAULT_PAYS_SLUG = 'france'
export const DEFAULT_MATIERE_SLUG = 'maths'

export const buildExerciseChapterRouteParams = ({ paysNom, matiereNom, niveauNom, niveauGroup, name, title, notionNom, id } = {}) => {
  const paysSlug = formatPaysSlug(paysNom || '') || DEFAULT_PAYS_SLUG
  const matiereSlug = formatMatiereSlug(matiereNom || '') || DEFAULT_MATIERE_SLUG
  const niveauGroupSlug = formatNiveauGroupSlug(niveauGroup || niveauNom || '')
  const slug = buildExerciseChapterSlug({ niveauNom, name, title, notionNom })
  return { pays: paysSlug, niveauGroup: niveauGroupSlug, matiere: matiereSlug, slug, id: id ?? null }
}
