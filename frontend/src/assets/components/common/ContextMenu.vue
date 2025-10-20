<template>
  <div 
    v-show="visible" 
    class="context-menu"
    :style="menuStyle"
    @click.stop
  >
    <div class="context-menu-item" @click="handleFavoriteToggle">
      <span class="context-menu-icon">
        {{ isFavorite ? '⭐' : '☆' }}
      </span>
      <span class="context-menu-text">
        {{ isFavorite ? 'Retirer des favoris' : 'Ajouter aux favoris' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  },
  isFavorite: {
    type: Boolean,
    default: false
  },
  matiereId: {
    type: [Number, String, null],
    default: null
  }
})

const emit = defineEmits(['favorite-toggle', 'close'])

const menuStyle = computed(() => ({
  position: 'fixed',
  left: `${props.x}px`,
  top: `${props.y}px`,
  zIndex: 12006
}))

function handleFavoriteToggle() {
  if (props.matiereId !== null) {
    emit('favorite-toggle', props.matiereId)
  }
  emit('close')
}

// Fermer le menu si on clique ailleurs
function handleClickOutside(event) {
  if (props.visible) {
    emit('close')
  }
}

// Fermer le menu avec la touche Escape
function handleKeydown(event) {
  if (event.key === 'Escape' && props.visible) {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.context-menu {
  position: fixed;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 10000;
  min-width: 180px;
  padding: 4px 0;
  font-size: 14px;
  color: #374151;
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.15s ease;
  user-select: none;
}

.context-menu-item:hover {
  background-color: #f3f4f6;
}

.context-menu-icon {
  font-size: 16px;
  width: 16px;
  text-align: center;
}

.context-menu-text {
  flex: 1;
  white-space: nowrap;
}
</style> 