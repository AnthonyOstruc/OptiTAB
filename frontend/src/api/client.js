import axios from 'axios'
import router from '@/router'
import { useUserStore } from '@/stores/user'

/**
 * Résolution robuste de l'URL de base API
 * - DEV: privilégie les URLs relatives (proxy Vite) ou force HTTP pour localhost
 * - PROD: utilise VITE_API_BASE_URL ou VITE_API_URL si fournie, sinon origine courante
 */
function resolveBaseUrl() {
  const isDev = import.meta.env.DEV || import.meta.env.MODE === 'development'
  let raw = (import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || '').trim()

  // En dev, si aucune base n'est fournie, utiliser les URLs relatives pour passer par le proxy Vite
  if (!raw) {
    return isDev ? '' : (typeof window !== 'undefined' ? window.location.origin : '')
  }

  // Éviter HTTPS vers localhost/127.0.0.1 (entraîne ERR_SSL_PROTOCOL_ERROR si le backend n'est pas en TLS)
  if (/^https:\/\/(127\.0\.0\.1|localhost)(:\d+)?/i.test(raw)) {
    raw = raw.replace(/^https:/i, 'http:')
  }

  // Nettoyer le trailing slash
  return raw.replace(/\/+$/, '')
}

/**
 * Configuration de l'API Client
 * Configuration centralisée et flexible pour l'API
 */
const API_CONFIG = {
  BASE_URL: resolveBaseUrl(),
  REFRESH_ENDPOINT: '/api/users/token/refresh/',
  
  // Timeouts
  REQUEST_TIMEOUT: 10000, // 10 secondes
  REFRESH_TIMEOUT: 5000,  // 5 secondes
  
  // Retry configuration
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000, // 1 seconde
  
  // Logging configuration
  LOGGING: {
    ENABLED: import.meta.env.DEV, // Actif uniquement en développement
    LEVEL: import.meta.env.DEV ? 'debug' : 'error', // Niveau de log
    SENSITIVE_FIELDS: ['password', 'token', 'refresh', 'access'], // Champs sensibles à masquer
  },
  
  // Headers par défaut
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
}

/**
 * Logger structuré pour l'API
 * Actif uniquement en mode développement pour éviter les fuites d'informations en production
 */
class ApiLogger {
  // Vérifier si on est en mode développement
  static isDevelopment() {
    return import.meta.env.DEV || import.meta.env.MODE === 'development'
  }
  
  // Vérifier si on est en mode production
  static isProduction() {
    return import.meta.env.PROD || import.meta.env.MODE === 'production'
  }
  
  static log(level, message, data = {}) {
    // Ne logger qu'en développement
    if (!this.isDevelopment()) {
      return
    }
    
    // Masquer les données sensibles
    const sanitizedData = this.sanitizeData(data)
    
    const timestamp = new Date().toISOString()
    const logEntry = {
      timestamp,
      level,
      message,
      data: sanitizedData,
      source: 'api-client'
    }
    
    switch (level) {
      case 'error':
        console.error(`[API] ${message}`, logEntry)
        break
      case 'warn':
        console.warn(`[API] ${message}`, logEntry)
        break
      case 'info':
        console.info(`[API] ${message}`, logEntry)
        break
      default:
        console.log(`[API] ${message}`, logEntry)
    }
  }
  
  /**
   * Masque les données sensibles dans les logs
   */
  static sanitizeData(data) {
    if (!data || typeof data !== 'object') {
      return data
    }
    
    const sanitized = { ...data }
    const sensitiveFields = API_CONFIG.LOGGING.SENSITIVE_FIELDS
    
    // Fonction récursive pour masquer les champs sensibles
    const maskSensitiveFields = (obj) => {
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          const lowerKey = key.toLowerCase()
          
          // Vérifier si le champ est sensible
          if (sensitiveFields.some(field => lowerKey.includes(field))) {
            obj[key] = '[MASKED]'
          } else if (typeof obj[key] === 'object' && obj[key] !== null) {
            // Récursion pour les objets imbriqués
            maskSensitiveFields(obj[key])
          }
        }
      }
    }
    
    maskSensitiveFields(sanitized)
    return sanitized
  }
  
  static error(message, error = null) {
    // En production, on peut vouloir logger les erreurs critiques
    // mais sans les détails sensibles
    if (this.isProduction()) {
      // Log minimal en production (sans données sensibles)
      console.error(`[API] ${message}`)
      return
    }
    
    // En développement, on peut avoir plus de détails
    const errorData = {
      message: error?.message,
      status: error?.response?.status,
      statusText: error?.response?.statusText,
      url: error?.config?.url,
      method: error?.config?.method
    }
    
    // Ne pas logger la stack trace en production
    if (this.isDevelopment()) {
      errorData.stack = error?.stack
    }
    
    this.log('error', message, errorData)
  }
  
  static warn(message, data = {}) {
    this.log('warn', message, data)
  }
  
  static info(message, data = {}) {
    this.log('info', message, data)
  }
  
  static debug(message, data = {}) {
    // Debug uniquement en développement
    if (this.isDevelopment()) {
      this.log('debug', message, data)
    }
  }
  
  /**
   * Vérifie si le logging est activé
   */
  static isLoggingEnabled() {
    return API_CONFIG.LOGGING.ENABLED && this.isDevelopment()
  }
  
  /**
   * Log sécurisé qui respecte la configuration
   */
  static secureLog(level, message, data = {}) {
    if (!this.isLoggingEnabled()) {
      return
    }
    
    // Vérifier le niveau de log configuré
    const levels = ['debug', 'info', 'warn', 'error']
    const currentLevelIndex = levels.indexOf(level)
    const configLevelIndex = levels.indexOf(API_CONFIG.LOGGING.LEVEL)
    
    if (currentLevelIndex >= configLevelIndex) {
      this.log(level, message, data)
    }
  }
}

