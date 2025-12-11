import apiClient from './client'

/**
 * API pour gérer les soumissions manuelles de quiz (envoyés par WhatsApp)
 */

/**
 * Récupère toutes les soumissions de quiz
 * Pour les élèves: seulement leurs soumissions
 * Pour les admins: toutes les soumissions avec filtres
 */
export const getQuizSubmissions = async (filters = {}) => {
  try {
    const params = new URLSearchParams()
    if (filters.status) params.append('status', filters.status)
    if (filters.user) params.append('user', filters.user)
    if (filters.quiz) params.append('quiz', filters.quiz)
    
    const queryString = params.toString()
    const response = await apiClient.get(`/api/suivis/quiz-submissions/${queryString ? '?' + queryString : ''}`)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des soumissions:', error)
    throw error
  }
}

/**
 * Récupère une soumission spécifique
 */
export const getQuizSubmission = async (id) => {
  try {
    const response = await apiClient.get(`/api/suivis/quiz-submissions/${id}/`)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération de la soumission:', error)
    throw error
  }
}

/**
 * Crée une nouvelle soumission de quiz
 */
export const createQuizSubmission = async (data) => {
  try {
    const response = await apiClient.post('/api/suivis/quiz-submissions/', {
      quiz: data.quizId,
      notes_admin: data.notes_admin || ''
    })
    return response.data
  } catch (error) {
    console.error('Erreur lors de la création de la soumission:', error)
    throw error
  }
}

/**
 * Note une soumission (admin seulement)
 */
export const gradeQuizSubmission = async (id, gradeData) => {
  try {
    const response = await apiClient.post(`/api/suivis/quiz-submissions/${id}/grade/`, {
      note: gradeData.note,
      commentaire: gradeData.commentaire || ''
    })
    return response.data
  } catch (error) {
    console.error('Erreur lors de la notation de la soumission:', error)
    throw error
  }
}

/**
 * Met à jour une soumission
 */
export const updateQuizSubmission = async (id, data) => {
  try {
    const response = await apiClient.patch(`/api/suivis/quiz-submissions/${id}/`, data)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la mise à jour de la soumission:', error)
    throw error
  }
}

/**
 * Supprime une soumission
 */
export const deleteQuizSubmission = async (id) => {
  try {
    await apiClient.delete(`/api/suivis/quiz-submissions/${id}/`)
  } catch (error) {
    console.error('Erreur lors de la suppression de la soumission:', error)
    throw error
  }
}

/**
 * Récupère les statistiques des soumissions
 */
export const getQuizSubmissionStats = async () => {
  try {
    const response = await apiClient.get('/api/suivis/quiz-submissions/stats/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des statistiques:', error)
    throw error
  }
}

