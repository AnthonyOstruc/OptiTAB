import client, { apiUtils } from './client'

// Normalise un payload de thème: alias nom -> titre, niveaux -> liste d'IDs
const normalizeThemePayload = (payload = {}) => {
  const normalized = {}
  if (payload.matiere != null) normalized.matiere = payload.matiere
  if (payload.contexte != null) normalized.contexte = payload.contexte
  if (payload.nom != null) normalized.titre = payload.nom
  if (payload.titre != null) normalized.titre = payload.titre
  if (payload.description != null) normalized.description = payload.description
  if (payload.couleur != null) normalized.couleur = payload.couleur
  if (payload.ordre != null) normalized.ordre = payload.ordre
  if (Array.isArray(payload.niveaux)) normalized.niveaux = payload.niveaux
  return normalized
}

// Récupérer tous les thèmes
export const getThemes = (params = {}) => client.get('/api/themes/', { params })

// Récupérer en une requête les thèmes + notions filtrés pour l'utilisateur courant
// Fallback public si non authentifié ou 401: combine /api/themes/ et /api/notions/
export const getThemesWithNotionsForUser = async (params = {}) => {
  // Extraire un éventuel signal (AbortController) du params
  const { signal, ...query } = params || {}
  const isAuth = apiUtils.isAuthenticated()
  if (isAuth) {
    try {
      // Utiliser le cache GET pour réduire les délais perçus
      return await apiUtils.cachedGet('/api/themes/notions-pour-utilisateur/', { params: query, ttl: 120000, signal })
    } catch (error) {
      if (error?.response?.status !== 401) throw error
      // 401 -> fallback public
    }
  }
  // Public fallback: retourne la même forme { data: { themes, notions } }
  const matiere = query?.matiere
  const [themesRes, notionsRes] = await Promise.all([
    apiUtils.cachedGet('/api/themes/', { params: { matiere }, ttl: 120000, signal }),
    apiUtils.cachedGet('/api/notions/', { params: { matiere }, ttl: 180000, signal })
  ])
  return { data: { themes: themesRes?.data || [], notions: notionsRes?.data || [] } }
}

// Récupérer les thèmes par contexte
export const getThemesByContexte = (contexteId) => getThemes({ contexte: contexteId })

// Récupérer les thèmes pour un niveau spécifique
export const getThemesByNiveau = (niveauId) => {
  return getThemes(null, niveauId)
}

// Récupérer un thème par ID
export const getTheme = (id) => {
  return client.get(`/api/themes/${id}/`)
}

// Créer un nouveau thème (supporte le champ contexte)
export const createTheme = (themeData) => client.post('/api/themes/', normalizeThemePayload(themeData))

// Modifier un thème
export const updateTheme = (id, themeData) => client.patch(`/api/themes/${id}/`, normalizeThemePayload(themeData))

// Supprimer un thème
export const deleteTheme = (id) => {
  return client.delete(`/api/themes/${id}/`)
}

/**
 * Récupère les thèmes pour l'utilisateur connecté (selon son pays et niveau)
 * @returns {Promise<Array>} Liste des thèmes de l'utilisateur
 */
export const getThemesPourUtilisateur = async () => {
  try {
    const response = await client.get('/api/themes/pour-utilisateur/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des thèmes pour utilisateur:', error)
    throw error
  }
}
