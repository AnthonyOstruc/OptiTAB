import apiClient from './client'

// Normalise un payload venant du formulaire admin vers le schéma attendu par le backend
const normalizeMatierePayload = (payload = {}) => {
  const normalized = {}
  if (payload.nom != null) normalized.titre = payload.nom
  if (payload.titre != null) normalized.titre = payload.titre
  if (payload.description != null) normalized.description = payload.description
  if (payload.svg_icon != null) normalized.svg_icon = payload.svg_icon
  // Associations supprimées: niveaux/pays ne se gèrent plus ici
  if (payload.ordre != null) normalized.ordre = payload.ordre
  if (payload.est_actif != null) normalized.est_actif = payload.est_actif
  return normalized
}

/**
 * Récupère les matières filtrées selon l'utilisateur connecté
 * - Pour les admins : toutes les matières
 * - Pour les utilisateurs : seulement les matières de leur pays/niveau
 */
export const getMatieres = () => {
  return apiClient.get('/api/matieres/')
}

/**
 * Récupère TOUTES les matières (pour l'interface admin uniquement)
 * Bypass le filtrage automatique par utilisateur
 */
export const getMatieresAdmin = () => {
  return apiClient.get('/api/matieres/admin_list/')
}

/**
 * Récupère les matières avec détails pour l'utilisateur connecté
 * Inclut les informations sur le filtrage appliqué
 */
export const getMatieresUtilisateur = () => {
  return apiClient.get('/api/matieres/user_matieres/')
}

/**
 * Filtre manuel des matières par pays et niveau (pour tests/admin)
 */
export const filtrerMatieres = (pays_id = null, niveau_id = null) => {
  const params = new URLSearchParams()
  if (pays_id) params.append('pays', pays_id)
  if (niveau_id) params.append('niveau', niveau_id)
  
  return apiClient.get(`/api/matieres/matieres_filtrees/?${params}`)
}

// ----- CRUD Admin -----
export const createMatiere = (payload) => apiClient.post('/api/matieres/', normalizeMatierePayload(payload))
export const updateMatiere = (id, payload) => apiClient.patch(`/api/matieres/${id}/`, normalizeMatierePayload(payload))
export const deleteMatiere = (id) => apiClient.delete(`/api/matieres/${id}/`) 