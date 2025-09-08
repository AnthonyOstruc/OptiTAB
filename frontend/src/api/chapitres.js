import apiClient from './client'

// ----- Admin CRUD Chapitres -----
export const getChapitres = (notionId = null, niveauId = null) => {
  const params = new URLSearchParams()
  if (notionId) params.append('notion', notionId)
  if (niveauId) params.append('niveau', niveauId)
  
  const url = `/api/chapitres/${params.toString() ? '?' + params.toString() : ''}`
  return apiClient.get(url)
}

export const getChapitresByNiveau = (niveauId) => {
  return getChapitres(null, niveauId)
}
export const createChapitre = (payload) => apiClient.post('/api/chapitres/', payload)
export const updateChapitre = (id, payload) => apiClient.patch(`/api/chapitres/${id}/`, payload)
export const deleteChapitre = (id) => apiClient.delete(`/api/chapitres/${id}/`) 