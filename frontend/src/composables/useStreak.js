import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notifications'
import { useXP } from '@/composables/useXP'
import { fetchMyStreaks, fetchUserGamification } from '@/api/users'
import apiClient from '@/api/client'

// Shared singleton state so all components see the same streak values
const __currentStreak = ref(0)
const __lastLoginDate = ref(null)
const __isStreakCheckedToday = ref(false)

/**
 * Composable pour gérer le système de streaks quotidiens
 * Compte les JOURS CONSECUTIFS où l'utilisateur ouvre le site (pas les connexions)
 * Logique XP : 1er jour = 1 XP, 2ème = 2 XP, ..., 5ème = 5 XP, puis 5 XP constant
 */
export function useStreak() {
  const userStore = useUserStore()
  const notificationStore = useNotificationStore()
  const { updateUserXPInstantly } = useXP()

  // État partagé des streaks (singleton)
  // Utiliser les refs de module définies ci‑dessus

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

      // Claim today's streak first (idempotent)
      try {
        await apiClient.post('/api/users/me/streaks/claim/')
      } catch (_) {}

      const res = await fetchMyStreaks()
      const payload = res?.data?.data || res?.data || null
      if (!payload) {
        return { success: false, error: 'no_payload' }
      }

      // Update shared state from server
      __currentStreak.value = Number(payload.current_streak || 0)
      __isStreakCheckedToday.value = true

      // Optionally refresh gamification to reflect XP awarded on server
      try {
        const g = await fetchUserGamification()
        const gData = g?.data?.data || g?.data
        if (gData && typeof gData.xp === 'number') {
          userStore.xp = Number(gData.xp)
        }
      } catch (_) {}

      // Client-side notification for visibility
      const xpToGain = calculateStreakXP(__currentStreak.value)
      notificationStore.notifyDailyStreak(__currentStreak.value, xpToGain)

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
      // Claim on app open to ensure up-to-date
      try { await apiClient.post('/api/users/me/streaks/claim/') } catch (_) {}
      const res = await fetchMyStreaks()
      const payload = res?.data?.data || res?.data || null
      if (payload) {
        __currentStreak.value = Number(payload.current_streak || 0)
        __isStreakCheckedToday.value = true
      }
    } catch (error) {
      // Do not block UI; keep defaults
    }
  }

  /**
   * Remet à zéro le streak (pour tests ou reset)
   */
  function resetStreak() {
    __currentStreak.value = 0
    __lastLoginDate.value = null
    __isStreakCheckedToday.value = false
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
    await initializeStreak()

    // Puis vérifier/mettre à jour
    return await updateStreak()
  }

  // Computed properties pour l'affichage
  const nextStreakXP = computed(() => {
    return calculateStreakXP(__currentStreak.value + 1)
  })

  // XP gagné pour le jour courant (utile pour affichage/test)
  const todayStreakXP = computed(() => {
    return calculateStreakXP(__currentStreak.value)
  })

  const streakMessage = computed(() => {
    if (__currentStreak.value === 0) return "Connectez-vous quotidiennement pour gagner des XP !"
    if (__currentStreak.value <= 5) return `${__currentStreak.value} jour${__currentStreak.value > 1 ? 's' : ''} de suite ! Prochain: +${nextStreakXP.value} XP`
    return `${__currentStreak.value} jours consécutifs ! +5 XP quotidiens`
  })

  return {
    // État
    currentStreak: computed(() => __currentStreak.value),
    lastLoginDate: computed(() => __lastLoginDate.value),
    isStreakCheckedToday: computed(() => __isStreakCheckedToday.value),
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
