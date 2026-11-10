// Pages de la vitrine livrées aussi en HTML complet, lisible sans JavaScript
// (Google, Bing, assistants d'IA, aperçus des réseaux sociaux).
//
// - L'accueil est écrit dans dist/index.html.
// - Les autres pages sont écrites dans dist/<page>/index.html : l'hébergeur ne
//   sert ce fichier qu'à l'adresse terminée par « / », qui devient donc
//   l'adresse officielle (canonique) de la page : https://www.optitab.net/tarifs/
//
// Contenu : relevé sur la vraie page par `node scripts/vitrine/instantanes.mjs`
// (fichiers contenu/vitrine/*.json), puis écrit à la construction par
// scripts/vitrine/prerendu.mjs. Relancer le relevé après toute modification
// d'une de ces pages.
export const PAGES_STATIQUES = [
  { chemin: '/', nom: 'accueil' },
  { chemin: '/tarifs', nom: 'tarifs' },
  { chemin: '/cours-particuliers', nom: 'cours-particuliers' },
  { chemin: '/about', nom: 'a-propos' },
  { chemin: '/contact', nom: 'contact' },
  { chemin: '/diagnostic-maths-gratuit', nom: 'diagnostic' }
]

const AVEC_BARRE = new Set(PAGES_STATIQUES.map((p) => p.chemin).filter((c) => c !== '/'))

// « /tarifs » → « /tarifs/ » pour les pages livrées en HTML complet ; les
// autres chemins sont rendus tels quels.
export const cheminCanonique = (chemin) => {
  const sans = chemin && chemin.length > 1 ? chemin.replace(/\/+$/, '') : chemin || '/'
  return AVEC_BARRE.has(sans) ? `${sans}/` : sans
}

// Même règle pour une adresse complète (https://www.optitab.net/tarifs).
export const urlCanonique = (url) => {
  try {
    const u = new URL(url)
    u.pathname = cheminCanonique(u.pathname)
    return u.toString()
  } catch (_) {
    return url
  }
}