/**
 * Gestionnaire de tokens JWT
 */
class TokenManager {
  constructor() {
    this.isRefreshing = false
    this.refreshSubscribers = []
    this.refreshPromise = null
  }
  
  /**
   * Récupère le token d'accès depuis le localStorage
   */
  getAccessToken() {
    return localStorage.getItem('access_token')
  }
  
  /**
   * Récupère le token de rafraîchissement depuis le localStorage
   */
  getRefreshToken() {
    return localStorage.getItem('refresh_token')
  }
  
  /**
   * Sauvegarde les tokens dans le localStorage
   */
  setTokens(accessToken, refreshToken = null) {
    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
    }
    if (refreshToken) {
      localStorage.setItem('refresh_token', refreshToken)
    }
  }
  
  /**
   * Supprime tous les tokens
   */
  clearTokens() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
  
  /**
   * Vérifie si un token est expiré (basé sur le payload JWT)
   */
  isTokenExpired(token) {
    if (!token) return true
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      return payload.exp < currentTime
    } catch (error) {
      ApiLogger.warn('Impossible de décoder le token JWT', { error: error.message })
      return true
    }
  }
  
  /**
   * Rafraîchit le token d'accès
   */
  async refreshAccessToken() {
    if (this.isRefreshing) {
      return this.refreshPromise
    }
    
    this.isRefreshing = true
    this.refreshPromise = this._performRefresh()
    
    try {
      const result = await this.refreshPromise
      return result
    } finally {
      this.isRefreshing = false
      this.refreshPromise = null
    }
  }
  
  /**
   * Effectue le rafraîchissement du token avec retry
   */
  async _performRefresh(maxRetries = 3) {
    const refreshToken = this.getRefreshToken()

    if (!refreshToken) {
      throw new Error('Aucun token de rafraîchissement disponible')
    }

    let lastError

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        ApiLogger.secureLog('info', `Tentative de rafraîchissement du token (essai ${attempt + 1}/${maxRetries + 1})`)

        const response = await axios.post(
          `${API_CONFIG.BASE_URL}${API_CONFIG.REFRESH_ENDPOINT}`,
          { refresh: refreshToken },
          {
            timeout: API_CONFIG.REFRESH_TIMEOUT,
            headers: { 'Content-Type': 'application/json' }
          }
        )

        const { access, refresh } = response.data
        this.setTokens(access, refresh)

        ApiLogger.secureLog('info', 'Token rafraîchi avec succès')
        return access

      } catch (error) {
        lastError = error
        ApiLogger.error(`Échec du rafraîchissement du token (essai ${attempt + 1})`, error)

        // Ne pas retry sur les erreurs 4xx (sauf timeout)
        if (error.response?.status >= 400 && error.response?.status < 500 && error.code !== 'ECONNABORTED') {
          break
        }

        // Attendre avant le prochain essai (backoff exponentiel)
        if (attempt < maxRetries) {
          const delay = Math.min(1000 * Math.pow(2, attempt), 10000) // Max 10 secondes
          ApiLogger.secureLog('info', `Nouvelle tentative dans ${delay}ms`)
          await this._sleep(delay)
        }
      }
    }

    // Si tous les essais ont échoué, nettoyer les tokens
    this.clearTokens()
    throw lastError
  }

  /**
   * Fonction utilitaire pour les délais
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
  
  /**
   * Notifie tous les abonnés du rafraîchissement
   */
  onRefreshed(newToken) {
    this.refreshSubscribers.forEach(callback => callback(newToken))
    this.refreshSubscribers = []
  }
  
  /**
   * Ajoute un abonné pour le rafraîchissement
   */
  addRefreshSubscriber(callback) {
    this.refreshSubscribers.push(callback)
  }

  /**
   * Vérifie si le token doit être rafraîchi (prochainement expiré)
   */
  shouldRefreshToken(token, thresholdMinutes = 5) {
    if (!token) return false

    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      const thresholdTime = thresholdMinutes * 60 // convertir en secondes

      return (payload.exp - currentTime) <= thresholdTime
    } catch (error) {
      ApiLogger.warn('Impossible de vérifier l\'expiration du token', { error: error.message })
      return false
    }
  }

  /**
   * Rafraîchissement proactif des tokens
   */
  async proactiveRefresh() {
    const accessToken = this.getAccessToken()
    const refreshToken = this.getRefreshToken()

    if (!accessToken || !refreshToken) {
      return false
    }

    // Vérifier si le token doit être rafraîchi (dans les 5 prochaines minutes)
    if (this.shouldRefreshToken(accessToken, 5)) {
      ApiLogger.secureLog('info', 'Rafraîchissement proactif du token')
      try {
        await this.refreshAccessToken()
        return true
      } catch (error) {
        ApiLogger.error('Échec du rafraîchissement proactif', error)
        return false
      }
    }

    return false
  }
}

