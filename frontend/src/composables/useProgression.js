import { ref } from 'vue'
import { getMyProgression } from '@/api/progression'
import { useUserStore } from '@/stores/user'

// Progression par chapitre partagée par toutes les pages du nouvel espace
// (accueil, chapitres, page chapitre, recherche) : un seul appel, gardé une
// minute, et invalidé dès qu'un exercice change de statut.
const progression = ref(null)
let proprietaire = null
let chargeA = 0
let enCours = null
let enCoursPour = null
const DUREE = 60000

export function useProgression() {
  const userStore = useUserStore()

  async function charger({ force = false } = {}) {
    // La progression dépend de l'élève ET de sa classe : changer de classe
    // invalide aussitôt ce qui était gardé.
    const moi = `${userStore.id || userStore.email || ''}|${userStore.niveau_pays?.id ?? ''}`
    const valide = progression.value && proprietaire === moi && Date.now() - chargeA < DUREE
    if (!force && valide) return progression.value
    // Autre classe : on n'affiche pas, même un instant, les chapitres de l'ancienne.
    if (proprietaire !== null && proprietaire !== moi) progression.value = null
    if (!force && enCours && enCoursPour === moi) return enCours
    enCoursPour = moi
    const demande = getMyProgression()
      .then((res) => {
        // Réponse d'une classe qui n'est plus la bonne : ignorée.
        if (enCoursPour !== moi) return progression.value
        progression.value = res?.data?.data || null
        proprietaire = moi
        chargeA = Date.now()
        return progression.value
      })
      .catch(() => progression.value)
      .finally(() => { if (enCours === demande) enCours = null })
    enCours = demande
    return demande
  }

  function invalider() {
    chargeA = 0
  }

  return { progression, charger, invalider }
}
