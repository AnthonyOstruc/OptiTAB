import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  addSelectedMatiere as apiAddSelected,
  removeSelectedMatiere as apiRemoveSelected
} from '@/api'
import { 
  STORAGE_KEYS, 
  DEFAULTS, 
  ERROR_MESSAGES 
} from './constants'
import { 
  normalizeId, 
  safeSetStorage, 
  safeGetStorage, 
  isUserAuthenticated,
  handleError,
  handleAuthError,
  canAddMore,
  logOperation,
  validateAndNormalizeIds
} from './utils'

/**
 * Store pour la gestion des matières sélectionnées (onglets)
 * Gère l'ajout/suppression des onglets avec synchronisation backend
 */
export const useSelectedStore = defineStore('subjects-selected', () => {
  // ========================================
  // ÉTAT RÉACTIF
  // ========================================
  
  /** IDs des matières ouvertes en tant que tabs */
  const selectedMatieresIds = ref([])
  
  /** Indicateur de synchronisation en cours */
  const isSyncing = ref(false)
  
  /** Dernière erreur de synchronisation */
  const lastSyncError = ref(null)

  // ========================================
  // GETTERS CALCULÉS
  // ========================================
  
  /** Nombre de matières sélectionnées */
  const selectedMatieresCount = computed(() => selectedMatieresIds.value.length)
  
  /** Vérifier si on peut ajouter plus de matières sélectionnées */
  const canAddMoreSelected = computed(() => {
    return canAddMore(selectedMatieresCount.value, DEFAULTS.MAX_SELECTED_MATIERES)
  })
  
  /** Vérifier si une matière est sélectionnée */
  const isSelectedMatiere = computed(() => (id) => {
    const numId = normalizeId(id)
    return numId !== null && selectedMatieresIds.value.includes(numId)
  })

  // ========================================
  // ACTIONS PRINCIPALES
  // ========================================
  
  /**
   * Ajouter une matière aux onglets sélectionnés (Backend + localStorage)
   * @param {number|string} id - ID de la matière à ajouter
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const addMatiereId = async (id) => {
    const numId = normalizeId(id)
    
    // Validation
    if (!numId) {
      logOperation('addMatiereId', { id, error: ERROR_MESSAGES.INVALID_ID }, 'warn')
      return false
    }
      
    if (selectedMatieresIds.value.includes(numId)) {
      logOperation('addMatiereId', { id: numId, status: 'already_selected' })
      return true
    }
      
    if (!canAddMoreSelected.value) {
      logOperation('addMatiereId', { 
        id: numId, 
        error: ERROR_MESSAGES.LIMIT_REACHED,
        currentCount: selectedMatieresCount.value,
        maxCount: DEFAULTS.MAX_SELECTED_MATIERES
      }, 'warn')
      return false
    }
      
    // Mise à jour locale (toujours)
    selectedMatieresIds.value.push(numId)
    safeSetStorage(STORAGE_KEYS.SELECTED_MATIERES, selectedMatieresIds.value)
    
    logOperation('addMatiereId', { 
      id: numId, 
      status: 'local_update',
      authenticated: isUserAuthenticated()
    })
      
    // Si utilisateur non connecté, on s'arrête là
    if (!isUserAuthenticated()) {
      return true
    }
    
    try {
      // Sync avec backend seulement si connecté
      isSyncing.value = true
      lastSyncError.value = null
      
      await apiAddSelected(numId)
      
      logOperation('addMatiereId', { 
        id: numId, 
        status: 'backend_success' 
      })
      
      return true
    } catch (error) {
      // Gestion d'erreur avec rollback si nécessaire
      if (handleAuthError(error, 'addMatiereId')) {
        return true // Garde le changement local
      }
      
      // Rollback pour autres erreurs
      selectedMatieresIds.value = selectedMatieresIds.value.filter(sel => sel !== numId)
      safeSetStorage(STORAGE_KEYS.SELECTED_MATIERES, selectedMatieresIds.value)
      
      lastSyncError.value = handleError(error, 'addMatiereId', { matiereId: numId })
      return false
    } finally {
      isSyncing.value = false
    }
  }
  
  /**
   * Supprimer une matière des onglets sélectionnés (Backend + localStorage)
   * @param {number|string} id - ID de la matière à supprimer
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const removeMatiereId = async (id) => {
    const numId = normalizeId(id)
    
    if (!numId) {
      logOperation('removeMatiereId', { id, error: ERROR_MESSAGES.INVALID_ID }, 'warn')
      return false
    }
    
    const index = selectedMatieresIds.value.indexOf(numId)
    if (index === -1) {
      logOperation('removeMatiereId', { id: numId, status: 'not_found' })
      return true
    }
    
    try {
      // Optimistic update
      selectedMatieresIds.value.splice(index, 1)
      safeSetStorage(STORAGE_KEYS.SELECTED_MATIERES, selectedMatieresIds.value)
      
      logOperation('removeMatiereId', { 
        id: numId, 
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
      
      await apiRemoveSelected(numId)
      
      logOperation('removeMatiereId', { 
        id: numId, 
        status: 'backend_success' 
      })
      
      return true
    } catch (error) {
      // Rollback en cas d'erreur
      selectedMatieresIds.value.splice(index, 0, numId)
      safeSetStorage(STORAGE_KEYS.SELECTED_MATIERES, selectedMatieresIds.value)
      
      lastSyncError.value = handleError(error, 'removeMatiereId', { matiereId: numId })
      return false
    } finally {
      isSyncing.value = false
    }
  }

  // ========================================
  // ACTIONS DE GESTION
  // ========================================
  
  /**
   * Charger les matières sélectionnées depuis localStorage
   */
  const loadSelectedMatieresIds = async () => {
    try {
      const stored = safeGetStorage(STORAGE_KEYS.SELECTED_MATIERES, [])
      const validIds = validateAndNormalizeIds(stored)
      selectedMatieresIds.value = validIds
      
      logOperation('loadSelectedMatieresIds', { 
        loadedCount: validIds.length,
        totalStored: stored.length 
      })
    } catch (error) {
      lastSyncError.value = handleError(error, 'loadSelectedMatieresIds')
      selectedMatieresIds.value = []
    }
  }
  
  /**
   * Vider toutes les matières sélectionnées
   */
  const clearSelectedMatieres = async () => {
    try {
      const selectedIds = [...selectedMatieresIds.value]
      
      for (const id of selectedIds) {
        await removeMatiereId(id)
      }
      
      logOperation('clearSelectedMatieres', { 
        clearedCount: selectedIds.length 
      })
      
      return true
    } catch (error) {
      lastSyncError.value = handleError(error, 'clearSelectedMatieres')
      return false
    }
  }
  
  /**
   * Définir les matières sélectionnées depuis un tableau d'IDs
   * @param {Array<number|string>} ids - IDs des matières sélectionnées
   */
  const setSelectedMatieresIds = (ids) => {
    const validIds = validateAndNormalizeIds(ids)
    selectedMatieresIds.value = validIds
    safeSetStorage(STORAGE_KEYS.SELECTED_MATIERES, validIds)
    
    logOperation('setSelectedMatieresIds', { 
      setCount: validIds.length,
      originalCount: ids.length 
    })
  }
  
  /**
   * Ajouter plusieurs matières en une seule fois
   * @param {Array<number|string>} ids - IDs des matières à ajouter
   * @returns {Promise<boolean>} - True si toutes les opérations ont réussi
   */
  const addMultipleMatieres = async (ids) => {
    try {
      const validIds = validateAndNormalizeIds(ids)
      const results = await Promise.all(
        validIds.map(id => addMatiereId(id))
      )
      
      const successCount = results.filter(Boolean).length
      const totalCount = validIds.length
      
      logOperation('addMultipleMatieres', { 
        successCount,
        totalCount,
        successRate: `${(successCount / totalCount * 100).toFixed(1)}%`
      })
      
      return successCount === totalCount
    } catch (error) {
      lastSyncError.value = handleError(error, 'addMultipleMatieres', { ids })
      return false
    }
  }

  // ========================================
  // RETOUR DU STORE
  // ========================================
  
  return {
    // État
    selectedMatieresIds,
    isSyncing,
    lastSyncError,
    
    // Getters
    selectedMatieresCount,
    canAddMoreSelected,
    isSelectedMatiere,
    
    // Actions principales
    addMatiereId,
    removeMatiereId,
    
    // Actions de gestion
    loadSelectedMatieresIds,
    clearSelectedMatieres,
    setSelectedMatieresIds,
    addMultipleMatieres
  }
}) 