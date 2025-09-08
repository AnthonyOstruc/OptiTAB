<template>
  <Teleport to="body">
    <Transition name="unlock-notification">
      <div v-if="show" class="unlock-notification-overlay">
        <div class="unlock-notification-card">
          <div class="unlock-notification-content">
            <div class="unlock-icon">🔓</div>
            <div class="unlock-message">
              <h3>Nouvel objectif débloqué !</h3>
              <p>{{ message }}</p>
            </div>
            <div class="unlock-objective-icon">{{ objectiveIcon }}</div>
          </div>
          <div class="unlock-progress-bar">
            <div class="unlock-progress-fill" :style="{ width: '100%' }"></div>
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
const objectiveIcon = ref('')

const showNotification = (data) => {
  message.value = `"${data.objective.name}" est maintenant disponible !`
  objectiveIcon.value = data.objective.icon || '🎯'
  show.value = true
  
  // Auto-hide après 3 secondes
  setTimeout(() => {
    show.value = false
  }, 3000)
}

const handleObjectiveUnlocked = (event) => {
  showNotification(event.detail)
}

onMounted(() => {
  window.addEventListener('objectiveUnlocked', handleObjectiveUnlocked)
})

onUnmounted(() => {
  window.removeEventListener('objectiveUnlocked', handleObjectiveUnlocked)
})
</script>

<style scoped>
.unlock-notification-overlay {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 9999;
  pointer-events: none;
}

.unlock-notification-card {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
  min-width: 300px;
  max-width: 400px;
  position: relative;
  overflow: hidden;
}

.unlock-notification-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.unlock-icon {
  font-size: 2rem;
  animation: unlock 1s ease-in-out;
}

.unlock-message {
  flex: 1;
}

.unlock-message h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 700;
}

.unlock-message p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.unlock-objective-icon {
  font-size: 2rem;
  animation: bounce 1s ease-in-out;
}

.unlock-progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
}

.unlock-progress-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.6);
  animation: progress 3s linear forwards;
}

/* Animations */
@keyframes unlock {
  0%, 20%, 50%, 80%, 100% {
    transform: rotate(0deg);
  }
  40% {
    transform: rotate(-10deg);
  }
  60% {
    transform: rotate(10deg);
  }
}

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

@keyframes progress {
  0% {
    width: 100%;
  }
  100% {
    width: 0%;
  }
}

/* Transition */
.unlock-notification-enter-active {
  transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.unlock-notification-leave-active {
  transition: all 0.3s ease-in;
}

.unlock-notification-enter-from {
  transform: translateX(-100%) scale(0.8);
  opacity: 0;
}

.unlock-notification-leave-to {
  transform: translateX(-100%) scale(0.8);
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .unlock-notification-overlay {
    top: 10px;
    left: 10px;
    right: 10px;
  }
  
  .unlock-notification-card {
    min-width: auto;
    max-width: none;
  }
  
  .unlock-notification-content {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
}
</style>
