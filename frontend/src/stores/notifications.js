import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { fetchNotifications, markNotificationRead, markAllNotificationsRead as apiMarkAllRead } from '@/api/users'

export const useNotificationStore = defineStore('notifications', () => {
  // État des notifications
  const notifications = ref([])
  const nextId = ref(1)

  // Computed pour les notifications non lues
  const unreadCount = computed(() => {
    return notifications.value.filter(n => !n.read).length
  })

  const hasUnread = computed(() => unreadCount.value > 0)

  // Types de notifications
  const NOTIFICATION_TYPES = {
    XP_GAINED: 'xp_gained',
    LEVEL_UP: 'level_up', 
    EXERCISE_UNLOCKED: 'exercise_unlocked',
    CHAPTER_COMPLETED: 'chapter_completed',
    ACHIEVEMENT: 'achievement',
    DAILY_STREAK: 'daily_streak'
  }

  // Durées d'affichage (en ms)
  const DISPLAY_DURATION = {
    XP_GAINED: 4000,
    LEVEL_UP: 6000,
    EXERCISE_UNLOCKED: 5000,
    CHAPTER_COMPLETED: 5000,
    ACHIEVEMENT: 7000,
    DAILY_STREAK: 5000
  }

  /**
   * Ajoute une nouvelle notification
   */
  function addNotification({
    type,
    title,
    message,
    data = {},
    autoRemove = false // Changé : par défaut les notifications restent jusqu'à suppression manuelle
  }) {
    const notification = {
      id: nextId.value++,
      type,
      title,
      message,
      data,
      read: false,
      timestamp: new Date(),
      autoRemove
    }

    notifications.value.unshift(notification)

    // Auto-suppression désactivée par défaut
    // Les utilisateurs doivent supprimer manuellement leurs notifications
    if (autoRemove) {
      const duration = DISPLAY_DURATION[type] || 5000
      setTimeout(() => {
        removeNotification(notification.id)
      }, duration)
    }

    console.log('🔔 Nouvelle notification:', notification)
    return notification
  }

  /**
   * Notifications spécialisées
   */
  function notifyXPGained(xpAmount, quizTitle, attempt = 1) {
    const isFirstAttempt = attempt === 1
    const title = isFirstAttempt ? '🎉 XP Gagnés !' : '🔄 Tentative Supplémentaire'
    
    let message
    if (isFirstAttempt && xpAmount > 0) {
      message = `+${xpAmount} XP pour "${quizTitle}"`
    } else {
      message = `Quiz "${quizTitle}" terminé (cooldown 1h30)`
    }

    return addNotification({
      type: NOTIFICATION_TYPES.XP_GAINED,
      title,
      message,
      data: { xpAmount, quizTitle, attempt, isFirstAttempt }
    })
  }

  function notifyLevelUp(newLevel, totalXP, xpToNext) {
    return addNotification({
      type: NOTIFICATION_TYPES.LEVEL_UP,
      title: '🏆 Niveau Supérieur !',
      message: `Félicitations ! Vous êtes maintenant niveau ${newLevel}`,
      data: { newLevel, totalXP, xpToNext }
      // autoRemove: false par défaut maintenant
    })
  }

  function notifyExerciseUnlocked(exerciseTitle, chapterTitle) {
    return addNotification({
      type: NOTIFICATION_TYPES.EXERCISE_UNLOCKED,
      title: '🔓 Nouvel Exercice !',
      message: `"${exerciseTitle}" disponible dans ${chapterTitle}`,
      data: { exerciseTitle, chapterTitle }
    })
  }

  function notifyChapterCompleted(chapterTitle, completionRate) {
    return addNotification({
      type: NOTIFICATION_TYPES.CHAPTER_COMPLETED,
      title: '✅ Chapitre Terminé !',
      message: `"${chapterTitle}" complété à ${completionRate}%`,
      data: { chapterTitle, completionRate }
    })
  }

  function notifyAchievement(title, description, icon = '🏅') {
    return addNotification({
      type: NOTIFICATION_TYPES.ACHIEVEMENT,
      title: `${icon} Réussite Débloquée !`,
      message: `${title}: ${description}`,
      data: { achievementTitle: title, description, icon }
      // autoRemove: false par défaut maintenant
    })
  }

  function notifyDailyStreak(streakDays, xpGained) {
    const getStreakMessage = (days) => {
      if (days === 1) return "Première connexion aujourd'hui !"
      if (days <= 5) return `${days} jours consécutifs ! Bravo !`
      return `${days} jours de suite ! Incroyable série !`
    }

    const getStreakIcon = (days) => {
      if (days === 1) return '🌟'
      if (days === 2) return '⭐'
      if (days === 3) return '🔥'
      if (days === 4) return '💫'
      if (days >= 5) return '🏆'
      return '🌟'
    }

    return addNotification({
      type: NOTIFICATION_TYPES.DAILY_STREAK,
      title: `${getStreakIcon(streakDays)} Série Quotidienne !`,
      message: `${getStreakMessage(streakDays)} +${xpGained} XP`,
      data: { streakDays, xpGained }
    })
  }

  /**
   * Marque une notification comme lue
   */
  async function markAsRead(notificationId) {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.read = true
      // Persister côté backend
      try { 
        await markNotificationRead(notificationId) 
      } catch (error) {
        console.warn('⚠️ Erreur lors du marquage comme lu:', error)
      }
    }
  }

  /**
   * Marque toutes les notifications comme lues
   */
  async function markAllAsRead() {
    notifications.value.forEach(n => n.read = true)
    try { 
      const result = await apiMarkAllRead() 
      console.log('✅ Notifications marquées comme lues:', result.count)
    } catch (error) {
      console.warn('⚠️ Erreur lors du marquage en masse:', error)
    }
  }

  /**
   * Supprime une notification
   */
  function removeNotification(notificationId) {
    const index = notifications.value.findIndex(n => n.id === notificationId)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  /**
   * Vide toutes les notifications
   */
  function clearAll() {
    notifications.value = []
  }

  /**
   * Supprime les notifications anciennes (garde les 20 plus récentes)
   */
  function cleanupOld() {
    if (notifications.value.length > 20) {
      notifications.value = notifications.value
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        .slice(0, 20)
    }
  }

  return {
    // État
    notifications: computed(() => notifications.value),
    unreadCount,
    hasUnread,
    NOTIFICATION_TYPES,

    // Chargement serveur
    loadFromServer: async () => {
      try {
        const res = await fetchNotifications()
        const list = Array.isArray(res?.data) ? res.data : (res?.data?.results || [])
        notifications.value = list.map(n => ({
          id: n.id,
          type: n.type,
          title: n.title,
          message: n.message,
          data: n.data || {},
          read: !!n.read,
          timestamp: n.created_at ? new Date(n.created_at) : new Date()
        }))
        const maxServerId = list.reduce((m, n) => Math.max(m, Number(n.id || 0)), 0)
        nextId.value = Math.max(nextId.value, maxServerId + 1)
      } catch (e) {
        console.warn('⚠️ Impossible de charger les notifications:', e)
      }
    },

    // Actions génériques
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
    cleanupOld,

    // Actions spécialisées
    notifyXPGained,
    notifyLevelUp,
    notifyExerciseUnlocked,
    notifyChapterCompleted,
    notifyAchievement,
    notifyDailyStreak
  }
})
