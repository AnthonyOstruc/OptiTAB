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
 * Met à jour le mot de passe de l'utilisateur connecté.
 * Expects: { current_password, new_password, confirm_password }
 */
export const changeUserPassword = (payload) => apiClient.post('/api/users/me/change-password/', payload)

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
 * Met à jour le rôle de l'utilisateur connecté (student/parent).
 * Expects: role (string) - 'student' ou 'parent'
 */
export const updateUserRole = (role) => apiClient.patch('/api/users/me/update/', { role })

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

// Streak supprimé

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
 * Invitations parentales côté élève
 */
export const fetchParentInvitations = () => apiClient.get('/api/users/me/parent-invitations/')
export const respondParentInvitation = (invitationId, action) =>
  apiClient.post(`/api/users/me/parent-invitations/${invitationId}/respond/`, { action })

/**
 * Met à jour les XP de l'utilisateur connecté.
 * Expects: { xp_delta: number, reason: string }
 */
export const updateUserXP = (payload) => apiClient.post('/api/users/me/update-xp/', payload)

/**
 * Déclenche la récompense quotidienne de connexion (+1 XP) et met à jour la streak.
 * Idempotent côté backend pour la journée courante.
 */
export const triggerDailyLogin = () => apiClient.post('/api/users/me/daily-login/')

// Notifications persistantes
export const fetchNotifications = (params = {}) => apiClient.get('/api/users/notifications/', { params })
export const createNotification = async (payload) => {
  // payload: { type, title, message, data }
  return apiClient.post('/api/users/notifications/', payload)
}
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
export const sendEmailVerificationLink = () => apiClient.post('/api/users/email/send-code/')
export const verifyEmailCode = (code) => apiClient.post('/api/users/email/verify-code/', { code })
export const requestEmailChange = (email) => apiClient.post('/api/users/email/change/', { email })

/**
 * Vérifie si un email correspond à un compte actif.
 * Returns: { exists: boolean, first_name?: string, last_name?: string }
 */
export const checkEmailExists = (email) => apiClient.post('/api/users/check-email-exists/', { email })

/**
 * Crée un compte enfant (pour les parents)
 * payload: { email, first_name, last_name, pays_id?, niveau_pays_id? }
 */
export const createChildAccount = (payload) => apiClient.post('/api/users/me/children/create/', payload)
