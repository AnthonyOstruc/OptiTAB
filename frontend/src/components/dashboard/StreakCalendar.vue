<template>
  <div class="streak-card">
    <div class="streak-header">
      <span class="streak-icon">🔥</span>
      <span class="streak-title">Série: {{ currentStreak }} jour{{ currentStreak > 1 ? 's' : '' }}</span>
      <span class="streak-xp">+{{ todayXP }} XP</span>
    </div>
    
    <div class="streak-progress">
      <div 
        v-for="i in 5" 
        :key="i"
        class="dot"
        :class="{ active: currentStreak >= i }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStreak } from '@/composables/useStreak'

const props = defineProps({
  statuses: { type: Array, default: () => [] }
})

const { currentStreak, todayStreakXP, initializeStreak } = useStreak()

const todayXP = computed(() => todayStreakXP.value)

onMounted(() => {
  initializeStreak()
})
</script>

<style scoped>
.streak-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
}

.streak-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.streak-icon {
  font-size: 1.5rem;
}

.streak-title {
  font-weight: 600;
  color: #374151;
}

.streak-xp {
  font-weight: 600;
  color: #059669;
}

.streak-progress {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #d1d5db;
  transition: all 0.2s;
}

.dot.active {
  background: #10b981;
}
</style>