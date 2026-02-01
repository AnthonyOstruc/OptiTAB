/*
🎯 Hook Composition API pour la gestion Pays/Niveaux
Architecture: Réactive, modulaire, avec gestion d'état optimisée
*/

import { ref, computed, reactive, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { usePreferencesStore } from '@/stores/preferences'
import { 
  getPaysActifs, 
  getNiveauxParPays, 
  getRecommandationsPays,
  getUserPaysNiveauPreferences,
  validatePaysNiveauConsistency,
  preloadEssentialData,
  PaysNiveauxAPIError
} from '@/api/pays-niveaux'
import { updateUserPaysNiveau } from '@/api/users'
import { useToast } from '@/composables/useToast'

/**
 * Hook principal pour la gestion des pays et niveaux
 * Fournit une interface réactive complète
 */
export function usePaysNiveaux() {
  // ===== STORES =====
  const userStore = useUserStore()
  const preferencesStore = usePreferencesStore()
  const { user } = storeToRefs(userStore)
  const { showToast } = useToast()

  // ===== ÉTAT RÉACTIF =====
  const state = reactive({
    // État de chargement
    isLoading: false,
    isLoadingNiveaux: false,
    isInitialized: false,
    
    // Données
    pays: [],
    niveauxDisponibles: [],
    recommendations: null,
    
    // Sélection actuelle
    paysSelectionne: null,
    niveauSelectionne: null,
    
    // Historique et navigation
    etapeActuelle: 'pays', // 'pays' | 'niveau' | 'confirmation'
    historique: [],
    
    // Filtres et recherche
    recherchePays: '',
    filtreAge: null,
    filtreType: 'tous', // 'tous' | 'primaire' | 'secondaire' | 'superieur'
    
    // État des erreurs
    erreur: null,
    erreurDetails: null
  })

  // ===== PROPRIÉTÉS CALCULÉES =====

  /**
   * Pays filtrés selon la recherche et les critères
   */
  const paysFiltres = computed(() => {
    let filtered = [...state.pays]

    // Filtrage par recherche
    if (state.recherchePays.trim()) {
      const searchTerm = state.recherchePays.toLowerCase().trim()
      filtered = filtered.filter(pays => 
        pays.nom.toLowerCase().includes(searchTerm) ||
        pays.nom_local?.toLowerCase().includes(searchTerm) ||
        pays.code_iso?.toLowerCase().includes(searchTerm)
      )
    }

    // Tri par recommandations puis par ordre/nom
    return filtered.sort((a, b) => {
      // Pays recommandés en premier
      const aRecommende = state.recommendations?.recommandations?.includes(a.id) || false
      const bRecommende = state.recommendations?.recommandations?.includes(b.id) || false
      
      if (aRecommende && !bRecommende) return -1
      if (!aRecommande && bRecommende) return 1
      
      // Puis par ordre défini
      if (a.ordre !== b.ordre) return a.ordre - b.ordre
      
      // Enfin par nom
      return a.nom.localeCompare(b.nom, 'fr')
    })
  })

  /**
   * Niveaux filtrés selon les critères
   */
  const niveauxFiltres = computed(() => {
    let filtered = [...state.niveauxDisponibles]

    // Filtrage par âge - désactivé car les champs age_min et age_max n'existent plus
    // if (state.filtreAge) {
    //   filtered = filtered.filter(niveau => {
    //     if (!niveau.age_min || !niveau.age_max) return true
    //     return state.filtreAge >= niveau.age_min && state.filtreAge <= niveau.age_max
    //   })
    // }

    // Filtrage par type d'éducation
    if (state.filtreType !== 'tous') {
      filtered = filtered.filter(niveau => {
        const nom = niveau.nom.toLowerCase()
        switch (state.filtreType) {
          case 'primaire':
            return nom.includes('primaire') || nom.includes('élémentaire') || 
                   nom.includes('cp') || nom.includes('ce') || nom.includes('cm')
          case 'secondaire':
            return nom.includes('collège') || nom.includes('lycée') || 
                   nom.includes('seconde') || nom.includes('première') || nom.includes('terminale') ||
                   nom.includes('6ème') || nom.includes('5ème') || nom.includes('4ème') || nom.includes('3ème')
          case 'superieur':
            return nom.includes('université') || nom.includes('master') || 
                   nom.includes('licence') || nom.includes('doctorat') || nom.includes('bts')
          default:
            return true
        }
      })
    }

    return filtered.sort((a, b) => a.ordre - b.ordre)
  })

  /**
   * Informations sur la sélection actuelle
   */
  const selectionInfo = computed(() => {
    if (!state.paysSelectionne) return null

    const info = {
      pays: state.paysSelectionne,
      niveau: state.niveauSelectionne,
      estComplete: !!(state.paysSelectionne && state.niveauSelectionne),
      peutNaviguer: state.etapeActuelle !== 'confirmation'
    }

    // Ajouter des statistiques si disponibles
    if (state.niveauSelectionne) {
      info.statistiques = {
        cours: state.niveauSelectionne.nombre_cours || 0,
        exercices: state.niveauSelectionne.nombre_exercices || 0,
        quiz: state.niveauSelectionne.nombre_quiz || 0
      }
      
      info.contenuDisponible = Object.values(info.statistiques).some(count => count > 0)
    }

    return info
  })

  /**
   * Indique si l'utilisateur peut avancer dans le processus
   */
  const peutAvancer = computed(() => {
    switch (state.etapeActuelle) {
      case 'pays':
        return !!state.paysSelectionne
      case 'niveau':
        return !!state.niveauSelectionne
      case 'confirmation':
        return true
      default:
        return false
    }
  })

  /**
   * Messages d'aide contextuels
   */
  const messageAide = computed(() => {
    switch (state.etapeActuelle) {
      case 'pays':
        return state.pays.length === 0 
          ? 'Chargement des pays disponibles...'
          : state.paysFiltres.length === 0
          ? 'Aucun pays ne correspond à votre recherche'
          : 'Sélectionnez votre pays pour accéder aux niveaux adaptés'
      
      case 'niveau':
        return state.niveauxDisponibles.length === 0
          ? 'Chargement des niveaux...'
          : state.niveauxFiltres.length === 0
          ? 'Aucun niveau ne correspond à vos critères'
          : 'Choisissez votre niveau d\'étude actuel'
      
      case 'confirmation':
        return 'Vérifiez votre sélection avant de confirmer'
      
      default:
        return ''
    }
  })

  // ===== MÉTHODES PRINCIPALES =====

  /**
   * Initialise le système de pays/niveaux
   */
  const initialiser = async (forceReload = false) => {
    if (state.isInitialized && !forceReload) return

    state.isLoading = true
    state.erreur = null

    try {
      console.log('[usePaysNiveaux] Initialisation...')
      
      // Charger les données essentielles
      const { pays, recommendations } = await preloadEssentialData()
      
      state.pays = pays || []
      state.recommendations = recommendations

      // Charger les préférences utilisateur si connecté
      if (user.value?.id) {
        await chargerPreferencesUtilisateur()
      }

      state.isInitialized = true
      console.log(`[usePaysNiveaux] Initialisé avec ${state.pays.length} pays`)

    } catch (error) {
      console.error('[usePaysNiveaux] Erreur initialisation:', error)
      state.erreur = 'Impossible de charger les données'
      state.erreurDetails = error

      if (error instanceof PaysNiveauxAPIError) {
        showToast(error.message, 'error')
      } else {
        showToast('Erreur de chargement des pays', 'error')
      }
    } finally {
      state.isLoading = false
    }
  }

  /**
   * Sélectionne un pays et charge ses niveaux
   */
  const selectionnerPays = async (pays) => {
    if (!pays || state.isLoadingNiveaux) return

    // Réinitialiser la sélection de niveau
    state.niveauSelectionne = null
    state.niveauxDisponibles = []
    state.isLoadingNiveaux = true
    state.erreur = null

    try {
      console.log(`[usePaysNiveaux] Sélection pays: ${pays.nom}`)
      
      state.paysSelectionne = pays
      
      // Charger les niveaux pour ce pays
      const niveaux = await getNiveauxParPays(pays.id, { avecContenu: true })
      state.niveauxDisponibles = niveaux

      // Ajouter à l'historique
      ajouterALHistorique('pays', pays)

      // Passer à l'étape suivante
      changerEtape('niveau')

      console.log(`[usePaysNiveaux] ${niveaux.length} niveaux chargés pour ${pays.nom}`)

    } catch (error) {
      console.error('[usePaysNiveaux] Erreur sélection pays:', error)
      state.erreur = 'Impossible de charger les niveaux pour ce pays'
      
      if (error instanceof PaysNiveauxAPIError) {
        showToast(error.message, 'error')
      } else {
        showToast('Erreur de chargement des niveaux', 'error')
      }
    } finally {
      state.isLoadingNiveaux = false
    }
  }

  /**
   * Sélectionne un niveau
   */
  const selectionnerNiveau = async (niveau) => {
    if (!niveau) return

    console.log(`[usePaysNiveaux] Sélection niveau: ${niveau.nom}`)
    
    state.niveauSelectionne = niveau
    
    // Ajouter à l'historique
    ajouterALHistorique('niveau', niveau)

    // Passer à la confirmation
    changerEtape('confirmation')
  }

  /**
   * Confirme la sélection et met à jour l'utilisateur
   */
  const confirmerSelection = async () => {
    if (!state.paysSelectionne || !state.niveauSelectionne) {
      showToast('Sélection incomplète', 'error')
      return false
    }

    state.isLoading = true

    try {
      // Valider la cohérence
      const estCoherent = await validatePaysNiveauConsistency(
        state.paysSelectionne.id, 
        state.niveauSelectionne.id
      )

      if (!estCoherent) {
        throw new Error('La combinaison pays/niveau n\'est pas valide')
      }

      // Mettre à jour l'utilisateur si connecté
      if (user.value?.id) {
        await updateUserPaysNiveau(
          state.paysSelectionne.id,
          state.niveauSelectionne.id
        )
        
        // Mettre à jour le store utilisateur
        if (typeof userStore.fetchUser === 'function') {
          await userStore.fetchUser()
        }
      }

      // Sauvegarder en local
      await preferencesStore.setPaysNiveauPreferences({
        pays_id: state.paysSelectionne.id,
        pays_nom: state.paysSelectionne.nom,
        niveau_id: state.niveauSelectionne.id,
        niveau_nom: state.niveauSelectionne.nom,
        date_selection: new Date().toISOString()
      })

      // Marquer la configuration comme complétée dans localStorage
      localStorage.setItem('configurationCompleted', 'true')
      localStorage.setItem('userConfiguration', JSON.stringify({
        pays: state.paysSelectionne,
        niveau: state.niveauSelectionne,
        timestamp: new Date().toISOString()
      }))

      showToast(
        `Configuration mise à jour: ${state.paysSelectionne.nom} - ${state.niveauSelectionne.nom}`,
        'success'
      )

      return true

    } catch (error) {
      console.error('[usePaysNiveaux] Erreur confirmation:', error)
      
      if (error instanceof PaysNiveauxAPIError) {
        showToast(error.message, 'error')
      } else {
        showToast('Erreur lors de la confirmation', 'error')
      }
      
      return false
    } finally {
      state.isLoading = false
    }
  }

  /**
   * Charge les préférences utilisateur
   */
  const chargerPreferencesUtilisateur = async () => {
    try {
      const preferences = await getUserPaysNiveauPreferences()
      
      if (preferences.pays_id && preferences.niveau_id) {
        // Trouver le pays dans la liste
        const pays = state.pays.find(p => p.id === preferences.pays_id)
        if (pays) {
          // Ne pas déclencher automatiquement la sélection,
          // juste stocker l'information
          console.log(`[usePaysNiveaux] Préférences chargées: ${pays.nom}`)
        }
      }
    } catch (error) {
      console.warn('[usePaysNiveaux] Impossible de charger les préférences:', error)
    }
  }

  // ===== MÉTHODES DE NAVIGATION =====

  /**
   * Change l'étape actuelle
   */
  const changerEtape = (nouvelleEtape) => {
    const etapesValides = ['pays', 'niveau', 'confirmation']
    if (!etapesValides.includes(nouvelleEtape)) return

    state.etapeActuelle = nouvelleEtape
    console.log(`[usePaysNiveaux] Étape changée: ${nouvelleEtape}`)
  }

  /**
   * Retourne à l'étape précédente
   */
  const etapePrecedente = () => {
    switch (state.etapeActuelle) {
      case 'niveau':
        changerEtape('pays')
        state.niveauSelectionne = null
        break
      case 'confirmation':
        changerEtape('niveau')
        break
    }
  }

  /**
   * Ajoute une action à l'historique
   */
  const ajouterALHistorique = (type, donnees) => {
    state.historique.push({
      type,
      donnees,
      timestamp: Date.now()
    })
    
    // Limiter l'historique
    if (state.historique.length > 10) {
      state.historique = state.historique.slice(-10)
    }
  }

  /**
   * Réinitialise la sélection
   */
  const reinitialiser = () => {
    state.paysSelectionne = null
    state.niveauSelectionne = null
    state.niveauxDisponibles = []
    state.etapeActuelle = 'pays'
    state.historique = []
    state.erreur = null
    state.recherchePays = ''
    state.filtreAge = null
    state.filtreType = 'tous'
    
    console.log('[usePaysNiveaux] Sélection réinitialisée')
  }

  // ===== MÉTHODES UTILITAIRES =====

  /**
   * Met à jour les filtres de recherche
   */
  const mettreAJourFiltres = (nouveauxFiltres) => {
    if (nouveauxFiltres.recherche !== undefined) {
      state.recherchePays = nouveauxFiltres.recherche
    }
    if (nouveauxFiltres.age !== undefined) {
      state.filtreAge = nouveauxFiltres.age
    }
    if (nouveauxFiltres.type !== undefined) {
      state.filtreType = nouveauxFiltres.type
    }
  }

  /**
   * Obtient les statistiques de la sélection
   */
  const obtenirStatistiques = () => {
    if (!selectionInfo.value?.statistiques) return null

    const stats = selectionInfo.value.statistiques
    const total = stats.cours + stats.exercices + stats.quiz

    return {
      ...stats,
      total,
      pourcentage: {
        cours: total > 0 ? Math.round((stats.cours / total) * 100) : 0,
        exercices: total > 0 ? Math.round((stats.exercices / total) * 100) : 0,
        quiz: total > 0 ? Math.round((stats.quiz / total) * 100) : 0
      }
    }
  }

  /**
   * Vérifie si un pays est recommandé
   */
  const estPaysRecommande = (paysId) => {
    return state.recommendations?.recommandations?.includes(paysId) || false
  }

  /**
   * Vérifie si l'utilisateur a déjà configuré son pays et niveau
   */
  const isConfigurationCompleted = computed(() => {
    // Vérifier si l'utilisateur a sélectionné pays et niveau
    const hasUserSelection = state.paysSelectionne && state.niveauSelectionne
    
    // Vérifier dans le localStorage pour la persistance
    const hasLocalStorage = localStorage.getItem('configurationCompleted') === 'true'
    
    // Vérifier si l'utilisateur connecté a déjà ses préférences
    const hasUserPreferences = user.value?.pays && user.value?.niveau_pays
    
    return hasUserSelection || hasLocalStorage || hasUserPreferences
  })

  // ===== WATCHERS =====

  // Initialiser automatiquement si des pays sont disponibles
  watch(() => user.value?.id, (userId) => {
    if (userId && state.isInitialized) {
      chargerPreferencesUtilisateur()
    }
  })

  // ===== INTERFACE PUBLIQUE =====

  return {
    // État
    ...storeToRefs(reactive(state)),
    
    // Propriétés calculées
    paysFiltres,
    niveauxFiltres,
    selectionInfo,
    peutAvancer,
    messageAide,
    
    // Méthodes principales
    initialiser,
    selectionnerPays,
    selectionnerNiveau,
    confirmerSelection,
    
    // Navigation
    changerEtape,
    etapePrecedente,
    reinitialiser,
    
    // Utilitaires
    mettreAJourFiltres,
    obtenirStatistiques,
    estPaysRecommande,
    chargerPreferencesUtilisateur,
    isConfigurationCompleted
  }
}

/**
 * Hook spécialisé pour l'administration des pays/niveaux
 */
export function usePaysNiveauxAdmin() {
  const { showToast } = useToast()
  
  const adminState = reactive({
    isLoading: false,
    pays: [],
    niveauxGlobaux: [],
    associations: []
  })

  // À implémenter selon les besoins admin
  const chargerDonneesAdmin = async () => {
    // Logique de chargement admin
  }

  const ajouterAssociation = async (paysId, niveauId, parametres = {}) => {
    // Logique d'ajout d'association
  }

  const supprimerAssociation = async (associationId) => {
    // Logique de suppression d'association
  }

  return {
    // État admin
    ...storeToRefs(reactive(adminState)),
    
    // Méthodes admin
    chargerDonneesAdmin,
    ajouterAssociation,
    supprimerAssociation
  }
}

/**
 * Hook pour les statistiques pays/niveaux
 */
export function usePaysNiveauxStats() {
  const statsState = reactive({
    isLoading: false,
    statistiquesGlobales: null,
    statistiquesParPays: new Map(),
    tendances: null
  })

  const chargerStatistiques = async () => {
    statsState.isLoading = true
    try {
      // Charger les statistiques
      // À implémenter
    } catch (error) {
      console.error('Erreur chargement statistiques:', error)
    } finally {
      statsState.isLoading = false
    }
  }

  return {
    ...storeToRefs(reactive(statsState)),
    chargerStatistiques
  }
}

export default usePaysNiveaux
