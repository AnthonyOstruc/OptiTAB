import { ref, nextTick } from 'vue'
import { fetchUserGamification, updateUserXP } from '@/api/users'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notifications'
import { calculateUserLevel } from '@/composables/useLevel'

// État global pour les notifications XP
const showXpNotification = ref(false)
const xpGained = ref(0)
const xpMessage = ref('')

/**
 * Composable pour gérer le système d'XP
 */
export function useXP() {
  const userStore = useUserStore()
  const notificationStore = useNotificationStore()

  /**
   * Affiche une notification XP
   */
  function showXpGain(xp = 0, message = 'XP gagné !') {
    xpGained.value = xp
    xpMessage.value = message
    showXpNotification.value = true
  }

  /**
   * Masque la notification XP
   */
  function hideXpNotification() {
    showXpNotification.value = false
    xpGained.value = 0
    xpMessage.value = ''
  }

  /**
   * Rafraîchit les données de gamification de l'utilisateur
   */
  async function refreshUserXP(skipStoreUpdate = false) {
    try {
      const response = await fetchUserGamification()
      // Supporte les deux formats possibles: { success, data: {...} } ou directement {...}
      const payload = response?.data?.data || response?.data || null
      if (payload) {
        const oldXp = Number(userStore.xp || 0)

        // Lire en toute sécurité, sinon conserver les valeurs actuelles
        const newXp = Number(payload.xp ?? userStore.xp ?? 0)
        const levelFromApi = payload.level
        const xpToNextFromApi = payload.xp_to_next ?? payload.next_level_xp ?? null

        // Calculer le niveau avec la même logique que le backend si non fourni
        const computed = calculateUserLevel(newXp)
        const newLevel = Number(levelFromApi ?? computed.level)
        const newXpToNext = Number(xpToNextFromApi ?? computed.xp_to_next)

        // Mettre à jour le store seulement si demandé (éviter d'écraser une mise à jour instantanée)
        if (!skipStoreUpdate) {
          userStore.xp = newXp
          userStore.level = newLevel
          userStore.xp_to_next = newXpToNext
        }

        // Calculer les XP gagnés
        const gainedXp = newXp - oldXp

        console.log('🎮 XP rafraîchis:', {
          oldXp,
          newXp,
          gainedXp,
          level: newLevel,
          xp_to_next: newXpToNext,
          skipStoreUpdate
        })

        return {
          success: true,
          gainedXp,
          newXp,
          newLevel,
          newXpToNext
        }
      }
    } catch (error) {
      console.warn('⚠️ Erreur lors du rafraîchissement des XP:', error)
      return {
        success: false,
        error
      }
    }
  }

  /**
   * Met à jour instantanément le store utilisateur avec de nouveaux XP
   */
  async function updateUserXPInstantly(xpDelta, reason = 'streak_daily') {
    if (xpDelta === null || xpDelta === undefined) return { success: false }

    const oldXp = Number(userStore.xp || 0)
    const oldLevel = Number(userStore.level || 0)
    const newXp = oldXp + Number(xpDelta)

    // Calculer le nouveau niveau avec la même logique que le backend
    const { level: newLevel, xp_to_next: newXpToNext } = calculateUserLevel(newXp)

    // Mettre à jour le store immédiatement
    userStore.xp = newXp
    userStore.level = newLevel
    userStore.xp_to_next = newXpToNext

    // Forcer la réactivité Vue pour s'assurer que les computed se mettent à jour
    await nextTick()

    // Synchroniser avec le backend en arrière-plan
    try {
      await updateUserXP({
        xp_delta: xpDelta,
        reason: reason
      })
      console.log('✅ XP synchronisé avec le backend:', { xpDelta, reason })
    } catch (error) {
      console.warn('⚠️ Erreur synchronisation XP avec backend:', error)
      // Continuer même si la synchronisation échoue
    }

    // Vérifier s'il y a une montée de niveau
    const levelUp = newLevel > oldLevel

    console.log('📊 XP instantané:', { oldXp, newXp, oldLevel, newLevel, levelUp })

    // Notification de montée de niveau
    if (levelUp) {
      notificationStore.notifyLevelUp(newLevel, newXp, newXpToNext)
    }

    return {
      success: true,
      oldXp,
      newXp,
      oldLevel,
      newLevel,
      levelUp
    }
  }

  /**
   * Gère la complétion d'un quiz avec notification XP
   */
  async function handleQuizCompletion(quizId, xpDelta, attempt = 1, quizTitle = 'Quiz') {
    // Notification de gain d'XP (moderne dans le header)
    notificationStore.notifyXPGained(xpDelta, quizTitle, attempt)

    if (xpDelta > 0) {
      // Messages différents selon la tentative (ancienne notification pour compatibilité)
      let message = 'Quiz réussi !'
      if (attempt === 1) {
        message = 'Premier essai réussi !'
      }

      // Afficher l'ancienne notification (peut être supprimée plus tard)
      showXpGain(xpDelta, message)

      // Mettre à jour instantanément les XP (avec vérification de level up)
      const updateResult = await updateUserXPInstantly(xpDelta, 'quiz_completion')

      // Rafraîchir les données réelles en arrière-plan (pour confirmation) sans écraser le store
      const result = await refreshUserXP(true)

      console.log('🎯 Quiz XP:', { quizId, xpGained: xpDelta, attempt, result, updateResult })

      return result
    } else if (attempt > 1) {
      // Afficher une notification pour les tentatives sans XP (ancienne pour compatibilité)
      showXpGain(0, 'Tentative supplémentaire (cooldown 1h30)')
    }

    return { success: true, gainedXp: 0 }
  }

  return {
    // État réactif
    showXpNotification,
    xpGained,
    xpMessage,

    // Méthodes
    showXpGain,
    hideXpNotification,
    refreshUserXP,
    updateUserXPInstantly,
    handleQuizCompletion
  }
}
