<template>
  <Teleport to="body">
    <Transition name="notification">
      <div v-if="show" class="xp-notification-overlay">
        <div class="xp-notification-card">
          <div class="xp-notification-content">
            <div class="xp-icon">🎉</div>
            <div class="xp-message">
              <h3>Défi complété !</h3>
              <p>{{ message }}</p>
            </div>
            <div class="xp-reward">
              <span class="xp-amount">+{{ xpAmount }} XP</span>
            </div>
          </div>
          <div class="xp-progress-bar">
            <div class="xp-progress-fill" :style="{ width: '100%' }"></div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const show = ref(false)
const message = ref('')
const xpAmount = ref(0)

const showNotification = (data) => {
  message.value = `Objectif "${getObjectiveLabel(data.objectiveType)}" terminé !`
  xpAmount.value = data.xpAmount
  show.value = true
  
  // Auto-hide après 4 secondes
  setTimeout(() => {
    show.value = false
  }, 4000)
}

const getObjectiveLabel = (objectiveType) => {
  const labels = {
    'quiz_easy': 'Quiz simples',
    'quiz_medium': 'Quiz moyens',
    'quiz_hard': 'Quiz difficiles',
    'quiz_perfect': 'Quiz parfaits',
    'quiz_streak': 'Série de quiz'
  }
  return labels[objectiveType] || 'Objectif'
}

const handleObjectiveCompleted = (event) => {
  showNotification(event.detail)
}

onMounted(() => {
  window.addEventListener('dailyObjectiveCompleted', handleObjectiveCompleted)
})

onUnmounted(() => {
  window.removeEventListener('dailyObjectiveCompleted', handleObjectiveCompleted)
})
</script>

<style scoped>
.xp-notification-overlay {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: none;
}

.xp-notification-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  min-width: 300px;
  max-width: 400px;
  position: relative;
  overflow: hidden;
}

.xp-notification-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.xp-icon {
  font-size: 2.5rem;
  animation: bounce 1s ease-in-out;
}

.xp-message {
  flex: 1;
}

.xp-message h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.xp-message p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.xp-reward {
  text-align: center;
}

.xp-amount {
  font-size: 1.5rem;
  font-weight: 800;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: inline-block;
  animation: pulse 2s infinite;
}

.xp-progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
}

.xp-progress-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.6);
  animation: progress 4s linear forwards;
}

/* Animations */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes progress {
  0% {
    width: 100%;
  }
  100% {
    width: 0%;
  }
}

/* Transition */
.notification-enter-active {
  transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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
@media (max-width: 768px) {
  .xp-notification-overlay {
    top: 10px;
    right: 10px;
    left: 10px;
  }
  
  .xp-notification-card {
    min-width: auto;
    max-width: none;
  }
  
  .xp-notification-content {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .xp-message {
    order: 1;
  }
  
  .xp-icon {
    order: 0;
  }
  
  .xp-reward {
    order: 2;
  }
}
</style>
