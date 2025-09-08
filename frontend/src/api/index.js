/**
 * API Index - Point d'entrée centralisé pour toutes les APIs
 * Architecture DRY et professionnelle
 */

// ========================================
// IMPORTS DES APIS
// ========================================

// API de base
export { BaseAPI, apiUtils } from './base'
export { default as apiClient } from './client'

// Imports pour l'API unifiée (utilisés dans le scope local)
import {
  getPays,
  getPaysDetail,
  getPaysActifs,
  searchPays,
  createPays,
  updatePays,
  deletePays,
  getPaysNiveaux,
  getPaysHierarchy,
  getNiveaux,
  getNiveauDetail,
  getNiveauxByPays,
  getNiveauxActifsByPays,
  createNiveau,
  updateNiveau,
  deleteNiveau,
  getNiveauMatieres,
  getNiveauHierarchy
} from './pays'

import {
  getMatieres,
  getMatiereDetail,
  createMatiere,
  updateMatiere,
  deleteMatiere,
  getMatieresByNiveau,
  getMatieresByPays,
  getMatiereThemes,
  getMatiereHierarchy,
  getThemes,
  getThemeDetail,
  createTheme,
  updateTheme,
  deleteTheme,
  getThemesByMatiere,
  getThemeNotions,
  getThemeHierarchy,
  getNotions,
  getNotionDetail,
  createNotion,
  updateNotion,
  deleteNotion,
  getNotionsByTheme,
  getNotionChapitres,
  getNotionHierarchy,
  getChapitres,
  getChapitreDetail,
  createChapitre,
  updateChapitre,
  deleteChapitre,
  getChapitresByNotion,
  getChapitreExercices,
  getChapitreHierarchy,
  getExercices,
  getExerciceDetail,
  createExercice,
  updateExercice,
  deleteExercice,
  getExercicesByChapitre
} from './curriculum'

import {
  getUserPreferences,
  bulkUpdatePreferences,
  syncPreferencesWithBackend,
  loadPreferencesFromBackend,
  getFavoriteMatieres,
  addFavoriteMatiere,
  removeFavoriteMatiere,
  getSelectedMatieres,
  addSelectedMatiere,
  removeSelectedMatiere,
  setActiveMatiere
} from './preferences'

// API Pays et Niveaux (ré-export)
export * from './pays'

// API Curriculum (ré-export)
export * from './curriculum'

// API Préférences et Favoris (ré-export)
export * from './preferences'

// Imports sélectifs pour éviter les conflits mais garder les fonctions importantes
export { 
  getMatieres,
  getMatieresUtilisateur,
  getMatieresAdmin,
  filtrerMatieres,
  createMatiere,
  updateMatiere,
  deleteMatiere
} from './matieres'

export { 
  getThemesPourUtilisateur 
} from './themes'

export { 
  getNotionsPourUtilisateur 
} from './notions'

export {
  getStatuses,
  createStatus,
  updateStatus,
  deleteStatus,
  getExerciceImages,
  createExerciceImage,
  updateExerciceImage,
  deleteExerciceImage
} from './exercices'

// APIs spécifiques (sans conflits)
export * from './cours'
export {
  getSynthesisSheets,
  getSynthesisSheet,
  createSynthesisSheet,
  updateSynthesisSheet,
  deleteSynthesisSheet,
  duplicateSynthesisSheet,
  getPreviewData
} from './synthesis'
export * from './quiz'
export * from './users'
export * from './auth'
export * from './calculator'
export * from './matiere-contextes'

// ========================================
// API UNIFIÉE
// ========================================

/**
 * API unifiée pour accès simplifié
 */
