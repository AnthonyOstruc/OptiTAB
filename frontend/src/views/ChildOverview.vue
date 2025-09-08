<template>
  <div class="child-overview">
    <div class="header">
      <button class="back" @click="goBack">← Retour</button>
      <div class="title">
        <h1>Détail de l'élève</h1>
        <p class="subtitle" v-if="child.display_name">
          {{ child.display_name }}
          <span v-if="child.pays_flag" class="flag">{{ child.pays_flag }}</span>
          <span v-if="child.niveau" class="niveau">• {{ child.niveau }}</span>
        </p>
      </div>
    </div>

    <div v-if="loading" class="loading"><span class="spinner"></span></div>

    <div v-else>
      <div class="kpis">
        <div class="kpi">
          <div class="label">XP</div>
          <div class="value primary">{{ child.xp }}</div>
          <div class="hint">Niveau {{ child.level }}</div>
        </div>
        <div class="kpi">
          <div class="label">Exercices réalisés</div>
          <div class="value">{{ metrics.done_total }}</div>
        </div>
        <div class="kpi">
          <div class="label">Acquis</div>
          <div class="value ok">{{ metrics.acquired_count }}</div>
        </div>
        <div class="kpi">
          <div class="label">À revoir</div>
          <div class="value ko">{{ metrics.not_acquired_count }}</div>
        </div>
      </div>

      <div class="cards-grid">
        <div class="card">
          <div class="card-header">
            <h3>Objectif hebdomadaire</h3>
            <div class="meta">{{ metrics.weekly_done }} / {{ metrics.weekly_goal }}</div>
          </div>
          <div class="progress-bar"><div class="fill" :style="{ width: metrics.weekly_progress + '%' }"></div></div>
          <div class="progress-hint">{{ weeklyMessage }}</div>
        </div>

        <div class="card">
          <div class="card-header"><h3>Tendance 7 jours</h3></div>
          <div class="trend">
            <div v-for="d in weekly_trend" :key="d.date" class="bar-col">
              <div class="bar-bg">
                <div class="bar-ok" :style="{ height: barHeight(d.correct) }"></div>
                <div class="bar-total" :style="{ height: barHeight(d.total) }"></div>
              </div>
              <div class="bar-label">{{ formatDay(d.date) }}</div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header"><h3>Activité récente</h3></div>
          <ul v-if="last_activities.length" class="activity">
            <li v-for="a in last_activities" :key="a.id" class="activity-item">
              <span class="status" :class="{ ok: a.est_correct, ko: !a.est_correct }">{{ a.est_correct ? '✅' : '❌' }}</span>
              <span class="text">{{ a.exercice_title }}</span>
              <span class="meta">• {{ a.chapitre_title || 'Chapitre' }} <span v-if="a.matiere">• {{ a.matiere }}</span></span>
              <span class="when">{{ humanizeDate(a.when) }}</span>
            </li>
          </ul>
          <div v-else class="empty">Aucune activité pour le moment.</div>
        </div>

        <div class="card">
          <div class="card-header"><h3>Matières à travailler</h3></div>
          <div v-if="by_matieres.length" class="matieres">
            <div class="matiere" v-for="m in by_matieres" :key="m.id">
              <div class="matiere-name">{{ m.name }}</div>
              <div class="matiere-stats">
                <span class="badge total">{{ m.total }} exos</span>
                <span class="badge ok">{{ m.acquired }} acquis</span>
                <span class="badge ko">{{ m.to_review }} à revoir</span>
              </div>
            </div>
          </div>
          <div v-else class="empty">Pas encore de répartition par matière.</div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/client'

const route = useRoute()
const router = useRouter()
const childId = route.params.childId

const loading = ref(true)
const child = ref({})
const metrics = ref({})
const weekly_trend = ref([])
const last_activities = ref([])
const by_matieres = ref([])

function goBack() {
  router.back()
}

function formatDay(isoDate) {
  const d = new Date(isoDate)
  return d.toLocaleDateString(undefined, { weekday: 'short' })
}

function barHeight(value) {
  const v = Math.min(8, Math.max(0, Number(value || 0)))
  return (v * 10) + 'px'
}

function humanizeDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const diffMs = Date.now() - d.getTime()
  const minutes = Math.floor(diffMs / 60000)
  if (minutes < 1) return "à l'instant"
  if (minutes < 60) return `il y a ${minutes} min`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `il y a ${hours} h`
  const days = Math.floor(hours / 24)
  if (days < 7) return `il y a ${days} j`
  return d.toLocaleDateString()
}

