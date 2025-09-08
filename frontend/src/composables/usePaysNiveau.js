/**
 * Composable pour simplifier l'utilisation du système Pays-Niveau
 */
import { ref, computed, watch, onMounted } from 'vue'
import { usePaysNiveauStore } from '@/stores/paysNiveau'

/**
 * Composable principal pour le système pays-niveau
 */
export function usePaysNiveau() {
  const store = usePaysNiveauStore()
  
  return {
    // État du store
    paysActuel: computed(() => store.paysActuel),
    niveauPaysActuel: computed(() => store.niveauPaysActuel),
    hasActiveSelection: computed(() => store.hasActiveSelection),
    selectionDisplay: computed(() => store.selectionDisplay),
    isLoading: computed(() => store.isLoading),
    error: computed(() => store.error),
    
    // Actions
    setPays: store.setPays,
    setNiveauPays: store.setNiveauPays,
    setSelection: store.setSelection,
    clearSelection: store.clearSelection,
    
    // Données
    paysDisponibles: computed(() => store.paysDisponibles),
    niveauxPourPaysActuel: computed(() => store.niveauxPourPaysActuel),
    
    // Méthodes utilitaires
    loadPaysDisponibles: store.loadPaysDisponibles,
    loadNiveauxPourPays: store.loadNiveauxPourPays,
    saveSelection: store.saveSelectionToStorage,
    loadSelection: store.loadSelectionFromStorage
  }
}

/**
 * Composable pour le contenu filtré par pays-niveau
 */
