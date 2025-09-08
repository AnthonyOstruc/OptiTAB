/*
🌍 API Client refactorisé pour la gestion Pays/Niveaux
Architecture: Modulaire, DRY, avec gestion d'erreurs avancée
*/

import apiClient from './client'
import { useToast } from '@/composables/useToast'

// Configuration des endpoints
const ENDPOINTS = {
  PAYS: '/api/pays',
  NIVEAUX_PAR_PAYS: '/api/niveaux-par-pays',
  RECOMMENDATIONS: '/api/pays/recommandations-pays',
  STATISTIQUES: '/api/pays/statistiques-globales'
}

// Classe utilitaire pour la gestion des erreurs
class PaysNiveauxAPIError extends Error {
  constructor(message, code, data = null) {
    super(message)
    this.name = 'PaysNiveauxAPIError'
    this.code = code
    this.data = data
  }
}

// Gestionnaire d'erreurs centralisé
const handleAPIError = (error, context = '') => {
  console.error(`[PaysNiveauxAPI] ${context}:`, error)
  
  const { showToast } = useToast()
  
  if (error.response) {
    // Erreur de réponse du serveur
    const status = error.response.status
    const message = error.response.data?.message || error.response.data?.error
    
    switch (status) {
      case 400:
        showToast(message || 'Données invalides', 'error')
        break
      case 401:
        showToast('Session expirée, veuillez vous reconnecter', 'error')
        break
      case 403:
        showToast('Accès non autorisé', 'error')
        break
      case 404:
        showToast(message || 'Ressource non trouvée', 'error')
        break
      case 500:
        showToast('Erreur serveur, veuillez réessayer', 'error')
        break
      default:
        showToast(message || 'Une erreur est survenue', 'error')
    }
    
    throw new PaysNiveauxAPIError(
      message || 'Erreur API',
      status,
      error.response.data
    )
  } else if (error.request) {
    // Erreur de réseau
    showToast('Problème de connexion, vérifiez votre réseau', 'error')
    throw new PaysNiveauxAPIError('Erreur de réseau', 'NETWORK_ERROR')
  } else {
    // Autre erreur
    showToast('Une erreur inattendue est survenue', 'error')
    throw new PaysNiveauxAPIError(error.message, 'UNKNOWN_ERROR')
  }
}

// Cache simple en mémoire
class APICache {
  constructor() {
    this.cache = new Map()
    this.timestamps = new Map()
    this.defaultTTL = 5 * 60 * 1000 // 5 minutes
  }

  set(key, data, ttl = this.defaultTTL) {
    this.cache.set(key, data)
    this.timestamps.set(key, Date.now() + ttl)
  }

  get(key) {
    const timestamp = this.timestamps.get(key)
    if (!timestamp || Date.now() > timestamp) {
      this.cache.delete(key)
      this.timestamps.delete(key)
      return null
    }
    return this.cache.get(key)
  }

  clear() {
    this.cache.clear()
    this.timestamps.clear()
  }

  delete(key) {
    this.cache.delete(key)
    this.timestamps.delete(key)
  }
}

const cache = new APICache()

// Utilitaires de validation
const validatePaysId = (paysId) => {
  if (!paysId || (typeof paysId !== 'number' && typeof paysId !== 'string')) {
    throw new PaysNiveauxAPIError('ID pays invalide', 'INVALID_PAYS_ID')
  }
}

const validateNiveauId = (niveauId) => {
  if (!niveauId || (typeof niveauId !== 'number' && typeof niveauId !== 'string')) {
    throw new PaysNiveauxAPIError('ID niveau invalide', 'INVALID_NIVEAU_ID')
  }
}

// ===== API PAYS =====

/**
 * Récupère tous les pays actifs
 * @param {Object} options - Options de requête
 * @param {boolean} options.useCache - Utiliser le cache (défaut: true)
 * @param {string} options.search - Terme de recherche
 * @param {string} options.ordering - Tri (nom, ordre, date_creation)
 * @returns {Promise<Array>} Liste des pays
 */
