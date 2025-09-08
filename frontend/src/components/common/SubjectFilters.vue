<template>
  <div class="subject-filters">
    <button 
      v-for="subject in subjects" 
      :key="subject.id"
      :class="['subject-btn', { active: selectedSubject === subject.id }]"
      @click="selectSubject(subject.id)"
    >
      {{ subject.name }}
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  subjects: {
    type: Array,
    default: () => [
      { id: 'maths', name: 'Mathématiques' },
      { id: 'physics', name: 'Physique' },
      { id: 'chemistry', name: 'Chimie' }
    ]
  },
  initialSubject: {
    type: String,
    default: 'maths'
  }
})

// Émissions
const emit = defineEmits(['subject-changed'])

// État local
const selectedSubject = ref(props.initialSubject)

// Méthodes
const selectSubject = (subjectId) => {
  selectedSubject.value = subjectId
  emit('subject-changed', subjectId)
}

// Watcher pour synchroniser avec les props externes
watch(() => props.initialSubject, (newValue) => {
  selectedSubject.value = newValue
})

// Exposer la valeur actuelle pour utilisation externe
defineExpose({
  selectedSubject: selectedSubject
})
</script>

<style scoped>
.subject-filters {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.subject-btn {
  padding: 0.75rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  color: #374151;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 120px;
  text-align: center;
}

.subject-btn:hover {
  border-color: #2563eb;
  color: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
}

.subject-btn.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

.subject-btn:active {
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 768px) {
  .subject-filters {
    gap: 0.5rem;
  }
  
  .subject-btn {
    padding: 0.6rem 1rem;
    min-width: 100px;
    font-size: 0.85rem;
  }
}
</style> 