import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notifications'
import { useXP } from '@/composables/useXP'
import { fetchMyStreaks, fetchUserGamification } from '@/api/users'

/**
 * Composable pour gérer le système de streaks quotidiens
 * Compte les JOURS CONSECUTIFS où l'utilisateur ouvre le site (pas les connexions)
 * Logique XP : 1er jour = 1 XP, 2ème = 2 XP, ..., 5ème = 5 XP, puis 5 XP constant
 */
export function useStreak() {
  const userStore = useUserStore()
  const notificationStore = useNotificationStore()
  const { updateUserXPInstantly } = useXP()

  // État des streaks
  const currentStreak = ref(0)
  const lastLoginDate = ref(null)
  const isStreakCheckedToday = ref(false)

  /**
   * Calcule les XP à gagner selon le nombre de jours de streak
   */
  function calculateStreakXP(streakDays) {
    if (streakDays <= 0) return 0
    if (streakDays <= 5) return streakDays // 1, 2, 3, 4, 5 XP
    return 5 // 5 XP constant au-delà du 5ème jour
  }

  /**
   * Vérifie si c'est un nouveau jour depuis la dernière connexion
   */
  function isNewDay(lastDate) {
    if (!lastDate) return true
    const today = new Date()
    const last = new Date(lastDate)
    const todayStr = today.toDateString()
    const lastStr = last.toDateString()
    return todayStr !== lastStr
  }

  /**
   * Vérifie si la streak est encore valide (connexion hier ou aujourd'hui)
   */
  function isStreakValid(lastDate) {
    if (!lastDate) return false
    const today = new Date()
    const last = new Date(lastDate)
    const diffTime = today - last
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
    return diffDays <= 1
  }

  /**
   * Met à jour le streak de l'utilisateur
   */
  async function updateStreak() {
    // Server authoritative refresh: fetch from backend, which also awards XP if increased
    try {
      if (!userStore.isAuthenticated) {
        return { success: false, reason: 'not_authenticated' }
      }

      const res = await fetchMyStreaks()
      const payload = res?.data?.data || res?.data || null
      if (!payload) {
        return { success: false, error: 'no_payload' }
      }

      // Update local state from server
      currentStreak.value = Number(payload.current_streak || 0)
      isStreakCheckedToday.value = true

      // Optionally refresh gamification to reflect XP awarded on server
      try {
        const g = await fetchUserGamification()
        const gData = g?.data?.data || g?.data
        if (gData && typeof gData.xp === 'number') {
          userStore.xp = Number(gData.xp)
        }
      } catch (_) {}

      // Client-side notification for visibility
      const xpToGain = calculateStreakXP(currentStreak.value)
      notificationStore.notifyDailyStreak(currentStreak.value, xpToGain)

      return { success: true, streakDays: currentStreak.value }
    } catch (error) {
      console.error('Erreur lors de la mise a jour du streak (server):', error)
      return { success: false, error }
    }
  }

  /**
   * Initialise le système de streaks depuis le localStorage
   */
  async function initializeStreak() {
    // Initialize from server for cross-device consistency
    if (!userStore.isAuthenticated) {
      currentStreak.value = 0
      isStreakCheckedToday.value = false
      return
    }
    try {
      const res = await fetchMyStreaks()
      const payload = res?.data?.data || res?.data || null
      if (payload) {
        currentStreak.value = Number(payload.current_streak || 0)
        isStreakCheckedToday.value = true
      }
    } catch (error) {
      // Do not block UI; keep defaults
    }
  }

  /**
   * Remet à zéro le streak (pour tests ou reset)
   */
  function resetStreak() {
    currentStreak.value = 0
    lastLoginDate.value = null
    isStreakCheckedToday.value = false
  }

  /**
   * Vérifie automatiquement le streak à chaque ouverture du site
   */
  async function checkDailyStreak() {
    // Seulement si l'utilisateur est connecté
    if (!userStore.isAuthenticated) {
      console.log('Utilisateur non connecte, pas de verification streak')
      return { success: false, reason: 'not_authenticated' }
    }

    // Initialiser d'abord
    initializeStreak()

    // Puis vérifier/mettre à jour
    return await updateStreak()
  }

  // Computed properties pour l'affichage
  const nextStreakXP = computed(() => {
    return calculateStreakXP(currentStreak.value + 1)
  })

  // XP gagné pour le jour courant (utile pour affichage/test)
  const todayStreakXP = computed(() => {
    return calculateStreakXP(currentStreak.value)
  })

  const streakMessage = computed(() => {
    if (currentStreak.value === 0) return "Connectez-vous quotidiennement pour gagner des XP !"
    if (currentStreak.value <= 5) return `${currentStreak.value} jour${currentStreak.value > 1 ? 's' : ''} de suite ! Prochain: +${nextStreakXP.value} XP`
    return `${currentStreak.value} jours consécutifs ! +5 XP quotidiens`
  })

  return {
    // État
    currentStreak: computed(() => currentStreak.value),
    lastLoginDate: computed(() => lastLoginDate.value),
    isStreakCheckedToday: computed(() => isStreakCheckedToday.value),
    nextStreakXP,
    todayStreakXP,
    streakMessage,

    // Méthodes
    checkDailyStreak,
    updateStreak,
    initializeStreak,
    resetStreak,
    calculateStreakXP,
    isNewDay,
    isStreakValid
  }
}
