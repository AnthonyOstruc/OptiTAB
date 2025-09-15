import apiClient, { apiUtils as clientUtils } from './client'

/**
 * API Base - Fonctions génériques pour éviter la répétition de code
 * Architecture DRY et professionnelle
 */

/**
 * Classe de base pour les opérations CRUD
 */
export class BaseAPI {
  constructor(endpoint) {
    this.endpoint = endpoint
  }

  // ========================================
  // OPÉRATIONS CRUD DE BASE
  // ========================================

  /**
   * Récupérer tous les éléments
   */
  async getAll(params = {}) {
    try {
      // Utiliser cachedGet pour réduire la charge et éviter les timeouts répétés
      const response = await clientUtils.cachedGet(this.endpoint, { params, ttl: 120000 })
      return response.data
    } catch (error) {
      this.handleError('récupération', error)
      throw error
    }
  }

  /**
   * Récupérer un élément par ID
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`${this.endpoint}${id}/`)
      return response.data
    } catch (error) {
      this.handleError(`récupération de l'élément ${id}`, error)
      throw error
    }
  }

  /**
   * Créer un nouvel élément
   */
  async create(data) {
    try {
      const response = await apiClient.post(this.endpoint, data)
      return response.data
    } catch (error) {
      this.handleError('création', error)
      throw error
    }
  }

  /**
   * Mettre à jour un élément
   */
  async update(id, data) {
    try {
      const response = await apiClient.patch(`${this.endpoint}${id}/`, data)
      return response.data
    } catch (error) {
      this.handleError(`mise à jour de l'élément ${id}`, error)
      throw error
    }
  }

  /**
   * Supprimer un élément
   */
  async delete(id) {
    try {
      await apiClient.delete(`${this.endpoint}${id}/`)
    } catch (error) {
      this.handleError(`suppression de l'élément ${id}`, error)
      throw error
    }
  }

  // ========================================
  // OPÉRATIONS AVANCÉES
  // ========================================

  /**
   * Récupérer avec filtres
   */
  async getByFilter(filters = {}) {
    return this.getAll(filters)
  }

  /**
   * Récupérer par relation
   */
  async getByRelation(relationField, relationId, params = {}) {
    return this.getAll({ ...params, [relationField]: relationId })
  }

  /**
   * Endpoint hiérarchique
   */
  async getHierarchical(parentId, childEndpoint) {
    try {
      const response = await apiClient.get(`${this.endpoint}${parentId}/${childEndpoint}/`)
      return response.data
    } catch (error) {
      this.handleError(`récupération hiérarchique ${childEndpoint}`, error)
      throw error
    }
  }

  // ========================================
  // UTILITAIRES
  // ========================================

  /**
   * Gestion centralisée des erreurs
   */
  handleError(operation, error) {
    console.error(`Erreur lors de la ${operation}:`, error)
  }

  /**
   * Récupérer la hiérarchie complète
   */
  async getHierarchy(id, childEndpoint) {
    try {
      const [parent, children] = await Promise.all([
        this.getById(id),
        this.getHierarchical(id, childEndpoint)
      ])
      
      return { parent, children }
    } catch (error) {
      this.handleError(`récupération de la hiérarchie ${id}`, error)
      throw error
    }
  }
}

/**
 * Fonctions utilitaires pour les endpoints
 */
export const apiUtils = {
  /**
   * Créer un endpoint avec gestion d'erreur
   */
  createEndpoint(endpoint) {
    return new BaseAPI(endpoint)
  },

  /**
   * Créer des fonctions CRUD pour un endpoint
   */
  createCRUDFunctions(endpoint) {
    const api = new BaseAPI(endpoint)
    
    return {
      getAll: (params) => api.getAll(params),
      getById: (id) => api.getById(id),
      create: (data) => api.create(data),
      update: (id, data) => api.update(id, data),
      delete: (id) => api.delete(id),
      getByFilter: (filters) => api.getByFilter(filters),
      getByRelation: (field, id, params) => api.getByRelation(field, id, params),
      getHierarchical: (parentId, childEndpoint) => api.getHierarchical(parentId, childEndpoint),
      getHierarchy: (id, childEndpoint) => api.getHierarchy(id, childEndpoint)
    }
  }
}
