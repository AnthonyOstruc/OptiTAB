<template>
  <div 
    class="option-card"
    :class="{ 
      selected: isSelected,
      current: isCurrent,
      disabled: isDisabled
    }"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
  >
    <!-- Indicateur visuel (drapeau pour pays, cercle pour niveau) -->
    <div v-if="type === 'pays'" class="flag">{{ item.drapeau_emoji }}</div>
    <div v-else class="niveau-indicator" :style="niveauStyle"></div>
    
    <!-- Informations -->
    <div class="option-info">
      <h5>{{ displayName }}</h5>
      <p>{{ displayDescription }}</p>
    </div>
    
    <!-- Badge "Actuel" si c'est l'option actuelle -->
    <div v-if="isCurrent" class="current-badge">
      Actuel
    </div>
    
    <!-- Indicateur de sélection -->
    <div v-if="isSelected" class="selected-indicator">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
  
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ['pays', 'niveau'].includes(value)
  },
  isSelected: {
    type: Boolean,
    default: false
  },
  isCurrent: {
    type: Boolean,
    default: false
  },
  isDisabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select', 'hover'])

// Computed pour l'affichage
const displayName = computed(() => {
  if (props.type === 'pays') {
    return props.item.nom
  }
  return props.item.nom_local || props.item.nom
})

const displayDescription = computed(() => {
  if (props.type === 'pays') {
    const nombreNiveaux = props.item.nombre_niveaux
    if (nombreNiveaux == null) {
      return 'Niveaux disponibles'
    }
    if (nombreNiveaux === 0) {
      return 'Aucun niveau disponible'
    }
    if (nombreNiveaux === 1) {
      return '1 niveau'
    }
    return `${nombreNiveaux} niveaux`
  }
  return props.item.description || ''
})

const niveauStyle = computed(() => {
  if (props.type !== 'niveau') return {}
  const color = props.item.couleur || '#667eea'
  return { background: color }
})

const handleClick = () => {
  if (props.isDisabled) return
  emit('select', props.item)
}

const handleMouseEnter = () => {
  if (props.isDisabled) return
  emit('hover', props.item)
}
</script>

<style scoped>
.option-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border: 2px solid #eef2f7;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  background: white;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.option-card:hover {
  border-color: #d9e0ea;
  box-shadow: 0 6px 16px rgba(16, 24, 40, 0.06);
}

.option-card:hover:not(.selected):not(.current) {
  background: white;
  border-color: #d9e0ea;
}

.option-card.selected {
  border-color: #667eea;
  background: #f5f7ff;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.18);
}

.option-card.current {
  border-color: #10b981;
  background: #edfff7;
  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.18);
}

/* S'assurer que les cartes non sélectionnées ont un fond blanc */
.option-card:not(.selected):not(.current) {
  background: white;
  border-color: #eef2f7;
}

.flag {
  font-size: 24px;
  flex-shrink: 0;
}

.niveau-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #e5e7eb;
  flex-shrink: 0;
}

.option-card.selected .niveau-indicator {
  background: #3b82f6;
}

.option-card.current .niveau-indicator {
  background: #10b981;
}

.option-info {
  flex: 1;
}

.option-info h5 {
  margin: 0 0 2px 0;
  font-size: 16px;
  font-weight: 500;
  color: #111827;
}

.option-info p {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.current-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #10b981;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.selected-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  color: #667eea;
}

.option-card.disabled {
  opacity: 0.55;
  cursor: not-allowed;
  filter: grayscale(10%);
}

.option-card.disabled:hover {
  transform: none;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
  border-color: #eef2f7;
}
</style>
