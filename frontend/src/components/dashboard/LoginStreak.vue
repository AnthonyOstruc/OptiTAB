<template>
  <div class="streak-card" :title="'Connexion quotidienne: 1→5 XP selon la série'">
    <div class="streak-top">
      <div class="streak-header">
        <span class="streak-icon">🔥</span>
        <span class="streak-title">Streak</span>
      </div>
      <div class="xp-pill">+{{ todayReward }} XP</div>
    </div>

    <div class="streak-main">
      <div class="streak-value">
        {{ streakCount }}
        <span class="streak-unit">{{ dayLabel }}</span>
      </div>
      <div class="streak-steps" aria-hidden="true">
        <span v-for="n in 5" :key="n" class="step" :class="{ filled: n <= filledSteps }"></span>
      </div>
      <div class="streak-hint">Revenez demain pour <b>+{{ tomorrowReward }}</b> XP</div>
      <div class="streak-note">1 à 5 XP / jour selon la série</div>
    </div>
  </div>
  
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const streakCount = computed(() => Number(userStore.loginStreakCount || 0))
const filledSteps = computed(() => Math.min(streakCount.value, 5))
const todayReward = computed(() => Math.min(Math.max(streakCount.value, 1), 5))
const tomorrowReward = computed(() => Math.min(streakCount.value + 1, 5))
const dayLabel = computed(() => (streakCount.value > 1 ? 'jours' : 'jour'))
</script>

<style scoped>
.streak-card {
  position: relative;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1rem 1rem 0.9rem 1rem;
  box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
  overflow: hidden;
}
.streak-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background: linear-gradient(180deg, #fb923c, #ef4444);
}

.streak-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.streak-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.streak-icon { font-size: 1.15rem; }
.streak-title { font-weight: 800; color: #0f172a; font-size: 0.98rem; }
.xp-pill {
  background: linear-gradient(135deg, #f97316, #ef4444);
  color: #fff;
  font-weight: 700;
  font-size: 0.78rem;
  padding: 0.25rem 0.55rem;
  border-radius: 999px;
  box-shadow: 0 4px 10px rgba(239, 68, 68, 0.25);
}

.streak-main { margin-top: 0.5rem; }
.streak-value { font-size: 1.6rem; font-weight: 900; color: #ef4444; line-height: 1.2; }
.streak-unit { font-size: 0.92rem; font-weight: 700; color: #475569; margin-left: 0.35rem; }

.streak-steps {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.4rem;
  margin: 0.45rem 0 0.2rem 0;
}
.step {
  height: 6px;
  border-radius: 999px;
  background: #f1f5f9;
  transition: all 0.3s ease;
}
.step.filled {
  background: linear-gradient(90deg, #fb923c, #ef4444);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.25);
}

.streak-hint { font-size: 0.78rem; color: #475569; margin-top: 0.25rem; }
.streak-hint b { color: #0f172a; }
.streak-note { font-size: 0.72rem; color: #64748b; margin-top: 0.15rem; }

@media (max-width: 640px) {
  .streak-value { font-size: 1.4rem; }
  .streak-title { font-size: 0.92rem; }
  .xp-pill { font-size: 0.72rem; }
}
</style>
