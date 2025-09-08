import { ref, computed, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

export function useAutoNiveauModal() {
  const userStore = useUserStore()
  const { openModal, closeModal, isModalOpen } = useModalManager()
  
  // État local pour éviter les appels multiples
  const hasShownModal = ref(false)
  const isChecking = ref(false)
  const hasUserSelected = ref(false) // Nouveau flag pour éviter la réouverture après sélection

  // Computed pour déterminer si le modal doit s'afficher
  const shouldShowModal = computed(() => {
    // Ne pas afficher si :
    // 1. L'utilisateur n'est pas authentifié
    // 2. L'utilisateur a déjà un pays ET un niveau_pays définis dans la base de données
    // 3. Le modal a déjà été affiché dans cette session
    // 4. On est en train de vérifier
    // 5. L'utilisateur a déjà fait une sélection manuelle
    // 6. Configuration déjà complétée dans localStorage
    const configCompleted = localStorage.getItem('configurationCompleted') === 'true'
    
    return (
      userStore.isAuthenticated &&
      (!userStore.pays || !userStore.niveau_pays) && // Pas de pays OU pas de niveau_pays
      !hasShownModal.value &&
      !isChecking.value &&
      !hasUserSelected.value && // Ne pas rouvrir si l'utilisateur a déjà sélectionné
      !configCompleted // Ne pas ouvrir si la configuration est déjà terminée
    )
  })

  // Computed pour l'état du modal
  const isAutoNiveauModalOpen = computed(() => isModalOpen(MODAL_IDS.AUTO_NIVEAU))

  // Méthode pour ouvrir le modal
  const openAutoNiveauModal = () => {
    if (shouldShowModal.value) {
      openModal(MODAL_IDS.AUTO_NIVEAU)
      hasShownModal.value = true
    }
  }

  // Méthode pour fermer le modal
  const closeAutoNiveauModal = () => {
    console.log('🚪 Fermeture du modal AutoNiveau...')
    closeModal(MODAL_IDS.AUTO_NIVEAU)
    hasShownModal.value = false // Reset pour permettre la réouverture si nécessaire
  }

  // Méthode pour gérer la sélection du niveau
  const handleNiveauSelected = () => {
    console.log('🎯 Niveau sélectionné, fermeture du modal...')
    hasUserSelected.value = true // Marquer que l'utilisateur a fait une sélection
    closeAutoNiveauModal()
    // Le store sera mis à jour automatiquement via le modal
  }

  // Vérifier si le modal doit s'afficher quand l'utilisateur se connecte
  const checkAndShowModal = async () => {
    if (isChecking.value) {
      return
    }
    
    isChecking.value = true
    
    try {
      // Vérifier d'abord localStorage
      const configCompleted = localStorage.getItem('configurationCompleted') === 'true'
      if (configCompleted) {
        console.log('🔒 Configuration déjà complétée dans localStorage')
        return
      }
      
      // Attendre que fetchUser soit terminé
      while (userStore.isLoading) {
        await new Promise(resolve => setTimeout(resolve, 100))
      }
      
      // Vérifier si l'utilisateur a déjà pays ET niveau_pays dans la BDD
      if (userStore.isAuthenticated && userStore.pays && userStore.niveau_pays) {
        console.log('✅ Utilisateur a déjà pays et niveau dans la BDD, pas besoin du modal')
        // Marquer comme terminé pour éviter les futures ouvertures
        localStorage.setItem('configurationCompleted', 'true')
        return
      }
      
      // Ne pas afficher si l'utilisateur a déjà fait une sélection dans cette session
      if (userStore.isAuthenticated && (!userStore.pays || !userStore.niveau_pays) && !hasUserSelected.value) {
        if (shouldShowModal.value) {
          console.log('🎯 Ouverture du modal de configuration')
          openAutoNiveauModal()
        }
      }
    } finally {
      isChecking.value = false
    }
  }

  // Surveiller les changements d'authentification (simplifié)
  watch(
    () => userStore.isAuthenticated,
    (isAuthenticated) => {
      if (!isAuthenticated) {
        // Reset quand l'utilisateur se déconnecte
        console.log('👋 Utilisateur déconnecté - reset des flags')
        hasShownModal.value = false
        hasUserSelected.value = false
        // NE PAS effacer localStorage ici car cela peut être temporaire
      }
    }
  )

  // Surveiller les changements de pays et niveau_pays
  watch(
    [() => userStore.pays, () => userStore.niveau_pays],
    ([pays, niveau_pays]) => {
      console.log('👀 Changement détecté dans le store:', { pays, niveau_pays })
      // Si l'utilisateur a maintenant un pays ET un niveau_pays, fermer le modal
      if (pays && niveau_pays) {
        console.log('✅ Pays et niveau_pays présents, fermeture du modal')
        
        // Marquer la configuration comme terminée
        localStorage.setItem('configurationCompleted', 'true')
        localStorage.setItem('userConfiguration', JSON.stringify({
          pays: pays,
          niveau_pays: niveau_pays,
          timestamp: new Date().toISOString()
        }))
        
        hasUserSelected.value = true // Empêcher la réouverture
        closeAutoNiveauModal()
      }
    }
  )

  // Watcher séparé pour vérifier l'ouverture initiale quand les données sont chargées
  watch(
    [() => userStore.isAuthenticated, () => userStore.isLoading, () => userStore.pays, () => userStore.niveau_pays],
    ([isAuth, isLoading, pays, niveauPays]) => {
      if (isAuth && !isLoading) {
        // Données chargées, vérifier si on doit ouvrir le modal
        if (pays && niveauPays) {
          // Utilisateur déjà configuré, marquer comme terminé
          console.log('✅ Utilisateur déjà configuré en BDD, pas de modal nécessaire')
          localStorage.setItem('configurationCompleted', 'true')
          hasUserSelected.value = true
        } else if (!hasShownModal.value && !hasUserSelected.value) {
          // Utilisateur pas encore configuré et modal pas encore montré
          console.log('🎯 Utilisateur non configuré, ouverture du modal')
          setTimeout(() => {
            if (shouldShowModal.value) {
              openAutoNiveauModal()
            }
          }, 500)
        }
      }
    },
    { immediate: true }
  )

  return {
    // État
    shouldShowModal,
    isAutoNiveauModalOpen,
    isChecking,
    
    // Méthodes
    openAutoNiveauModal,
    closeAutoNiveauModal,
    handleNiveauSelected,
    checkAndShowModal
  }
}
