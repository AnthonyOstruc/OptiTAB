import apiClient, { apiUtils } from './client'

/**
 * Récupère dynamiquement la liste des cours pour une matière, notion ou chapitre donné depuis le backend.
 * @param {number|string} matiereId
 * @param {number|string} notionId
 * @param {number|string} chapitreId
 */
export const getCours = (matiereId = null, notionId = null, chapitreId = null) => {
  let url = '/api/cours/cours/'
  const params = []
  
  if (matiereId) params.push(`matiere=${matiereId}`)
  if (notionId) params.push(`notion=${notionId}`)
  // chapitreId obsolète
  
  if (params.length > 0) {
    url += '?' + params.join('&')
  }
  // Utiliser un cache mémoire avec TTL pour accélérer les rechargements
  // Contenus de cours changent rarement → TTL généreux (5 minutes)
  return apiUtils.cachedGet(url, { ttl: 300000 })
}

/**
 * Récupère les cours pour l'utilisateur connecté (selon son pays et niveau)
 * @returns {Promise<Array>} Liste des cours de l'utilisateur
 */
export const getCoursPourUtilisateur = async () => {
  try {
    const response = await apiClient.get('/api/cours/pour-utilisateur/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des cours pour utilisateur:', error)
    throw error
  }
}

// ----- Admin CRUD Cours -----
export const createCours = (payload) => apiClient.post('/api/cours/cours/', payload)
export const updateCours = (id, payload) => apiClient.patch(`/api/cours/cours/${id}/`, payload)
export const updateCoursFormData = (id, formData) => apiClient.patch(`/api/cours/cours/${id}/`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
export const deleteCours = (id) => apiClient.delete(`/api/cours/cours/${id}/`)

// ----- Cours Images -----
export const getCoursImages = (coursId) => apiClient.get(`/api/cours/cours-images/?cours=${coursId}`)
export const createCoursImage = (payload) => {
  const formData = new FormData()
  formData.append('cours', payload.cours)
  if (payload.image) {
    const imageName = payload.imageName || payload.image?.name
    if (imageName) {
      formData.append('image', payload.image, imageName)
    } else {
      formData.append('image', payload.image)
    }
  }
  formData.append('image_type', payload.image_type)
  if (payload.position) formData.append('position', payload.position)
  if (payload.legende) formData.append('legende', payload.legende)
  return apiClient.post('/api/cours/cours-images/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
export const updateCoursImage = (id, payload) => {
  const formData = new FormData()
  if (payload.cours) formData.append('cours', payload.cours)
  if (payload.image) {
    const imageName = payload.imageName || payload.image?.name
    if (imageName) {
      formData.append('image', payload.image, imageName)
    } else {
      formData.append('image', payload.image)
    }
  }
  if (payload.image_type) formData.append('image_type', payload.image_type)
  if (payload.position !== undefined) formData.append('position', payload.position)
  if (payload.legende !== undefined) formData.append('legende', payload.legende)
  return apiClient.patch(`/api/cours/cours-images/${id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
export const deleteCoursImage = (id) => apiClient.delete(`/api/cours/cours-images/${id}/`) 

export const duplicateCoursImages = ({ sourceCoursId, targetCoursId, replaceExisting = false }) => {
  return apiClient.post('/api/cours/cours-images/duplicate/', {
    source_cours: sourceCoursId,
    target_cours: targetCoursId,
    replace_existing: replaceExisting
  })
}
