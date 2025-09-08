import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notifications'
import { useXP } from '@/composables/useXP'

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
    
    // Comparer juste les dates (sans l'heure)
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
    
    // Streak valide si connexion hier (1 jour) ou aujourd'hui (0 jour)
    return diffDays <= 1
  }

  /**
   * Met à jour le streak de l'utilisateur
   */
  async function updateStreak() {
    try {
      // Vérifier si déjà traité aujourd'hui
      if (isStreakCheckedToday.value) {
        console.log('Streak deja verifie aujourdhui')
        return { success: true, alreadyChecked: true }
      }

      const today = new Date().toISOString().split('T')[0] // Format YYYY-MM-DD
      const storedLastLogin = localStorage.getItem('lastLoginDate')
      const storedStreak = parseInt(localStorage.getItem('currentStreak') || '0')

      console.log('Verification streak:', { 
        today, 
        storedLastLogin, 
        storedStreak,
        isNewDay: isNewDay(storedLastLogin)
      })

      // Si ce n'est pas un nouveau jour, pas de streak
      if (!isNewDay(storedLastLogin)) {
        isStreakCheckedToday.value = true
        currentStreak.value = storedStreak
        return { success: true, alreadyChecked: true }
      }

      let newStreak = 1 // Par défaut, redémarrer à 1

      // Si la streak précédente est encore valide, l'incrémenter
      if (isStreakValid(storedLastLogin)) {
        newStreak = storedStreak + 1
      }

      // Calculer les XP à gagner
      const xpToGain = calculateStreakXP(newStreak)

      console.log('Nouveau streak:', { 
        newStreak, 
        xpToGain,
        wasValid: isStreakValid(storedLastLogin)
      })

      // Mettre à jour les données locales
      currentStreak.value = newStreak
      lastLoginDate.value = today
      isStreakCheckedToday.value = true

      // Sauvegarder dans localStorage
      localStorage.setItem('currentStreak', newStreak.toString())
      localStorage.setItem('lastLoginDate', today)
      localStorage.setItem('streakCheckedToday', 'true')

      // Donner les XP à l'utilisateur
      if (xpToGain > 0) {
        await updateUserXPInstantly(xpToGain, 'streak_daily')
      }

      // Afficher la notification
      notificationStore.notifyDailyStreak(newStreak, xpToGain)

      console.log('Streak mis a jour:', { 
        streak: newStreak, 
        xp: xpToGain,
        userXP: userStore.xp 
      })

      return {
        success: true,
        streakDays: newStreak,
        xpGained: xpToGain,
        isNewStreak: newStreak === 1 && !isStreakValid(storedLastLogin)
      }

    } catch (error) {
      console.error('Erreur lors de la mise a jour du streak:', error)
      return { success: false, error }
    }
  }

  /**
   * Initialise le système de streaks depuis le localStorage
   */
  function initializeStreak() {
    try {
      const storedStreak = parseInt(localStorage.getItem('currentStreak') || '0')
      const storedLastLogin = localStorage.getItem('lastLoginDate')
      const checkedToday = localStorage.getItem('streakCheckedToday') === 'true'
      
      currentStreak.value = storedStreak
      lastLoginDate.value = storedLastLogin
      
      // Vérifier si c'est un nouveau jour
      if (isNewDay(storedLastLogin)) {
        isStreakCheckedToday.value = false
        localStorage.removeItem('streakCheckedToday')
      } else {
        isStreakCheckedToday.value = checkedToday
      }

      console.log('Streak initialise:', {
        streak: currentStreak.value,
        lastLogin: lastLoginDate.value,
        checkedToday: isStreakCheckedToday.value
      })

    } catch (error) {
      console.warn('Erreur initialisation streak:', error)
      currentStreak.value = 0
      lastLoginDate.value = null
      isStreakCheckedToday.value = false
    }
  }

  /**
   * Remet à zéro le streak (pour tests ou reset)
   */
  function resetStreak() {
    currentStreak.value = 0
    lastLoginDate.value = null
    isStreakCheckedToday.value = false
    
    localStorage.removeItem('currentStreak')
    localStorage.removeItem('lastLoginDate')
    localStorage.removeItem('streakCheckedToday')
    
    console.log('Streak remis a zero')
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
