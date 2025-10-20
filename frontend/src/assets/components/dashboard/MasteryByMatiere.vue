<template>
  <div class="mastery-card">
    <div class="mastery-header">
      <div class="mastery-title">Maîtrise par matière</div>
    </div>
    <div v-if="!items.length" class="empty">Pas encore de données</div>
    <div v-else class="mastery-list">
      <div v-for="it in itemsSorted" :key="it.id" class="mastery-row">
        <div class="left">
          <div class="name">{{ it.name }}</div>
          <div class="sub">{{ it.acquired }} / {{ it.total }} acquis</div>
        </div>
        <div class="bar">
          <div class="fill" :style="{ width: percent(it) + '%' }"></div>
        </div>
        <div class="cta">
          <button class="open-btn" @click="$emit('open-matiere', it.id)">Ouvrir</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  byMatieres: { type: Array, default: () => [] }
})

const items = computed(() => props.byMatieres || [])
const itemsSorted = computed(() => [...items.value].sort((a,b) => (b.total - a.total)))
const percent = (it) => {
  const total = Math.max(1, Number(it.total) || 0)
  const acq = Math.max(0, Number(it.acquired) || 0)
  return Math.min(100, Math.round((acq / total) * 100))
}
</script>

<style scoped>
.mastery-card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:1rem 1.25rem; box-shadow:0 2px 6px rgba(30,41,59,0.06); }
.mastery-header { display:flex; align-items:center; justify-content:space-between; }
.mastery-title { font-weight:800; color:#1f2937; }
.empty { color:#64748b; font-size:.95rem; margin-top:.5rem; }
.mastery-list { display:flex; flex-direction:column; gap:.5rem; margin-top:.5rem; }
.mastery-row { display:grid; grid-template-columns: 1fr 2fr auto; align-items:center; gap:.75rem; border:1px solid #e5e7eb; border-radius:10px; padding:.5rem .75rem; }
.left .name { font-weight:700; color:#111827; }
.left .sub { color:#64748b; font-size:.9rem; }
.bar { height:12px; background:#eef2ff; border-radius:999px; overflow:hidden; }
.fill { height:100%; background:linear-gradient(90deg,#22c55e,#16a34a); width:0; transition:width .3s ease; }
.open-btn { background:#334155; color:#fff; border:none; border-radius:8px; padding:.4rem .75rem; font-weight:700; cursor:pointer; }
.open-btn:hover { background:#1f2937; }
</style>


