// Quiz des chapitres (onglet « Quiz ») : un fichier <id de la notion>.json par
// chapitre, produit par frontend/cours/format_v1/outils/construire_quiz.py.
// Les figures sont dans public/quiz/<id>/. Chargés seulement à l'ouverture.
const fichiers = import.meta.glob('./*.json')

export function aUnQuiz(notionId) {
  return `./${notionId}.json` in fichiers
}

export async function chargerQuiz(notionId) {
  const charger = fichiers[`./${notionId}.json`]
  if (!charger) return null
  const module = await charger()
  return module.default || module
}
