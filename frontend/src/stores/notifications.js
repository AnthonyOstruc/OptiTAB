import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { fetchNotifications, markNotificationRead, markAllNotificationsRead as apiMarkAllRead, createNotification } from '@/api/users'
import { useUserStore } from '@/stores/user'

export const useNotificationStore = defineStore('notifications', () => {
  // État des notifications
  const notifications = ref([])
  const nextId = ref(1)
  const userStore = useUserStore()

  // Clé de stockage local par utilisateur pour persistance
  const getStorageKey = () => `optitab_notifications_${userStore?.id || 'guest'}`

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
    ACHIEVEMENT: 'achievement'
  }

  // Durées d'affichage (en ms)
  const DISPLAY_DURATION = {
    XP_GAINED: 4000,
    LEVEL_UP: 6000,
    EXERCISE_UNLOCKED: 5000,
    CHAPTER_COMPLETED: 5000,
    ACHIEVEMENT: 7000
  }

  /**
   * Ajoute une nouvelle notification
   */
  async function addNotification({
    type,
    title,
    message,
    data = {},
    autoRemove = false, // Changé : par défaut les notifications restent jusqu'à suppression manuelle
    persist = false, // Nouveau: persister côté backend
    persistLocally = true // Nouveau: persister dans localStorage
  }) {
    const notification = {
      id: nextId.value++,
      type,
      title,
      message,
      data,
      read: false,
      timestamp: new Date(),
      autoRemove,
      _persistLocally: !!persistLocally
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

    // Persistance côté serveur optionnelle
    if (persist && userStore?.isAuthenticated) {
      try {
        const res = await createNotification({
          type,
          title,
          message,
          data
        })
        const server = res?.data
        if (server && server.id) {
          // Remplacer l'ID local par l'ID serveur pour éviter les doublons au merge
          notification.id = Number(server.id)
          notification.timestamp = server.created_at ? new Date(server.created_at) : notification.timestamp
        }
      } catch (e) {
        console.warn('⚠️ Échec persistance notification serveur, conserve localement:', e?.response?.status || e?.message)
      }
    }

    console.log('🔔 Nouvelle notification:', notification)
    return notification
  }

  /**
   * Notifications spécialisées
   */
  async function notifyXPGained(xpAmount, quizTitle, attempt = 1) {
    const isFirstAttempt = attempt === 1
    // Ne pas notifier pour les tentatives > 1
    if (!isFirstAttempt) return null

    const title = '🎉 XP Gagnés !'
    
    let message
    if (isFirstAttempt && xpAmount > 0) {
      message = `+${xpAmount} XP pour "${quizTitle}"`
    } else {
      message = `Quiz "${quizTitle}" terminé (aucun XP)`
    }

    // Persistance côté serveur:
    // - Premier essai avec XP > 0: déjà créé côté backend via /me/update-xp/ → ne pas dupliquer
    // - Premier essai avec XP = 0: persister explicitement côté serveur
    const persist = (xpAmount <= 0)

    return await addNotification({
      type: NOTIFICATION_TYPES.XP_GAINED,
      title,
      message,
      data: { xpAmount, quizTitle, attempt, isFirstAttempt },
      persist,
      // Ne pas persister dans localStorage (on s'appuie sur la BDD, évite tout doublon au refresh)
      persistLocally: false
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

  // Streak supprimé

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

  // Persistance automatique locale à chaque changement
  watch(
    notifications,
    (list) => {
      try {
        const payload = list
          .filter(n => n._persistLocally !== false)
          .map(n => ({
            id: n.id,
            type: n.type,
            title: n.title,
            message: n.message,
            data: n.data || {},
            read: !!n.read,
            timestamp: n.timestamp instanceof Date ? n.timestamp.toISOString() : n.timestamp
          }))
        localStorage.setItem(getStorageKey(), JSON.stringify(payload))
      } catch (e) {
        // silencieux
      }
    },
    { deep: true }
  )

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
        // Construire les notifs serveur
        const serverItems = list.map(n => ({
          id: Number(n.id),
          type: n.type,
          title: n.title,
          message: n.message,
          data: n.data || {},
          read: !!n.read,
          timestamp: n.created_at ? new Date(n.created_at) : new Date()
        }))
        // Fusionner avec les notifs locales existantes (sans écraser)
        const existing = notifications.value.slice()
        const byId = new Map(existing.map(n => [String(n.id), n]))
        for (const item of serverItems) {
          const key = String(item.id)
          if (!byId.has(key)) {
            existing.push(item)
          } else {
            // Mise à jour lecture/texte si même id
            const old = byId.get(key)
            old.type = item.type
            old.title = item.title
            old.message = item.message
            old.data = item.data
            old.read = item.read
            old.timestamp = item.timestamp
          }
        }
        // Ordonner plus récentes d'abord
        existing.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        notifications.value = existing
        const maxServerId = list.reduce((m, n) => Math.max(m, Number(n.id || 0)), 0)
        nextId.value = Math.max(nextId.value, maxServerId + 1)
      } catch (e) {
        console.warn('⚠️ Impossible de charger les notifications:', e)
      }
    },
    // Chargement local (persistance côté client)
    loadFromLocal: async () => {
      try {
        const raw = localStorage.getItem(getStorageKey())
        if (!raw) return
        const stored = JSON.parse(raw)
        if (!Array.isArray(stored)) return
        const items = stored.map(n => ({
          id: n.id,
          type: n.type,
          title: n.title,
          message: n.message,
          data: n.data || {},
          read: !!n.read,
          timestamp: n.timestamp ? new Date(n.timestamp) : new Date()
        }))
        // Fusion simple avec existant
        const existing = notifications.value.slice()
        const byId = new Map(existing.map(n => [String(n.id), n]))
        for (const it of items) {
          const key = String(it.id)
          if (!byId.has(key)) existing.push(it)
        }
        existing.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        notifications.value = existing
        const maxLocalId = items.reduce((m, n) => Math.max(m, Number(n.id || 0)), 0)
        nextId.value = Math.max(nextId.value, maxLocalId + 1)
      } catch (e) {
        console.warn('⚠️ Impossible de charger les notifications locales:', e)
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
    notifyAchievement
  }
})
