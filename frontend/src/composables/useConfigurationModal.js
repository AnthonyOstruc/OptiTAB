/**
 * Composable pour gérer l'affichage automatique du modal de configuration pays/niveau
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'

export function useConfigurationModal() {
  const userStore = useUserStore()
  const isModalOpen = ref(false)

  /**
   * Détermine si le modal doit être ouvert
   */
  const shouldShowModal = computed(() => {
    // Vérifier d'abord si la configuration est complétée dans localStorage
    const configCompleted = localStorage.getItem('configurationCompleted') === 'true'
    if (configCompleted) return false

    // Ne pas montrer le modal si l'utilisateur n'est pas connecté ou en cours de chargement
    if (!userStore.isAuthenticated || userStore.isLoading) {
      return false
    }

    // Montrer le modal si l'utilisateur connecté n'a pas de pays/niveau
    return !userStore.pays || !userStore.niveau_pays
  })

  /**
   * Ouvre le modal de configuration
   */
  const openModal = () => {
    isModalOpen.value = true
  }

  /**
   * Ferme le modal de configuration
   */
  const closeModal = () => {
    isModalOpen.value = false
  }

  /**
   * Gère la confirmation de la configuration
   */
  const handleConfigurationConfirmed = (config) => {
    console.log('Configuration confirmée:', config)
    // Le modal se fermera automatiquement grâce à la logique ajoutée
  }

  // Watcher pour ouvrir automatiquement le modal si nécessaire
  watch([shouldShowModal, () => userStore.isAuthenticated], ([should, isAuth]) => {
    if (should && isAuth && !isModalOpen.value) {
      // Attendre un petit délai pour s'assurer que l'interface est prête
      setTimeout(() => {
        openModal()
      }, 500)
    }
  }, { immediate: true })

  // Vérifier au montage du composant
  onMounted(() => {
    if (shouldShowModal.value) {
      setTimeout(() => {
        openModal()
      }, 1000) // Délai plus long au montage initial
    }
  })

  return {
    isModalOpen,
    shouldShowModal,
    openModal,
    closeModal,
    handleConfigurationConfirmed
  }
}
