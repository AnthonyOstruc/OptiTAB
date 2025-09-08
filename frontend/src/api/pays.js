import { apiUtils } from './base'

/**
 * API Pays et Niveaux - Architecture DRY et professionnelle
 * Pays → Niveaux → Matières
 */

// ========================================
// PAYS API
// ========================================

// Fonction pour obtenir l'API de manière paresseuse
const getPaysAPI = () => {
  if (!getPaysAPI._instance) {
    getPaysAPI._instance = apiUtils.createCRUDFunctions('/api/pays/')
  }
  return getPaysAPI._instance
}

// Fonctions de base
export const getPays = (params) => getPaysAPI().getAll(params)
export const getPaysDetail = (id) => getPaysAPI().getById(id)
export const createPays = (data) => getPaysAPI().create(data)
export const updatePays = (id, data) => getPaysAPI().update(id, data)
export const deletePays = (id) => getPaysAPI().delete(id)

// Fonctions spécialisées
export const getPaysActifs = (params = {}) => 
  getPaysAPI().getByFilter({ ...params, est_actif: true })

export const searchPays = (searchTerm, params = {}) => 
  getPaysAPI().getByFilter({ ...params, search: searchTerm })

// ========================================
// NIVEAUX API
// ========================================

// Fonction pour obtenir l'API niveaux de manière paresseuse
const getNiveauxAPI = () => {
  if (!getNiveauxAPI._instance) {
    getNiveauxAPI._instance = apiUtils.createCRUDFunctions('/api/niveaux/')
  }
  return getNiveauxAPI._instance
}

// Fonctions de base
export const getNiveaux = (params) => getNiveauxAPI().getAll(params)
export const getNiveauDetail = (id) => getNiveauxAPI().getById(id)
export const createNiveau = (data) => getNiveauxAPI().create(data)
export const updateNiveau = (id, data) => getNiveauxAPI().update(id, data)
export const deleteNiveau = (id) => getNiveauxAPI().delete(id)

// Fonctions spécialisées
export const getNiveauxByPays = (paysId, params = {}) => 
  getNiveauxAPI().getByRelation('pays_id', paysId, params)

export const getNiveauxActifsByPays = (paysId, params = {}) => 
  getNiveauxAPI().getByRelation('pays_id', paysId, { ...params, est_actif: true })

// ========================================
// ENDPOINTS HIÉRARCHIQUES
// ========================================

export const getPaysNiveaux = (paysId) => 
  getPaysAPI().getHierarchical(paysId, 'niveaux')

export const getNiveauMatieres = (niveauId) => 
  getNiveauxAPI().getHierarchical(niveauId, 'matieres')

// ========================================
// UTILITAIRES HIÉRARCHIQUES
// ========================================

export const getPaysHierarchy = (paysId) => 
  getPaysAPI().getHierarchy(paysId, 'niveaux')

export const getNiveauHierarchy = (niveauId) => 
  getNiveauxAPI().getHierarchy(niveauId, 'matieres')
