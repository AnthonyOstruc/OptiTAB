/**
 * Composable pour la navigation intelligente basée sur les matières
 * 
 * Fonctionnalités:
 * - Redirection automatique vers les sections spécifiques d'une matière
 * - Gestion des routes avec matière active
 * - Navigation contextuelle intelligente
 * - Intégration avec le système de matières sélectionnées
 * 
 * @author OptiTAB Team
 * @version 1.0.0
 */

import { computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'

/**
 * Configuration des routes liées aux matières
 */
const MATIERE_ROUTES = {
  // Routes qui nécessitent une matière pour fonctionner
  MATIERE_DEPENDENT: [
    'Exercises',      // Page générale exercices -> vers Notions
    'Quiz',           // Page générale quiz -> vers QuizNotions  
    'Sheets',         // Page générale fiches -> vers fiches spécifiques
    'OnlineCourses'   // Page générale cours -> vers CourseNotions
  ],
  
  // Routes qui bénéficient d'une matière active mais ne la nécessitent pas
  MATIERE_ENHANCED: [
    'Dashboard',
    'Account', 
    'Progress'
  ],
  
  // Mapping des routes vers leurs équivalents avec matière
  ROUTE_MAPPING: {
    'Exercises': (matiereId) => ({ name: 'Notions', params: { matiereId } }),
    'Quiz': (matiereId) => ({ name: 'QuizNotions', params: { matiereId } }),
    'Sheets': (matiereId) => ({ name: 'Sheets', query: { matiereId } }), // Utiliser query pour Sheets
    'OnlineCourses': (matiereId) => ({ name: 'CourseNotions', params: { matiereId } })
  }
}

/**
 * Hook principal pour la navigation intelligente
 * @returns {Object} - Fonctions et propriétés pour la navigation intelligente
 */
export const useSmartNavigation = () => {
  const router = useRouter()
  const route = useRoute()
  const subjectsStore = useSubjectsStore()
  
  // S'assurer que le store est initialisé
  if (typeof subjectsStore.initialize === 'function') {
    subjectsStore.initialize().catch(console.error)
  }

  // ========================================
  // PROPRIÉTÉS CALCULÉES
  // ========================================

  /**
   * Vérifie si la route actuelle nécessite une matière
   */
  const currentRouteNeedsMatiere = computed(() => {
    return MATIERE_ROUTES.MATIERE_DEPENDENT.includes(route.name)
  })

  /**
   * Vérifie si la route actuelle peut bénéficier d'une matière
   */
  const currentRouteCanUseMatiere = computed(() => {
    return MATIERE_ROUTES.MATIERE_ENHANCED.includes(route.name) ||
           currentRouteNeedsMatiere.value
  })

  /**
   * Obtient l'ID de matière depuis les paramètres de route actuels
   */
  const matiereIdFromRoute = computed(() => {
    return route.params.matiereId || route.query.matiereId || null
  })

  /**
   * Vérifie si on a une matière active ou disponible
   */
  const hasAvailableMatiere = computed(() => {
    return subjectsStore.activeMatiereId || 
           subjectsStore.selectedMatieresIds.length > 0
  })

  // ========================================
  // MÉTHODES UTILITAIRES
  // ========================================

  /**
   * Gestion centralisée des erreurs
   * @param {Error} error - L'erreur à traiter
   * @param {string} context - Le contexte où l'erreur s'est produite
   */
  const handleError = (error, context) => {
    console.error(`[SmartNavigation] Erreur dans ${context}:`, error)
    // Ici on pourrait ajouter une notification utilisateur
  }

  /**
   * Valide un ID de matière
   * @param {any} id - L'ID à valider
   * @returns {boolean} - True si l'ID est valide
   */
  const isValidMatiereId = (id) => {
    return id !== null && id !== undefined && !isNaN(Number(id)) && Number(id) > 0
  }

  // ========================================
  // MÉTHODES DE NAVIGATION
  // ========================================

  /**
   * Navigue vers une section avec une matière spécifique
   * @param {string} sectionName - Le nom de la section (exercises, quiz, sheets)
   * @param {number|string} matiereId - L'ID de la matière (optionnel)
   * @returns {Promise<void>}
   */
  const navigateToSectionWithMatiere = async (sectionName, matiereId = null) => {
    try {
      console.log(`[SmartNavigation] navigateToSectionWithMatiere appelée pour: ${sectionName}`)
      
      // Déterminer la matière à utiliser (en gérant les appels async)
      let targetMatiereId = matiereId || subjectsStore.activeMatiereId
      if (!targetMatiereId) {
        targetMatiereId = await subjectsStore.getOrSetSmartActiveMatiere(subjectsStore.selectedMatieresIds)
      }
      // Normaliser en nombre si nécessaire
      if (typeof targetMatiereId === 'string') {
        targetMatiereId = Number(targetMatiereId)
      }

      console.log(`[SmartNavigation] Matière déterminée: ${targetMatiereId}`)
      console.log(`[SmartNavigation] Store state:`, {
        activeMatiereId: subjectsStore.activeMatiereId,
        selectedMatieresIds: subjectsStore.selectedMatieresIds
      })

      if (!isValidMatiereId(targetMatiereId)) {
        console.warn(`[SmartNavigation] Aucune matière valide disponible pour ${sectionName}`)
        // Rediriger vers la page de sélection de matière
        await redirectToMatiereSelection(sectionName)
        return
      }

      // Définir comme matière active
      console.log(`[SmartNavigation] Définition de la matière active: ${targetMatiereId}`)
      subjectsStore.setActiveMatiere(targetMatiereId)

      // Obtenir la route de destination
      const routeConfig = getRouteForSection(sectionName, targetMatiereId)
      console.log(`[SmartNavigation] Configuration de route:`, routeConfig)
      
      if (!routeConfig) {
        console.warn(`[SmartNavigation] Configuration de route introuvable pour ${sectionName}`)
        return
      }

      // Naviguer vers la destination
      console.log(`[SmartNavigation] Tentative de navigation vers:`, routeConfig)
      await router.push(routeConfig)
      console.log(`[SmartNavigation] Navigation réussie vers ${sectionName} avec matière ${targetMatiereId}`)

    } catch (error) {
      handleError(error, 'navigateToSectionWithMatiere')
      throw error // Re-throw pour debugging
    }
  }

  /**
   * Obtient la configuration de route pour une section donnée
   * @param {string} sectionName - Le nom de la section
   * @param {number} matiereId - L'ID de la matière
   * @returns {Object|null} - Configuration de route Vue Router
   */
  const getRouteForSection = (sectionName, matiereId) => {
    const routeGenerators = {
      'exercises': (id) => ({ name: 'Notions', params: { matiereId: id } }),
      'quiz': (id) => ({ name: 'QuizNotions', params: { matiereId: id } }),
      'sheets': (id) => ({ name: 'Sheets', query: { matiereId: id } })
    }

    const generator = routeGenerators[sectionName.toLowerCase()]
    return generator ? generator(matiereId) : null
  }

  /**
   * Redirige vers la page de sélection de matière appropriée
   * @param {string} intendedSection - La section vers laquelle l'utilisateur voulait aller
   * @returns {Promise<void>}
   */
  const redirectToMatiereSelection = async (intendedSection) => {
    try {
      const sectionRoutes = {
        'exercises': 'Exercises',
        'quiz': 'Quiz', 
        'sheets': 'Sheets'
      }

      const routeName = sectionRoutes[intendedSection.toLowerCase()] || 'Dashboard'
      console.log(`[SmartNavigation] Redirection vers sélection de matière: ${routeName}`)
      await router.push({ name: routeName })
      
      console.log(`[SmartNavigation] Redirection réussie vers: ${routeName}`)
    } catch (error) {
      handleError(error, 'redirectToMatiereSelection')
      throw error
    }
  }

  /**
   * Gère la navigation intelligente depuis les liens de menu
   * @param {string} menuItemKey - La clé de l'élément de menu (exercises, quiz, etc.)
   * @returns {Promise<void>}
   */
  const handleMenuNavigation = async (menuItemKey) => {
    try {
      console.log(`[SmartNavigation] Début navigation pour: ${menuItemKey}`)
      
      const keyToSection = {
        'exercices': 'exercises',
        'quiz': 'quiz',
        'fiches': 'sheets'
      }

      const sectionName = keyToSection[menuItemKey]
      if (!sectionName) {
        console.warn(`[SmartNavigation] Section inconnue: ${menuItemKey}`)
        return
      }

      console.log(`[SmartNavigation] Section mappée: ${menuItemKey} -> ${sectionName}`)
      await navigateToSectionWithMatiere(sectionName)
    } catch (error) {
      handleError(error, 'handleMenuNavigation')
      throw error // Re-throw pour que le composant parent puisse gérer
    }
  }

  /**
   * Synchronise la matière active avec la route actuelle
   * Utile quand l'utilisateur navigue directement via URL
   */
  const syncMatiereWithRoute = () => {
    try {
      const routeMatiereId = matiereIdFromRoute.value
      
      if (isValidMatiereId(routeMatiereId)) {
        // S'assurer que cette matière est dans les sélectionnées
        if (!subjectsStore.selectedMatieresIds.includes(Number(routeMatiereId))) {
          subjectsStore.addMatiereId(routeMatiereId)
        }
        
        // Définir comme active
        subjectsStore.setActiveMatiere(routeMatiereId)
        console.log(`[SmartNavigation] Matière synchronisée depuis route: ${routeMatiereId}`)
      }
    } catch (error) {
      handleError(error, 'syncMatiereWithRoute')
    }
  }

  /**
   * Vérifie si l'utilisateur doit être redirigé et effectue la redirection si nécessaire
   * @returns {Promise<boolean>} - True si une redirection a été effectuée
   */
  const checkAndRedirectIfNeeded = async () => {
    try {
      // Si la route actuelle a besoin d'une matière mais qu'on en a pas
      if (currentRouteNeedsMatiere.value && !matiereIdFromRoute.value) {
        // Essayer d'obtenir une matière intelligemment
      const smartMatiereId = await subjectsStore.getOrSetSmartActiveMatiere(subjectsStore.selectedMatieresIds)
        
        if (smartMatiereId) {
          // Rediriger vers la même section mais avec la matière
          const currentSection = route.name.toLowerCase()
          await navigateToSectionWithMatiere(currentSection, smartMatiereId)
          return true
        } else {
          // Aucune matière disponible, rester sur la page de sélection
          console.log(`[SmartNavigation] Aucune matière disponible, restant sur ${route.name}`)
          return false
        }
      }

      return false
    } catch (error) {
      handleError(error, 'checkAndRedirectIfNeeded')
      return false
    }
  }

  // ========================================
  // WATCHERS
  // ========================================

  /**
   * Surveillance des changements de route pour synchronisation automatique
   */
  watch(
    () => route.path,
    () => {
      syncMatiereWithRoute()
    },
    { immediate: true }
  )

  // ========================================
  // API PUBLIQUE
  // ========================================

  return {
    // Propriétés calculées
    currentRouteNeedsMatiere,
    currentRouteCanUseMatiere,
    matiereIdFromRoute,
    hasAvailableMatiere,
    
    // Méthodes de navigation
    navigateToSectionWithMatiere,
    handleMenuNavigation,
    redirectToMatiereSelection,
    
    // Utilitaires
    syncMatiereWithRoute,
    checkAndRedirectIfNeeded,
    getRouteForSection,
    
    // Validation
    isValidMatiereId
  }
}

/**
 * Version simplifiée pour utilisation dans les composants basiques
 * @returns {Object} - API simplifiée
 */
export const useSimpleNavigation = () => {
  const { navigateToSectionWithMatiere, handleMenuNavigation } = useSmartNavigation()
  
  return {
    navigateToSection: navigateToSectionWithMatiere,
    handleMenu: handleMenuNavigation
  }
}

export default useSmartNavigation 