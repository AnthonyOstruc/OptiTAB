import apiClient from './client'

/**
 * Récupérer toutes les préférences utilisateur (favoris + onglets sélectionnés)
 */
export const getUserPreferences = () => {
  return apiClient.get('/api/users/preferences/')
}

/**
 * Mettre à jour en masse les préférences de l'utilisateur
 */
export const bulkUpdatePreferences = (preferences) => {
  return apiClient.post('/api/users/preferences/bulk-update/', preferences)
}

// === GESTION DES MATIÈRES FAVORITES ===

/**
 * Récupérer les matières favorites de l'utilisateur
 */
export const getFavoriteMatieres = () => {
  return apiClient.get('/api/users/favorites/')
}

/**
 * Ajouter une matière aux favoris
 */
export const addFavoriteMatiere = (matiereId) => {
  return apiClient.post(`/api/users/favorites/add/${matiereId}/`)
}

/**
 * Supprimer une matière des favoris
 */
export const removeFavoriteMatiere = (matiereId) => {
  return apiClient.delete(`/api/users/favorites/remove/${matiereId}/`)
}

// === GESTION DES ONGLETS SÉLECTIONNÉS ===

/**
 * Récupérer les onglets sélectionnés de l'utilisateur
 */
export const getSelectedMatieres = () => {
  return apiClient.get('/api/users/selected/')
}

/**
 * Ajouter une matière aux onglets sélectionnés
 */
export const addSelectedMatiere = (matiereId) => {
  return apiClient.post(`/api/users/selected/add/${matiereId}/`)
}

/**
 * Supprimer une matière des onglets sélectionnés
 */
export const removeSelectedMatiere = (matiereId) => {
  return apiClient.delete(`/api/users/selected/remove/${matiereId}/`)
}

/**
 * Définir une matière comme active
 */
export const setActiveMatiere = (matiereId) => {
  return apiClient.post(`/api/users/selected/set-active/${matiereId}/`)
}

// === FONCTIONS UTILITAIRES POUR LA SYNCHRONISATION ===

/**
 * Synchroniser les préférences localStorage avec le backend
 * (Pour la migration depuis l'ancien système)
 */
export const syncPreferencesWithBackend = async () => {
  try {
    // Récupérer les données du localStorage
    const localSelectedIds = JSON.parse(localStorage.getItem('selected-matieres-ids') || '[]')
    const localFavoriteIds = JSON.parse(localStorage.getItem('favorite-matieres-ids') || '[]')
    const localActiveId = localStorage.getItem('active-matiere-id')

    // Préparer les données pour l'envoi
    const preferences = {}

    if (localFavoriteIds.length > 0) {
      preferences.favorite_matiere_ids = localFavoriteIds
    }

    if (localSelectedIds.length > 0) {
      preferences.selected_matieres = localSelectedIds.map((id, index) => ({
        matiere_id: parseInt(id),
        order: index,
        is_active: parseInt(id) === parseInt(localActiveId)
      }))
    }

    if (localActiveId) {
      preferences.active_matiere_id = parseInt(localActiveId)
    }

    // Envoyer au backend
    if (Object.keys(preferences).length > 0) {
      await bulkUpdatePreferences(preferences)
      console.log('[API] Synchronisation des préférences avec le backend réussie')
    }

    return true
  } catch (error) {
    console.error('[API] Erreur lors de la synchronisation des préférences:', error)
    return false
  }
}

/**
 * Charger les préférences depuis le backend et les sauvegarder en local
 * (Pour la compatibilité avec l'ancien système)
 */
export const loadPreferencesFromBackend = async () => {
  try {
    const { data } = await getUserPreferences()
    
    // Extraire les données
    const favoriteIds = data.favorite_matieres?.map(f => f.matiere.id) || []
    const selectedMatieres = data.selected_matieres || []
    const activeId = data.active_matiere_id

    // Sauvegarder en localStorage pour la compatibilité
    localStorage.setItem('favorite-matieres-ids', JSON.stringify(favoriteIds))
    localStorage.setItem('selected-matieres-ids', JSON.stringify(selectedMatieres.map(s => s.matiere.id)))
    
    if (activeId) {
      localStorage.setItem('active-matiere-id', activeId.toString())
    } else {
      localStorage.removeItem('active-matiere-id')
    }

    console.log('[API] Préférences chargées depuis le backend')
    return {
      favoriteIds,
      selectedIds: selectedMatieres.map(s => s.matiere.id),
      activeId,
      selectedMatieres
    }
  } catch (error) {
    console.error('[API] Erreur lors du chargement des préférences:', error)
    return null
  }
} 