/**
 * Gestionnaire de retry intelligent
 */
class RetryManager {
  /**
   * Retry une requête avec backoff exponentiel
   */
  static async retryRequest(requestFn, maxRetries = API_CONFIG.MAX_RETRIES) {
    let lastError
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await requestFn()
      } catch (error) {
        lastError = error
        
        // Ne pas retry sur les erreurs 4xx (sauf 429) et 5xx spécifiques
        if (this.shouldNotRetry(error)) {
          throw error
        }
        
        if (attempt < maxRetries) {
          const delay = this.calculateDelay(attempt)
          ApiLogger.secureLog('warn', `Tentative ${attempt + 1} échouée, nouvelle tentative dans ${delay}ms`, {
            error: error.message,
            status: error.response?.status
          })
          
          await this.sleep(delay)
        }
      }
    }
    
    throw lastError
  }
  
  /**
   * Détermine si une erreur ne doit pas être retry
   */
  static shouldNotRetry(error) {
    const status = error.response?.status
    
    // Ne pas retry sur les erreurs client (4xx) sauf 429 (rate limit)
    if (status >= 400 && status < 500 && status !== 429) {
      return true
    }
    
    // Ne pas retry sur les erreurs de timeout réseau
    if (error.code === 'ECONNABORTED') {
      return false // On retry les timeouts
    }
    
    return false
  }
  
  /**
   * Calcule le délai de retry avec backoff exponentiel
   */
  static calculateDelay(attempt) {
    return Math.min(API_CONFIG.RETRY_DELAY * Math.pow(2, attempt), 10000)
  }
  
  /**
   * Pause asynchrone
   */
  static sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

/**
 * Gestionnaire d'authentification
 */
class AuthManager {
  /**
   * Déconnecte l'utilisateur et redirige
   */
  static logout(reason = 'Session expirée') {
    ApiLogger.secureLog('info', 'Déconnexion utilisateur', { reason })
    
    // Nettoyer les tokens
    tokenManager.clearTokens()
    
    // Nettoyer le store utilisateur
          try {
            const userStore = useUserStore()
            userStore.clearUser()
    } catch (error) {
      ApiLogger.secureLog('warn', 'Erreur lors du nettoyage du store utilisateur', { error: error.message })
    }
    
    // Rediriger vers la page d'accueil
          router.push('/')
  }
}

// Instances globales
const tokenManager = new TokenManager()

// Variable pour l'intervalle de surveillance des tokens
let tokenMonitoringInterval = null

/**
 * Instance Axios centralisée avec configuration avancée
 */
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.REQUEST_TIMEOUT,
  headers: API_CONFIG.DEFAULT_HEADERS,
  withCredentials: true, // Inclure les cookies si le backend les utilise
})

/**
 * Intercepteur de requête
 * Ajoute automatiquement le token d'authentification
 */
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenManager.getAccessToken()
    
    if (token && !tokenManager.isTokenExpired(token)) {
      config.headers.Authorization = `Bearer ${token}`
      ApiLogger.secureLog('info', 'Token ajouté à la requête', { 
        url: config.url,
        method: config.method 
      })
    }
    
    return config
  },
  (error) => {
    ApiLogger.error('Erreur dans l\'intercepteur de requête', error)
    return Promise.reject(error)
  }
)

