import { defineStore } from 'pinia'
import { ref } from 'vue'
import { 
  syncPreferencesWithBackend,
  loadPreferencesFromBackend
} from '@/api'
import { logOperation, isUserAuthenticated, handleError, handleAuthError } from './utils'

/**
 * Store pour la synchronisation avec le backend
 * Gère le chargement et la synchronisation des préférences
 */
export const useSyncStore = defineStore('subjects-sync', () => {
  // ========================================
  // ÉTAT RÉACTIF
  // ========================================
  
  /** Indicateur de synchronisation en cours */
  const isSyncing = ref(false)
  
  /** Dernière erreur de synchronisation */
  const lastSyncError = ref(null)
  
  /** Timestamp de la dernière synchronisation réussie */
  const lastSyncTimestamp = ref(null)

  // ========================================
  // ACTIONS PRINCIPALES
  // ========================================
  
  /**
   * Charger les préférences depuis le backend
   * @param {Object} stores - Objet contenant les stores à mettre à jour
   * @returns {Promise<boolean>} - True si le chargement a réussi
   */
  const loadPreferencesFromServer = async (stores) => {
    // Vérifier l'authentification avant d'essayer
    if (!isUserAuthenticated()) {
      logOperation('loadPreferencesFromServer', { 
        status: 'user_not_authenticated',
        message: 'Utilisateur non connecté, chargement depuis localStorage uniquement'
      })
      return false
    }

    try {
      isSyncing.value = true
      lastSyncError.value = null
      
      logOperation('loadPreferencesFromServer', { 
        status: 'starting',
        authenticated: true
      })
      
      const preferences = await loadPreferencesFromBackend()
      
      if (preferences) {
        // Mettre à jour les stores avec les données du backend
        if (stores.selectedStore) {
          stores.selectedStore.setSelectedMatieresIds(preferences.selectedIds || [])
        }
        if (stores.favoritesStore) {
          stores.favoritesStore.setFavoriteMatieresIds(preferences.favoriteIds || [])
        }
        if (stores.activeStore) {
          stores.activeStore.setActiveMatiereId(preferences.activeId || null)
        }
        
        lastSyncTimestamp.value = new Date().toISOString()
        
        logOperation('loadPreferencesFromServer', { 
          status: 'success',
          selectedCount: preferences.selectedIds?.length || 0,
          favoritesCount: preferences.favoriteIds?.length || 0,
          activeId: preferences.activeId
        })
        
        return true
      }
      
      logOperation('loadPreferencesFromServer', { 
        status: 'no_data',
        message: 'Aucune donnée reçue du backend'
      })
      
      return false
    } catch (error) {
      // Si erreur 401, pas de log d'erreur (normal pour utilisateur non connecté)
      if (handleAuthError(error, 'loadPreferencesFromServer')) {
        return false
      }
      
      lastSyncError.value = handleError(error, 'loadPreferencesFromServer')
      return false
    } finally {
      isSyncing.value = false
    }
  }
  
  /**
   * Synchroniser les préférences avec le backend
   * @returns {Promise<boolean>} - True si la synchronisation a réussi
   */
  const syncWithBackend = async () => {
    // Si non connecté, pas de sync
    if (!isUserAuthenticated()) {
      logOperation('syncWithBackend', { 
        status: 'user_not_authenticated',
        message: 'Synchronisation ignorée (utilisateur non connecté)'
      })
      return true
    }

    try {
      isSyncing.value = true
      lastSyncError.value = null
      
      logOperation('syncWithBackend', { 
        status: 'starting',
        authenticated: true
      })
      
      const success = await syncPreferencesWithBackend()
      
      if (success) {
        lastSyncTimestamp.value = new Date().toISOString()
        
        logOperation('syncWithBackend', { 
          status: 'success',
          timestamp: lastSyncTimestamp.value
        })
      }
      
      return success
    } catch (error) {
      // Si erreur 401, considérer comme succès (normal si non connecté)
      if (handleAuthError(error, 'syncWithBackend')) {
        return true
      }
      
      lastSyncError.value = handleError(error, 'syncWithBackend')
      return false
    } finally {
      isSyncing.value = false
    }
  }
  
  /**
   * Initialiser après connexion utilisateur
   * Synchronise les préférences locales avec le backend
   * @param {Object} stores - Objet contenant les stores à synchroniser
   * @returns {Promise<boolean>} - True si l'initialisation a réussi
   */
  const initializeAfterLogin = async (stores) => {
    if (!isUserAuthenticated()) {
      logOperation('initializeAfterLogin', { 
        status: 'user_not_authenticated',
        message: 'initializeAfterLogin appelé sans authentification'
      }, 'warn')
      return false
    }

    try {
      logOperation('initializeAfterLogin', { 
        status: 'starting',
        message: 'Initialisation après connexion...'
      })
      
      // 1. Charger les préférences depuis le backend
      const backendLoaded = await loadPreferencesFromServer(stores)
      
      // 2. Si le backend n'a pas de données, synchroniser localStorage vers backend
      if (!backendLoaded) {
        const hasLocalData = stores.selectedStore?.selectedMatieresCount > 0 || 
                           stores.favoritesStore?.favoriteMatieresCount > 0
        
        if (hasLocalData) {
          logOperation('initializeAfterLogin', { 
            status: 'syncing_local_to_backend',
            message: 'Synchronisation des données locales vers le backend...'
          })
          
          await syncWithBackend()
        }
      }
      
      logOperation('initializeAfterLogin', { 
        status: 'completed',
        message: 'Initialisation après connexion terminée'
      })
      
      return true
    } catch (error) {
      logOperation('initializeAfterLogin', { 
        status: 'error',
        error: error.message
      }, 'error')
      
      return false
    }
  }

  // ========================================
  // ACTIONS DE GESTION
  // ========================================
  
  /**
   * Obtenir le statut de la synchronisation
   * @returns {Object} - Statut détaillé de la synchronisation
   */
  const getSyncStatus = () => {
    return {
      isSyncing: isSyncing.value,
      lastSyncError: lastSyncError.value,
      lastSyncTimestamp: lastSyncTimestamp.value,
      isAuthenticated: isUserAuthenticated(),
      canSync: isUserAuthenticated() && !isSyncing.value
    }
  }
  
  /**
   * Réinitialiser les erreurs de synchronisation
   */
  const clearSyncErrors = () => {
    lastSyncError.value = null
    logOperation('clearSyncErrors', { 
      status: 'errors_cleared'
    })
  }
  
  /**
   * Forcer une synchronisation complète
   * @param {Object} stores - Objet contenant les stores à synchroniser
   * @returns {Promise<boolean>} - True si la synchronisation a réussi
   */
  const forceSync = async (stores) => {
    try {
      logOperation('forceSync', { 
        status: 'starting',
        message: 'Synchronisation forcée...'
      })
      
      // Charger depuis le backend
      const loadSuccess = await loadPreferencesFromServer(stores)
      
      // Puis synchroniser vers le backend
      const syncSuccess = await syncWithBackend()
      
      const overallSuccess = loadSuccess || syncSuccess
      
      logOperation('forceSync', { 
        status: overallSuccess ? 'success' : 'partial_failure',
        loadSuccess,
        syncSuccess
      })
      
      return overallSuccess
    } catch (error) {
      lastSyncError.value = handleError(error, 'forceSync')
      return false
    }
  }

  // ========================================
  // RETOUR DU STORE
  // ========================================
  
  return {
    // État
    isSyncing,
    lastSyncError,
    lastSyncTimestamp,
    
    // Actions principales
    loadPreferencesFromServer,
    syncWithBackend,
    initializeAfterLogin,
    
    // Actions de gestion
    getSyncStatus,
    clearSyncErrors,
    forceSync
  }
}) 