<template>
  <div class="wb" role="img" :aria-label="resume">
    <div v-for="jour in jours" :key="jour.date" :class="['wb__day', { 'is-today': jour.today }]">
      <span class="wb__count" aria-hidden="true">{{ jour.total || '' }}</span>
      <span class="wb__track" aria-hidden="true">
        <span class="wb__fill" :style="{ height: jour.hauteur + '%' }"></span>
      </span>
      <span class="wb__label" aria-hidden="true">{{ jour.label }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // [{ date: 'AAAA-MM-JJ', total, correct }] sur 7 jours, du plus ancien au plus récent
  trend: { type: Array, default: () => [] }
})

const LETTRES = ['D', 'L', 'M', 'M', 'J', 'V', 'S']

const jours = computed(() => {
  const max = Math.max(4, ...props.trend.map((d) => d.total || 0))
  const today = new Date().toISOString().slice(0, 10)
  return props.trend.map((d) => ({
    date: d.date,
    total: d.total || 0,
    today: d.date === today,
    label: LETTRES[new Date(`${d.date}T12:00:00`).getDay()],
    hauteur: d.total ? Math.max(10, Math.round((d.total / max) * 100)) : 0
  }))
})

const resume = computed(() => {
  const actifs = jours.value.filter((j) => j.total > 0).length
  const total = jours.value.reduce((s, j) => s + j.total, 0)
  return `${total} exercices sur les 7 derniers jours, ${actifs} jours actifs`
})
</script>

<style scoped>
.wb {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 6px;
  align-items: end;
}

.wb__day {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.wb__count {
  min-height: 15px;
  font-size: 11px;
  font-weight: 700;
  color: var(--es-muted);
}

.wb__track {
  position: relative;
  display: block;
  width: 100%;
  max-width: 26px;
  height: 64px;
  overflow: hidden;
  border-radius: 8px;
  background: var(--es-navy-50);
}

.wb__fill {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  border-radius: 8px;
  background: var(--es-navy);
  opacity: 0.75;
  transition: height 0.4s ease;
}

.wb__label {
  font-size: 12px;
  font-weight: 600;
  color: var(--es-muted);
}

.wb__day.is-today .wb__fill {
  background: var(--es-green);
  opacity: 1;
}

.wb__day.is-today .wb__label {
  color: var(--es-ink);
  font-weight: 700;
}
</style>
