<template>
  <div class="user-config-selector">
    <!-- Carte de configuration actuelle -->
    <PaysNiveauDisplayCard 
      :user-pays="userPays" 
      :user-niveau="userNiveau" 
      @edit="showConfigModal = true" 
    />
    
    <!-- Modal de configuration -->
    <PaysNiveauSelectionModal
      v-model="showConfigModal"
      :pays-list="paysList"
      :filtered-niveaux="filteredNiveaux"
      :loading-niveaux="loadingNiveaux"
      :selected-pays-id="selectedPaysId"
      :selected-niveau-id="selectedNiveauId"
      :user-pays="userPays"
      :user-niveau="userNiveau"
      :current-step="currentStep"
      :can-save="canSave"
      :saving="saving"
      @select-pays="selectPays"
      @select-niveau="selectNiveau"
      @save="saveConfiguration"
      @prefetch-niveaux="prefetchNiveauxForPays"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import PaysNiveauDisplayCard from './PaysNiveauDisplayCard.vue'
import PaysNiveauSelectionModal from './PaysNiveauSelectionModal.vue'
import { usePaysNiveauConfig } from '@/composables/usePaysNiveauConfig'

// Utiliser le composable pour toute la logique métier
const {
  // État
  paysList,
  niveauxList,
  selectedPaysId,
  selectedNiveauId,
  saving,
  showConfigModal,
  currentStep,
  loadingNiveaux,
  
  // Computed
  userPays,
  userNiveau,
  filteredNiveaux,
  canSave,
  
  // Méthodes
  loadData,
  selectPays,
  selectNiveau,
  saveConfiguration,
  prefetchNiveauxForPays
} = usePaysNiveauConfig()

// Lifecycle
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.user-config-selector {
  width: 100%;
}
</style>
