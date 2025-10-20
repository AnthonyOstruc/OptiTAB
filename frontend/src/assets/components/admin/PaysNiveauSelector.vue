<template>
  <div class="pays-niveau-selector">
    <!-- Sélection du pays -->
    <div class="selector-section">
      <label class="selector-label">🌍 Pays</label>
      <select 
        v-model="selectedPaysId" 
        @change="onPaysChange"
        class="selector-select"
        :disabled="loadingPays"
      >
        <option value="">Sélectionnez un pays</option>
        <option 
          v-for="pays in paysList" 
          :key="pays.id" 
          :value="pays.id"
        >
          {{ pays.drapeau_emoji }} {{ pays.nom }}
        </option>
      </select>
      <div v-if="loadingPays" class="loading-indicator">
        <span class="spinner"></span>
        Chargement des pays...
      </div>
    </div>

    <!-- Sélection du niveau -->
    <div v-if="selectedPaysId" class="selector-section">
      <label class="selector-label">📚 Niveaux disponibles</label>
      <div v-if="loadingNiveaux" class="loading-indicator">
        <span class="spinner"></span>
        Chargement des niveaux...
      </div>
      <div v-else-if="niveauxList.length === 0" class="no-niveaux">
        Aucun niveau disponible pour ce pays
      </div>
      <div v-else class="niveaux-grid">
        <div 
          v-for="niveau in niveauxList" 
          :key="niveau.id"
          class="niveau-item"
          :class="{ selected: selectedNiveauId === niveau.id }"
          @click="selectNiveau(niveau)"
        >
          <div 
            class="niveau-color" 
            :style="{ backgroundColor: niveau.couleur }"
          ></div>
          <div class="niveau-info">
            <span class="niveau-nom">{{ niveau.nom }}</span>
            <span class="niveau-pays">{{ selectedPays?.nom }}</span>
          </div>
          <div v-if="selectedNiveauId === niveau.id" class="selected-indicator">
            ✓
          </div>
        </div>
      </div>
    </div>

    <!-- Résumé de la sélection -->
    <div v-if="selectedPays && selectedNiveau" class="selection-summary">
      <h4>✅ Sélection actuelle</h4>
      <div class="summary-item">
        <strong>Pays:</strong> {{ selectedPays.drapeau_emoji }} {{ selectedPays.nom }}
      </div>
      <div class="summary-item">
        <strong>Niveau:</strong> 
        <span 
          class="niveau-badge"
          :style="{ backgroundColor: selectedNiveau.couleur }"
        >
          {{ selectedNiveau.nom }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { getPaysActifs } from '@/api/pays.js'
import { getNiveauxParPays } from '@/api/niveaux.js'

export default {
  name: 'PaysNiveauSelector',
  props: {
    modelValue: {
      type: Object,
      default: () => ({ pays_id: null, niveau_id: null })
    }
  },
  emits: ['update:modelValue', 'selection-change'],
  setup(props, { emit }) {
    // États réactifs
    const paysList = ref([])
    const niveauxList = ref([])
    const selectedPaysId = ref(props.modelValue.pays_id || null)
    const selectedNiveauId = ref(props.modelValue.niveau_id || null)
    const loadingPays = ref(false)
    const loadingNiveaux = ref(false)

    // Computed
    const selectedPays = computed(() => 
      paysList.value.find(p => p.id === selectedPaysId.value)
    )
    
    const selectedNiveau = computed(() => 
      niveauxList.value.find(n => n.id === selectedNiveauId.value)
    )

    // Méthodes
    const loadPays = async () => {
      try {
        loadingPays.value = true
        const data = await getPaysActifs()
        paysList.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des pays:', error)
      } finally {
        loadingPays.value = false
      }
    }

    const loadNiveaux = async (paysId) => {
      if (!paysId) {
        niveauxList.value = []
        return
      }

      try {
        loadingNiveaux.value = true
        const data = await getNiveauxParPays(paysId)
        niveauxList.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des niveaux:', error)
        niveauxList.value = []
      } finally {
        loadingNiveaux.value = false
      }
    }

    const onPaysChange = () => {
      selectedNiveauId.value = null // Reset niveau quand pays change
      loadNiveaux(selectedPaysId.value)
      emitSelection()
    }

    const selectNiveau = (niveau) => {
      selectedNiveauId.value = niveau.id
      emitSelection()
    }

    const emitSelection = () => {
      const selection = {
        pays_id: selectedPaysId.value,
        niveau_id: selectedNiveauId.value,
        pays: selectedPays.value,
        niveau: selectedNiveau.value
      }
      
      emit('update:modelValue', selection)
      emit('selection-change', selection)
    }

    // Watchers
    watch(() => props.modelValue, (newValue) => {
      if (newValue.pays_id !== selectedPaysId.value) {
        selectedPaysId.value = newValue.pays_id
        if (newValue.pays_id) {
          loadNiveaux(newValue.pays_id)
        }
      }
      if (newValue.niveau_id !== selectedNiveauId.value) {
        selectedNiveauId.value = newValue.niveau_id
      }
    }, { deep: true })

    // Initialisation
    onMounted(() => {
      loadPays()
      if (selectedPaysId.value) {
        loadNiveaux(selectedPaysId.value)
      }
    })

    return {
      paysList,
      niveauxList,
      selectedPaysId,
      selectedNiveauId,
      loadingPays,
      loadingNiveaux,
      selectedPays,
      selectedNiveau,
      onPaysChange,
      selectNiveau
    }
  }
}
</script>

<style scoped>
.pays-niveau-selector {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.selector-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selector-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.selector-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background-color: white;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.selector-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.no-niveaux {
  color: #6b7280;
  font-style: italic;
  padding: 1rem;
  text-align: center;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.niveau-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  background-color: white;
}

.niveau-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.niveau-item.selected {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.niveau-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.niveau-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.niveau-nom {
  font-weight: 600;
  color: #111827;
  font-size: 0.875rem;
}

.niveau-pays {
  font-size: 0.75rem;
  color: #6b7280;
}

.selected-indicator {
  color: #3b82f6;
  font-weight: bold;
  font-size: 1.125rem;
}

.selection-summary {
  padding: 1rem;
  background-color: #f0f9ff;
  border: 1px solid #0ea5e9;
  border-radius: 0.5rem;
}

.selection-summary h4 {
  margin: 0 0 0.75rem 0;
  color: #0c4a6e;
  font-size: 1rem;
}

.summary-item {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.niveau-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.5rem;
}
</style> 