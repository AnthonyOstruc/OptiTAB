<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-wrapper">
      <!-- Modal Overlay -->
      <div 
        class="modal-overlay"
        @click="handleOverlayClick"
        role="presentation"
      />

      <!-- Modal Content -->
      <div 
      class="modal-content"
      :class="`modal-${size}`"
      role="dialog"
      :aria-modal="isOpen"
      :aria-labelledby="titleId"
      @click.stop
    >

        <!-- Modal Header -->
        <div v-if="showHeader" class="modal-header">
          <h2 v-if="title" :id="titleId" class="modal-title">{{ title }}</h2>
          <button 
            v-if="showCloseButton && canClose"
            class="modal-close-btn" 
            @click="handleClose"
            :aria-label="closeButtonLabel"
          >
            <CloseIcon />
          </button>
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { computed, onMounted, onUnmounted } from 'vue'
import CloseIcon from './CloseIcon.vue'

export default {
  name: 'Modal',
  components: {
    CloseIcon
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    showHeader: {
      type: Boolean,
      default: true
    },
    showCloseButton: {
      type: Boolean,
      default: true
    },
    closeButtonLabel: {
      type: String,
      default: 'Fermer'
    },
    closeOnOverlay: {
      type: Boolean,
      default: true
    },
    canClose: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large', 'full'].includes(value)
    },
    contentClass: {
      type: String,
      default: ''
    }
  },
  emits: ['close', 'overlay-click'],
  setup(props, { emit }) {
    // Computed
    const titleId = computed(() => 
      props.title ? `modal-title-${Date.now()}` : ''
    )

    // Methods
    const handleClose = () => {
      emit('close')
    }

    const handleOverlayClick = () => {
      if (props.closeOnOverlay && props.canClose) {
        emit('overlay-click')
        emit('close')
      }
    }

    // Handle Escape key
    const handleKeyDown = (event) => {
      if (event.key === 'Escape' && props.isOpen && props.canClose) {
        handleClose()
      }
    }

    // Lifecycle
    onMounted(() => {
      document.addEventListener('keydown', handleKeyDown)
    })

    onUnmounted(() => {
      document.removeEventListener('keydown', handleKeyDown)
    })

    return {
      titleId,
      handleClose,
      handleOverlayClick,
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

// Modal wrapper
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 13000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

// Modal overlay
.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

// Modal content
.modal-content {
  position: relative;
  background: $white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease;
  
  // Size variants
  &.modal-small {
    width: 90%;
    max-width: 450px;
  }
  
  &.modal-medium {
    width: 90%;
    max-width: 800px;
  }
  
  &.modal-large {
    width: 90%;
    max-width: 700px;
  }
  
  &.modal-full {
    width: 95%;
    max-width: none;
  }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

// Modal header
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 0;
  gap: 16px;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: $text-color;
  margin: 0;
  flex: 1;
}

.modal-close-btn {
  @extend .btn;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0;

  &:hover {
    background: $background-light;
  }
  
  &:focus {
    outline: 2px solid $primary-color;
    outline-offset: 2px;
  }
}

// Modal body
.modal-body {
  padding: 24px;
}

// Responsive adjustments
@media (max-width: 768px) {
  .modal-wrapper {
    padding: 10px;
  }
  
  .modal-content {
    &.modal-small,
    &.modal-medium,
    &.modal-large {
      width: 100%;
      max-width: none;
    }
  }
  
  .modal-header {
    padding: 20px 20px 0;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .modal-title {
    font-size: 20px;
  }
}
</style> 