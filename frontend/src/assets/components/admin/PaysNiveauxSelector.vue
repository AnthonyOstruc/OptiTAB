<template>
  <div class="pays-niveaux-selector">
    <div class="global-actions" v-if="niveauxList.length > 0">
      <button 
        type="button"
        @click="selectAllFromAllCountries"
        class="btn-global-select"
      >
        🌍 Sélectionner tous les niveaux de tous les pays
      </button>
      <button 
        type="button"
        @click="clearAllSelections"
        class="btn-global-clear"
        v-if="modelValue.length > 0"
      >
        🗑️ Effacer toute la sélection
      </button>
    </div>

    <div class="pays-section">
      <label class="section-label">Pays :</label>
      <select 
        v-model="selectedPaysId" 
        @change="onPaysChange"
        class="pays-select"
      >
        <option value="">-- Sélectionner un pays --</option>
        <option 
          v-for="pays in paysList" 
          :key="pays.id" 
          :value="pays.id"
        >
          {{ pays.drapeau_emoji }} {{ pays.nom }}
        </option>
      </select>
    </div>

    <div v-if="selectedPaysId" class="niveaux-section">
      <div class="niveaux-header">
        <label class="section-label">Niveaux pour {{ selectedPaysName }} :</label>
        <div class="niveaux-actions">
          <button 
            type="button"
            @click="selectAllNiveaux"
            class="btn-select-all"
            v-if="filteredNiveaux.length > 0"
          >
            Tout sélectionner
          </button>
          <button 
            type="button"
            @click="deselectAllNiveaux"
            class="btn-deselect-all"
            v-if="hasSelectedNiveauxInCurrentPays"
          >
            Tout désélectionner
          </button>
        </div>
      </div>
      
      <div v-if="filteredNiveaux.length > 0" class="niveaux-checkboxes">
        <label 
          v-for="niveau in filteredNiveaux" 
          :key="niveau.id" 
          class="niveau-checkbox"
        >
          <input 
            type="checkbox" 
            :value="niveau.id" 
            :checked="isNiveauSelected(niveau.id)"
            @change="toggleNiveau(niveau.id)"
          />
          <span 
            class="niveau-badge"
            :style="{ backgroundColor: niveau.couleur || '#6366f1' }"
          >
            {{ niveau.nom }}
          </span>
        </label>
      </div>
      <div v-else class="no-niveaux">
        <p>Aucun niveau disponible pour ce pays</p>
      </div>
    </div>

    <div v-if="!selectedPaysId && modelValue.length > 0" class="current-selection">
      <label class="section-label">Sélection actuelle :</label>
      <div class="current-niveaux">
        <span 
          v-for="niveau in currentSelectedNiveaux" 
          :key="niveau.id"
          class="current-niveau-badge"
          :style="{ backgroundColor: niveau.couleur || '#6366f1' }"
        >
          {{ niveau.pays_info?.drapeau_emoji }} {{ niveau.nom }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getPays } from '@/api/pays.js'
import { getNiveauxByPays } from '@/api/niveaux.js'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

// État
const paysList = ref([])
const niveauxList = ref([])
const selectedPaysId = ref('')

// Computed
const selectedPaysName = computed(() => {
  const pays = paysList.value.find(p => p.id === selectedPaysId.value)
  return pays ? pays.nom : ''
})

const filteredNiveaux = computed(() => {
  if (!selectedPaysId.value) return []
  return niveauxList.value.filter(niveau => niveau.pays === selectedPaysId.value)
})

const currentSelectedNiveaux = computed(() => {
  if (!props.modelValue.length) return []
  return niveauxList.value.filter(niveau => props.modelValue.includes(niveau.id))
})

const hasSelectedNiveauxInCurrentPays = computed(() => {
  if (!selectedPaysId.value || !filteredNiveaux.value.length) return false
  return filteredNiveaux.value.some(niveau => props.modelValue.includes(niveau.id))
})

