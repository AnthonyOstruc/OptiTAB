<template>
  <div class="reco-card">
    <div class="reco-header">
      <div class="reco-title">Prochaines étapes recommandées</div>
      <button class="refresh-btn" @click="load">↻</button>
    </div>
    <div v-if="loading" class="loading">Chargement…</div>
    <div v-else-if="!items.length" class="empty">Aucune recommandation pour le moment</div>
    <div v-else class="reco-grid">
      <div v-for="(it, idx) in items" :key="idx" class="reco-item">
        <div class="reco-type" :class="it.type">{{ labelMap[it.type] || 'Action' }}</div>
        <div class="reco-title-item">{{ it.title }}</div>
        <div class="reco-meta">{{ it.chapitre_title }}</div>
        <button class="reco-btn" @click="open(it)">Commencer</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchRecommendations } from '@/api/users'

const router = useRouter()
const loading = ref(false)
const items = ref([])

const labelMap = {
  review: 'Révision ciblée',
  new_exercice: 'Nouveau défi',
  quick_quiz: 'Quiz rapide'
}

async function load() {
  loading.value = true
  try {
    const { data } = await fetchRecommendations()
    items.value = data?.data?.recommendations || []
  } catch (e) {
    items.value = []
  } finally {
    loading.value = false
  }
}

function open(it) {
  if (it.chapitre_id) {
    router.push({ name: 'Exercices', params: { chapitreId: String(it.chapitre_id) } })
  }
}

onMounted(load)
</script>

<style scoped>
.reco-card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:1rem 1.25rem; box-shadow:0 2px 6px rgba(30,41,59,0.06); }
.reco-header { display:flex; align-items:center; justify-content:space-between; }
.reco-title { font-weight:800; color:#1f2937; }
.refresh-btn { border:none; background:#f1f5f9; color:#334155; border-radius:8px; padding:.35rem .55rem; cursor:pointer; }
.loading, .empty { color:#64748b; font-size:.95rem; margin-top:.5rem; }
.reco-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:.75rem; margin-top:.5rem; }
.reco-item { border:1px solid #e5e7eb; border-radius:10px; padding:.75rem; display:flex; flex-direction:column; gap:.35rem; }
.reco-type { font-size:.8rem; font-weight:700; color:#2563eb; }
.reco-type.review { color:#9333ea; }
.reco-type.new_exercice { color:#0ea5e9; }
.reco-type.quick_quiz { color:#f59e0b; }
.reco-title-item { font-weight:700; color:#111827; }
.reco-meta { color:#64748b; font-size:.9rem; }
.reco-btn { align-self:flex-start; margin-top:.35rem; background:#2563eb; color:#fff; border:none; border-radius:8px; padding:.4rem .75rem; font-weight:700; cursor:pointer; }
.reco-btn:hover { background:#1e40af; }
</style>


