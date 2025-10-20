import { ERROR_MESSAGES, HTTP_STATUS } from './constants'

/**
 * Utilitaires pour le store Subjects
 * Fonctions helper pour la validation, gestion d'erreurs et localStorage
 */

/**
 * Gestion centralisée des erreurs avec logging détaillé
 * @param {Error} error - L'erreur à traiter
 * @param {string} context - Le contexte où l'erreur s'est produite
 * @param {Object} additionalData - Données supplémentaires pour le debug
 */
export const handleError = (error, context, additionalData = {}) => {
  const errorInfo = {
    context,
    message: error.message,
    timestamp: new Date().toISOString(),
    ...additionalData
  }

  console.error(`[SubjectsStore] Erreur dans ${context}:`, errorInfo)
  
  // Log détaillé pour les erreurs réseau
  if (!error.response) {
    console.warn('🔌 [SubjectsStore] Problème de connexion réseau - Backend indisponible ?')
  } else if (error.response.status === HTTP_STATUS.NOT_FOUND) {
    console.warn('⚠️ [SubjectsStore] Endpoint non trouvé - Le backend est-il démarré ? URL correcte ?')
    console.warn('🔧 [SubjectsStore] Vérifiez que le serveur Django tourne sur http://127.0.0.1:8000')
  }

  return errorInfo
}

/**
 * Valide un ID de matière
 * @param {any} id - L'ID à valider
 * @returns {boolean} - True si l'ID est valide
 */
export const isValidMatiereId = (id) => {
  if (id === null || id === undefined) return false
  const numId = Number(id)
  return !isNaN(numId) && numId > 0 && Number.isInteger(numId)
}

/**
 * Normalise un ID de matière en nombre
 * @param {any} id - L'ID à normaliser
 * @returns {number|null} - L'ID normalisé ou null si invalide
 */
export const normalizeId = (id) => {
  if (!isValidMatiereId(id)) return null
  return Number(id)
}

/**
 * Vérifie si l'utilisateur est authentifié
 * @returns {boolean} - True si l'utilisateur a un token valide
 */
export const isUserAuthenticated = () => {
  return !!localStorage.getItem('access_token')
}

/**
 * Sauvegarde sécurisée dans localStorage
 * @param {string} key - La clé de stockage
 * @param {any} value - La valeur à sauvegarder
 * @returns {boolean} - True si la sauvegarde a réussi
 */
export const safeSetStorage = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value))
    return true
  } catch (error) {
    console.warn(`[SubjectsStore] Impossible de sauvegarder ${key}:`, error)
    return false
  }
}

/**
 * Chargement sécurisé depuis localStorage
 * @param {string} key - La clé de stockage
 * @param {any} defaultValue - Valeur par défaut
 * @param {boolean} [parseJson=true] - Si true, parse la valeur comme du JSON
 * @returns {any} - La valeur chargée ou la valeur par défaut
 */
export const safeGetStorage = (key, defaultValue, parseJson = true) => {
  try {
    const item = localStorage.getItem(key)
    if (!item) return defaultValue
    
    // Si on ne veut pas parser comme JSON, retourner la valeur telle quelle
    if (!parseJson) return item
    
    // Sinon essayer de parser comme JSON
    try {
      return JSON.parse(item)
    } catch (parseError) {
      // Si le parsing échoue mais que la valeur existe, la retourner telle quelle
      return item
    }
  } catch (error) {
    console.warn(`[SubjectsStore] Impossible de charger ${key}:`, error)
    return defaultValue
  }
}

/**
 * Valide et filtre un tableau d'IDs
 * @param {Array} ids - Tableau d'IDs à valider
 * @returns {Array<number>} - Tableau d'IDs valides normalisés
 */
export const validateAndNormalizeIds = (ids) => {
  if (!Array.isArray(ids)) return []
  return ids.filter(isValidMatiereId).map(normalizeId)
}

/**
 * Gère les erreurs d'authentification de manière silencieuse
 * @param {Error} error - L'erreur à traiter
 * @param {string} context - Le contexte de l'erreur
 * @returns {boolean} - True si c'est une erreur d'auth (à ignorer)
 */
export const handleAuthError = (error, context) => {
  if (error.response?.status === HTTP_STATUS.UNAUTHORIZED) {
    console.log(`[SubjectsStore] ${context} - Authentification requise, fallback localStorage`)
    return true
  }
  return false
}

/**
 * Crée un message d'erreur standardisé
 * @param {string} type - Type d'erreur (clé de ERROR_MESSAGES)
 * @param {string} [customMessage] - Message personnalisé optionnel
 * @returns {string} - Message d'erreur formaté
 */
export const createErrorMessage = (type, customMessage = null) => {
  return customMessage || ERROR_MESSAGES[type] || 'Erreur inconnue'
}

/**
 * Vérifie si on peut ajouter plus d'éléments
 * @param {number} currentCount - Nombre actuel
 * @param {number} maxCount - Nombre maximum autorisé
 * @returns {boolean} - True si on peut ajouter
 */
export const canAddMore = (currentCount, maxCount) => {
  return currentCount < maxCount
}

/**
 * Log une opération avec des détails
 * @param {string} operation - Nom de l'opération
 * @param {Object} details - Détails de l'opération
 * @param {string} [level='info'] - Niveau de log ('info', 'warn', 'error')
 */
export const logOperation = (operation, details = {}, level = 'info') => {
  const logData = {
    operation,
    timestamp: new Date().toISOString(),
    ...details
  }

  switch (level) {
    case 'warn':
      console.warn(`[SubjectsStore] ${operation}:`, logData)
      break
    case 'error':
      console.error(`[SubjectsStore] ${operation}:`, logData)
      break
    default:
      console.log(`[SubjectsStore] ${operation}:`, logData)
  }
} 