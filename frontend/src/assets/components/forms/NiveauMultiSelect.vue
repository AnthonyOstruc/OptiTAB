<template>
  <div class="niveau-multi-select">
    <label v-if="label" class="form-label">{{ label }}</label>
    
    <div class="niveaux-grid">
      <div 
        v-for="niveau in niveaux" 
        :key="niveau.id"
        class="niveau-option"
        :class="{ selected: selectedNiveaux.includes(niveau.id) }"
        @click="toggleNiveau(niveau.id)"
      >
        <div class="niveau-color" :style="{ backgroundColor: niveau.couleur }"></div>
        <div class="niveau-info">
          <span class="niveau-nom">{{ niveau.nom }}</span>
          <span class="niveau-desc">{{ niveau.description }}</span>
        </div>
        <div class="checkbox">
          <input 
            type="checkbox" 
            :checked="selectedNiveaux.includes(niveau.id)"
            @change="toggleNiveau(niveau.id)"
          />
        </div>
      </div>
    </div>

    <div v-if="selectedNiveaux.length > 0" class="selected-summary">
      <span class="summary-label">Niveaux sélectionnés :</span>
      <div class="selected-badges">
        <span 
          v-for="niveauId in selectedNiveaux" 
          :key="niveauId"
          class="selected-badge"
          :style="{ backgroundColor: getNiveauColor(niveauId) }"
        >
          {{ getNiveauName(niveauId) }}
          <button 
            @click="removeNiveau(niveauId)" 
            class="remove-btn"
            type="button"
          >
            ×
          </button>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { getNiveaux } from '@/api/niveaux.js'

export default {
  name: 'NiveauMultiSelect',
  props: {
    modelValue: {
      type: Array,
      default: () => []
    },
    label: {
      type: String,
      default: 'Niveaux concernés'
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const niveaux = ref([])
    const selectedNiveaux = ref([...props.modelValue])

    // Computed
    const getNiveauName = (niveauId) => {
      const niveau = niveaux.value.find(n => n.id === niveauId)
      return niveau ? niveau.nom : ''
    }

    const getNiveauColor = (niveauId) => {
      const niveau = niveaux.value.find(n => n.id === niveauId)
      return niveau ? niveau.couleur : '#6b7280'
    }

    // Methods
    const loadNiveaux = async () => {
      try {
        const data = await getNiveaux()
        niveaux.value = data
      } catch (error) {
        console.error('Erreur lors du chargement des niveaux:', error)
      }
    }

    const toggleNiveau = (niveauId) => {
      const index = selectedNiveaux.value.indexOf(niveauId)
      if (index > -1) {
        selectedNiveaux.value.splice(index, 1)
      } else {
        selectedNiveaux.value.push(niveauId)
      }
    }

    const removeNiveau = (niveauId) => {
      const index = selectedNiveaux.value.indexOf(niveauId)
      if (index > -1) {
        selectedNiveaux.value.splice(index, 1)
      }
    }

    // Watch for changes
    watch(selectedNiveaux, (newValue) => {
      emit('update:modelValue', newValue)
    }, { deep: true })

    watch(() => props.modelValue, (newValue) => {
      selectedNiveaux.value = [...newValue]
    })

    onMounted(() => {
      loadNiveaux()
    })

    return {
      niveaux,
      selectedNiveaux,
      getNiveauName,
      getNiveauColor,
      toggleNiveau,
      removeNiveau
    }
  }
}
</script>

<style scoped>
.niveau-multi-select {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.niveaux-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.niveau-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.niveau-option:hover {
  border-color: #3b82f6;
  background: #f8fafc;
}

.niveau-option.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.niveau-color {
  width: 20px;
  height: 20px;
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
  color: #1f2937;
  font-size: 0.875rem;
}

.niveau-desc {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.125rem;
}

.checkbox {
  flex-shrink: 0;
}

.checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.selected-summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.summary-label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.selected-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.selected-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  background: #3b82f6;
  color: white;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.remove-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .niveaux-grid {
    grid-template-columns: 1fr;
  }
}
</style> 