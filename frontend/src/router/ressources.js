import { START_LOCATION } from 'vue-router'

// Les ressources gratuites sont des pages statiques générées à la construction
// du site (scripts/ressources). Toute adresse /ressources-gratuites… qui passe
// par l'application mène à la bonne page statique, par un chargement complet :
// nouvelles adresses telles quelles, anciennes adresses (cours, fiches,
// exercices des versions précédentes) grâce à la table redirections.json.

export const RACINE_RESSOURCES = '/ressources-gratuites/'

let table = null
async function tableDesRedirections() {
  if (table) return table
  try {
    const reponse = await fetch(`${RACINE_RESSOURCES}redirections.json`, { headers: { Accept: 'application/json' } })
    table = reponse.ok ? await reponse.json() : {}
  } catch {
    table = {}
  }
  return table
}

const numero = (texte) => (String(texte || '').match(/(?:^|-)(\d+)(?:-|$)/) || [])[1]

const TYPE_DE_ROUTE = {
  FreeCourseSlugGrouped: 'cours',
  FreeCourseSlug: 'cours',
  FreeCourseDetail: 'cours',
  FreeSummarySlugGrouped: 'fiche',
  FreeSummarySlug: 'fiche',
  FreeSummaryDetail: 'fiche',
  FreeExerciseChapterSlugGrouped: 'notion',
  FreeExerciseChapterSlug: 'notion',
  FreeExerciseChapterSlugLegacy: 'notion',
  FreeExerciseChapter: 'notion',
  FreeExerciseDetail: 'exercice'
}

async function adresseCible(to) {
  const chemin = to.path
  if (/^\/ressources-gratuites\/maths(\/|$)/.test(chemin)) return chemin.endsWith('/') ? chemin : `${chemin}/`
  const type = TYPE_DE_ROUTE[to.name]
  if (!type) return RACINE_RESSOURCES
  const id = to.params.id || to.params.notionId || numero(to.params.slug)
  const correspondances = await tableDesRedirections()
  return (id && correspondances[type]?.[id]) || RACINE_RESSOURCES
}

// Garde des routes /ressources-gratuites… : quitte l'application vers la page
// statique. Au premier chargement, si l'adresse est déjà la bonne, la page
// statique n'existe pas (ex. serveur de développement sans génération) : on
// affiche la page de secours au lieu de boucler.
export async function versRessources(to, from) {
  const cible = await adresseCible(to)
  const premierChargement = from === START_LOCATION
  if (premierChargement && cible === to.path) return true
  if (premierChargement) window.location.replace(cible + (to.hash || ''))
  else window.location.assign(cible + (to.hash || ''))
  // Le navigateur quitte l'application : la navigation reste en attente
  // (l'annuler laisserait une erreur « Navigation aborted » dans la console).
  return new Promise(() => {})
}

// Blog : pages statiques générées avec les ressources (scripts/ressources/blog.mjs).
// Anciennes catégories et étiquettes, adresses inconnues : accueil du blog.
export const RACINE_BLOG = '/blog/'

export async function versBlog(to, from) {
  const chemin = to.path.endsWith('/') ? to.path : `${to.path}/`
  const cible = /^\/blog\/(categorie|tag)\//.test(chemin) ? RACINE_BLOG : chemin
  const premierChargement = from === START_LOCATION
  if (premierChargement && cible === to.path) {
    // La page statique demandée n'existe pas : accueil du blog (ou page de
    // secours si l'accueil lui-même manque, ex. serveur de développement).
    if (to.path === RACINE_BLOG) return true
    window.location.replace(RACINE_BLOG)
    return new Promise(() => {})
  }
  if (premierChargement) window.location.replace(cible + (to.hash || ''))
  else window.location.assign(cible + (to.hash || ''))
  return new Promise(() => {})
}
