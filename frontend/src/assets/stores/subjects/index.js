import { defineStore } from 'pinia'
import { computed, unref } from 'vue'

// Import des stores spécialisés
import { useFavoritesStore } from './favorites'
import { useSelectedStore } from './selected'
import { useActiveStore } from './active'
import { useSyncStore } from './sync'

// Import des utilitaires
import { STORAGE_KEYS, DEFAULTS, ERROR_MESSAGES } from './constants'
import { 
  normalizeId, 
  safeGetStorage, 
  isUserAuthenticated,
  logOperation,
  handleError
} from './utils'

/**
 * Store principal pour la gestion des matières
 * Orchestrateur qui coordonne tous les modules spécialisés
 */
export const useSubjectsStore = defineStore('subjects', () => {
  // ========================================
  // INITIALISATION DES STORES SPÉCIALISÉS
  // ========================================
  
  const favoritesStore = useFavoritesStore()
  const selectedStore = useSelectedStore()
  const activeStore = useActiveStore()
  const syncStore = useSyncStore()

  // ========================================
  // GETTERS UNIFIÉS
  // ========================================
  
  /** IDs des matières favorites (valeur primitive, pas de Ref imbriquée) */
  const favoriteMatieresIds = computed(() => unref(favoritesStore.favoriteMatieresIds))
  
  /** IDs des matières sélectionnées (onglets) - valeur primitive */
  const selectedMatieresIds = computed(() => unref(selectedStore.selectedMatieresIds))
  
  /** ID de la matière active - valeur primitive */
  const activeMatiereId = computed(() => unref(activeStore.activeMatiereId))
  
  /** Nombre de matières favorites */
  const favoriteMatieresCount = computed(() => unref(favoritesStore.favoriteMatieresCount))
  
  /** Nombre de matières sélectionnées */
  const selectedMatieresCount = computed(() => unref(selectedStore.selectedMatieresCount))
  
  /** Vérifier si une matière est favorite */
  const isFavoriteMatiere = computed(() => favoritesStore.isFavoriteMatiere)
  
  /** Vérifier si une matière est sélectionnée */
  const isSelectedMatiere = computed(() => selectedStore.isSelectedMatiere)
  
  /** Vérifier si une matière est active */
  const isActiveMatiere = computed(() => activeStore.isActiveMatiere)
  
  /** Vérifier s'il y a une matière active */
  const hasActiveMatiere = computed(() => unref(activeStore.hasActiveMatiere))
  
  /** Vérifier si on peut ajouter plus de favoris */
  const canAddMoreFavorites = computed(() => unref(favoritesStore.canAddMoreFavorites))
  
  /** Vérifier si on peut ajouter plus de matières sélectionnées */
  const canAddMoreSelected = computed(() => unref(selectedStore.canAddMoreSelected))
  
  /** Statut de synchronisation global */
  const isSyncing = computed(() => 
    unref(favoritesStore.isSyncing) || 
    unref(selectedStore.isSyncing) || 
    unref(activeStore.isSyncing) || 
    unref(syncStore.isSyncing)
  )
  
  /** Dernière erreur de synchronisation */
  const lastSyncError = computed(() => 
    unref(favoritesStore.lastSyncError) || 
    unref(selectedStore.lastSyncError) || 
    unref(activeStore.lastSyncError) || 
    unref(syncStore.lastSyncError)
  )

  // ========================================
  // ACTIONS UNIFIÉES - FAVORIS
  // ========================================
  
  /**
   * Ajouter une matière aux favoris
   * @param {number|string} id - ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const addFavoriteMatiere = async (id) => {
    return await favoritesStore.addFavoriteMatiere(id)
  }
  
  /**
   * Supprimer une matière des favoris
   * @param {number|string} id - ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const removeFavoriteMatiere = async (id) => {
    return await favoritesStore.removeFavoriteMatiere(id)
  }
  
  /**
   * Basculer le statut favori d'une matière
   * @param {number|string} id - ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const toggleFavoriteMatiere = async (id) => {
    return await favoritesStore.toggleFavoriteMatiere(id)
  }

  // ========================================
  // ACTIONS UNIFIÉES - SÉLECTION
  // ========================================
  
  /**
   * Ajouter une matière aux onglets sélectionnés
   * @param {number|string} id - ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const addMatiereId = async (id) => {
    return await selectedStore.addMatiereId(id)
  }
  
  /**
   * Supprimer une matière des onglets sélectionnés
   * @param {number|string} id - ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const removeMatiereId = async (id) => {
    return await selectedStore.removeMatiereId(id)
  }
  
  /**
   * Ajouter plusieurs matières en lot
   * @param {Array<number|string>} ids - IDs des matières
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const addMultipleMatieres = async (ids) => {
    return await selectedStore.addMultipleMatieres(ids)
  }

  // ========================================
  // ACTIONS UNIFIÉES - MATIÈRE ACTIVE
  // ========================================
  
  /**
   * Définir une matière comme active
   * @param {number|string} id - ID de la matière
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const setActiveMatiere = async (id) => {
    return await activeStore.setActiveMatiere(id)
  }
  
  /**
   * Effacer la matière active
   * @returns {Promise<boolean>} - True si l'opération a réussi
   */
  const clearActiveMatiere = async () => {
    return await activeStore.clearActiveMatiere()
  }
  
  /**
   * Obtenir ou définir intelligemment la matière active
   * @param {Array<number|string>} selectedIds - IDs des matières sélectionnées
   * @returns {Promise<number|null>} - ID de la matière active
   */
  const getOrSetSmartActiveMatiere = async (selectedIds = []) => {
    return await activeStore.getOrSetSmartActiveMatiere(selectedIds)
  }

  // ========================================
  // ACTIONS UNIFIÉES - SYNCHRONISATION
  // ========================================
  
  /**
   * Charger les préférences depuis le backend
   * @returns {Promise<boolean>} - True si le chargement a réussi
   */
  const loadPreferencesFromServer = async () => {
    const stores = {
      selectedStore,
      favoritesStore,
      activeStore
    }
    return await syncStore.loadPreferencesFromServer(stores)
  }
  
  /**
   * Synchroniser avec le backend
   * @returns {Promise<boolean>} - True si la synchronisation a réussi
   */
  const syncWithBackend = async () => {
    const stores = {
      selectedStore,
      favoritesStore,
      activeStore
    }
    return await syncStore.syncWithBackend(stores)
  }
  
  /**
   * Initialiser après connexion
   * @returns {Promise<boolean>} - True si l'initialisation a réussi
   */
  const initializeAfterLogin = async () => {
    const stores = {
      selectedStore,
      favoritesStore,
      activeStore
    }
    return await syncStore.initializeAfterLogin(stores)
  }

  // ========================================
  // ACTIONS UNIFIÉES - GESTION D'ÉTAT
  // ========================================
  
  /**
   * Initialiser le store (chargement depuis localStorage + backend si connecté)
   * @returns {Promise<void>}
   */
  const initialize = async () => {
    try {
      logOperation('initialize', { status: 'starting' })
      
      // Charger depuis localStorage
      await Promise.all([
        favoritesStore.loadFavoriteMatieresIds(),
        selectedStore.loadSelectedMatieresIds(),
        activeStore.loadActiveMatiereId()
      ])
      
      // Si utilisateur connecté, synchroniser avec le backend
      if (isUserAuthenticated()) {
        await loadPreferencesFromServer()
      }
      
      logOperation('initialize', { 
        status: 'success',
        favoritesCount: favoriteMatieresCount.value,
        selectedCount: selectedMatieresCount.value,
        activeId: activeMatiereId.value
      })
    } catch (error) {
      handleError(error, 'initialize')
      throw error
    }
  }
  
  /**
   * Effacer toutes les données
   * @returns {Promise<void>}
   */
  const clearAll = async () => {
    try {
      await Promise.all([
        favoritesStore.clearFavorites(),
        selectedStore.clearSelectedMatieres(),
        activeStore.clearActiveMatiere()
      ])
      
      logOperation('clearAll', { status: 'success' })
    } catch (error) {
      handleError(error, 'clearAll')
      throw error
    }
  }
  
  /**
   * Obtenir le statut de synchronisation
   * @returns {Object} - Statut de synchronisation
   */
  const getSyncStatus = () => {
    return syncStore.getSyncStatus()
  }
  
  /**
   * Effacer les erreurs de synchronisation
   */
  const clearSyncErrors = () => {
    favoritesStore.lastSyncError = null
    selectedStore.lastSyncError = null
    activeStore.lastSyncError = null
    syncStore.clearSyncErrors()
  }

  // ========================================
  // ACTIONS UNIFIÉES - CHARGEMENT
  // ========================================
  
  /**
   * Charger les matières favorites depuis localStorage
   * @returns {Promise<void>}
   */
  const loadFavoriteMatieresIds = async () => {
    return await favoritesStore.loadFavoriteMatieresIds()
  }
  
  /**
   * Charger les matières sélectionnées depuis localStorage
   * @returns {Promise<void>}
   */
  const loadSelectedMatieresIds = async () => {
    return await selectedStore.loadSelectedMatieresIds()
  }
  
  /**
   * Charger la matière active depuis localStorage
   * @returns {Promise<void>}
   */
  const loadActiveMatiereId = async () => {
    return await activeStore.loadActiveMatiereId()
  }

  /**
   * Obtenir les statistiques complètes du store
   * @returns {Object} - Statistiques du store
   */
  const getStats = () => {
    return {
      // État général
      hasActiveMatiere: hasActiveMatiere.value,
      activeMatiereId: activeMatiereId.value,
      
      // Compteurs
      favoritesCount: favoriteMatieresCount.value,
      selectedCount: selectedMatieresCount.value,
      
      // Limites
      canAddMoreFavorites: canAddMoreFavorites.value,
      canAddMoreSelected: canAddMoreSelected.value,
      
      // Synchronisation
      isSyncing: isSyncing.value,
      lastSyncError: lastSyncError.value,
      
      // Données détaillées
      favoriteMatieresIds: favoriteMatieresIds.value,
      selectedMatieresIds: selectedMatieresIds.value,
      
      // Authentification
      isAuthenticated: isUserAuthenticated(),
      
      // Timestamp
      timestamp: new Date().toISOString()
    }
  }

  // ========================================
  // EXPORT DES STORES SPÉCIALISÉS (pour compatibilité)
  // ========================================
  
  const stores = {
    favorites: favoritesStore,
    selected: selectedStore,
    active: activeStore,
    sync: syncStore
  }

  return {
    // État réactif
    favoriteMatieresIds,
    selectedMatieresIds,
    activeMatiereId,
    favoriteMatieresCount,
    selectedMatieresCount,
    isFavoriteMatiere,
    isSelectedMatiere,
    isActiveMatiere,
    hasActiveMatiere,
    canAddMoreFavorites,
    canAddMoreSelected,
    isSyncing,
    lastSyncError,
    
    // Actions - Favoris
    addFavoriteMatiere,
    removeFavoriteMatiere,
    toggleFavoriteMatiere,
    
    // Actions - Sélection
    addMatiereId,
    removeMatiereId,
    addMultipleMatieres,
    
    // Actions - Matière active
    setActiveMatiere,
    clearActiveMatiere,
    getOrSetSmartActiveMatiere,
    
    // Actions - Synchronisation
    loadPreferencesFromServer,
    syncWithBackend,
    initializeAfterLogin,
    
    // Actions - Gestion d'état
    initialize,
    clearAll,
    getSyncStatus,
    clearSyncErrors,
    getStats,
    
    // Actions - Chargement
    loadFavoriteMatieresIds,
    loadSelectedMatieresIds,
    loadActiveMatiereId,
    
    // Stores spécialisés (pour compatibilité)
    stores
  }
}) 