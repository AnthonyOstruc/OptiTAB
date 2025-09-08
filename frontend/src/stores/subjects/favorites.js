import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  addFavoriteMatiere as apiAddFavorite,
  removeFavoriteMatiere as apiRemoveFavorite
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
 * Store pour la gestion des matières favorites
 * Gère l'ajout/suppression des favoris avec synchronisation backend
 */
export const useFavoritesStore = defineStore('subjects-favorites', () => {
  // ========================================
  // ÉTAT RÉACTIF
  // ========================================
  
  /** IDs des matières marquées comme favorites */
  const favoriteMatieresIds = ref([])
  
  /** Indicateur de synchronisation en cours */
  const isSyncing = ref(false)
  
  /** Dernière erreur de synchronisation */
  const lastSyncError = ref(null)

  // ========================================
  // GETTERS CALCULÉS
  // ========================================
  
  /** Nombre de matières favorites */
  const favoriteMatieresCount = computed(() => favoriteMatieresIds.value.length)
  
  /** Vérifier si on peut ajouter plus de matières favorites */
  const canAddMoreFavorites = computed(() => {
    return canAddMore(favoriteMatieresCount.value, DEFAULTS.MAX_FAVORITE_MATIERES)
  })
  
  /** Vérifier si une matière est favorite */
  const isFavoriteMatiere = computed(() => (id) => {
    const numId = normalizeId(id)
    return numId !== null && favoriteMatieresIds.value.includes(numId)
  })

  // ========================================
  // ACTIONS PRINCIPALES
  // ========================================
  
  /**
   * Ajouter une matière aux favoris (Backend + localStorage)
   * @param {number|string} id - ID de la matière à ajouter
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const addFavoriteMatiere = async (id) => {
    const numId = normalizeId(id)
    
    // Validation
    if (!numId) {
      logOperation('addFavoriteMatiere', { id, error: ERROR_MESSAGES.INVALID_ID }, 'warn')
      return false
    }
    
    if (favoriteMatieresIds.value.includes(numId)) {
      logOperation('addFavoriteMatiere', { id: numId, status: 'already_favorite' })
      return true
    }
      
    if (!canAddMoreFavorites.value) {
      logOperation('addFavoriteMatiere', { 
        id: numId, 
        error: ERROR_MESSAGES.LIMIT_REACHED,
        currentCount: favoriteMatieresCount.value,
        maxCount: DEFAULTS.MAX_FAVORITE_MATIERES
      }, 'warn')
      return false
    }
    
    // Mise à jour locale (toujours)
    favoriteMatieresIds.value.push(numId)
    safeSetStorage(STORAGE_KEYS.FAVORITE_MATIERES, favoriteMatieresIds.value)
    
    logOperation('addFavoriteMatiere', { 
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
      
      await apiAddFavorite(numId)
      
      logOperation('addFavoriteMatiere', { 
        id: numId, 
        status: 'backend_success' 
      })
      
      return true
    } catch (error) {
      // Gestion d'erreur avec rollback si nécessaire
      if (handleAuthError(error, 'addFavoriteMatiere')) {
        return true // Garde le changement local
      }
      
      // Rollback pour autres erreurs
      favoriteMatieresIds.value = favoriteMatieresIds.value.filter(fav => fav !== numId)
      safeSetStorage(STORAGE_KEYS.FAVORITE_MATIERES, favoriteMatieresIds.value)
      
      lastSyncError.value = handleError(error, 'addFavoriteMatiere', { matiereId: numId })
      return false
    } finally {
      isSyncing.value = false
    }
  }
  
  /**
   * Supprimer une matière des favoris (Backend + localStorage)
   * @param {number|string} id - ID de la matière à supprimer
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const removeFavoriteMatiere = async (id) => {
    const numId = normalizeId(id)
    
    if (!numId) {
      logOperation('removeFavoriteMatiere', { id, error: ERROR_MESSAGES.INVALID_ID }, 'warn')
      return false
    }
    
    const index = favoriteMatieresIds.value.indexOf(numId)
    if (index === -1) {
      logOperation('removeFavoriteMatiere', { id: numId, status: 'not_found' })
      return true
    }
    
    // Mise à jour locale (toujours)
    favoriteMatieresIds.value.splice(index, 1)
    safeSetStorage(STORAGE_KEYS.FAVORITE_MATIERES, favoriteMatieresIds.value)
    
    logOperation('removeFavoriteMatiere', { 
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
      
      await apiRemoveFavorite(numId)
      
      logOperation('removeFavoriteMatiere', { 
        id: numId, 
        status: 'backend_success' 
      })
      
      return true
    } catch (error) {
      // Gestion d'erreur avec rollback si nécessaire
      if (handleAuthError(error, 'removeFavoriteMatiere')) {
        return true // Garde le changement local
      }
      
      // Rollback pour autres erreurs
      favoriteMatieresIds.value.splice(index, 0, numId)
      safeSetStorage(STORAGE_KEYS.FAVORITE_MATIERES, favoriteMatieresIds.value)
      
      lastSyncError.value = handleError(error, 'removeFavoriteMatiere', { matiereId: numId })
      return false
    } finally {
      isSyncing.value = false
    }
  }
  
  /**
   * Bascule le statut favori d'une matière
   * @param {number|string} matiereId - L'ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const toggleFavoriteMatiere = async (matiereId) => {
    const numId = normalizeId(matiereId)
    
    if (!numId) {
      logOperation('toggleFavoriteMatiere', { matiereId, error: ERROR_MESSAGES.INVALID_ID }, 'warn')
      return false
    }
      
    try {
      if (favoriteMatieresIds.value.includes(numId)) {
        // Retirer des favoris
        return await removeFavoriteMatiere(numId)
      } else {
        // Ajouter aux favoris
        return await addFavoriteMatiere(numId)
      }
    } catch (error) {
      lastSyncError.value = handleError(error, 'toggleFavoriteMatiere', { matiereId: numId })
      return false
    }
  }

  // ========================================
  // ACTIONS DE GESTION
  // ========================================
  
  /**
   * Charger les favoris depuis localStorage
   */
  const loadFavoriteMatieresIds = async () => {
    try {
      const stored = safeGetStorage(STORAGE_KEYS.FAVORITE_MATIERES, [])
      const validIds = validateAndNormalizeIds(stored)
      favoriteMatieresIds.value = validIds
      
      logOperation('loadFavoriteMatieresIds', { 
        loadedCount: validIds.length,
        totalStored: stored.length 
      })
    } catch (error) {
      lastSyncError.value = handleError(error, 'loadFavoriteMatieresIds')
      favoriteMatieresIds.value = []
    }
  }
  
  /**
   * Vider tous les favoris
   */
  const clearFavorites = async () => {
    try {
      const favoriteIds = [...favoriteMatieresIds.value]
      
      for (const id of favoriteIds) {
        await removeFavoriteMatiere(id)
      }
      
      logOperation('clearFavorites', { 
        clearedCount: favoriteIds.length 
      })
      
      return true
    } catch (error) {
      lastSyncError.value = handleError(error, 'clearFavorites')
      return false
    }
  }
  
  /**
   * Définir les favoris depuis un tableau d'IDs
   * @param {Array<number|string>} ids - IDs des matières favorites
   */
  const setFavoriteMatieresIds = (ids) => {
    const validIds = validateAndNormalizeIds(ids)
    favoriteMatieresIds.value = validIds
    safeSetStorage(STORAGE_KEYS.FAVORITE_MATIERES, validIds)
    
    logOperation('setFavoriteMatieresIds', { 
      setCount: validIds.length,
      originalCount: ids.length 
    })
  }

  // ========================================
  // RETOUR DU STORE
  // ========================================
  
  return {
    // État
    favoriteMatieresIds,
    isSyncing,
    lastSyncError,
    
    // Getters
    favoriteMatieresCount,
    canAddMoreFavorites,
    isFavoriteMatiere,
    
    // Actions principales
    addFavoriteMatiere,
    removeFavoriteMatiere,
    toggleFavoriteMatiere,
    
    // Actions de gestion
    loadFavoriteMatieresIds,
    clearFavorites,
    setFavoriteMatieresIds
  }
}) 