export function useContenuAvecFiltrage(typeContenu = 'matieres') {
  const store = usePaysNiveauStore()
  const contenu = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Charger le contenu automatiquement quand la sélection change
  watch(
    () => store.hasActiveSelection,
    async (hasSelection) => {
      if (hasSelection) {
        await loadContenu()
      } else {
        contenu.value = []
      }
    },
    { immediate: true }
  )
  
  async function loadContenu() {
    if (!store.hasActiveSelection) {
      contenu.value = []
      return
    }
    
    loading.value = true
    error.value = null
    
    try {
      contenu.value = await store.loadContenuPourSelection(typeContenu)
    } catch (err) {
      error.value = err.message
      contenu.value = []
    } finally {
      loading.value = false
    }
  }
  
  async function rechercherContenu(terme) {
    if (!terme || terme.length < 2) {
      await loadContenu()
      return
    }
    
    loading.value = true
    error.value = null
    
    try {
      const resultats = await store.rechercherContenu(terme, typeContenu)
      contenu.value = resultats.resultats[typeContenu] || []
    } catch (err) {
      error.value = err.message
      contenu.value = []
    } finally {
      loading.value = false
    }
  }
  
  return {
    contenu: computed(() => contenu.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    hasActiveSelection: computed(() => store.hasActiveSelection),
    loadContenu,
    rechercherContenu
  }
}

/**
 * Composable pour les matières avec filtrage
 */
export function useMatieres() {
  return useContenuAvecFiltrage('matieres')
}

/**
 * Composable pour les exercices avec filtrage
 */
export function useExercices() {
  return useContenuAvecFiltrage('exercices')
}

/**
 * Composable pour les cours avec filtrage
 */
export function useCours() {
  return useContenuAvecFiltrage('cours')
}

/**
 * Composable pour la navigation hiérarchique
 */
export function useNavigationHierarchique() {
  const store = usePaysNiveauStore()
  const matiereActuelle = ref(null)
  const themeActuel = ref(null)
  const notionActuelle = ref(null)
  const chapitreActuel = ref(null)
  
  const themes = ref([])
  const notions = ref([])
  const chapitres = ref([])
  const exercices = ref([])
  
  // Charger les thèmes quand une matière est sélectionnée
  watch(matiereActuelle, async (matiere) => {
    if (matiere && store.hasActiveSelection) {
      try {
        const response = await apiClient.get(`/api/themes/`, {
          params: {
            matiere: matiere.id,
            ...store.apiParams
          }
        })
        themes.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur chargement thèmes:', error)
        themes.value = []
      }
    } else {
      themes.value = []
    }
    
    // Réinitialiser les niveaux inférieurs
    themeActuel.value = null
    notionActuelle.value = null
    chapitreActuel.value = null
  })
  
  // Charger les notions quand un thème est sélectionné
  watch(themeActuel, async (theme) => {
    if (theme && store.hasActiveSelection) {
      try {
        const response = await apiClient.get(`/api/notions/`, {
          params: {
            theme: theme.id,
            ...store.apiParams
          }
        })
        notions.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur chargement notions:', error)
        notions.value = []
      }
    } else {
      notions.value = []
    }
    
    notionActuelle.value = null
    chapitreActuel.value = null
  })
  
  // Charger les chapitres quand une notion est sélectionnée
  watch(notionActuelle, async (notion) => {
    if (notion && store.hasActiveSelection) {
      try {
        const response = await apiClient.get(`/api/chapitres/`, {
          params: {
            notion: notion.id,
            ...store.apiParams
          }
        })
        chapitres.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur chargement chapitres:', error)
        chapitres.value = []
      }
    } else {
      chapitres.value = []
    }
    
    chapitreActuel.value = null
  })
  
  // Charger les exercices quand un chapitre est sélectionné
  watch(chapitreActuel, async (chapitre) => {
    if (chapitre && store.hasActiveSelection) {
      try {
        const response = await apiClient.get(`/api/exercices/`, {
          params: {
            chapitre: chapitre.id,
            ...store.apiParams
          }
        })
        exercices.value = response.data.results || response.data
      } catch (error) {
        console.error('Erreur chargement exercices:', error)
        exercices.value = []
      }
    } else {
      exercices.value = []
    }
  })
  
  function resetNavigation() {
    matiereActuelle.value = null
    themeActuel.value = null
    notionActuelle.value = null
    chapitreActuel.value = null
    themes.value = []
    notions.value = []
    chapitres.value = []
    exercices.value = []
  }
  
  return {
    // Sélections actuelles
    matiereActuelle,
    themeActuel,
    notionActuelle,
    chapitreActuel,
    
    // Données chargées
    themes: computed(() => themes.value),
    notions: computed(() => notions.value),
    chapitres: computed(() => chapitres.value),
    exercices: computed(() => exercices.value),
    
    // Méthodes
    resetNavigation
  }
}

/**
 * Composable pour les statistiques
 */
export function useStatistiques() {
  const store = usePaysNiveauStore()
  const statistiques = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  async function loadStatistiques() {
    if (!store.hasActiveSelection) {
      statistiques.value = null
      return
    }
    
    loading.value = true
    error.value = null
    
    try {
      statistiques.value = await store.getStatistiques()
    } catch (err) {
      error.value = err.message
      statistiques.value = null
    } finally {
      loading.value = false
    }
  }
  
  // Charger automatiquement quand la sélection change
  watch(
    () => store.hasActiveSelection,
    (hasSelection) => {
      if (hasSelection) {
        loadStatistiques()
      } else {
        statistiques.value = null
      }
    },
    { immediate: true }
  )
  
  return {
    statistiques: computed(() => statistiques.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    loadStatistiques
  }
}

/**
 * Composable pour la recherche avancée
 */
export function useRecherche() {
  const store = usePaysNiveauStore()
  const resultats = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const termeActuel = ref('')
  
  async function rechercher(terme) {
    if (!terme || terme.length < 2) {
      resultats.value = null
      return
    }
    
    termeActuel.value = terme
    loading.value = true
    error.value = null
    
    try {
      resultats.value = await store.rechercherContenu(terme)
    } catch (err) {
      error.value = err.message
      resultats.value = null
    } finally {
      loading.value = false
    }
  }
  
  function clearRecherche() {
    resultats.value = null
    termeActuel.value = ''
    error.value = null
  }
  
  return {
    resultats: computed(() => resultats.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    termeActuel: computed(() => termeActuel.value),
    rechercher,
    clearRecherche
  }
}

/**
 * Composable pour l'initialisation automatique
 */
export function useAutoInit() {
  const { loadPaysDisponibles, loadSelection } = usePaysNiveau()
  
  onMounted(async () => {
    try {
      // Charger les pays disponibles
      await loadPaysDisponibles()
      
      // Tenter de restaurer une sélection sauvegardée
      loadSelection()
    } catch (error) {
      console.error('Erreur initialisation pays-niveau:', error)
    }
  })
}
