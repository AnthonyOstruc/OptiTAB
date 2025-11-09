import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { useToast } from '@/composables/useToast'
import { getPays } from '@/api/pays.js'
import { getNiveauxParPays } from '@/api/niveaux.js'
import { updateUserPaysNiveau, updateUserProfile } from '@/api/users.js'

export function usePaysNiveauConfig() {
  const userStore = useUserStore()
  const subscriptionStore = useSubscriptionStore()
  const { showToast } = useToast()

  // État réactif
  const paysList = ref([])
  const niveauxList = ref([])
  const selectedPaysId = ref(null)
  const selectedNiveauId = ref(null)
  const selectedRole = ref('student')
  const saving = ref(false)
  const showConfigModal = ref(false)
  const currentStep = ref('pays')
  const loadingNiveaux = ref(false)

  // Cache local pour éviter les requêtes répétées
  const niveauxCacheByPays = new Map()
  let currentNiveauxFetchId = 0

  // Computed properties
  const userPays = computed(() => userStore.pays)
  const userNiveau = computed(() => userStore.niveau_pays)
  const userRole = computed(() => userStore.role || 'student')
  const restrictedLevels = computed(() => {
    const levels = subscriptionStore.unlockedLevels || []
    return levels
      .filter(level => level?.id != null)
      .map(level => ({
        niveauId: Number(level.id),
        paysId: level.pays?.id ? Number(level.pays.id) : (level.pays_id ? Number(level.pays_id) : null),
        label: level.pays?.nom ? `${level.nom} (${level.pays.nom})` : level.nom
      }))
  })
  const isSelectionRestricted = computed(() => restrictedLevels.value.length > 0)

  const filteredNiveaux = computed(() => {
    if (!selectedPaysId.value) return []
    return niveauxList.value
  })

  const canSave = computed(() => {
    const paysChanged = selectedPaysId.value !== userPays.value?.id
    const niveauChanged = selectedNiveauId.value !== userNiveau.value?.id
    const roleChanged = selectedRole.value !== userRole.value
    const hasPaysNiveau = Boolean(selectedPaysId.value && selectedNiveauId.value)
    return Boolean(paysChanged || niveauChanged || roleChanged) && (hasPaysNiveau || roleChanged)
  })

  // Méthodes
  const loadData = async () => {
    try {
      const paysData = await getPays()
      paysList.value = paysData
      
      if (userPays.value) {
        selectedPaysId.value = userPays.value.id
        await loadNiveauxForPays(userPays.value.id)
      } else if (paysList.value.length) {
        selectedPaysId.value = paysList.value[0].id
        await loadNiveauxForPays(paysList.value[0].id)
      }
      if (userNiveau.value) {
        selectedNiveauId.value = userNiveau.value.id
      }

      // S'assurer que les utilisateurs normaux ont toujours le rôle "student"
      selectedRole.value = userStore.isAdmin ? userRole.value : 'student'
    } catch (error) {
      console.error('Error loading data:', error)
      showToast('Erreur lors du chargement des données', 'error')
    }
  }

  // Prefetch silencieux pour améliorer la réactivité (hover par ex.)
  const prefetchNiveauxForPays = async (paysId) => {
    if (!paysId || niveauxCacheByPays.has(paysId)) return
    try {
      const niveauxData = await getNiveauxParPays(paysId)
      niveauxCacheByPays.set(paysId, niveauxData)
      const paysIndex = paysList.value.findIndex(p => p.id === paysId)
      if (paysIndex !== -1) {
        paysList.value[paysIndex] = {
          ...paysList.value[paysIndex],
          nombre_niveaux: niveauxData.length
        }
      }
    } catch (error) {
      // silencieux
    }
  }

  const loadNiveauxForPays = async (paysId) => {
    if (!paysId) {
      niveauxList.value = []
      return
    }

    // Utiliser le cache si disponible
    if (niveauxCacheByPays.has(paysId)) {
      niveauxList.value = niveauxCacheByPays.get(paysId)
      return
    }

    try {
      loadingNiveaux.value = true
      // Vider immédiatement pour éviter d'afficher les anciens niveaux
      niveauxList.value = []

      const fetchId = ++currentNiveauxFetchId
      const niveauxData = await getNiveauxParPays(paysId)

      // Si une autre requête a été lancée entre-temps, ignorer ce résultat
      if (fetchId !== currentNiveauxFetchId) {
        return
      }

      niveauxList.value = niveauxData

      // Mettre en cache
      niveauxCacheByPays.set(paysId, niveauxData)
      
      // Mettre à jour le nombre de niveaux dans la liste des pays
      const paysIndex = paysList.value.findIndex(pays => pays.id === paysId)
      if (paysIndex !== -1) {
        paysList.value[paysIndex] = {
          ...paysList.value[paysIndex],
          nombre_niveaux: niveauxData.length
        }
      }
    } catch (error) {
      console.error('Error loading niveaux for pays:', error)
      showToast('Erreur lors du chargement des niveaux', 'error')
    } finally {
      loadingNiveaux.value = false
    }
  }

  const selectPays = async (pays) => {
    selectedPaysId.value = pays.id
    if (pays.id !== userPays.value?.id) {
      selectedNiveauId.value = null
      currentStep.value = 'niveau'
    }
    // Ne pas bloquer l'UI: lancer le chargement sans attendre
    loadNiveauxForPays(pays.id)
  }

  const selectNiveau = (niveau) => {
    selectedNiveauId.value = niveau.id
  }

  const selectRole = (role) => {
    // Seuls les admins peuvent sélectionner le rôle "parent"
    if (role === 'student' || (role === 'parent' && userStore.isAdmin)) {
      selectedRole.value = role
    } else if (role === 'parent' && !userStore.isAdmin) {
      // Forcer le rôle "student" pour les utilisateurs normaux
      selectedRole.value = 'student'
    }
  }

  const saveConfiguration = async () => {
    if (!canSave.value) return
    
    try {
      saving.value = true
      const actions = []
      const paysChanged = selectedPaysId.value !== userPays.value?.id
      const niveauChanged = selectedNiveauId.value !== userNiveau.value?.id
      const roleChanged = selectedRole.value !== userRole.value

      if (paysChanged || niveauChanged) {
        actions.push(
          updateUserPaysNiveau({
            pays_id: selectedPaysId.value,
            niveau_id: selectedNiveauId.value
          })
        )
      }

      if (roleChanged) {
        actions.push(updateUserProfile({ role: selectedRole.value }))
      }

      if (actions.length) {
        await Promise.all(actions)
      }
      
      await userStore.fetchUser()
      showToast('Configuration mise à jour avec succès !', 'success')
      showConfigModal.value = false
      
      // Marquer la configuration comme terminée
      if (userStore.id) {
        const userConfigKey = `configurationCompleted_${userStore.id}`
        localStorage.setItem(userConfigKey, 'true')
      }
      
    } catch (error) {
      console.error('Error saving configuration:', error)
      showToast('Erreur lors de la sauvegarde', 'error')
    } finally {
      saving.value = false
    }
  }

  const closeModal = () => {
    showConfigModal.value = false
    // Réinitialiser les sélections
    selectedPaysId.value = userPays.value?.id || null
    selectedNiveauId.value = userNiveau.value?.id || null
    currentStep.value = 'pays'
  }

  // Watchers
  watch(selectedPaysId, (newPaysId) => {
    if (newPaysId && filteredNiveaux.value.length > 0) {
      if (!selectedNiveauId.value || !filteredNiveaux.value.find(n => n.id === selectedNiveauId.value)) {
        selectedNiveauId.value = filteredNiveaux.value[0]?.id
      }
    }
  })

  return {
    // État
    paysList,
    niveauxList,
    selectedPaysId,
    selectedNiveauId,
    selectedRole,
    saving,
    showConfigModal,
    currentStep,
    loadingNiveaux,
    
    // Computed
    userPays,
    userNiveau,
    userRole,
    filteredNiveaux,
    canSave,
    restrictedLevels,
    isSelectionRestricted,
    
    // Méthodes
    loadData,
    selectPays,
    selectNiveau,
    selectRole,
    saveConfiguration,
    closeModal,
    prefetchNiveauxForPays
  }
}
