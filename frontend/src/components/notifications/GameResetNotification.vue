<template>
  <transition name="notification" appear>
    <div v-if="show" class="game-reset-notification">
      <div class="notification-icon">
        <span>🎮</span>
      </div>
      <div class="notification-content">
        <div class="notification-title">
          Système de gamification mis à jour !
        </div>
        <div class="notification-message">
          <p>🎯 <strong>Nouveau :</strong> Seuls les <strong>quiz</strong> donnent maintenant des XP</p>
          <p>📚 Les exercices guidés restent éducatifs (0 XP)</p>
          <p>🏆 Tous les compteurs ont été remis à zéro pour un restart équitable</p>
        </div>
      </div>
      <button @click="dismiss" class="notification-close">
        ✕
      </button>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  autoHide: {
    type: Number,
    default: 8000 // 8 secondes
  }
})

const show = ref(false)

function dismiss() {
  show.value = false
  // Marquer comme vu dans localStorage
  localStorage.setItem('game-reset-notification-seen', 'true')
}

onMounted(() => {
  // Vérifier si déjà vu
  const alreadySeen = localStorage.getItem('game-reset-notification-seen')
  if (!alreadySeen) {
    show.value = true
    
    // Auto-hide après le délai
    if (props.autoHide > 0) {
      setTimeout(() => {
        if (show.value) {
          dismiss()
        }
      }, props.autoHide)
    }
  }
})
</script>

<style scoped>
.game-reset-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  max-width: 420px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.notification-icon {
  font-size: 2rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #ffffff;
}

.notification-message p {
  margin: 0.5rem 0;
  font-size: 0.875rem;
  line-height: 1.4;
  opacity: 0.95;
}

.notification-message strong {
  color: #fbbf24;
  font-weight: 600;
}

.notification-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.notification-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Animations */
.notification-enter-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.notification-leave-active {
  transition: all 0.3s ease-in;
}

.notification-enter-from {
  transform: translateX(100%) scale(0.8);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(100%) scale(0.8);
  opacity: 0;
}

/* Responsive */
@media (max-width: 640px) {
  .game-reset-notification {
    top: 10px;
    right: 10px;
    left: 10px;
    max-width: none;
    padding: 1.25rem;
  }
  
  .notification-icon {
    font-size: 1.75rem;
  }
  
  .notification-title {
    font-size: 1rem;
  }
  
  .notification-message p {
    font-size: 0.8rem;
  }
}
</style>
