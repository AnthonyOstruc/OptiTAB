<template>
  <div class="toast-container">
    <TransitionGroup name="toast" tag="div" class="toasts">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="toast.type"
        @click="removeToast(toast.id)"
      >
        <div class="toast-content">
          <span class="toast-message">{{ toast.message }}</span>
          <button class="toast-close" @click.stop="removeToast(toast.id)">
            ×
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast'

export default {
  name: 'Toast',
  setup() {
    const { toasts, removeToast } = useToast()
    
    return {
      toasts,
      removeToast
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9999;
  pointer-events: none;
}

.toasts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  pointer-events: auto;
}

.toast {
  min-width: 300px;
  max-width: 400px;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  border-left: 4px solid;
}

.toast:hover {
  transform: translateX(-4px);
}

.toast.success {
  border-left-color: #10b981;
  background: #f0fdf4;
}

.toast.error {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.toast.warning {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.toast.info {
  border-left-color: #3b82f6;
  background: #eff6ff;
}

.toast-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.toast-message {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  font-weight: bold;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-close:hover {
  opacity: 1;
}

/* Transition animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}

@media (max-width: 768px) {
  .toast-container {
    top: 0.5rem;
    right: 0.5rem;
    left: 0.5rem;
  }
  
  .toast {
    min-width: auto;
    max-width: none;
  }
}
</style> 