<template>
  <div class="trend-card">
    <div class="trend-header">
      <div class="trend-title">Tendance hebdomadaire</div>
    </div>
    <div v-if="!items.length" class="empty">Aucune activité récente</div>
    <div v-else class="trend-bars">
      <div v-for="d in items" :key="d.date" class="bar-item">
        <div class="bar-outer" :title="tooltip(d)">
          <div class="bar-inner" :style="{ height: heightPct(d) + '%' }"></div>
        </div>
        <div class="bar-label">{{ shortDay(d.date) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  weeklyTrend: { type: Array, default: () => [] }
})

const items = computed(() => props.weeklyTrend || [])
const maxVal = computed(() => Math.max(1, ...items.value.map(i => i.total || 0)))
const heightPct = (d) => Math.round(((d.total || 0) / maxVal.value) * 100)
const tooltip = (d) => `${d.total} exercices • ${d.correct} acquis`
function shortDay(iso) {
  const date = new Date(iso)
  return ['Di','Lu','Ma','Me','Je','Ve','Sa'][date.getDay()]
}
</script>

<style scoped>
.trend-card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:1rem 1.25rem; box-shadow:0 2px 6px rgba(30,41,59,0.06); }
.trend-header { display:flex; align-items:center; justify-content:space-between; }
.trend-title { font-weight:800; color:#1f2937; }
.empty { color:#64748b; font-size:.95rem; margin-top:.5rem; }
.trend-bars { display:grid; grid-template-columns: repeat(7, 1fr); gap:.5rem; margin-top:.5rem; }
.bar-item { display:flex; flex-direction:column; align-items:center; gap:.25rem; }
.bar-outer { width:100%; height:120px; background:#f1f5f9; border-radius:8px; display:flex; align-items:flex-end; overflow:hidden; }
.bar-inner { width:100%; background:linear-gradient(180deg,#60a5fa,#3b82f6); height:0; transition:height .4s ease; }
.bar-label { color:#64748b; font-size:.8rem; text-align:center; }
</style>