export const getPaysActifs = async (options = {}) => {
  const { useCache = true, search, ordering = 'ordre,nom' } = options
  
  // Construire la clé de cache
  const cacheKey = `pays_actifs_${JSON.stringify({ search, ordering })}`
  
  // Vérifier le cache
  if (useCache) {
    const cachedData = cache.get(cacheKey)
    if (cachedData) {
      console.log('[PaysAPI] Données depuis le cache:', cacheKey)
      return cachedData
    }
  }

  try {
    const params = new URLSearchParams({
      est_actif: 'true',
      ordering
    })
    
    if (search) {
      params.append('search', search)
    }

    const response = await apiClient.get(`${ENDPOINTS.PAYS}/actifs/?${params}`)
    const data = response.data

    // Validation des données
    if (!Array.isArray(data)) {
      throw new PaysNiveauxAPIError('Format de données invalide', 'INVALID_DATA_FORMAT')
    }

    // Mise en cache
    if (useCache) {
      cache.set(cacheKey, data)
    }

    console.log(`[PaysAPI] ${data.length} pays chargés`)
    return data

  } catch (error) {
    handleAPIError(error, 'getPaysActifs')
  }
}

/**
 * Récupère un pays par son ID avec ses niveaux
 * @param {number|string} paysId - ID du pays
 * @param {Object} options - Options
 * @returns {Promise<Object>} Données complètes du pays
 */
export const getPaysAvecNiveaux = async (paysId, options = {}) => {
  validatePaysId(paysId)
  
  const { useCache = true } = options
  const cacheKey = `pays_avec_niveaux_${paysId}`

  if (useCache) {
    const cachedData = cache.get(cacheKey)
    if (cachedData) {
      return cachedData
    }
  }

  try {
    const response = await apiClient.get(`${ENDPOINTS.PAYS}/${paysId}/niveaux-complets/`)
    const data = response.data

    if (useCache) {
      cache.set(cacheKey, data)
    }

    return data

  } catch (error) {
    handleAPIError(error, 'getPaysAvecNiveaux')
  }
}

/**
 * Récupère les recommandations de pays pour l'utilisateur
 * @param {Object} options - Options
 * @returns {Promise<Object>} Recommandations
 */
export const getRecommandationsPays = async (options = {}) => {
  const { useCache = true } = options
  const cacheKey = 'recommendations_pays'

  if (useCache) {
    const cachedData = cache.get(cacheKey)
    if (cachedData) {
      return cachedData
    }
  }

  try {
    const response = await apiClient.get(ENDPOINTS.RECOMMENDATIONS)
    const data = response.data

    if (useCache) {
      cache.set(cacheKey, data, 2 * 60 * 1000) // Cache plus court pour les recommandations
    }

    return data

  } catch (error) {
    // Les recommandations ne sont pas critiques, on peut continuer sans
    console.warn('[PaysAPI] Impossible de charger les recommandations:', error)
    return { recommandations: [], criteres: [] }
  }
}

/**
 * Récupère les statistiques globales du système
 * @returns {Promise<Object>} Statistiques
 */
export const getStatistiquesGlobales = async () => {
  const cacheKey = 'statistiques_globales'
  
  const cachedData = cache.get(cacheKey)
  if (cachedData) {
    return cachedData
  }

  try {
    const response = await apiClient.get(ENDPOINTS.STATISTIQUES)
    const data = response.data

    cache.set(cacheKey, data, 10 * 60 * 1000) // Cache 10 minutes

    return data

  } catch (error) {
    handleAPIError(error, 'getStatistiquesGlobales')
  }
}

// ===== API NIVEAUX =====

/**
 * Récupère les niveaux disponibles pour un pays
 * @param {number|string} paysId - ID du pays
 * @param {Object} options - Options
 * @param {boolean} options.useCache - Utiliser le cache
 * @param {boolean} options.avecContenu - Inclure les statistiques de contenu
 * @returns {Promise<Array>} Liste des niveaux
 */
