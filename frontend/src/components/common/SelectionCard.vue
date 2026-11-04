<template>
  <button
    type="button"
    class="option-card"
    :class="{ selected: isSelected, current: isCurrent, disabled: isDisabled, 'option-card--pays': type === 'pays' }"
    :aria-pressed="isSelected"
    :disabled="isDisabled"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
    @focus="handleMouseEnter"
  >
    <!-- Drapeau pour un pays, pastille de couleur pour une classe -->
    <span v-if="type === 'pays'" class="flag" aria-hidden="true">{{ item.drapeau_emoji }}</span>
    <span v-else class="niveau-indicator" :style="niveauStyle" aria-hidden="true"></span>

    <span class="option-info">
      <span class="option-name">
        {{ displayName }}
        <span v-if="isCurrent" class="current-badge">Actuel</span>
      </span>
      <span v-if="displayDescription" class="option-description">{{ displayDescription }}</span>
    </span>
  </button>
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
      return 'Classes disponibles'
    }
    if (nombreNiveaux === 0) {
      return 'Aucune classe disponible'
    }
    if (nombreNiveaux === 1) {
      return '1 classe'
    }
    return `${nombreNiveaux} classes`
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
/* Tuile de choix, même style que les fenêtres (variables --om-* de components/common/Modal.vue). */
.option-card {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-height: 52px;
  padding: 10px 12px;
  border: 1.5px solid var(--om-line, #e4e8f0);
  border-radius: 14px;
  background: #fff;
  color: var(--om-ink, #121a33);
  font-family: var(--om-font, 'Montserrat', sans-serif);
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
}

.option-card:hover:not(:disabled) {
  border-color: var(--om-navy-100, #dfe6f5);
  box-shadow: 0 4px 14px rgba(16, 32, 79, 0.08);
}

.option-card.selected {
  border-color: var(--om-navy, #1b3c8e);
  background: var(--om-navy-50, #f1f4fb);
}

.option-card:focus-visible {
  outline: 2px solid var(--om-navy, #1b3c8e);
  outline-offset: 2px;
}

.option-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.flag {
  font-size: 26px;
  line-height: 1;
}

.niveau-indicator {
  width: 10px;
  height: 10px;
  flex-shrink: 0;
  border-radius: 50%;
}

.option-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.option-name {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 8px;
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
}

.option-description {
  color: var(--om-muted, #5d667d);
  font-size: 13px;
}

.current-badge {
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--om-green-50, #ecf7ec);
  color: var(--om-green-700, #2f7a3a);
  font-size: 11.5px;
  font-weight: 700;
}
</style>
