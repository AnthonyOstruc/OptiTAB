<template>
  <div class="goal-card">
    <div class="goal-header">
      <div class="goal-title">🎯 Objectif hebdo</div>
      <div class="goal-controls">
        <button class="ctrl decrease" @click="decrease" :disabled="goal <= 1">−</button>
        <div class="value">{{ goal }}</div>
        <button class="ctrl increase" @click="increase" :disabled="goal >= 100">+</button>
      </div>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progress + '%' }" :class="progressClass"></div>
    </div>
    <div class="progress-info">
      <div class="progress-hint">{{ progressMessage }}</div>
      <div class="progress-count">{{ done }} / {{ goal }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'

const props = defineProps({
  initialGoal: { type: Number, default: 20 },
  done: { type: Number, default: 0 },
  userId: { type: [String, Number], default: null }
})

const goal = ref(props.initialGoal)

function key() {
  return `weekly_goal_${props.userId || 'me'}`
}

onMounted(() => {
  const s = localStorage.getItem(key())
  if (s) {
    const v = parseInt(s, 10)
    if (!Number.isNaN(v) && v > 0) goal.value = v
  }
})

watch(goal, (v) => {
  localStorage.setItem(key(), String(v))
})

const progress = computed(() => Math.min(100, Math.round((props.done / Math.max(1, goal.value)) * 100)))

const progressClass = computed(() => {
  if (progress.value >= 100) return 'completed'
  if (progress.value >= 75) return 'almost-done'
  if (progress.value >= 50) return 'half-way'
  return 'starting'
})

const progressMessage = computed(() => {
  const remaining = Math.max(0, goal.value - props.done)
  if (remaining === 0) return 'Objectif atteint ! 🎉'
  if (remaining === 1) return '1 exercice restant'
  return `${remaining} exercices restants`
})

function increase() { goal.value = Math.min(100, goal.value + 1) }
function decrease() { goal.value = Math.max(1, goal.value - 1) }
</script>

<style scoped>
.goal-card { 
  background: #fff; 
  border: 1px solid #e5e7eb; 
  border-radius: 12px; 
  padding: 1rem 1.25rem; 
  box-shadow: 0 2px 6px rgba(30,41,59,0.06);
  min-width: 280px;
}

.goal-header { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  margin-bottom: 0.75rem;
}

.goal-title { 
  font-weight: 800; 
  color: #1f2937; 
  font-size: 1rem;
}

.goal-controls { 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
}

.ctrl { 
  background: #f1f5f9; 
  color: #334155; 
  border: none; 
  border-radius: 8px; 
  padding: 0.375rem 0.625rem; 
  cursor: pointer; 
  font-weight: 800; 
  font-size: 1.1rem;
  transition: all 0.2s;
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ctrl:hover:not(:disabled) { 
  background: #e2e8f0; 
  transform: scale(1.05);
}

.ctrl:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.ctrl.decrease:hover:not(:disabled) {
  background: #fee2e2;
  color: #dc2626;
}

.ctrl.increase:hover:not(:disabled) {
  background: #dcfce7;
  color: #16a34a;
}

.value { 
  min-width: 2.5rem; 
  text-align: center; 
  font-weight: 800; 
  color: #1f2937; 
  font-size: 1.1rem;
}

.progress-bar { 
  height: 12px; 
  background: #f1f5f9; 
  border-radius: 999px; 
  overflow: hidden; 
  margin: 0.5rem 0;
}

.progress-fill { 
  height: 100%; 
  border-radius: 999px; 
  transition: all 0.3s ease;
}

.progress-fill.starting {
  background: linear-gradient(90deg, #f59e0b, #f97316);
}

.progress-fill.half-way {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.progress-fill.almost-done {
  background: linear-gradient(90deg, #8b5cf6, #7c3aed);
}

.progress-fill.completed {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.progress-hint {
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
}

.progress-count {
  color: #1f2937;
  font-weight: 700;
  font-size: 0.9rem;
}
</style>