/**
 * Intercepteur de réponse
 * Gère le rafraîchissement automatique des tokens et les retries
 */
apiClient.interceptors.response.use(
  (response) => {
    ApiLogger.secureLog('info', 'Requête réussie', {
      url: response.config.url,
      method: response.config.method,
      status: response.status
    })
    return response
  },
  async (error) => {
    const { config, response } = error
    
    // Vérifier si c'est une erreur 404 sur les notifications
    const isNotificationError = config?.url?.includes('/api/users/notifications/') && response?.status === 404
    
    // Log de l'erreur (mais pas pour les 404 de notifications)
    if (!isNotificationError) {
      ApiLogger.error('Erreur de requête', error)
    } else {
      ApiLogger.debug('Notification introuvable (404)', {
        url: config.url,
        method: config.method,
        status: response.status
      })
    }
    
    // Gestion du token expiré (401) et des erreurs d'autorisation (403)
    // Vérifier si c'est bien une erreur de token expiré et pas une erreur d'authentification générale
    if ((response?.status === 401 || response?.status === 403) && !config.__isRetryRequest) {
      // Vérifier si on a un token d'accès dans le localStorage
      const hasAccessToken = !!tokenManager.getAccessToken()
      const hasRefreshToken = !!tokenManager.getRefreshToken()

      // Analyser la réponse pour mieux comprendre le type d'erreur
      const isTokenExpiredError = response?.data?.code === 'token_not_valid' ||
                                  response?.data?.detail?.includes('token') ||
                                  response?.data?.messages?.some(msg => msg?.token?.includes('expired'))

      const isRefreshTokenError = response?.data?.detail?.includes('refresh') ||
                                  response?.data?.messages?.some(msg => msg?.token?.includes('refresh'))

      if (hasAccessToken && hasRefreshToken && (isTokenExpiredError || response?.status === 401)) {
        // C'est probablement un token expiré, essayer de rafraîchir
        ApiLogger.secureLog('info', 'Erreur de token détectée, tentative de rafraîchissement', {
          status: response.status,
          url: config.url,
          isTokenExpiredError,
          isRefreshTokenError
        })
        return handleTokenExpiration(config, error)
      } else if (response?.status === 403) {
        // Erreur d'autorisation (pas de droits)
        ApiLogger.secureLog('warn', 'Erreur 403 - Accès refusé', {
          url: config.url,
          hasAccessToken,
          hasRefreshToken
        })
        // Pour les erreurs 403, on peut essayer de rafraîchir une fois
        if (hasAccessToken && hasRefreshToken && !config.__isRetryRequest) {
          return handleTokenExpiration(config, error)
        }
      } else {
        // Pas de tokens disponibles ou erreur d'authentification générale
        ApiLogger.secureLog('warn', `Erreur ${response?.status} sans tokens valides ou erreur d'authentification`, {
          url: config.url,
          status: response?.status,
          hasAccessToken,
          hasRefreshToken
        })
      }
    }
    
    // Gestion des erreurs réseau et timeouts
    if (!response && (error.code === 'ECONNABORTED' || error.code === 'NETWORK_ERROR')) {
      return handleNetworkError(config, error)
    }

    return Promise.reject(error)
  }
)

/**
 * Gère l'expiration du token
 */
async function handleTokenExpiration(config, originalError) {
  try {
    const refreshToken = tokenManager.getRefreshToken()

    // Ne pas vérifier l'expiration du refresh token ici - laisser le serveur décider
    // Cette vérification peut être inexacte à cause des différences d'horloge
    if (!refreshToken) {
      ApiLogger.secureLog('warn', 'Aucun token de rafraîchissement disponible')
      AuthManager.logout('Aucun token de rafraîchissement disponible')
      return Promise.reject(originalError)
    }

    ApiLogger.secureLog('info', 'Tentative de rafraîchissement du token', { url: config.url })

    // Tentative de rafraîchissement du token
    const newToken = await tokenManager.refreshAccessToken()

    if (!newToken) {
      throw new Error('Aucun nouveau token reçu')
    }

    // Notifier les abonnés
    tokenManager.onRefreshed(newToken)

    // Retry la requête originale avec le nouveau token
    config.headers.Authorization = `Bearer ${newToken}`
    config.__isRetryRequest = true

    ApiLogger.secureLog('info', 'Requête retry avec le nouveau token', { url: config.url })
    return apiClient(config)

  } catch (refreshError) {
    ApiLogger.error('Échec du rafraîchissement du token', refreshError)

    // Analyser le type d'erreur pour une meilleure gestion
    const errorStatus = refreshError.response?.status
    let logoutReason = 'Échec du rafraîchissement du token'

    if (errorStatus === 401) {
      logoutReason = 'Token de rafraîchissement invalide ou expiré'
    } else if (errorStatus === 400) {
      logoutReason = 'Requête de rafraîchissement malformée'
    } else if (!refreshError.response) {
      logoutReason = 'Erreur réseau lors du rafraîchissement'
    }

    // Échec du rafraîchissement => déconnexion
    AuthManager.logout(logoutReason)
    return Promise.reject(originalError)
  }
}

