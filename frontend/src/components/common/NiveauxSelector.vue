<template>
  <div class="niveaux-section">
    <label class="niveaux-label">{{ label || 'Niveaux concernés :' }}</label>
    <div v-if="niveaux.length > 0" class="niveaux-checkboxes">
      <label 
        v-for="niveau in niveaux" 
        :key="niveau.id" 
        class="niveau-checkbox"
      >
        <input 
          type="checkbox" 
          :value="niveau.id" 
          :checked="isSelected(niveau.id)"
          @change="toggleNiveau(niveau.id)"
        />
        <span 
          class="niveau-badge"
          :style="{ backgroundColor: niveau.couleur }"
        >
          {{ niveau.nom }}
        </span>
      </label>
    </div>
    <div v-else class="niveaux-loading">
      <p>Chargement des niveaux...</p>
      <p>Niveaux disponibles: {{ niveaux.length }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getNiveaux } from '@/api/niveaux'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  label: {
    type: String,
    default: 'Niveaux concernés :'
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const niveaux = ref([])

// Charger les niveaux au montage
onMounted(async () => {
  try {
    const nivData = await getNiveaux()
    niveaux.value = nivData || []
  } catch (error) {
    console.error('[NiveauxSelector] Erreur lors du chargement des niveaux:', error)
    niveaux.value = []
  }
})

// Vérifier si un niveau est sélectionné
const isSelected = (niveauId) => {
  return props.modelValue.includes(niveauId)
}

// Basculer la sélection d'un niveau
const toggleNiveau = (niveauId) => {
  const newValue = [...props.modelValue]
  const index = newValue.indexOf(niveauId)
  
  if (index > -1) {
    newValue.splice(index, 1)
  } else {
    newValue.push(niveauId)
  }
  
  emit('update:modelValue', newValue)
  emit('change', newValue)
}
</script>

<style scoped>
.niveaux-section {
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}

.niveaux-label {
  font-size: 0.9rem;
  color: #4b5563;
  margin-bottom: 0.5rem;
  font-weight: 500;
  display: block;
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
}

.niveau-checkbox input[type="checkbox"] {
  margin: 0;
}

.niveau-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  text-align: center;
  min-width: 60px;
  color: white;
}

.niveaux-loading {
  padding: 0.5rem;
  background-color: #f3f4f6;
  border-radius: 0.375rem;
  border: 1px solid #e5e7eb;
}

.niveaux-loading p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #6b7280;
}
</style> 