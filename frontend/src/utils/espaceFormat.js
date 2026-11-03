// Petits formats français pour l'espace élève et parent.

export function depuis(iso) {
  if (!iso) return ''
  const date = new Date(iso)
  const minutes = Math.round((Date.now() - date.getTime()) / 60000)
  if (minutes < 1) return 'à l’instant'
  if (minutes < 60) return `il y a ${minutes} min`
  const heures = Math.round(minutes / 60)
  if (heures < 24) return `il y a ${heures} h`
  const jours = Math.round(heures / 24)
  if (jours === 1) return 'hier'
  if (jours < 7) return `il y a ${jours} jours`
  return `le ${date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' })}`
}

export function joursDepuis(iso) {
  if (!iso) return null
  return Math.floor((Date.now() - new Date(iso).getTime()) / 86400000)
}

export const pluriel = (n, singulier, pluriel = `${singulier}s`) => `${n} ${n > 1 ? pluriel : singulier}`

export function dateDuJour() {
  const texte = new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })
  return texte.charAt(0).toUpperCase() + texte.slice(1)
}

export function initiales(prenom = '', nom = '') {
  return `${(prenom || '').trim().charAt(0)}${(nom || '').trim().charAt(0)}`.toUpperCase() || '?'
}

// État d'un chapitre à partir de ses compteurs.
export function etatChapitre(c) {
  if (!c || !c.faits) return { cle: 'new', label: 'À commencer' }
  if (c.exercices && c.acquis >= c.exercices) return { cle: 'done', label: 'Maîtrisé' }
  if (c.a_revoir > 0) return { cle: 'review', label: `${c.a_revoir} à revoir` }
  return { cle: 'progress', label: 'En cours' }
}

export function pourcent(part, total) {
  if (!total) return 0
  return Math.max(0, Math.min(100, Math.round((part / total) * 100)))
}
