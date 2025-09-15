import apiClient from './client'

/**
 * Récupère le profil utilisateur à partir du token d'auth.
 */
export const fetchUserProfile = () => apiClient.get('/api/users/me/')

/**
 * Met à jour le profil utilisateur connecté.
 * Expects: { first_name, last_name, civilite, phone, birth_date, ... }
 */
export const updateUserProfile = (payload) => apiClient.patch('/api/users/me/update/', payload)

/**
 * Met à jour le niveau de l'utilisateur connecté.
 * Expects: niveau_id (number)
 */
export const updateUserNiveau = (niveauId) => apiClient.patch('/api/users/me/niveau/', { niveau_pays_id: niveauId }) 

/**
 * Met à jour le pays de l'utilisateur connecté.
 * Expects: pays_id (number)
 */
export const updateUserPays = (paysId) => apiClient.patch('/api/users/me/pays/', { pays_id: paysId }) 

/**
 * Met à jour le pays et niveau de l'utilisateur connecté.
 * Expects: { pays_id, niveau_id }
 */
export const updateUserPaysNiveau = (paysOrPayload, maybeNiveauId) => {
  // Supporte deux signatures:
  // 1) updateUserPaysNiveau({ pays_id, niveau_id | niveau_pays_id })
  // 2) updateUserPaysNiveau(paysId, niveauId)
  let pays_id
  let niveau_id

  if (typeof paysOrPayload === 'object' && paysOrPayload !== null) {
    pays_id = paysOrPayload.pays_id ?? paysOrPayload.pays
    niveau_id = paysOrPayload.niveau_id ?? paysOrPayload.niveau_pays_id ?? paysOrPayload.niveau
  } else {
    pays_id = paysOrPayload
    niveau_id = maybeNiveauId
  }

  return apiClient.patch('/api/users/me/pays-niveau/', {
    pays_id,
    niveau_pays_id: niveau_id
  })
}

/**
 * Récupère les infos de gamification (xp, level, xp_to_next)
 */
export const fetchUserGamification = () => apiClient.get('/api/users/me/gamification/')

/**
 * Récupère le leaderboard (classement) des utilisateurs.
 * params: { scope?: 'global'|'pays'|'niveau', limit?: number }
 */
export const fetchLeaderboard = (params = {}) => {
  const scope = params.scope || 'global'
  const limit = params.limit || 20
  return apiClient.get('/api/users/leaderboard/', { params: { scope, limit } })
}

/**
 * Vue d'ensemble élève courant (KPIs, tendance, activités, répartition)
 */
export const fetchMyOverview = () => apiClient.get('/api/users/me/overview/')

/**
 * Streaks élève courant (streak actuel, meilleur, heatmap)
 */
export const fetchMyStreaks = () => apiClient.get('/api/users/me/streaks/')

/**
 * Recommandations (révision due, exercice non tenté, ...)
 */
export const fetchRecommendations = () => apiClient.get('/api/users/me/recommendations/')

/**
 * Récupère les enfants rattachés au parent connecté.
 */
export const fetchMyChildren = () => apiClient.get('/api/users/me/children/')

/**
 * Ajoute un enfant au compte parent (par email ou child_id)
 * payload: { email?: string, child_id?: number }
 */
export const addChild = (payload) => apiClient.post('/api/users/me/children/add/', payload)

/**
 * Retire un enfant du compte parent
 */
export const removeChild = (childId) => apiClient.delete(`/api/users/me/children/${childId}/remove/`)

/**
 * Met à jour les XP de l'utilisateur connecté.
 * Expects: { xp_delta: number, reason: string }
 */
export const updateUserXP = (payload) => apiClient.post('/api/users/me/update-xp/', payload)

// Notifications persistantes
export const fetchNotifications = (params = {}) => apiClient.get('/api/users/notifications/', { params })
export const markNotificationRead = async (id) => {
  try {
    return await apiClient.patch(`/api/users/notifications/${id}/`, { read: true })
  } catch (error) {
    // Si la notification n'existe plus (404) ou autre erreur, on ignore silencieusement
    console.warn(`⚠️ Impossible de marquer la notification ${id} comme lue:`, error.response?.status || error.message)
    return { success: false, error: error.response?.status || 'unknown' }
  }
}
export const markAllNotificationsRead = async () => {
  // Backend n'a pas d'endpoint bulk: faire en parallèle côté client
  const res = await fetchNotifications({ unread: 1 })
  const list = res?.data || []
  const results = await Promise.allSettled(list.map(n => markNotificationRead(n.id)))
  const successful = results.filter(r => r.status === 'fulfilled' && r.value.success !== false).length
  return { count: successful }
}
export const deleteNotification = async (id) => {
  try {
    return await apiClient.delete(`/api/users/notifications/${id}/`)
  } catch (error) {
    // Si la notification n'existe plus (404) ou autre erreur, on ignore silencieusement
    console.warn(`⚠️ Impossible de supprimer la notification ${id}:`, error.response?.status || error.message)
    return { success: false, error: error.response?.status || 'unknown' }
  }
}
export const deleteAllNotifications = async () => {
  const res = await fetchNotifications()
  const list = res?.data || []
  const results = await Promise.allSettled(list.map(n => deleteNotification(n.id)))
  const successful = results.filter(r => r.status === 'fulfilled' && r.value.success !== false).length
  return { count: successful }
}

// Email verification
export const sendEmailVerificationCode = () => apiClient.post('/api/users/email/send-code/')
export const verifyEmailCode = (code) => apiClient.post('/api/users/email/verify-code/', { code })