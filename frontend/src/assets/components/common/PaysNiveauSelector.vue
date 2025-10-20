<template>
  <div class="pays-niveau-selector">
    <!-- En-tête -->
    <div class="selector-header mb-4">
      <h3 class="text-lg font-semibold text-gray-800">
        <i class="fas fa-globe mr-2"></i>
        Sélection Pays & Niveau
      </h3>
      <p class="text-sm text-gray-600">
        Choisissez votre pays et niveau scolaire pour filtrer le contenu
      </p>
    </div>

    <!-- Sélecteurs -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Sélecteur Pays -->
      <div class="form-group">
        <label class="form-label">
          <i class="fas fa-flag mr-1"></i>
          Pays
        </label>
        <select 
          v-model="selectedPaysId" 
          @change="onPaysChange"
          class="form-select w-full"
          :disabled="loading"
        >
          <option value="">Sélectionnez un pays</option>
          <option 
            v-for="pays in paysDisponibles" 
            :key="pays.id" 
            :value="pays.id"
          >
            {{ pays.drapeau_emoji }} {{ pays.nom }}
          </option>
        </select>
      </div>

      <!-- Sélecteur Niveau -->
      <div class="form-group">
        <label class="form-label">
          <i class="fas fa-graduation-cap mr-1"></i>
          Niveau scolaire
        </label>
        <select 
          v-model="selectedNiveauPaysId" 
          @change="onNiveauChange"
          class="form-select w-full"
          :disabled="loading || !selectedPaysId"
        >
          <option value="">Sélectionnez un niveau</option>
          <option 
            v-for="niveauPays in niveauxDisponibles" 
            :key="niveauPays.id" 
            :value="niveauPays.id"
          >
            {{ niveauPays.niveau_pays?.nom || niveauPays.nom_local || 'Niveau' }}
          </option>
        </select>
      </div>
    </div>

    <!-- Affichage de la sélection -->
    <div v-if="selectionActive" class="selection-display mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
      <div class="flex items-center">
        <div class="flex-1">
          <p class="text-sm font-medium text-blue-800">
            Sélection active
          </p>
          <p class="text-sm text-blue-600">
            {{ paysSélectionné?.drapeau_emoji }} {{ paysSélectionné?.nom }} - 
            {{ niveauPaysSélectionné?.nom_local }}
            <span v-if="niveauPaysSélectionné?.tranche_age">
              ({{ niveauPaysSélectionné.tranche_age }})
            </span>
          </p>
        </div>
        <button 
          @click="clearSelection" 
          class="text-blue-400 hover:text-blue-600 transition-colors"
          title="Effacer la sélection"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <!-- Messages d'état -->
    <div v-if="loading" class="loading-state mt-4 text-center">
      <i class="fas fa-spinner fa-spin mr-2"></i>
      <span class="text-gray-600">Chargement...</span>
    </div>

    <div v-if="error" class="error-state mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-red-600 text-sm">
        <i class="fas fa-exclamation-triangle mr-2"></i>
        {{ error }}
      </p>
    </div>

    <!-- Mode debug (dev seulement) -->
    <div v-if="debug && selectionActive" class="debug-info mt-4 p-3 bg-gray-50 rounded-lg text-xs">
      <p><strong>Debug Info:</strong></p>
      <p>Pays ID: {{ selectedPaysId }}</p>
      <p>Niveau-Pays ID: {{ selectedNiveauPaysId }}</p>
      <p>Code unique: {{ niveauPaysSélectionné?.code_unique }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import apiClient from '@/api/client'

// Props
const props = defineProps({
  modelValuePays: {
    type: [String, Number],
    default: ''
  },
  modelValueNiveauPays: {
    type: [String, Number], 
    default: ''
  },
  debug: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValuePays', 'update:modelValueNiveauPays', 'change'])

// État local
const loading = ref(false)
const error = ref('')
const paysDisponibles = ref([])
const niveauxDisponibles = ref([])

// V-model local
const selectedPaysId = ref(props.modelValuePays)
const selectedNiveauPaysId = ref(props.modelValueNiveauPays)

// Computed
const paysSélectionné = computed(() => {
  return paysDisponibles.value.find(p => p.id == selectedPaysId.value)
})

const niveauPaysSélectionné = computed(() => {
  return niveauxDisponibles.value.find(np => np.id == selectedNiveauPaysId.value)
})

const selectionActive = computed(() => {
  return selectedPaysId.value && selectedNiveauPaysId.value
})

// Watchers pour la synchronisation v-model
watch(() => props.modelValuePays, (newVal) => {
  if (newVal !== selectedPaysId.value) {
    selectedPaysId.value = newVal
    if (newVal) {
      loadNiveauxPourPays(newVal)
    }
  }
})

watch(() => props.modelValueNiveauPays, (newVal) => {
  selectedNiveauPaysId.value = newVal
})

// Méthodes
async function loadPaysDisponibles() {
  try {
    loading.value = true
    error.value = ''
    
    const response = await apiClient.get('/api/clean/pays/')
    paysDisponibles.value = response.data.results || response.data
    
    if (props.debug) {
      console.log('🌍 Pays chargés:', paysDisponibles.value.length)
    }
  } catch (err) {
    error.value = 'Erreur lors du chargement des pays'
    console.error('Erreur chargement pays:', err)
  } finally {
    loading.value = false
  }
}

async function loadNiveauxPourPays(paysId) {
  if (!paysId) {
    niveauxDisponibles.value = []
    return
  }
  
  try {
    loading.value = true
    error.value = ''
    
    const response = await apiClient.get(`/api/clean/niveaux-pays/?pays=${paysId}`)
    niveauxDisponibles.value = response.data.results || response.data
    
    if (props.debug) {
      console.log('🎓 Niveaux chargés pour', paysId, ':', niveauxDisponibles.value.length)
    }
  } catch (err) {
    console.error('Erreur lors du chargement des niveaux pour le pays', paysId, ':', err)
    error.value = 'Erreur lors du chargement des niveaux'
    niveauxDisponibles.value = []
  } finally {
    loading.value = false
  }
}

async function onPaysChange() {
  // Réinitialiser le niveau quand le pays change
  selectedNiveauPaysId.value = ''
  niveauxDisponibles.value = []
  
  // Émettre la mise à jour
  emit('update:modelValuePays', selectedPaysId.value)
  emit('update:modelValueNiveauPays', '')
  
  // Charger les niveaux du nouveau pays
  if (selectedPaysId.value) {
    await loadNiveauxPourPays(selectedPaysId.value)
  }
  
  // Émettre l'événement de changement
  emitChange()
}

function onNiveauChange() {
  // Émettre la mise à jour
  emit('update:modelValueNiveauPays', selectedNiveauPaysId.value)
  
  // Émettre l'événement de changement
  emitChange()
}

function emitChange() {
  const changeData = {
    pays: paysSélectionné.value || null,
    niveauPays: niveauPaysSélectionné.value || null,
    isComplete: selectionActive.value
  }
  
  emit('change', changeData)
  
  if (props.debug) {
    console.log('🔄 Changement émis:', changeData)
  }
}

function clearSelection() {
  selectedPaysId.value = ''
  selectedNiveauPaysId.value = ''
  niveauxDisponibles.value = []
  
  emit('update:modelValuePays', '')
  emit('update:modelValueNiveauPays', '')
  emitChange()
}

// Initialisation
onMounted(async () => {
  await loadPaysDisponibles()
  
  // Si un pays est déjà sélectionné, charger ses niveaux
  if (selectedPaysId.value) {
    await loadNiveauxPourPays(selectedPaysId.value)
  }
})
</script>

<style scoped>
.pays-niveau-selector {
  @apply bg-white rounded-lg border border-gray-200 p-4;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-select {
  @apply block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed;
}

.form-select:disabled {
  @apply opacity-60;
}

.loading-state {
  @apply py-2;
}

.selection-display {
  @apply transition-all duration-200;
}

.error-state {
  @apply transition-all duration-200;
}

.debug-info {
  @apply font-mono border border-gray-300;
}

/* Animation pour les changements d'état */
.pays-niveau-selector > * {
  @apply transition-opacity duration-200;
}

/* Responsive */
@media (max-width: 768px) {
  .pays-niveau-selector .grid {
    @apply grid-cols-1;
  }
}
</style>