export const getNiveauxParPays = async (paysId, options = {}) => {
  validatePaysId(paysId)
  
  const { useCache = true, avecContenu = false } = options
  const cacheKey = `niveaux_pays_${paysId}_${avecContenu ? 'avec_contenu' : 'simple'}`

  if (useCache) {
    const cachedData = cache.get(cacheKey)
    if (cachedData) {
      console.log('[NiveauxAPI] Données depuis le cache:', cacheKey)
      return cachedData
    }
  }

  try {
    const endpoint = avecContenu 
      ? `${ENDPOINTS.NIVEAUX_PAR_PAYS}/avec-contenu/`
      : ENDPOINTS.NIVEAUX_PAR_PAYS
    
    const params = new URLSearchParams({ pays_id: paysId })
    const response = await apiClient.get(`${endpoint}?${params}`)
    const data = response.data

    // Validation
    if (!Array.isArray(data)) {
      throw new PaysNiveauxAPIError('Format de données invalide', 'INVALID_DATA_FORMAT')
    }

    // Enrichissement des données
    const enrichedData = data.map(niveau => ({
      ...niveau,
      // Normaliser les compteurs
      nombre_cours: niveau.nombre_cours || 0,
      nombre_exercices: niveau.nombre_exercices || 0,
      nombre_quiz: niveau.nombre_quiz || 0
    }))

    if (useCache) {
      cache.set(cacheKey, enrichedData)
    }

    console.log(`[NiveauxAPI] ${enrichedData.length} niveaux chargés pour le pays ${paysId}`)
    return enrichedData

  } catch (error) {
    handleAPIError(error, 'getNiveauxParPays')
  }
}

/**
 * Récupère un niveau spécifique avec ses détails pour un pays
 * @param {number|string} paysId - ID du pays
 * @param {number|string} niveauId - ID du niveau
 * @returns {Promise<Object>} Détails du niveau
 */
export const getNiveauPourPays = async (paysId, niveauId) => {
  validatePaysId(paysId)
  validateNiveauId(niveauId)

  const cacheKey = `niveau_${niveauId}_pays_${paysId}`
  const cachedData = cache.get(cacheKey)
  if (cachedData) {
    return cachedData
  }

  try {
    // D'abord récupérer tous les niveaux du pays
    const niveaux = await getNiveauxParPays(paysId, { avecContenu: true })
    
    // Trouver le niveau spécifique
    const niveau = niveaux.find(n => n.id === parseInt(niveauId))
    
    if (!niveau) {
      throw new PaysNiveauxAPIError(
        'Niveau non trouvé pour ce pays', 
        'NIVEAU_NOT_FOUND'
      )
    }

    cache.set(cacheKey, niveau)
    return niveau

  } catch (error) {
    handleAPIError(error, 'getNiveauPourPays')
  }
}

// ===== API UTILISATEUR =====

/**
 * Met à jour le pays et niveau de l'utilisateur
 * @param {number|string} paysId - ID du pays
 * @param {number|string} niveauId - ID du niveau
 * @returns {Promise<Object>} Données utilisateur mises à jour
 */
export const updateUserPaysNiveau = async (paysId, niveauId) => {
  validatePaysId(paysId)
  validateNiveauId(niveauId)

  try {
    // Vérifier que le niveau est bien disponible pour ce pays
    const niveaux = await getNiveauxParPays(paysId)
    const niveauExists = niveaux.some(n => n.id === parseInt(niveauId))
    
    if (!niveauExists) {
      throw new PaysNiveauxAPIError(
        'Ce niveau n\'est pas disponible pour le pays sélectionné',
        'NIVEAU_NOT_AVAILABLE_FOR_PAYS'
      )
    }

    // Utiliser l'endpoint backend dédié pour mettre à jour pays + niveau
    const response = await apiClient.patch('/api/users/me/pays-niveau/', {
      pays_id: paysId,
      niveau_pays_id: niveauId
    })

    // Invalider les caches liés à l'utilisateur
    cache.delete('recommendations_pays')
    
    console.log('[UserAPI] Pays et niveau mis à jour')
    return response.data

  } catch (error) {
    handleAPIError(error, 'updateUserPaysNiveau')
  }
}

/**
 * Récupère les préférences pays/niveau de l'utilisateur
 * @returns {Promise<Object>} Préférences utilisateur
 */
