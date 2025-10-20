<template>
  <div v-if="show" class="xp-notification-overlay">
    <div class="xp-notification" :class="{ 'no-xp': xp === 0 }">
      <div class="xp-content">
        <span class="xp-icon">{{ xp > 0 ? '🎉' : '💡' }}</span>
        <div class="xp-details">
          <span class="xp-text">{{ xp > 0 ? `+${xp} XP` : '0 XP' }}</span>
          <span class="xp-message">{{ message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  xp: {
    type: Number,
    default: 0
  },
  message: {
    type: String,
    default: 'Exercice terminé !'
  },
  duration: {
    type: Number,
    default: 3000
  }
})

const emit = defineEmits(['hide'])

// Auto-hide after duration
watch(() => props.show, (newShow) => {
  if (newShow && props.duration > 0) {
    setTimeout(() => {
      emit('hide')
    }, props.duration)
  }
})
</script>

<style scoped>
.xp-notification-overlay {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  pointer-events: none;
}

.xp-notification {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border: 2px solid #22c55e;
  border-radius: 12px;
  padding: 16px 20px;
  min-width: 200px;
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
  animation: slideInRight 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  pointer-events: auto;
}

.xp-notification.no-xp {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-color: #64748b;
  box-shadow: 0 10px 25px rgba(100, 116, 139, 0.2);
}

.xp-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.xp-icon {
  font-size: 2rem;
  flex-shrink: 0;
  animation: bounce 1.5s infinite;
}

.xp-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.xp-text {
  font-size: 1.25rem;
  font-weight: 800;
  color: #15803d;
  line-height: 1;
}

.xp-notification.no-xp .xp-text {
  color: #475569;
}

.xp-message {
  font-size: 0.875rem;
  font-weight: 600;
  color: #16a34a;
  line-height: 1;
}

.xp-notification.no-xp .xp-message {
  color: #64748b;
}

@keyframes slideInRight {
  0% {
    transform: translateX(100%) scale(0.8);
    opacity: 0;
  }
  50% {
    transform: translateX(-10px) scale(1.05);
    opacity: 1;
  }
  100% {
    transform: translateX(0) scale(1);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-4px);
  }
  60% {
    transform: translateY(-2px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .xp-notification-overlay {
    top: 10px;
    right: 10px;
    left: 10px;
  }
  
  .xp-notification {
    width: 100%;
    min-width: auto;
    padding: 12px 16px;
  }
  
  .xp-icon {
    font-size: 1.5rem;
  }
  
  .xp-text {
    font-size: 1.125rem;
  }
  
  .xp-message {
    font-size: 0.8rem;
  }
}
</style>
