import apiClient from './client'

/**
 * API pour la gestion des niveaux
 */

// Récupérer tous les niveaux
export async function getNiveaux(params = {}) {
  try {
    const response = await apiClient.get('/api/niveaux/', { params })
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des niveaux:', error)
    throw error
  }
}

// Récupérer un niveau spécifique
export async function getNiveau(niveauId) {
  try {
    const response = await apiClient.get(`/api/niveaux/${niveauId}/`)
    return response.data
  } catch (error) {
    console.error(`Erreur lors de la récupération du niveau ${niveauId}:`, error)
    throw error
  }
}

// Récupérer les statistiques d'un niveau
export async function getNiveauStatistiques(niveauId) {
  try {
    const response = await apiClient.get(`/api/niveaux/${niveauId}/statistiques/`)
    return response.data
  } catch (error) {
    console.error(`Erreur lors de la récupération des statistiques du niveau ${niveauId}:`, error)
    throw error
  }
}

// Récupérer les recommandations d'un niveau
export async function getNiveauRecommandations(niveauId) {
  try {
    const response = await apiClient.get(`/api/niveaux/${niveauId}/recommandations/`)
    return response.data
  } catch (error) {
    console.error(`Erreur lors de la récupération des recommandations du niveau ${niveauId}:`, error)
    throw error
  }
}

// Récupérer le contenu complet d'un niveau
export async function getNiveauContenuComplet(niveauId) {
  try {
    const response = await apiClient.get(`/api/niveaux/${niveauId}/contenu_complet/`)
    return response.data
  } catch (error) {
    console.error(`Erreur lors de la récupération du contenu complet du niveau ${niveauId}:`, error)
    throw error
  }
}

// Récupérer le niveau pour l'utilisateur connecté
export async function getNiveauPourUtilisateur() {
  try {
    const response = await apiClient.get('/api/niveaux/pour_utilisateur/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération du niveau pour utilisateur:', error)
    throw error
  }
}

// Récupérer les niveaux actifs
export async function getNiveauxActifs(params = {}) {
  try {
    const response = await apiClient.get('/api/niveaux/actifs/', { params })
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des niveaux actifs:', error)
    throw error
  }
}

// Récupérer les niveaux avec statistiques
export async function getNiveauxAvecStatistiques(params = {}) {
  try {
    const response = await apiClient.get('/api/niveaux/avec_statistiques/', { params })
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des niveaux avec statistiques:', error)
    throw error
  }
}

// Créer un nouveau niveau (admin)
export async function createNiveau(niveauData) {
  try {
    const response = await apiClient.post('/api/niveaux/', niveauData)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la création du niveau:', error)
    throw error
  }
}

// Mettre à jour un niveau (admin)
export async function updateNiveau(niveauId, niveauData) {
  try {
    const response = await apiClient.patch(`/api/niveaux/${niveauId}/`, niveauData)
    return response.data
  } catch (error) {
    console.error(`Erreur lors de la mise à jour du niveau ${niveauId}:`, error)
    throw error
  }
}

// Supprimer un niveau (admin)
export async function deleteNiveau(niveauId) {
  try {
    await apiClient.delete(`/api/niveaux/${niveauId}/`)
  } catch (error) {
    console.error(`Erreur lors de la suppression du niveau ${niveauId}:`, error)
    throw error
  }
}

// Assigner du contenu à un niveau
export async function assignerContenuNiveau(niveauId, contenuData) {
  try {
    const response = await apiClient.post(`/api/niveaux/${niveauId}/assigner_contenu/`, {
      matieres: contenuData.matieres || [],
      cours: contenuData.cours || [],
      exercices: contenuData.exercices || [],
      quiz: contenuData.quiz || []
    })
    return response.data
  } catch (error) {
    console.error(`Erreur lors de l'assignation de contenu au niveau ${niveauId}:`, error)
    throw error
  }
}

/**
 * Récupère les niveaux actifs pour un pays spécifique
 * @param {number} paysId - ID du pays
 * @returns {Promise<Array>} Liste des niveaux du pays
 */
export const getNiveauxParPays = async (paysId) => {
  try {
    const response = await apiClient.get(`/api/pays/${paysId}/niveaux/`)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des niveaux par pays:', error)
    throw error
  }
}

/**
 * Récupère tous les niveaux avec leur pays associé
 * @returns {Promise<Array>} Liste de tous les niveaux avec leurs pays
 */
export const getNiveauxByPays = async () => {
  try {
    const response = await apiClient.get('/api/niveaux/')
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des niveaux:', error)
    throw error
  }
} 