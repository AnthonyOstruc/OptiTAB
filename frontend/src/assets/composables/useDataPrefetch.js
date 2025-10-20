/**
 * Composable pour le préchargement intelligent des données
 * Permet de charger les données en arrière-plan avant la navigation
 */

import { ref } from 'vue'
import { getThemesWithNotionsForUser } from '@/api/themes'
import { getQuiz } from '@/api/quiz'
import { getExercices } from '@/api'
import { getCours } from '@/api/cours'
import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'

// Cache global pour le prefetch (partagé entre toutes les instances)
const prefetchCache = new Map()
const prefetchInFlight = new Map()
const PREFETCH_TTL = 300000 // 5 minutes

export function useDataPrefetch() {
  const subjectsStore = useSubjectsStore()

  /**
   * Précharge les thèmes et notions pour une matière
   * @param {number} matiereId - ID de la matière
   * @returns {Promise<void>}
   */
  async function prefetchThemesNotions(matiereId) {
    if (!matiereId) return

    const cacheKey = `themes_notions_${matiereId}`
    
    // Si déjà en cache et valide, ne rien faire
    const cached = prefetchCache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < PREFETCH_TTL) {
      return
    }

    // Si une requête est déjà en cours, l'attendre
    if (prefetchInFlight.has(cacheKey)) {
      return prefetchInFlight.get(cacheKey)
    }

    // Lancer le prefetch en arrière-plan
    const prefetchPromise = (async () => {
      try {
        // Utiliser AbortController pour pouvoir annuler si nécessaire
        const controller = new AbortController()
        const { data } = await getThemesWithNotionsForUser({ 
          matiere: matiereId,
          signal: controller.signal 
        })
        
        // Stocker dans le cache
        prefetchCache.set(cacheKey, {
          data,
          timestamp: Date.now()
        })
        
        return data
      } catch (error) {
        // Ignorer les erreurs de prefetch (navigation annulée, etc.)
        if (error?.name === 'CanceledError' || error?.name === 'AbortError') {
          return null
        }
        console.warn('[Prefetch] Erreur lors du préchargement:', error)
        return null
      } finally {
        prefetchInFlight.delete(cacheKey)
      }
    })()

    prefetchInFlight.set(cacheKey, prefetchPromise)
    return prefetchPromise
  }

  /**
   * Précharge les données pour toutes les matières sélectionnées
   * @param {Array<number>} matiereIds - Liste des IDs de matières
   */
  async function prefetchSelectedMatieres(matiereIds = []) {
    if (!Array.isArray(matiereIds) || matiereIds.length === 0) {
      return
    }

    // Précharger en parallèle (max 3 à la fois pour ne pas surcharger)
    const BATCH_SIZE = 3
    for (let i = 0; i < matiereIds.length; i += BATCH_SIZE) {
      const batch = matiereIds.slice(i, i + BATCH_SIZE)
      await Promise.all(batch.map(id => prefetchThemesNotions(id)))
    }
  }

  /**
   * Précharge automatiquement la matière active
   */
  async function prefetchActiveMatiere() {
    const activeMatiereId = subjectsStore.activeMatiereId
    if (activeMatiereId) {
      await prefetchThemesNotions(activeMatiereId)
    }
  }

  /**
   * Précharge les quiz pour une notion
   * @param {number} notionId - ID de la notion
   * @returns {Promise<void>}
   */
  async function prefetchQuizByNotion(notionId) {
    if (!notionId) return

    const cacheKey = `quiz_notion_${notionId}`
    
    // Si déjà en cache et valide, ne rien faire
    const cached = prefetchCache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < PREFETCH_TTL) {
      return
    }

    // Si une requête est déjà en cours, l'attendre
    if (prefetchInFlight.has(cacheKey)) {
      return prefetchInFlight.get(cacheKey)
    }

    // Lancer le prefetch en arrière-plan
    const prefetchPromise = (async () => {
      try {
        // getQuiz attend juste notionId comme paramètre
        const data = await getQuiz(notionId)
        
        // Stocker dans le cache
        prefetchCache.set(cacheKey, {
          data,
          timestamp: Date.now()
        })
        
        return data
      } catch (error) {
        if (error?.name === 'CanceledError' || error?.name === 'AbortError') {
          return null
        }
        console.warn('[Prefetch Quiz] Erreur:', error)
        return null
      } finally {
        prefetchInFlight.delete(cacheKey)
      }
    })()

    prefetchInFlight.set(cacheKey, prefetchPromise)
    return prefetchPromise
  }

  /**
   * Précharge les exercices pour une notion
   * @param {number} notionId - ID de la notion
   * @returns {Promise<void>}
   */
  async function prefetchExercicesByNotion(notionId) {
    if (!notionId) return

    const userStore = useUserStore()
    const niveauId = userStore.niveau_pays?.id

    const cacheKey = `exercices_notion_${notionId}_${niveauId || 'n'}`
    
    // Si déjà en cache et valide, ne rien faire
    const cached = prefetchCache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < PREFETCH_TTL) {
      return
    }

    // Si une requête est déjà en cours, l'attendre
    if (prefetchInFlight.has(cacheKey)) {
      return prefetchInFlight.get(cacheKey)
    }

    // Lancer le prefetch en arrière-plan
    const prefetchPromise = (async () => {
      try {
        // getExercices attend un objet params unique
        const data = await getExercices({ 
          notion: notionId, 
          niveau: niveauId 
        })
        
        // Stocker dans le cache
        prefetchCache.set(cacheKey, {
          data,
          timestamp: Date.now()
        })
        
        return data
      } catch (error) {
        if (error?.name === 'CanceledError' || error?.name === 'AbortError') {
          return null
        }
        console.warn('[Prefetch Exercices] Erreur:', error)
        return null
      } finally {
        prefetchInFlight.delete(cacheKey)
      }
    })()

    prefetchInFlight.set(cacheKey, prefetchPromise)
    return prefetchPromise
  }

  /**
   * Précharge les cours pour une notion
   * @param {number} notionId - ID de la notion
   * @returns {Promise<void>}
   */
  async function prefetchCoursByNotion(notionId) {
    if (!notionId) return

    const cacheKey = `cours_notion_${notionId}`
    
    // Si déjà en cache et valide, ne rien faire
    const cached = prefetchCache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < PREFETCH_TTL) {
      return
    }

    // Si une requête est déjà en cours, l'attendre
    if (prefetchInFlight.has(cacheKey)) {
      return prefetchInFlight.get(cacheKey)
    }

    // Lancer le prefetch en arrière-plan
    const prefetchPromise = (async () => {
      try {
        // getCours attend des paramètres positionnels: (matiereId, notionId, chapitreId)
        // On passe null pour matiereId, notionId pour le deuxième paramètre
        const data = await getCours(null, notionId, null)
        
        // Stocker dans le cache
        prefetchCache.set(cacheKey, {
          data,
          timestamp: Date.now()
        })
        
        return data
      } catch (error) {
        if (error?.name === 'CanceledError' || error?.name === 'AbortError') {
          return null
        }
        console.warn('[Prefetch Cours] Erreur:', error)
        return null
      } finally {
        prefetchInFlight.delete(cacheKey)
      }
    })()

    prefetchInFlight.set(cacheKey, prefetchPromise)
    return prefetchPromise
  }

  /**
   * Précharge tout le contenu d'une notion (quiz + exercices + cours)
   * @param {number} notionId - ID de la notion
   * @returns {Promise<void>}
   */
  async function prefetchNotionContent(notionId) {
    if (!notionId) return

    // Précharger en parallèle tous les types de contenu
    await Promise.allSettled([
      prefetchQuizByNotion(notionId),
      prefetchExercicesByNotion(notionId),
      prefetchCoursByNotion(notionId)
    ])
  }

  /**
   * Nettoie le cache de prefetch (anciennes entrées)
   */
  function cleanupPrefetchCache() {
    const now = Date.now()
    for (const [key, value] of prefetchCache.entries()) {
      if (now - value.timestamp > PREFETCH_TTL) {
        prefetchCache.delete(key)
      }
    }
  }

  /**
   * Invalide le cache pour une matière spécifique
   * @param {number} matiereId - ID de la matière
   */
  function invalidatePrefetchCache(matiereId) {
    if (matiereId) {
      const cacheKey = `themes_notions_${matiereId}`
      prefetchCache.delete(cacheKey)
    }
  }

  /**
   * Nettoie tout le cache de prefetch
   */
  function clearAllPrefetchCache() {
    prefetchCache.clear()
    prefetchInFlight.clear()
  }

  return {
    prefetchThemesNotions,
    prefetchSelectedMatieres,
    prefetchActiveMatiere,
    prefetchQuizByNotion,
    prefetchExercicesByNotion,
    prefetchCoursByNotion,
    prefetchNotionContent,
    cleanupPrefetchCache,
    invalidatePrefetchCache,
    clearAllPrefetchCache
  }
}

