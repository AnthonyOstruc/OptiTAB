import apiClient, { apiUtils } from './client'

// ----- Quiz QCM -----
// Remarque: le backend monte le router sous /api/quiz/ + register('quiz') → endpoints réels: /api/quiz/quiz/
// Désormais filtrage par notion directement (suppression chapitres)
export const getQuiz = (notionId) => apiClient.get(`/api/quiz/quiz/?notion=${notionId}`)
export const getQuizAdmin = () => apiClient.get('/api/quiz/quiz/')
export const createQuiz = (payload) => apiClient.post('/api/quiz/quiz/', payload)
export const updateQuiz = (id, payload) => apiClient.patch(`/api/quiz/quiz/${id}/`, payload)
export const deleteQuiz = (id) => apiClient.delete(`/api/quiz/quiz/${id}/`) 

/**
 * Récupère les quiz pour l'utilisateur connecté (selon son pays et niveau)
 * @returns {Promise<Array>} Liste des quiz de l'utilisateur
 */
export const getQuizPourUtilisateur = async () => {
  try {
    const response = await apiClient.get('/api/quiz/pour-utilisateur/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des quiz pour utilisateur:', error)
    throw error
  }
}

/**
 * Soumet le résultat d'un quiz pour la gamification
 * @param {Object} quizResult - Résultat du quiz
 * @param {number} quizResult.quiz_id - ID du quiz
 * @param {number} quizResult.score - Score obtenu
 * @param {number} quizResult.total_points - Total des points possibles
 * @param {number} quizResult.temps_total_seconde - Temps total en secondes
 * @returns {Promise<Object>} Réponse avec les XP gagnés
 */
export const submitQuizResult = async (quizResult) => {
  try {
    console.log('📤 Envoi des données quiz:', {
      quiz: quizResult.quiz_id,
      score: quizResult.score,
      total_points: quizResult.total_points,
      temps_total_seconde: quizResult.temps_total_seconde
    })
    
    const response = await apiClient.post('/api/suivis/quiz/', {
      quiz: quizResult.quiz_id,
      score: quizResult.score,
      total_points: quizResult.total_points,
      temps_total_seconde: quizResult.temps_total_seconde
    })
    
    console.log('📥 Réponse reçue:', response.data)
    return response.data
  } catch (error) {
    console.error('❌ Erreur lors de la soumission du résultat de quiz:', error)
    console.error('❌ Détails de l\'erreur:', error.response?.data)
    console.error('❌ Status de l\'erreur:', error.response?.status)
    throw error
  }
}

/**
 * Récupère l'historique des tentatives pour un quiz
 * @param {number} quizId - ID du quiz
 * @returns {Promise<Array>} Liste des tentatives
 */
export const getQuizAttempts = async (quizId) => {
  try {
    const response = await apiClient.get(`/api/suivis/quiz/?quiz=${quizId}`)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des tentatives:', error)
    throw error
  }
}

/**
 * Récupère toutes les tentatives de quiz pour un chapitre
 * @param {number} chapitreId - ID du chapitre
 * @returns {Promise<Array>} Liste des tentatives pour le chapitre
 */
// Legacy supprimé: tentatives par chapitre remplacées par tentatives par quiz

/**
 * Vérifie le cooldown pour un quiz spécifique
 * @param {number} quizId - ID du quiz
 * @returns {Promise<Object>} Informations sur le cooldown
 */
export const checkQuizCooldown = async (quizId) => {
  try {
    const DEBUG = import.meta.env && import.meta.env.DEV
    if (DEBUG) console.debug('📤 Vérification cooldown pour quiz:', quizId)
    // Utiliser un cache court pour éviter le spam serveur (TTL 20s)
    const response = await apiUtils.cachedGet(`/api/suivis/quiz/check-cooldown/${quizId}/`, { ttl: 20000 })
    if (DEBUG) console.debug('📥 Cooldown reçu:', response.data)
    return response.data
  } catch (error) {
    const DEBUG = import.meta.env && import.meta.env.DEV
    if (DEBUG) {
      console.error('❌ Erreur lors de la vérification du cooldown:', error)
      console.error('❌ Détails de l\'erreur:', error.response?.data)
      console.error('❌ Status de l\'erreur:', error.response?.status)
    }
    throw error
  }
}

/**
 * Récupère les statistiques des quiz pour le dashboard
 * @returns {Promise<Object>} Statistiques des quiz par notion
 */
export const getQuizStats = async () => {
  try {
    const response = await apiClient.get('/api/suivis/quiz/stats/')
    return response.data
  } catch (error) {
    console.error('❌ Erreur lors de la récupération des stats quiz:', error)
    throw error
  }
}

// ----- Quiz Images -----
export const getQuizImages = (quizId) => apiClient.get(`/api/quiz/quiz-images/?quiz=${quizId}`)
export const createQuizImage = (payload) => {
  const formData = new FormData()
  formData.append('quiz', payload.quiz)
  formData.append('image', payload.image)
  formData.append('image_type', payload.image_type)
  if (payload.position) formData.append('position', payload.position)
  return apiClient.post('/api/quiz/quiz-images/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
export const updateQuizImage = (id, payload) => {
  const formData = new FormData()
  if (payload.quiz) formData.append('quiz', payload.quiz)
  if (payload.image) formData.append('image', payload.image)
  if (payload.image_type) formData.append('image_type', payload.image_type)
  if (payload.position !== undefined) formData.append('position', payload.position)
  return apiClient.patch(`/api/quiz/quiz-images/${id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
export const deleteQuizImage = (id) => apiClient.delete(`/api/quiz/quiz-images/${id}/`) 