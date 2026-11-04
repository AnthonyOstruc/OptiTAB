import { getCours } from '@/api/cours'
import { getExercices, getStatuses } from '@/api'
import { apiUtils } from '@/api/client'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUserStore } from '@/stores/user'

// Contenu d'un chapitre (cours, fiche, exercices). Les onglets et le
// préchargement passent par ces fonctions, appuyées sur le cache mémoire des
// API (5 min pour les contenus, 1 à 2 min pour les exercices et les statuts) :
// un préchargement et l'ouverture qui suit partagent la même requête.

const DUREE_CONTENU = 300000
const IMAGE_NUMEROTEE = /\[\s*IMAGE\s*_?\s*\d+\s*\]/i

export async function chargerCours(notionId) {
  const { data } = await getCours(null, notionId, null)
  return Array.isArray(data) ? data[0] || null : data || null
}

// La liste contient déjà le texte de la fiche : le détail n'est demandé que
// pour placer ses images numérotées ([IMAGE 1]…).
export async function chargerFiche(notionId) {
  const { data } = await apiUtils.cachedGet('/api/sheets/', { params: { notion: notionId, sheet_type: 'summary' }, ttl: DUREE_CONTENU })
  const premiere = Array.isArray(data) ? data[0] : (data?.results || [])[0]
  if (!premiere?.id) return null
  if (!IMAGE_NUMEROTEE.test(premiere.summary || '')) return premiere
  const detail = await apiUtils.cachedGet(`/api/sheets/${premiere.id}/`, { ttl: DUREE_CONTENU }).catch(() => null)
  return detail?.data || premiere
}

export function chargerExercices(notionId) {
  const niveau = useUserStore().niveau_pays?.id
  return Promise.all([getExercices({ notion: notionId, niveau }), getStatuses()])
}

const CHARGEURS = { cours: chargerCours, fiche: chargerFiche, exercices: chargerExercices }

let vuePrete = false
function prechargerVue() {
  if (vuePrete) return
  vuePrete = true
  import('@/views/espace/EspaceChapitre.vue').catch(() => { vuePrete = false })
}

// Même règle que le routeur : on ne demande pas un contenu que l'élève ne peut pas ouvrir.
async function accesAuChapitre(notionId) {
  const userStore = useUserStore()
  if (userStore.isAdmin) return true
  if (Number(userStore.niveau_pays?.demo_notion) === Number(notionId)) return true
  const abonnement = useSubscriptionStore()
  await abonnement.fetchStatus()
  return abonnement.accessForLevel(userStore.niveau_pays?.id)
}

// Prépare l'ouverture d'un chapitre (page, vérification d'accès, contenu des
// onglets demandés) pour que le clic affiche une page déjà prête.
export async function prechargerChapitre(notionId, onglets = ['cours']) {
  if (!notionId) return
  prechargerVue()
  try {
    if (!(await accesAuChapitre(notionId))) return
    await Promise.all(onglets.map((onglet) => CHARGEURS[onglet]?.(notionId)))
  } catch {
    // Simple anticipation : l'onglet refera la demande à son ouverture.
  }
}

// Lien vers un chapitre (/chapitre/12?onglet=fiche) → { notionId, onglet }.
export function chapitreDuLien(href) {
  try {
    const url = new URL(href, window.location.origin)
    const m = url.pathname.match(/^\/chapitre\/(\d+)\/?$/)
    if (!m || url.origin !== window.location.origin) return null
    const onglet = url.searchParams.get('onglet')
    return { notionId: m[1], onglet: CHARGEURS[onglet] ? onglet : 'cours' }
  } catch {
    return null
  }
}
