import apiClient from './client'

/**
 * Récupère dynamiquement la liste des exercices depuis le backend.
 * @param {number|string} chapitreId - ID du chapitre (optionnel)
 * @param {number|string} niveauId - ID du niveau pour filtrer (optionnel)
 */
export const getExercices = (chapitreId = null, niveauId = null) => {
  const params = new URLSearchParams()
  if (chapitreId) params.append('chapitre', chapitreId)
  if (niveauId) params.append('niveau', niveauId)
  
  const url = `/api/exercices/${params.toString() ? '?' + params.toString() : ''}`
  return apiClient.get(url)
}

/**
 * Récupère les exercices pour un niveau spécifique
 * @param {number|string} niveauId - ID du niveau
 */
export const getExercicesByNiveau = (niveauId) => {
  return getExercices(null, niveauId)
}

/**
 * Récupère les exercices pour l'utilisateur connecté (selon son pays et niveau)
 * @returns {Promise<Array>} Liste des exercices de l'utilisateur
 */
export const getExercicesPourUtilisateur = async () => {
  try {
    const response = await apiClient.get('/api/exercices/pour-utilisateur/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des exercices pour utilisateur:', error)
    throw error
  }
}

// ----- Admin CRUD Exercises -----
export const createExercice = (payload) => apiClient.post('/api/exercices/', payload)
export const updateExercice = (id, payload) => apiClient.patch(`/api/exercices/${id}/`, payload)
export const deleteExercice = (id) => apiClient.delete(`/api/exercices/${id}/`)

// ----- Exercice Images -----
export const getExerciceImages = (exerciceId) => apiClient.get(`/api/exercice-images/?exercice=${exerciceId}`)
export const createExerciceImage = (payload) => {
  const formData = new FormData()
  formData.append('exercice', payload.exercice)
  formData.append('image', payload.image)
  formData.append('image_type', payload.image_type)
  if (payload.position) formData.append('position', payload.position)
  return apiClient.post('/api/exercice-images/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
export const updateExerciceImage = (id, payload) => {
  const formData = new FormData()
  if (payload.exercice) formData.append('exercice', payload.exercice)
  if (payload.image) formData.append('image', payload.image)
  if (payload.image_type) formData.append('image_type', payload.image_type)
  if (payload.position !== undefined) formData.append('position', payload.position)
  return apiClient.patch(`/api/exercice-images/${id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
export const deleteExerciceImage = (id) => apiClient.delete(`/api/exercice-images/${id}/`)

// ----- Exercice status -----
export const getStatuses = () => apiClient.get('/api/suivis/status/')
export const createStatus = (payload) => apiClient.post('/api/suivis/status/', payload)
export const updateStatus = (id, payload) => apiClient.patch(`/api/suivis/status/${id}/`, payload)
// Supprime un statut d'exercice
export const deleteStatus = (id) => apiClient.delete(`/api/suivis/status/${id}/`) 

// ----- Backend PDF (rendu serveur, qualité éditoriale) -----
export const downloadExercicePDF = async (exerciceId, includeSolution = false) => {
  const url = `/api/exercices/${exerciceId}/pdf/?include_solution=${includeSolution ? '1' : '0'}`
  const res = await apiClient.get(url, { responseType: 'blob' })
  const blob = new Blob([res.data], { type: 'application/pdf' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `Exercice_${exerciceId}${includeSolution ? '_corrige' : ''}.pdf`
  document.body.appendChild(link)
  link.click()
  link.remove()
}