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
const DUREE = 60000

export function useProgression() {
  const userStore = useUserStore()

  async function charger({ force = false } = {}) {
    const moi = userStore.id || userStore.email || null
    const valide = progression.value && proprietaire === moi && Date.now() - chargeA < DUREE
    if (!force && valide) return progression.value
    if (!force && enCours) return enCours
    enCours = getMyProgression()
      .then((res) => {
        progression.value = res?.data?.data || null
        proprietaire = moi
        chargeA = Date.now()
        return progression.value
      })
      .catch(() => progression.value)
      .finally(() => { enCours = null })
    return enCours
  }

  function invalider() {
    chargeA = 0
  }

  return { progression, charger, invalider }
}