// Méthodes
const loadData = async () => {
  try {
    const [paysData, niveauxData] = await Promise.all([
      getPays(),
      getNiveauxByPays()
    ])
    
    paysList.value = paysData
    niveauxList.value = niveauxData
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error)
  }
}

const onPaysChange = () => {
  // Ne pas réinitialiser automatiquement les niveaux sélectionnés
  // L'admin peut vouloir ajouter des niveaux d'un autre pays
}

const isNiveauSelected = (niveauId) => {
  return props.modelValue.includes(niveauId)
}

const toggleNiveau = (niveauId) => {
  const newValue = [...props.modelValue]
  const index = newValue.indexOf(niveauId)
  
  if (index > -1) {
    newValue.splice(index, 1)
  } else {
    newValue.push(niveauId)
  }
  
  emit('update:modelValue', newValue)
}

const selectAllNiveaux = () => {
  if (!selectedPaysId.value || !filteredNiveaux.value.length) return
  
  const currentValues = [...props.modelValue]
  const niveauxToAdd = filteredNiveaux.value
    .map(niveau => niveau.id)
    .filter(id => !currentValues.includes(id))
  
  const newValue = [...currentValues, ...niveauxToAdd]
  emit('update:modelValue', newValue)
}

const deselectAllNiveaux = () => {
  if (!selectedPaysId.value || !filteredNiveaux.value.length) return
  
  const niveauxIds = filteredNiveaux.value.map(niveau => niveau.id)
  const newValue = props.modelValue.filter(id => !niveauxIds.includes(id))
  
  emit('update:modelValue', newValue)
}

const selectAllFromAllCountries = () => {
  const allNiveauxIds = niveauxList.value.map(niveau => niveau.id)
  emit('update:modelValue', allNiveauxIds)
}

const clearAllSelections = () => {
  emit('update:modelValue', [])
}

// Lifecycle
onMounted(async () => {
  await loadData()
  // Pré-sélectionner automatiquement le premier pays ayant déjà des niveaux sélectionnés
  if (props.modelValue.length > 0) {
    const paysWithSelected = niveauxList.value.find(n => props.modelValue.includes(n.id))?.pays
    if (paysWithSelected) {
      selectedPaysId.value = paysWithSelected
    }
  }
})
</script>

<style scoped>
.pays-niveaux-selector {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 1rem;
}

.global-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.btn-global-select,
.btn-global-clear {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-global-select {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.btn-global-select:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
}

.btn-global-clear {
  background: #fee2e2;
  color: #991b1b;
  border-color: #f87171;
}

.btn-global-clear:hover {
  background: #fecaca;
  border-color: #ef4444;
}

.pays-section {
  margin-bottom: 1rem;
}

.section-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.pays-select {
  width: 100%;
  max-width: 300px;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
}

.pays-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}

.niveaux-section {
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
}

.niveaux-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.niveaux-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-select-all,
.btn-deselect-all {
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid;
}

.btn-select-all {
  background: #ecfdf5;
  color: #065f46;
  border-color: #10b981;
}

.btn-select-all:hover {
  background: #d1fae5;
  border-color: #059669;
}

.btn-deselect-all {
  background: #fef2f2;
  color: #991b1b;
  border-color: #ef4444;
}

.btn-deselect-all:hover {
  background: #fee2e2;
  border-color: #dc2626;
}

.niveaux-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.niveau-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.niveau-checkbox:hover {
  background-color: rgba(59, 130, 246, 0.1);
}

.niveau-checkbox input[type="checkbox"] {
  margin: 0;
  cursor: pointer;
}

.niveau-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
  color: white;
  min-width: 60px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.no-niveaux {
  padding: 1rem;
  background-color: #fef3cd;
  border: 1px solid #fbbf24;
  border-radius: 6px;
  color: #92400e;
  text-align: center;
}

.current-selection {
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
}

.current-niveaux {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.current-niveau-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .pays-select {
    max-width: 100%;
  }
  
  .niveaux-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .niveaux-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .niveaux-checkboxes {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .current-niveaux {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>
