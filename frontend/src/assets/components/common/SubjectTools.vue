<template>
  <div class="tools-section">
    <h3 class="tools-title">{{ currentSubject.name }} - Outils disponibles</h3>
    
    <div class="tools-grid">
      <div 
        v-for="category in toolCategories" 
        :key="category.id"
        class="tool-category"
      >
        <h4>{{ category.name }}</h4>
        
        <!-- Outils avec items (pour les mathématiques) -->
        <SimpleCalculator
          v-if="category.items"
          :tabs="category.items"
          @input="handleToolInput"
        >
          <template #fraction>
            <img src="/scientificIcons/fraction.svg" alt="fraction" class="svg-dark" />
          </template>
          <template #sqrt>
            <img src="/scientificIcons/sqrt.svg" alt="sqrt" class="svg-dark" />
          </template>
          <template #nsqrt>
            <img src="/scientificIcons/nsqrt.svg" alt="nsqrt" class="svg-dark" />
          </template>
          <template #exposant>
            <img src="/scientificIcons/exposant.svg" alt="exposant" class="svg-dark" />
          </template>
          <template #exp>
            <img src="/scientificIcons/exp.svg" alt="exp" class="svg-dark" />
          </template>
        </SimpleCalculator>
        
        <!-- Outils avec actions (pour physique/chimie) -->
        <div v-else-if="category.actions" class="action-buttons">
          <button 
            v-for="action in category.actions"
            :key="action.action"
            class="action-btn"
            @click="handleAction(action.action)"
          >
            {{ action.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSubjectsStore } from '@/stores/subjects/index'
import { getSubjectTools, getToolCategories } from '@/config/subjectTools'
import SimpleCalculator from '@/components/SimpleCalculator.vue'

// Props
const props = defineProps({
  // Permettre de passer une matière spécifique ou utiliser celle du store
  subjectId: {
    type: String,
    default: null
  }
})

// Émissions
const emit = defineEmits(['tool-input', 'action'])

// Store
const subjectsStore = useSubjectsStore()

// Computed
const currentSubject = computed(() => {
  const subjectId = props.subjectId || subjectsStore.selectedSubject
  return getSubjectTools(subjectId)
})

const toolCategories = computed(() => {
  const subjectId = props.subjectId || subjectsStore.selectedSubject
  return getToolCategories(subjectId)
})

// Méthodes
const handleToolInput = (input) => {
  emit('tool-input', input)
}

const handleAction = (action) => {
  emit('action', action)
}
</script>

<style scoped>
.tools-section {
  margin: 2rem 0;
}

.tools-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 1.5rem;
  text-align: center;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.tool-category {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tool-category h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e3a8a;
  margin-bottom: 1rem;
  text-align: center;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.action-btn {
  padding: 0.75rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.action-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.action-btn:active {
  transform: translateY(0);
}

.svg-dark {
  width: 32px;
  height: 32px;
  object-fit: contain;
  filter: invert(0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style> 