const weeklyMessage = computed(() => {
  const d = metrics.value?.weekly_done || 0
  const g = metrics.value?.weekly_goal || 20
  const r = Math.max(0, g - d)
  return r === 0 ? 'Objectif atteint 🎯' : `${r} exercice(s) restants cette semaine`
})

onMounted(async () => {
  try {
    const res = await apiClient.get(`/api/users/children/${childId}/overview/`)
    const data = res?.data?.data || {}
    child.value = data.child || {}
    metrics.value = data.metrics || {}
    weekly_trend.value = data.weekly_trend || []
    last_activities.value = data.last_activities || []
    by_matieres.value = data.by_matieres || []
  } catch (e) {
    child.value = {}
    metrics.value = {}
    weekly_trend.value = []
    last_activities.value = []
    by_matieres.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.child-overview { margin-bottom: 1.25rem; }
.header { display:flex; align-items:center; gap:.75rem; margin: 1rem 0 .75rem; }
.back { background:#f1f5f9; color:#0f172a; border:1px solid #e2e8f0; padding:.4rem .6rem; border-radius:8px; cursor:pointer; }
.title h1 { margin:0; font-size:1.25rem; font-weight:800; color:#1f2937; }
.subtitle { margin:.2rem 0 0; color:#64748b; }
.flag { margin-left:.35rem; }
.niveau { color:#94a3b8; }

.loading { display:flex; align-items:center; justify-content:center; height:80px; }
.spinner { width:36px; height:36px; border:4px solid #e5e7eb; border-top:4px solid #2563eb; border-radius:50%; animation:spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.kpis { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:.75rem; margin-top:.75rem; }
.kpi { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:.75rem 1rem; box-shadow:0 2px 6px rgba(30,41,59,.06); }
.kpi .label { color:#475569; font-weight:700; }
.kpi .value { font-size:1.6rem; font-weight:800; color:#0f172a; }
.kpi .value.primary { color:#2563eb; }
.kpi .value.ok { color:#16a34a; }
.kpi .value.ko { color:#dc2626; }
.kpi .hint { color:#64748b; font-weight:700; font-size:.9rem; }

.cards-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:.9rem; margin-top:.9rem; }
.card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding: .9rem 1rem; box-shadow:0 2px 6px rgba(30,41,59,.06); }
.card-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:.4rem; }
.card-header h3 { margin:0; font-size:1.05rem; font-weight:800; color:#1f2937; }
.meta { color:#2563eb; font-weight:700; }

.progress-bar { height:10px; background:#eef2ff; border-radius:999px; overflow:hidden; margin-top:.4rem; }
.progress-bar .fill { height:100%; background:#10b981; width:0; transition: width .3s ease; }
.progress-hint { color:#64748b; font-size:.9rem; margin-top:.35rem; }

.trend { display:grid; grid-template-columns: repeat(7, 1fr); gap:.6rem; align-items:end; margin-top:.25rem; }
.bar-col { text-align:center; }
.bar-bg { position:relative; height:80px; background:linear-gradient(to top, #f8fafc, #eef2ff); border-radius:8px; overflow:hidden; border:1px solid #e5e7eb; }
.bar-total { position:absolute; bottom:0; left:0; right:0; background:#93c5fd; opacity:.6; }
.bar-ok { position:absolute; bottom:0; left:0; right:0; background:#34d399; }
.bar-label { color:#94a3b8; font-size:.85rem; margin-top:.25rem; }

.activity { list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:.5rem; }
.activity-item { display:flex; align-items:center; gap:.5rem; padding:.5rem .75rem; border:1px solid #e5e7eb; border-radius:10px; }
.status.ok { color:#16a34a; }
.status.ko { color:#dc2626; }
.text { font-weight:600; color:#111827; }
.when { margin-left:auto; color:#94a3b8; font-size:.85rem; }

.matieres { display:grid; gap:.5rem; }
.matiere { display:flex; align-items:center; justify-content:space-between; border:1px solid #e5e7eb; border-radius:10px; padding:.5rem .75rem; }
.matiere-name { font-weight:700; color:#0f172a; }
.badge { background:#f1f5f9; color:#334155; border:1px solid #e2e8f0; border-radius:999px; padding:.2rem .5rem; font-size:.8rem; }
.badge.ok { background:#ecfdf5; color:#065f46; border-color:#a7f3d0; }
.badge.ko { background:#fef2f2; color:#991b1b; border-color:#fecaca; }

@media (max-width: 600px) {
  .cards-grid { grid-template-columns: 1fr; }
}
</style>


