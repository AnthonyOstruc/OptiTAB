import { ref } from 'vue'
import apiClient from '@/api/client'
import { useProgression } from './useProgression'

// La rubrique Quiz n'apparaît dans le menu que si au moins un quiz est publié
// pour une matière de la classe de l'élève (vérifié une fois par session).
const disponible = ref(false)
let verification = null

export function useQuizDisponible() {
  const { charger } = useProgression()

  function verifier() {
    if (verification) return verification
    verification = (async () => {
      const progression = await charger()
      const matieres = [...new Set((progression?.chapitres || []).map((c) => c.matiere_id).filter(Boolean))]
      for (const matiere of matieres) {
        const { data } = await apiClient.get('/api/quiz/quiz/', { params: { matiere, limit: 1 } })
        const total = typeof data?.count === 'number' ? data.count : (Array.isArray(data) ? data.length : (data?.results || []).length)
        if (total > 0) {
          disponible.value = true
          break
        }
      }
      return disponible.value
    })().catch(() => {
      verification = null
      return disponible.value
    })
    return verification
  }

  return { quizDisponible: disponible, verifier }
}
