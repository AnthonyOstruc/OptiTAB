import { ref, computed } from 'vue'
import { getStatuses, createStatus, updateStatus, deleteStatus } from '@/api'
import { useNotificationStore } from '@/stores/notifications'

/**
 * Composable pour gérer les statuts d'exercices de manière centralisée
 * Les exercices guidés ne donnent PAS d'XP (seuls les quiz en donnent)
 */
export function useExerciseStatus() {
  const notificationStore = useNotificationStore()
  
  // État réactif
  const statusMap = ref({})
  const isLoadingStatuses = ref(false)
  const statusError = ref('')

  /**
   * Charge tous les statuts d'exercices depuis l'API
   */
  async function loadStatuses() {
    isLoadingStatuses.value = true
    statusError.value = ''
    
    try {
      const { data: stats } = await getStatuses()
      const list = Array.isArray(stats) ? stats : (stats?.results || [])
      
      statusMap.value = Object.fromEntries(
        list.map(s => [
          s.exercice,
          { 
            status: s.est_correct ? 'acquired' : 'not_acquired', 
            id: s.id 
          }
        ])
      )
      
      console.log('📊 Statuts chargés:', Object.keys(statusMap.value).length)
      return statusMap.value
    } catch (error) {
      console.error('❌ Erreur chargement statuts:', error)
      statusError.value = 'Impossible de charger les statuts'
      throw error
    } finally {
      isLoadingStatuses.value = false
    }
  }

  /**
   * Met à jour le statut d'un exercice
   */
  async function updateExerciseStatus(exerciceId, status) {
    if (!exerciceId) {
      throw new Error('ID exercice requis')
    }

    try {
      const wasAlreadyCompleted = !!statusMap.value[exerciceId]
      
      if (status) {
        const existingStatus = statusMap.value[exerciceId]
        
        if (existingStatus) {
          // Mettre à jour le statut existant
          await updateStatus(existingStatus.id, {
            exercice: exerciceId,
            reponse_donnee: status,
            est_correct: status === 'acquired'
          })
          
          // Mettre à jour le statut local
          statusMap.value[exerciceId] = { 
            status, 
            id: existingStatus.id 
          }
        } else {
          // Créer un nouveau statut
          const response = await createStatus({
            exercice: exerciceId,
            reponse_donnee: status,
            est_correct: status === 'acquired',
            points_obtenus: status === 'acquired' ? 1 : 0,
            temps_seconde: 0
          })
          
          const newId = response?.data?.id || response?.id
          statusMap.value[exerciceId] = { status, id: newId }

          // Si c'est un nouveau succès, vérifier les débloquages
          if (status === 'acquired' && !wasAlreadyCompleted) {
            await checkForUnlockedExercises(exerciceId)
          }
        }
      } else {
        // Supprimer le statut
        const existingStatus = statusMap.value[exerciceId]
        
        if (existingStatus) {
          await deleteStatus(existingStatus.id)
        }
        
        delete statusMap.value[exerciceId]
      }

      // Les exercices guidés ne donnent pas d'XP (seuls les quiz en donnent)

      console.log('✅ Statut mis à jour:', { exerciceId, status, wasAlreadyCompleted })
      
    } catch (error) {
      console.error('❌ Erreur mise à jour statut:', error)
      
      // En cas d'erreur, mettre à jour le statut local quand même
      if (status) {
        statusMap.value[exerciceId] = { status, id: null }
      } else {
        delete statusMap.value[exerciceId]
      }
      
      throw error
    }
  }

  /**
   * Récupère le statut d'un exercice
   */
  function getExerciseStatus(exerciceId) {
    return statusMap.value[exerciceId]?.status || null
  }

  /**
   * Vérifie si un exercice est acquis
   */
  function isExerciseAcquired(exerciceId) {
    return statusMap.value[exerciceId]?.status === 'acquired'
  }

  /**
   * Vérifie si un exercice a un statut (acquis ou non acquis)
   */
  function hasExerciseStatus(exerciceId) {
    return !!statusMap.value[exerciceId]
  }

  /**
   * Compte les exercices par statut
   */
  const statusCounts = computed(() => {
    const counts = {
      acquired: 0,
      not_acquired: 0,
      total: 0
    }
    
    Object.values(statusMap.value).forEach(({ status }) => {
      if (status === 'acquired') counts.acquired++
      else if (status === 'not_acquired') counts.not_acquired++
      counts.total++
    })
    
    return counts
  })

  /**
   * Filtre les exercices par statut
   */
  function filterExercisesByStatus(exercices, statusFilter) {
    if (!Array.isArray(exercices)) return []
    
    switch (statusFilter) {
      case 'acquired':
        return exercices.filter(e => isExerciseAcquired(e.id))
      case 'not_acquired':
        return exercices.filter(e => 
          statusMap.value[e.id]?.status === 'not_acquired'
        )
      case 'done':
        return exercices.filter(e => hasExerciseStatus(e.id))
      case 'all':
        return exercices.filter(e => !hasExerciseStatus(e.id))
      default:
        return exercices
    }
  }

  /**
   * Réinitialise tous les statuts
   */
  function resetStatuses() {
    statusMap.value = {}
    statusError.value = ''
  }

  /**
   * Vérifie si de nouveaux exercices sont débloqués suite à la complétion d'un exercice
   */
  async function checkForUnlockedExercises(completedExerciceId) {
    try {
      // Dans un vrai système, vous pourriez avoir une API pour vérifier les débloquages
      // Pour l'instant, on simule une logique simple : 
      // Chaque exercice complété peut débloquer l'exercice suivant dans le même chapitre
      
      // Cette fonction peut être étendue pour appeler une API backend qui retourne
      // les exercices nouvellement débloqués
      console.log('🔍 Vérification des débloquages pour exercice:', completedExerciceId)
      
      // Exemple de notification (à adapter selon votre logique métier)
      // notificationStore.notifyExerciseUnlocked(
      //   'Exercice suivant', 
      //   'Chapitre actuel'
      // )
      
    } catch (error) {
      console.warn('⚠️ Erreur lors de la vérification des débloquages:', error)
    }
  }

  /**
   * Notifie manuellement qu'un exercice a été débloqué
   */
  function notifyExerciseUnlocked(exerciseTitle, chapterTitle) {
    notificationStore.notifyExerciseUnlocked(exerciseTitle, chapterTitle)
  }

  /**
   * Notifie qu'un chapitre a été complété
   */
  function notifyChapterCompleted(chapterTitle, completionRate) {
    notificationStore.notifyChapterCompleted(chapterTitle, completionRate)
  }

  return {
    // État réactif
    statusMap,
    isLoadingStatuses,
    statusError,
    statusCounts,
    
    // Méthodes principales
    loadStatuses,
    updateExerciseStatus,
    
    // Méthodes utilitaires
    getExerciseStatus,
    isExerciseAcquired,
    hasExerciseStatus,
    filterExercisesByStatus,
    resetStatuses,
    
    // Notifications
    checkForUnlockedExercises,
    notifyExerciseUnlocked,
    notifyChapterCompleted
  }
}
