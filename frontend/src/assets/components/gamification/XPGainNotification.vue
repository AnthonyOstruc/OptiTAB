<template>
  <transition name="xp-gain" appear>
    <div v-if="show" class="xp-gain-notification" :class="{ 'no-xp': xpGained === 0 }">
      <div class="xp-icon">
        <span v-if="xpGained > 0">🎉</span>
        <span v-else-if="attemptNumber >= 3">💡</span>
        <span v-else>⚡</span>
      </div>
      <div class="xp-content">
        <div class="xp-title">
          <span v-if="xpGained > 0">{{ xpGained }} XP gagnés !</span>
          <span v-else-if="attemptNumber >= 3">Aucun XP</span>
          <span v-else>{{ xpGained }} XP</span>
        </div>
        <div class="xp-subtitle">
          <span v-if="attemptNumber === 1 && xpGained > 0">🥇 Première tentative réussie</span>
          <span v-else-if="attemptNumber === 2 && xpGained > 0">🥈 Deuxième tentative (50% XP)</span>
          <span v-else-if="attemptNumber >= 3">🥉 Plus d'XP après la 3ème tentative</span>
          <span v-else>Continue tes efforts !</span>
        </div>
      </div>
      <div v-if="levelUp" class="level-up">
        <div class="level-up-icon">🆙</div>
        <div class="level-up-text">Niveau {{ newLevel }} !</div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  xpGained: {
    type: Number,
    default: 0
  },
  attemptNumber: {
    type: Number,
    default: 1
  },
  levelUp: {
    type: Boolean,
    default: false
  },
  newLevel: {
    type: Number,
    default: 0
  },
  duration: {
    type: Number,
    default: 4000
  }
})

const show = ref(false)

onMounted(() => {
  show.value = true
  setTimeout(() => {
    show.value = false
  }, props.duration)
})
</script>

<style scoped>
.xp-gain-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 350px;
  backdrop-filter: blur(10px);
}

.xp-gain-notification.no-xp {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  box-shadow: 0 4px 20px rgba(107, 114, 128, 0.3);
}

.xp-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.xp-content {
  flex: 1;
}

.xp-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.xp-subtitle {
  font-size: 0.875rem;
  opacity: 0.9;
  font-weight: 500;
}

.level-up {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  animation: pulse 2s infinite;
}

.level-up-icon {
  font-size: 1.5rem;
}

.level-up-text {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Animations */
.xp-gain-enter-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.xp-gain-leave-active {
  transition: all 0.3s ease-in;
}

.xp-gain-enter-from {
  transform: translateX(100%) scale(0.8);
  opacity: 0;
}

.xp-gain-leave-to {
  transform: translateX(100%) scale(0.8);
  opacity: 0;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Responsive */
@media (max-width: 640px) {
  .xp-gain-notification {
    top: 10px;
    right: 10px;
    left: 10px;
    max-width: none;
    padding: 0.875rem 1rem;
  }
  
  .xp-icon {
    font-size: 1.5rem;
  }
  
  .xp-title {
    font-size: 1rem;
  }
  
  .xp-subtitle {
    font-size: 0.8rem;
  }
}
</style>