/**
 * Gère les erreurs réseau avec retry
 */
async function handleNetworkError(config, error) {
  return RetryManager.retryRequest(() => {
    ApiLogger.secureLog('info', 'Retry de la requête réseau', { url: config.url })
    return apiClient(config)
  })
}

/**
 * Méthodes utilitaires pour l'API
 */
export const apiUtils = {
  /**
   * Effectue une requête avec retry automatique
   */
  async request(config) {
    return RetryManager.retryRequest(() => apiClient(config))
  },
  
  /**
   * Vérifie si l'utilisateur est authentifié
   */
  isAuthenticated() {
    const token = tokenManager.getAccessToken()
    return token && !tokenManager.isTokenExpired(token)
  },
  
  /**
   * Force le rafraîchissement du token
   */
  async refreshToken() {
    return tokenManager.refreshAccessToken()
  },
  
  /**
   * Déconnecte l'utilisateur
   */
  logout(reason) {
    AuthManager.logout(reason)
  },
  
  /**
   * Obtient les statistiques de l'API
   */
  getStats() {
    return {
      isRefreshing: tokenManager.isRefreshing,
      hasValidToken: this.isAuthenticated(),
      refreshSubscribersCount: tokenManager.refreshSubscribers.length
    }
  },

  /**
   * Nettoie les tokens expirés automatiquement
   */
  cleanExpiredTokens() {
    const accessToken = tokenManager.getAccessToken()
    const refreshToken = tokenManager.getRefreshToken()

    let cleaned = false

    if (accessToken && tokenManager.isTokenExpired(accessToken)) {
      ApiLogger.secureLog('info', 'Nettoyage du token d\'accès expiré')
      localStorage.removeItem('access_token')
      cleaned = true
    }

    if (refreshToken && tokenManager.isTokenExpired(refreshToken)) {
      ApiLogger.secureLog('info', 'Nettoyage du token de rafraîchissement expiré')
      localStorage.removeItem('refresh_token')
      cleaned = true
    }

    if (cleaned) {
      ApiLogger.secureLog('info', 'Tokens expirés nettoyés automatiquement')
    }

    return cleaned
  },

  /**
   * Vérifie si l'utilisateur a des tokens valides
   */
  hasValidTokens() {
    const accessToken = tokenManager.getAccessToken()
    const refreshToken = tokenManager.getRefreshToken()

    const hasAccess = accessToken && !tokenManager.isTokenExpired(accessToken)
    const hasRefresh = refreshToken && !tokenManager.isTokenExpired(refreshToken)

    return { hasAccess, hasRefresh, hasAnyValid: hasAccess || hasRefresh }
  },

  /**
   * Démarre la surveillance automatique des tokens
   */
  startTokenMonitoring() {
    if (tokenMonitoringInterval) {
      clearInterval(tokenMonitoringInterval)
    }

    // Vérifier les tokens toutes les 30 secondes
    tokenMonitoringInterval = setInterval(async () => {
      try {
        // Nettoyer les tokens expirés
        this.cleanExpiredTokens()

        // Rafraîchissement proactif si nécessaire
        await tokenManager.proactiveRefresh()
      } catch (error) {
        ApiLogger.error('Erreur lors de la surveillance des tokens', error)
      }
    }, 30000) // 30 secondes

    ApiLogger.secureLog('info', 'Surveillance automatique des tokens démarrée')
  },

  /**
   * Arrête la surveillance automatique des tokens
   */
  stopTokenMonitoring() {
    if (tokenMonitoringInterval) {
      clearInterval(tokenMonitoringInterval)
      tokenMonitoringInterval = null
      ApiLogger.secureLog('info', 'Surveillance automatique des tokens arrêtée')
    }
  },

  /**
   * Rafraîchissement proactif manuel
   */
  async proactiveTokenRefresh() {
    return tokenManager.proactiveRefresh()
  }
}

// Export de l'instance Axios configurée
export default apiClient 