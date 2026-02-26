export const FREE_RESOURCES_ACTION_CARDS = Object.freeze([
  {
    key: 'course',
    title: 'Cours',
    subtitle: 'Progression claire du college a la prepa pour comprendre chaque notion.',
    badge: 'Base solide',
    hint: 'Ideal pour preparer un chapitre avant les exercices.',
    cta: 'Voir les cours gratuits',
    seoLabel: 'Acceder aux cours de maths gratuits',
    to: { name: 'FreeCourses' }
  },
  {
    key: 'exercise',
    title: 'Exercices corriges',
    subtitle: 'Entrainement cible avec corrections detaillees et methode pas a pas.',
    badge: 'Le plus clique',
    hint: 'Parfait pour passer de la theorie a la pratique.',
    cta: 'Faire des exercices corriges',
    seoLabel: 'Acceder aux exercices de maths corriges',
    to: { name: 'FreeExercises' }
  },
  {
    key: 'summary',
    title: 'Fiches de revision',
    subtitle: 'Syntheses visuelles et rappels de methodes avant DS, brevet ou bac.',
    badge: 'Revision express',
    hint: 'A relire rapidement avant une evaluation.',
    cta: 'Ouvrir les fiches de revision',
    seoLabel: 'Acceder aux fiches de revision de maths gratuites',
    to: { name: 'FreeSummaries' }
  }
])

export const FREE_RESOURCES_LEVEL_LINKS = Object.freeze([
  { key: 'college', label: 'College', query: 'college' },
  { key: 'seconde', label: 'Seconde', query: 'seconde' },
  { key: 'premiere', label: 'Premiere', query: 'premiere' },
  { key: 'terminale', label: 'Terminale', query: 'terminale' },
  { key: 'prepa', label: 'Prepa', query: 'mpsi' }
])

export const FREE_RESOURCES_QUICK_START_ITEMS = Object.freeze([
  'Choisis ton niveau.',
  'Ouvre un chapitre cible.',
  'Fais 3 exercices corriges.',
  'Termine avec une fiche de revision.'
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