export const API = {
  // Pays et Niveaux
  pays: {
    getAll: getPays,
    getById: getPaysDetail,
    getActifs: getPaysActifs,
    search: searchPays,
    create: createPays,
    update: updatePays,
    delete: deletePays,
    getNiveaux: getPaysNiveaux,
    getHierarchy: getPaysHierarchy
  },
  
  niveaux: {
    getAll: getNiveaux,
    getById: getNiveauDetail,
    getByPays: getNiveauxByPays,
    getActifsByPays: getNiveauxActifsByPays,
    create: createNiveau,
    update: updateNiveau,
    delete: deleteNiveau,
    getMatieres: getNiveauMatieres,
    getHierarchy: getNiveauHierarchy
  },

  // Curriculum
  matieres: {
    getAll: getMatieres,
    getById: getMatiereDetail,
    getByNiveau: getMatieresByNiveau,
    getByPays: getMatieresByPays,
    create: createMatiere,
    update: updateMatiere,
    delete: deleteMatiere,
    getThemes: getMatiereThemes,
    getHierarchy: getMatiereHierarchy
  },

  themes: {
    getAll: getThemes,
    getById: getThemeDetail,
    getByMatiere: getThemesByMatiere,
    create: createTheme,
    update: updateTheme,
    delete: deleteTheme,
    getNotions: getThemeNotions,
    getHierarchy: getThemeHierarchy
  },

  notions: {
    getAll: getNotions,
    getById: getNotionDetail,
    getByTheme: getNotionsByTheme,
    create: createNotion,
    update: updateNotion,
    delete: deleteNotion,
    getChapitres: getNotionChapitres,
    getHierarchy: getNotionHierarchy
  },

  chapitres: {
    getAll: getChapitres,
    getById: getChapitreDetail,
    getByNotion: getChapitresByNotion,
    create: createChapitre,
    update: updateChapitre,
    delete: deleteChapitre,
    getExercices: getChapitreExercices,
    getHierarchy: getChapitreHierarchy
  },

  exercices: {
    getAll: getExercices,
    getById: getExerciceDetail,
    getByChapitre: getExercicesByChapitre,
    create: createExercice,
    update: updateExercice,
    delete: deleteExercice
  },

  // Préférences et Favoris
  preferences: {
    getAll: getUserPreferences,
    bulkUpdate: bulkUpdatePreferences,
    sync: syncPreferencesWithBackend,
    load: loadPreferencesFromBackend
  },

  favorites: {
    getAll: getFavoriteMatieres,
    add: addFavoriteMatiere,
    remove: removeFavoriteMatiere
  },

  selected: {
    getAll: getSelectedMatieres,
    add: addSelectedMatiere,
    remove: removeSelectedMatiere,
    setActive: setActiveMatiere
  }
}

// ========================================
// UTILITAIRES GLOBAUX
// ========================================

/**
 * Récupérer la hiérarchie complète du curriculum
 */
export const getFullCurriculum = async (paysId) => {
  try {
    const pays = await getPaysDetail(paysId)
    const niveaux = await getPaysNiveaux(paysId)
    
    const niveauxAvecMatieres = await Promise.all(
      niveaux.map(async (niveau) => {
        const matieres = await getNiveauMatieres(niveau.id)
        return { ...niveau, matieres }
      })
    )
    
    return {
      pays,
      niveaux: niveauxAvecMatieres
    }
  } catch (error) {
    console.error('Erreur lors de la récupération du curriculum complet:', error)
    throw error
  }
}

/**
 * Recherche globale dans le curriculum
 */
export const searchCurriculum = async (searchTerm) => {
  try {
    const [pays, matieres, themes, notions, chapitres, exercices] = await Promise.all([
      searchPays(searchTerm),
      getMatieres({ search: searchTerm }),
      getThemes({ search: searchTerm }),
      getNotions({ search: searchTerm }),
      getChapitres({ search: searchTerm }),
      getExercices({ search: searchTerm })
    ])
    
    return {
      pays,
      matieres,
      themes,
      notions,
      chapitres,
      exercices
    }
  } catch (error) {
    console.error('Erreur lors de la recherche globale:', error)
    throw error
  }
}

// ========================================
// CONSTANTES
// ========================================

export const ENDPOINTS = {
  PAYS: '/api/pays/',
  NIVEAUX: '/api/niveaux/',
  MATIERES: '/api/matieres/',
  THEMES: '/api/themes/',
  NOTIONS: '/api/notions/',
  CHAPITRES: '/api/chapitres/',
  EXERCICES: '/api/exercices/'
}

export const RELATIONS = {
  PAYS_NIVEAUX: 'pays_id',
  NIVEAU_MATIERES: 'niveau',
  MATIERE_THEMES: 'matiere',
  THEME_NOTIONS: 'theme',
  NOTION_CHAPITRES: 'notion',
  CHAPITRE_EXERCICES: 'chapitre'
}

// Export par défaut
export default API 