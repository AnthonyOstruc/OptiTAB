/**
 * Middleware de routage pour la gestion intelligente des matières
 * 
 * Fonctionnalités:
 * - Redirection automatique vers les sections spécifiques d'une matière
 * - Synchronisation de la matière active avec les routes
 * - Gestion des routes nécessitant une matière
 * 
 * @author OptiTAB Team
 * @version 1.0.0
 */

import { useSubjectsStore } from '@/stores/subjects/index'

/**
 * Configuration des routes nécessitant une matière
 */
const MATIERE_DEPENDENT_ROUTES = ['Exercises', 'Quiz', 'Sheets', 'OnlineCourses']

/**
 * Mapping des routes vers leurs équivalents avec matière
 */
const ROUTE_REDIRECTIONS = {
  'Exercises': (matiereId) => ({ 
    name: 'Notions', 
    params: { matiereId: String(matiereId) } 
  }),
  'Quiz': (matiereId) => ({ 
    name: 'QuizNotions', 
    params: { matiereId: String(matiereId) } 
  }),
  'Sheets': (matiereId) => ({ 
    name: 'Sheets', 
    query: { matiereId: String(matiereId) } 
  }),
  'OnlineCourses': (matiereId) => ({ 
    name: 'CourseNotions', 
    params: { matiereId: String(matiereId) } 
  })
}

/**
 * Middleware principal pour la gestion des matières
 * @param {Object} to - Route de destination
 * @param {Object} from - Route d'origine
 * @param {Function} next - Fonction de navigation suivante
 */
export const matiereMiddleware = (to, from, next) => {
  try {
    const subjectsStore = useSubjectsStore()
    
    // Vérifier si la route nécessite une matière
    if (!MATIERE_DEPENDENT_ROUTES.includes(to.name)) {
      // Synchroniser la matière active si présente dans les paramètres
      syncMatiereFromRoute(to, subjectsStore)
      next()
      return
    }
    
    // Route nécessitant une matière - vérifier si on a une matière dans l'URL
    const routeMatiereId = to.params.matiereId || to.query.matiereId
    
    if (routeMatiereId && isValidMatiereId(routeMatiereId)) {
      // Matière présente dans l'URL, synchroniser avec le store
      syncMatiereFromRoute(to, subjectsStore)
      next()
      return
    }
    
    // Aucune matière dans l'URL, essayer de rediriger intelligemment
    const targetMatiereId = getSmartMatiereId(subjectsStore)
    
    if (targetMatiereId) {
      // Rediriger vers la même route avec la matière
      const redirectRoute = ROUTE_REDIRECTIONS[to.name]
      if (redirectRoute) {
        const newRoute = redirectRoute(targetMatiereId)
        console.log(`[MatiereMiddleware] Redirection intelligente: ${to.name} -> ${newRoute.name} avec matière ${targetMatiereId}`)
        next(newRoute)
        return
      }
    }
    
    // Aucune matière disponible, laisser accéder à la page de sélection
    console.log(`[MatiereMiddleware] Aucune matière disponible, accès à ${to.name} pour sélection`)
    next()
    
  } catch (error) {
    console.error('[MatiereMiddleware] Erreur dans le middleware:', error)
    next() // En cas d'erreur, laisser passer
  }
}

/**
 * Synchronise la matière active depuis les paramètres de route
 * @param {Object} route - Route Vue Router
 * @param {Object} store - Store des matières
 */
const syncMatiereFromRoute = (route, store) => {
  try {
    const matiereId = route.params.matiereId || route.query.matiereId
    
    if (isValidMatiereId(matiereId)) {
      const numericId = Number(matiereId)
      
      // Ajouter aux matières sélectionnées si pas déjà présente
      if (!store.selectedMatieresIds.includes(numericId)) {
        store.addMatiereId(numericId)
      }
      
      // Définir comme matière active
      store.setActiveMatiere(numericId)
      
      console.log(`[MatiereMiddleware] Matière synchronisée depuis route: ${numericId}`)
    }
  } catch (error) {
    console.error('[MatiereMiddleware] Erreur lors de la synchronisation:', error)
  }
}

/**
 * Obtient l'ID de matière à utiliser intelligemment
 * @param {Object} store - Store des matières
 * @returns {number|null} - ID de la matière ou null
 */
const getSmartMatiereId = (store) => {
  try {
    // 1. Matière actuellement active
    if (store.activeMatiereId) {
      return store.activeMatiereId
    }
    
    // 2. Première matière sélectionnée
    if (store.selectedMatieresIds.length > 0) {
      const firstSelectedId = store.selectedMatieresIds[0]
      store.setActiveMatiere(firstSelectedId)
      return firstSelectedId
    }
    
    // 3. Aucune matière disponible
    return null
  } catch (error) {
    console.error('[MatiereMiddleware] Erreur lors de la sélection intelligente:', error)
    return null
  }
}

/**
 * Valide un ID de matière
 * @param {any} id - L'ID à valider
 * @returns {boolean} - True si l'ID est valide
 */
const isValidMatiereId = (id) => {
  return id !== null && id !== undefined && !isNaN(Number(id)) && Number(id) > 0
}

/**
 * Middleware spécialisé pour les routes d'exercices
 * @param {Object} to - Route de destination
 * @param {Object} from - Route d'origine  
 * @param {Function} next - Fonction de navigation suivante
 */
export const exercicesMiddleware = (to, from, next) => {
  try {
    const subjectsStore = useSubjectsStore()
    
    // Pour les routes d'exercices spécifiques, s'assurer que la matière est bien définie
    if (to.name === 'Notions' && to.params.matiereId) {
      syncMatiereFromRoute(to, subjectsStore)
    }
    
    next()
  } catch (error) {
    console.error('[ExercicesMiddleware] Erreur:', error)
    next()
  }
}

/**
 * Middleware spécialisé pour les routes de quiz
 * @param {Object} to - Route de destination
 * @param {Object} from - Route d'origine
 * @param {Function} next - Fonction de navigation suivante
 */
export const quizMiddleware = (to, from, next) => {
  try {
    const subjectsStore = useSubjectsStore()
    
    // Pour les routes de quiz spécifiques, s'assurer que la matière est bien définie
    if (['QuizNotions', 'QuizChapitres', 'ChapterQuiz'].includes(to.name)) {
      // Extraire l'ID de matière depuis les paramètres ou via l'API
      if (to.params.matiereId) {
        syncMatiereFromRoute(to, subjectsStore)
      }
    }
    
    next()
  } catch (error) {
    console.error('[QuizMiddleware] Erreur:', error)
    next()
  }
}

/**
 * Middleware de nettoyage pour réinitialiser la matière active si nécessaire
 * @param {Object} to - Route de destination
 * @param {Object} from - Route d'origine
 * @param {Function} next - Fonction de navigation suivante
 */
export const cleanupMiddleware = (to, from, next) => {
  try {
    const subjectsStore = useSubjectsStore()
    
    // Routes où il faut potentiellement nettoyer la matière active
    const CLEANUP_ROUTES = ['Home', 'Dashboard', 'Account', 'Pricing', 'About']
    
    if (CLEANUP_ROUTES.includes(to.name)) {
      // Ne pas nettoyer automatiquement - laisser l'utilisateur garder sa matière active
      // Optionnel: on pourrait nettoyer seulement sur des routes spécifiques
    }
    
    next()
  } catch (error) {
    console.error('[CleanupMiddleware] Erreur:', error)
    next()
  }
}

export default matiereMiddleware 