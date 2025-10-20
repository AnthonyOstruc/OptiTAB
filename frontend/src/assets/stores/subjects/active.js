import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { setActiveMatiere as apiSetActive } from '@/api'
import { STORAGE_KEYS, ERROR_MESSAGES } from './constants'
import { 
  normalizeId, 
  safeSetStorage, 
  safeGetStorage, 
  isUserAuthenticated,
  handleError,
  handleAuthError,
  logOperation
} from './utils'

/**
 * Store pour la gestion de la matière active
 * Gère la matière actuellement sélectionnée pour la navigation
 */
export const useActiveStore = defineStore('subjects-active', () => {
  // ========================================
  // ÉTAT RÉACTIF
  // ========================================
  
  /** ID de la matière actuellement active */
  const activeMatiereId = ref(null)
  
  /** Indicateur de synchronisation en cours */
  const isSyncing = ref(false)
  
  /** Dernière erreur de synchronisation */
  const lastSyncError = ref(null)

  // ========================================
  // GETTERS CALCULÉS
  // ========================================
  
  /** Vérifier si une matière est active */
  const isActiveMatiere = computed(() => (id) => {
    const numId = normalizeId(id)
    return numId !== null && activeMatiereId.value === numId
  })
  
  /** Vérifier s'il y a une matière active */
  const hasActiveMatiere = computed(() => activeMatiereId.value !== null)

  // ========================================
  // ACTIONS PRINCIPALES
  // ========================================
  
  /**
   * Définir une matière comme active (Backend + localStorage)
   * @param {number|string} id - ID de la matière à activer
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const setActiveMatiere = async (id) => {
    const numId = normalizeId(id)
    
    if (!numId) {
      logOperation('setActiveMatiere', { id, error: ERROR_MESSAGES.INVALID_ID }, 'warn')
      return false
    }
    
    if (activeMatiereId.value === numId) {
      logOperation('setActiveMatiere', { id: numId, status: 'already_active' })
      return true
    }
    
    try {
      // Optimistic update
      const previousId = activeMatiereId.value
      activeMatiereId.value = numId
      safeSetStorage(STORAGE_KEYS.ACTIVE_MATIERE, numId)
      
      logOperation('setActiveMatiere', { 
        id: numId, 
        previousId,
        status: 'local_update',
        authenticated: isUserAuthenticated()
      })
      
      // Si utilisateur non connecté, on s'arrête là
      if (!isUserAuthenticated()) {
        return true
      }
      
      // Sync avec backend
      isSyncing.value = true
      lastSyncError.value = null
      
      await apiSetActive(numId)
      
      logOperation('setActiveMatiere', { 
        id: numId, 
        status: 'backend_success' 
      })
      
      return true
    } catch (error) {
      // Rollback en cas d'erreur
      activeMatiereId.value = previousId
      if (previousId) {
        safeSetStorage(STORAGE_KEYS.ACTIVE_MATIERE, previousId)
      } else {
        localStorage.removeItem(STORAGE_KEYS.ACTIVE_MATIERE)
      }
      
      lastSyncError.value = handleError(error, 'setActiveMatiere', { matiereId: numId })
      return false
    } finally {
      isSyncing.value = false
    }
  }
  
  /**
   * Désactiver la matière active
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const clearActiveMatiere = async () => {
    try {
      const previousId = activeMatiereId.value
      activeMatiereId.value = null
      localStorage.removeItem(STORAGE_KEYS.ACTIVE_MATIERE)
      
      logOperation('clearActiveMatiere', { 
        previousId,
        status: 'cleared'
      })
      
      return true
    } catch (error) {
      lastSyncError.value = handleError(error, 'clearActiveMatiere')
      return false
    }
  }

  // ========================================
  // ACTIONS DE GESTION
  // ========================================
  
  /**
   * Charger la matière active depuis localStorage
   */
  const loadActiveMatiereId = async () => {
    try {
      const stored = safeGetStorage(STORAGE_KEYS.ACTIVE_MATIERE, null)
      const validId = stored !== null ? normalizeId(stored) : null
      activeMatiereId.value = validId
      
      logOperation('loadActiveMatiereId', { 
        loadedId: validId,
        storedValue: stored 
      })
    } catch (error) {
      lastSyncError.value = handleError(error, 'loadActiveMatiereId')
      activeMatiereId.value = null
    }
  }
  
  /**
   * Définir la matière active intelligemment selon le contexte
   * Si aucune matière n'est active, prend la première des matières sélectionnées
   * @param {Array<number>} selectedIds - IDs des matières sélectionnées
   * @returns {Promise<number|null>} - L'ID de la matière active ou null
   */
  const getOrSetSmartActiveMatiere = async (selectedIds = []) => {
    try {
      // Si on a déjà une matière active, la retourner
      if (activeMatiereId.value) {
        return activeMatiereId.value
      }
      
      // Si on a des matières sélectionnées, prendre la première
      if (selectedIds.length > 0) {
        const firstSelectedId = selectedIds[0]
        const success = await setActiveMatiere(firstSelectedId)
        if (success) {
          return firstSelectedId
        }
      }
      
      // Aucune matière disponible
      logOperation('getOrSetSmartActiveMatiere', { 
        status: 'no_matiere_available',
        selectedCount: selectedIds.length 
      })
      
      return null
    } catch (error) {
      lastSyncError.value = handleError(error, 'getOrSetSmartActiveMatiere')
      return null
    }
  }
  
  /**
   * Définir la matière active depuis un ID
   * @param {number|string} id - ID de la matière à définir comme active
   */
  const setActiveMatiereId = (id) => {
    const numId = normalizeId(id)
    activeMatiereId.value = numId
    
    if (numId) {
      safeSetStorage(STORAGE_KEYS.ACTIVE_MATIERE, numId)
    } else {
      localStorage.removeItem(STORAGE_KEYS.ACTIVE_MATIERE)
    }
    
    logOperation('setActiveMatiereId', { 
      id: numId,
      status: 'direct_set'
    })
  }

  // ========================================
  // RETOUR DU STORE
  // ========================================
  
  return {
    // État
    activeMatiereId,
    isSyncing,
    lastSyncError,
    
    // Getters
    isActiveMatiere,
    hasActiveMatiere,
    
    // Actions principales
    setActiveMatiere,
    clearActiveMatiere,
    
    // Actions de gestion
    loadActiveMatiereId,
    getOrSetSmartActiveMatiere,
    setActiveMatiereId
  }
}) 