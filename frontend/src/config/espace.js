// Espace élève et parent (en place depuis le 2026-11-03).
export const ESPACE_ROUTES = {
  accueil: '/dashboard',
  chapitres: '/chapitres',
  chapitre: '/chapitre'
}

export const chapitreLink = (notionId, onglet = null, exerciceId = null) => {
  const query = {}
  if (onglet && onglet !== 'cours') query.onglet = onglet
  if (exerciceId) query.ex = String(exerciceId)
  return { path: `${ESPACE_ROUTES.chapitre}/${notionId}`, query }
}

export const OBJECTIF_SEMAINE = 20

// Les écrans d'exemple (?exemple=1, ?vue=parent) servent aux démonstrations :
// seuls le compte démo et les administrateurs peuvent les afficher.
export const COMPTE_DEMO = 'demo@optitab.net'
export const peutVoirExemple = (userStore) =>
  Boolean(userStore?.isAdmin) || String(userStore?.email || '').toLowerCase() === COMPTE_DEMO

// ---------------------------------------------------------------------------
// Données d'exemple : UNIQUEMENT pour l'aperçu (adresse avec ?exemple=1), afin
// de montrer un tableau de bord rempli avec le compte démo, qui n'a encore rien
// fait. Rien n'est écrit en base. Un bandeau le signale à l'écran.
// ---------------------------------------------------------------------------

const EXEMPLE_PROGRES = [
  // [faits, acquis] appliqués aux premiers chapitres d'analyse puis de probabilités
  [12, 10], [14, 9], [9, 7], [6, 3], [4, 2]
]

const EXEMPLE_A_REVOIR = [
  'Entraînement - Aire entre deux courbes',
  'Problème - Valeur moyenne d’une fonction',
  'Entraînement - Intégration par parties',
  'Découverte - Dérivée d’une composée'
]

export function appliquerExemple(progression) {
  const chapitres = (progression?.chapitres || []).map((c) => ({ ...c }))
  const cibles = chapitres.filter((c) => /analyse|probabilit/i.test(c.theme || '')).slice(0, EXEMPLE_PROGRES.length)
  const maintenant = Date.now()
  cibles.forEach((c, i) => {
    const [faits, acquis] = EXEMPLE_PROGRES[i]
    c.faits = Math.min(faits, c.exercices || faits)
    c.acquis = Math.min(acquis, c.faits)
    c.a_revoir = c.faits - c.acquis
    c.derniere_activite = new Date(maintenant - i * 86400000 * 1.5).toISOString()
  })
  const recent = cibles[cibles.length - 1] || chapitres[0]
  const a_revoir = cibles.length
    ? EXEMPLE_A_REVOIR.map((titre, i) => {
        const c = cibles[(i + 1) % cibles.length]
        return { exercice_id: null, exercice: titre, notion_id: c.id, notion: c.titre, quand: new Date(maintenant - i * 86400000).toISOString() }
      })
    : []
  return {
    ...progression,
    chapitres,
    a_revoir,
    derniere_activite: recent
      ? { notion_id: recent.id, notion: recent.titre, exercice_id: null, quand: new Date(maintenant - 3600000 * 5).toISOString() }
      : null
  }
}

function semaineExemple() {
  const valeurs = [3, 0, 5, 2, 4, 1, 6]
  return valeurs.map((total, i) => {
    const d = new Date(Date.now() - (6 - i) * 86400000)
    return { date: d.toISOString().slice(0, 10), total, correct: Math.max(0, total - (i % 3 === 0 ? 1 : 0)) }
  })
}

export function overviewExemple() {
  const weekly_trend = semaineExemple()
  const weekly_done = weekly_trend.reduce((s, d) => s + d.total, 0)
  return {
    metrics: { done_total: 45, acquired_count: 31, not_acquired_count: 14, weekly_done, weekly_goal: OBJECTIF_SEMAINE, weekly_progress: Math.round((weekly_done / OBJECTIF_SEMAINE) * 100) },
    weekly_trend,
    last_activities: [],
    by_matieres: []
  }
}

export function enfantsExemple() {
  const overview = overviewExemple()
  return [
    {
      id: 'exemple',
      first_name: 'Lucas',
      last_name: 'Martin',
      display_name: 'Lucas M.',
      niveau: 'Terminale',
      metrics: overview.metrics,
      last_activity: { chapitre_title: 'Calcul intégral', exercice_title: 'Aire entre deux courbes', when: new Date(Date.now() - 3600000 * 5).toISOString() },
      status: 'accepted'
    }
  ]
}
