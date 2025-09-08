import { apiUtils } from './base'

/**
 * API Curriculum - Architecture DRY et professionnelle
 * Matières → Thèmes → Notions → Chapitres → Exercices
 */

// ========================================
// MATIÈRES API
// ========================================

// Fonction pour obtenir l'API matières de manière paresseuse
const getMatieresAPI = () => {
  if (!getMatieresAPI._instance) {
    getMatieresAPI._instance = apiUtils.createCRUDFunctions('/api/matieres/')
  }
  return getMatieresAPI._instance
}

// Fonctions de base
export const getMatieres = (params) => getMatieresAPI().getAll(params)
export const getMatiereDetail = (id) => getMatieresAPI().getById(id)
export const createMatiere = (data) => getMatieresAPI().create(data)
export const updateMatiere = (id, data) => getMatieresAPI().update(id, data)
export const deleteMatiere = (id) => getMatieresAPI().delete(id)

// Fonctions spécialisées
export const getMatieresByNiveau = (niveauId, params = {}) => 
  getMatieresAPI().getByRelation('niveau', niveauId, params)

export const getMatieresByPays = (paysId, params = {}) => 
  getMatieresAPI().getByRelation('pays', paysId, params)

// ========================================
// THÈMES API
// ========================================

// Fonction pour obtenir l'API thèmes de manière paresseuse
const getThemesAPI = () => {
  if (!getThemesAPI._instance) {
    getThemesAPI._instance = apiUtils.createCRUDFunctions('/api/themes/')
  }
  return getThemesAPI._instance
}

// Fonctions de base
export const getThemes = (params) => getThemesAPI().getAll(params)
export const getThemeDetail = (id) => getThemesAPI().getById(id)
export const createTheme = (data) => getThemesAPI().create(data)
export const updateTheme = (id, data) => getThemesAPI().update(id, data)
export const deleteTheme = (id) => getThemesAPI().delete(id)

// Fonctions spécialisées
export const getThemesByMatiere = (matiereId, params = {}) => 
  getThemesAPI().getByRelation('matiere', matiereId, params)

// ========================================
// NOTIONS API
// ========================================

// Fonction pour obtenir l'API notions de manière paresseuse
const getNotionsAPI = () => {
  if (!getNotionsAPI._instance) {
    getNotionsAPI._instance = apiUtils.createCRUDFunctions('/api/notions/')
  }
  return getNotionsAPI._instance
}

// Fonctions de base
export const getNotions = (params) => getNotionsAPI().getAll(params)
export const getNotionDetail = (id) => getNotionsAPI().getById(id)
export const createNotion = (data) => getNotionsAPI().create(data)
export const updateNotion = (id, data) => getNotionsAPI().update(id, data)
export const deleteNotion = (id) => getNotionsAPI().delete(id)

// Fonctions spécialisées
export const getNotionsByTheme = (themeId, params = {}) => 
  getNotionsAPI().getByRelation('theme', themeId, params)

// ========================================
// CHAPITRES API
// ========================================

// Fonction pour obtenir l'API chapitres de manière paresseuse
const getChapitresAPI = () => {
  if (!getChapitresAPI._instance) {
    getChapitresAPI._instance = apiUtils.createCRUDFunctions('/api/chapitres/')
  }
  return getChapitresAPI._instance
}

// Fonctions de base
export const getChapitres = (params) => getChapitresAPI().getAll(params)
export const getChapitreDetail = (id) => getChapitresAPI().getById(id)
export const createChapitre = (data) => {
  const payload = { ...data }
  if (payload.nom != null && payload.titre == null) payload.titre = payload.nom
  return getChapitresAPI().create(payload)
}
export const updateChapitre = (id, data) => {
  const payload = { ...data }
  if (payload.nom != null && payload.titre == null) payload.titre = payload.nom
  return getChapitresAPI().update(id, payload)
}
export const deleteChapitre = (id) => getChapitresAPI().delete(id)

// Fonctions spécialisées
export const getChapitresByNotion = (notionId, params = {}) => 
  getChapitresAPI().getByRelation('notion', notionId, params)

// ========================================
// EXERCICES API
// ========================================

// Fonction pour obtenir l'API exercices de manière paresseuse
const getExercicesAPI = () => {
  if (!getExercicesAPI._instance) {
    getExercicesAPI._instance = apiUtils.createCRUDFunctions('/api/exercices/')
  }
  return getExercicesAPI._instance
}

// Fonctions de base
export const getExercices = (params) => getExercicesAPI().getAll(params)
export const getExerciceDetail = (id) => getExercicesAPI().getById(id)
export const createExercice = (data) => getExercicesAPI().create(data)
export const updateExercice = (id, data) => getExercicesAPI().update(id, data)
export const deleteExercice = (id) => getExercicesAPI().delete(id)

// Fonctions spécialisées
export const getExercicesByChapitre = (chapitreId, params = {}) => 
  getExercicesAPI().getByRelation('chapitre', chapitreId, params)

// ========================================
// ENDPOINTS HIÉRARCHIQUES
// ========================================

export const getMatiereThemes = (matiereId) => 
  getMatieresAPI().getHierarchical(matiereId, 'themes')

export const getThemeNotions = (themeId) => 
  getThemesAPI().getHierarchical(themeId, 'notions')

export const getNotionChapitres = (notionId) => 
  getNotionsAPI().getHierarchical(notionId, 'chapitres')

export const getNotionChapitresAvecMeta = async (notionId) => {
  // Appel direct via apiClient.get pour éviter la dépendance à apiUtils.request
  const { default: apiClient } = await import('./client')
  return apiClient.get(`/api/notions/${notionId}/chapitres-avec-meta/`)
}

export const getChapitreExercices = (chapitreId) => 
  getChapitresAPI().getHierarchical(chapitreId, 'exercices')

// ========================================
// UTILITAIRES HIÉRARCHIQUES
// ========================================

export const getMatiereHierarchy = (matiereId) => 
  getMatieresAPI().getHierarchy(matiereId, 'themes')

export const getThemeHierarchy = (themeId) => 
  getThemesAPI().getHierarchy(themeId, 'notions')

export const getNotionHierarchy = (notionId) => 
  getNotionsAPI().getHierarchy(notionId, 'chapitres')

export const getChapitreHierarchy = (chapitreId) => 
  getExercicesAPI().getHierarchy(chapitreId, 'exercices')
