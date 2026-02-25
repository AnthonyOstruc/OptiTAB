export const FREE_RESOURCES_ACTION_CARDS = Object.freeze([
  {
    key: 'course',
    title: 'Cours',
    subtitle: 'Cours gratuits structurés et progressifs.',
    to: { name: 'FreeCourses' }
  },
  {
    key: 'exercise',
    title: 'Exercices corrigés',
    subtitle: 'Entraînement avec correction pas à pas.',
    to: { name: 'FreeExercises' }
  },
  {
    key: 'summary',
    title: 'Fiches de révision',
    subtitle: 'Synthèses rapides à relire avant contrôle.',
    to: { name: 'FreeSummaries' }
  }
])

export const FREE_RESOURCES_LEVEL_LINKS = Object.freeze([
  { key: 'college', label: 'Collège', query: 'college' },
  { key: 'seconde', label: 'Seconde', query: 'seconde' },
  { key: 'premiere', label: 'Première', query: 'premiere' },
  { key: 'terminale', label: 'Terminale', query: 'terminale' },
  { key: 'prepa', label: 'Prépa', query: 'mpsi' }
])

export const FREE_RESOURCES_QUICK_START_ITEMS = Object.freeze([
  'Choisis ton niveau.',
  'Ouvre un chapitre ciblé.',
  'Fais 3 exercices corrigés.',
  'Termine avec une fiche de révision.'
])

export const FREE_RESOURCES_SEO_SECTION_TITLES = Object.freeze([
  'Comprendre le parcours',
  'Structurer la progression',
  'Ancrer les automatismes'
])

export function getFreeResourcesListPath(resourceType) {
  const type = String(resourceType || '').trim().toLowerCase()
  if (type === 'exercise') return '/ressources-gratuites/exercices'
  if (type === 'summary') return '/ressources-gratuites/syntheses'
  return '/ressources-gratuites/cours'
}