export const getUserPaysNiveauPreferences = async () => {
  try {
    const response = await apiClient.get('/api/users/me/preferences-pays-niveau/')
    return response.data
  } catch (error) {
    handleAPIError(error, 'getUserPaysNiveauPreferences')
  }
}

// ===== API ADMIN =====

/**
 * Ajoute un niveau à un pays (admin)
 * @param {number|string} paysId - ID du pays
 * @param {Object} niveauData - Données du niveau
 * @returns {Promise<Object>} Niveau créé
 */
export const addNiveauToPays = async (paysId, niveauData) => {
  validatePaysId(paysId)

  if (!niveauData.niveau_id) {
    throw new PaysNiveauxAPIError('niveau_id requis', 'MISSING_NIVEAU_ID')
  }

  try {
    const response = await apiClient.post(
      `${ENDPOINTS.PAYS}/${paysId}/ajouter-niveau-intelligent/`,
      niveauData
    )

    // Invalider les caches concernés
    cache.delete(`niveaux_pays_${paysId}_simple`)
    cache.delete(`niveaux_pays_${paysId}_avec_contenu`)
    cache.delete(`pays_avec_niveaux_${paysId}`)

    return response.data

  } catch (error) {
    handleAPIError(error, 'addNiveauToPays')
  }
}

// ===== UTILITAIRES =====

/**
 * Invalide tous les caches liés aux pays/niveaux
 */
export const clearPaysNiveauxCache = () => {
  cache.clear()
  console.log('[PaysNiveauxAPI] Cache vidé')
}

/**
 * Invalide le cache pour un pays spécifique
 * @param {number|string} paysId - ID du pays
 */
export const clearCacheForPays = (paysId) => {
  const keysToDelete = [
    `niveaux_pays_${paysId}_simple`,
    `niveaux_pays_${paysId}_avec_contenu`,
    `pays_avec_niveaux_${paysId}`
  ]
  
  keysToDelete.forEach(key => cache.delete(key))
  console.log(`[PaysNiveauxAPI] Cache vidé pour le pays ${paysId}`)
}

/**
 * Précharge les données essentielles
 * @returns {Promise<Object>} Données préchargées
 */
export const preloadEssentialData = async () => {
  try {
    console.log('[PaysNiveauxAPI] Préchargement des données essentielles...')
    
    const [pays, recommendations, stats] = await Promise.allSettled([
      getPaysActifs(),
      getRecommandationsPays(),
      getStatistiquesGlobales()
    ])

    const result = {
      pays: pays.status === 'fulfilled' ? pays.value : [],
      recommendations: recommendations.status === 'fulfilled' ? recommendations.value : null,
      stats: stats.status === 'fulfilled' ? stats.value : null
    }

    console.log('[PaysNiveauxAPI] Préchargement terminé')
    return result

  } catch (error) {
    console.error('[PaysNiveauxAPI] Erreur lors du préchargement:', error)
    throw error
  }
}

/**
 * Valide la cohérence pays/niveau
 * @param {number|string} paysId - ID du pays
 * @param {number|string} niveauId - ID du niveau
 * @returns {Promise<boolean>} True si cohérent
 */
export const validatePaysNiveauConsistency = async (paysId, niveauId) => {
  try {
    const niveaux = await getNiveauxParPays(paysId)
    return niveaux.some(n => n.id === parseInt(niveauId))
  } catch (error) {
    console.error('[PaysNiveauxAPI] Erreur validation cohérence:', error)
    return false
  }
}

// Export par défaut avec toutes les fonctions
export default {
  // Pays
  getPaysActifs,
  getPaysAvecNiveaux,
  getRecommandationsPays,
  getStatistiquesGlobales,
  
  // Niveaux
  getNiveauxParPays,
  getNiveauPourPays,
  
  // Utilisateur
  updateUserPaysNiveau,
  getUserPaysNiveauPreferences,
  
  // Admin
  addNiveauToPays,
  
  // Utilitaires
  clearPaysNiveauxCache,
  clearCacheForPays,
  preloadEssentialData,
  validatePaysNiveauConsistency,
  
  // Classes d'erreur
  PaysNiveauxAPIError
}
