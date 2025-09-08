import apiClient from './client'

// Normalise un payload venant du formulaire admin vers le schéma attendu par le backend
const normalizeNotionPayload = (payload = {}) => {
  const normalized = {}
  if (payload.nom != null) normalized.titre = payload.nom
  if (payload.titre != null) normalized.titre = payload.titre
  if (payload.theme != null) normalized.theme = payload.theme
  if (Array.isArray(payload.niveaux)) normalized.niveaux = payload.niveaux
  if (payload.description != null) normalized.description = payload.description
  if (payload.ordre != null) normalized.ordre = payload.ordre
  if (payload.est_actif != null) normalized.est_actif = payload.est_actif
  return normalized
}

// ----- Admin CRUD Notions -----
export const getNotions = (matiereId = null, niveauId = null) => {
  const params = new URLSearchParams()
  if (matiereId) params.append('matiere', matiereId)
  if (niveauId) params.append('niveau', niveauId)
  params.append('format', 'json')
  const url = `/api/notions/${params.toString() ? '?' + params.toString() : ''}`
  return apiClient.get(url)
}

export const getNotionsByNiveau = (niveauId) => getNotions(null, niveauId)
export const createNotion = (payload) => apiClient.post('/api/notions/', normalizeNotionPayload(payload))
export const updateNotion = (id, payload) => apiClient.patch(`/api/notions/${id}/`, normalizeNotionPayload(payload))
export const deleteNotion = (id) => apiClient.delete(`/api/notions/${id}/`)

/**
 * Récupère les notions pour l'utilisateur connecté (selon son pays et niveau)
 * @returns {Promise<Array>} Liste des notions de l'utilisateur
 */
export const getNotionsPourUtilisateur = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/notions/pour-utilisateur/', { params })
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des notions pour utilisateur:', error)
    throw error
  }
}