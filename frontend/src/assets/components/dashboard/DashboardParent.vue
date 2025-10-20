<template>
  <div class="parent-dashboard">
    <div class="header">
      <h1>Tableau de bord Parent</h1>
      <p class="subtitle">Suivez la progression de vos enfants, simplement.</p>
    </div>

    <div class="add-child">
      <input v-model="newChildEmail" type="email" placeholder="Email de l'élève" class="input" />
      <button class="btn" :disabled="adding" @click="handleAddChild">Ajouter</button>
      <span v-if="addMessage" class="hint">{{ addMessage }}</span>
    </div>

    <div class="create-child">
      <details>
        <summary>Créer un compte pour un enfant</summary>
        <div class="form-row">
          <input v-model="create.first_name" class="input" placeholder="Prénom" />
          <input v-model="create.last_name" class="input" placeholder="Nom" />
        </div>
        <div class="form-row">
          <input v-model="create.email" class="input" placeholder="Email" />
        </div>
        <button class="btn" :disabled="creating" @click="handleCreateChild">Créer le compte</button>
        <div v-if="createMessage" class="hint">{{ createMessage }}</div>
        <div v-if="tempPassword" class="temp-pass">Mot de passe temporaire: <code>{{ tempPassword }}</code></div>
      </details>
    </div>

    <div v-if="loading" class="loading">
      <span class="spinner"></span>
    </div>

    <div v-else>
      <div v-if="children.length === 0" class="empty">
        <p>Aucun enfant rattaché pour le moment.</p>
      </div>

      <div class="children-grid" v-else>
        <div class="child-card" v-for="c in children" :key="c.id">
          <div class="child-header">
            <div class="avatar">{{ initials(c.display_name) }}</div>
            <div class="child-info">
              <div class="name">
                <span v-if="c.pays_flag" class="flag">{{ c.pays_flag }}</span>
                {{ c.display_name }}
              </div>
              <div class="meta">
                <span v-if="c.niveau">{{ c.niveau }}</span>
              </div>
            </div>
            <div class="xp">
              <div class="xp-value">{{ c.xp }} XP</div>
              <div class="level">Niveau {{ c.level }}</div>
            </div>
          </div>

          <div class="child-body">
            <div class="metrics-grid">
              <div class="metric">
                <div class="label">Objectif hebdo</div>
                <div class="bar">
                  <div class="fill" :style="{ width: (c.metrics?.weekly_progress || 0) + '%' }"></div>
                </div>
                <div class="hint">{{ c.metrics ? (c.metrics.weekly_done + ' / ' + c.metrics.weekly_goal) : '—' }}</div>
              </div>
              <div class="metric small">
                <div class="kpi">{{ c.metrics?.done_total ?? '—' }}</div>
                <div class="kpi-label">Exercices</div>
              </div>
              <div class="metric small ok">
                <div class="kpi">{{ c.metrics?.acquired_count ?? '—' }}</div>
                <div class="kpi-label">Acquis</div>
              </div>
              <div class="metric small ko">
                <div class="kpi">{{ c.metrics?.not_acquired_count ?? '—' }}</div>
                <div class="kpi-label">À revoir</div>
              </div>
            </div>
            <div class="last-activity" v-if="c.last_activity">
              <div class="label">Dernière activité</div>
              <div class="activity-line">
                <span class="activity-title">{{ c.last_activity.exercice_title }}</span>
                <span class="activity-meta" v-if="c.last_activity.chapitre_title">• {{ c.last_activity.chapitre_title }}</span>
              </div>
            </div>
            <div class="actions">
              <button class="btn" @click="openChild(c.id)">Voir détails</button>
              <button class="btn secondary" @click="handleRemoveChild(c.id)" :disabled="removingId === c.id">Retirer</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchMyChildren, addChild, removeChild } from '@/api/users'
import apiClient from '@/api/client'

const loading = ref(true)
const children = ref([])
const router = useRouter()
const newChildEmail = ref('')
const adding = ref(false)
const addMessage = ref('')
const removingId = ref(null)
const creating = ref(false)
const createMessage = ref('')
const tempPassword = ref('')
const create = ref({ first_name: '', last_name: '', email: '' })

function initials(name) {
  if (!name) return 'E'
  const parts = String(name).trim().split(/\s+/)
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase()
  return (parts[0].substring(0, 1) + parts[1].substring(0, 1)).toUpperCase()
}

function weeklyProgress(child) {
  // Placeholder MVP: sans stats par enfant, afficher une progression symbolique selon le niveau
  const lvl = child?.level || 0
  return Math.min(100, (lvl % 10) * 10)
}

function weeklyHint(child) {
  const progress = weeklyProgress(child)
  return progress >= 100 ? 'Objectif atteint 🎯' : `Progression: ${progress}%`
}

function openChild(childId) {
  router.push({ name: 'ChildOverview', params: { childId: String(childId) } })
}

onMounted(async () => {
  try {
    const res = await fetchMyChildren()
    const data = res?.data?.data || {}
    children.value = data.children || []
  } catch (e) {
    children.value = []
  } finally {
    loading.value = false
  }
})

async function refreshChildren() {
  try {
    const res = await fetchMyChildren()
    const data = res?.data?.data || {}
    children.value = data.children || []
  } catch {
    children.value = []
  }
}

async function handleAddChild() {
  addMessage.value = ''
  const email = String(newChildEmail.value || '').trim()
  if (!email) {
    addMessage.value = "Renseignez l'email de l'élève"
    return
  }
  adding.value = true
  try {
    await addChild({ email })
    newChildEmail.value = ''
    addMessage.value = 'Élève ajouté ✅'
    await refreshChildren()
  } catch (e) {
    addMessage.value = "Impossible d'ajouter cet élève"
  } finally {
    adding.value = false
    setTimeout(() => { addMessage.value = '' }, 2500)
  }
}

async function handleRemoveChild(childId) {
  removingId.value = childId
  try {
    await removeChild(childId)
    await refreshChildren()
  } catch {}
  removingId.value = null
}

async function handleCreateChild() {
  createMessage.value = ''
  tempPassword.value = ''
  const payload = {
    first_name: String(create.value.first_name || '').trim(),
    last_name: String(create.value.last_name || '').trim(),
    email: String(create.value.email || '').trim().toLowerCase(),
  }
  if (!payload.first_name || !payload.last_name || !payload.email) {
    createMessage.value = 'Renseignez prénom, nom et email'
    return
  }
  creating.value = true
  try {
    const res = await apiClient.post('/api/users/me/children/create/', payload)
    const data = res?.data?.data || {}
    tempPassword.value = data.temp_password || ''
    createMessage.value = 'Compte créé et lié ✅'
    create.value = { first_name: '', last_name: '', email: '' }
    await refreshChildren()
  } catch (e) {
    createMessage.value = 'Création impossible (email déjà utilisé?)'
  } finally {
    creating.value = false
    setTimeout(() => { createMessage.value = '' }, 3000)
  }
}
</script>

<style scoped>
.parent-dashboard { margin: 1rem 0 1.5rem; padding-bottom: 40px; }
.header h1 { margin: 0; font-size: 1.5rem; font-weight: 800; color: #1f2937; }
.subtitle { margin: .25rem 0 0; color: #64748b; }

.add-child { display:flex; align-items:center; gap:.5rem; margin-top:.75rem; }
.input { flex:1; padding:.5rem .6rem; border:1px solid #e5e7eb; border-radius:8px; }
.hint { color:#64748b; }
.create-child { margin-top:.5rem; }
.form-row { display:flex; gap:.5rem; margin-top:.35rem; }
.temp-pass { margin-top:.5rem; background:#f8fafc; border:1px solid #e2e8f0; padding:.5rem .6rem; border-radius:8px; }

.loading { display: flex; justify-content: center; align-items: center; height: 80px; }
.spinner { width: 36px; height: 36px; border: 4px solid #e5e7eb; border-top: 4px solid #2563eb; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty { text-align: center; color: #64748b; padding: 1rem; }

.children-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-top: .75rem; }
.child-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: .9rem; box-shadow: 0 2px 6px rgba(30,41,59,0.06); }
.child-header { display: grid; grid-template-columns: auto 1fr auto; gap: .6rem; align-items: center; }
.avatar { width: 38px; height: 38px; border-radius: 50%; background: #eef2ff; color: #4f46e5; display:flex; align-items:center; justify-content:center; font-weight: 800; }
.child-info .name { font-weight: 800; color: #111827; display:flex; align-items:center; gap:.4rem; }
.child-info .meta { color: #64748b; font-size: .85rem; }
.flag { font-size: 1.1rem; }
.xp { text-align: right; }
.xp-value { font-weight: 800; color: #2563eb; }
.level { color: #64748b; font-weight: 700; font-size: .9rem; }

.child-body { margin-top: .6rem; display: grid; gap: .6rem; }
.metrics-grid { display: grid; grid-template-columns: 1.5fr repeat(3, 1fr); gap: .6rem; align-items: end; }
.metric .label { color: #475569; font-weight: 700; margin-bottom: .25rem; }
.metric .bar { height: 10px; background:#eef2ff; border-radius: 999px; overflow: hidden; }
.metric .fill { height: 100%; background:#10b981; width: 0; transition: width .3s ease; }
.metric .hint { color: #64748b; font-size:.875rem; margin-top:.25rem; }
.metric.small { text-align: center; background:#f8fafc; border:1px solid #e5e7eb; border-radius:10px; padding:.4rem .5rem; }
.metric.small .kpi { font-weight: 800; color:#111827; }
.metric.small.ok .kpi { color:#16a34a; }
.metric.small.ko .kpi { color:#dc2626; }
.metric.small .kpi-label { color:#64748b; font-size:.8rem; }
.last-activity { margin-top:.6rem; }
.last-activity .label { color:#475569; font-weight:700; margin-bottom:.25rem; }
.activity-line { display:flex; gap:.4rem; align-items: baseline; }
.activity-title { font-weight:700; color:#111827; }
.activity-meta { color:#64748b; font-size:.9rem; }

.actions { display:flex; justify-content:flex-end; }
.btn { background:#2563eb; color:white; border:none; border-radius:8px; padding:.5rem .9rem; font-weight:700; cursor:pointer; }
.btn:hover { background:#1e40af; }
.btn.secondary { background:#f1f5f9; color:#0f172a; border:1px solid #e2e8f0; }
.btn.secondary:hover { background:#e2e8f0; }

@media (max-width: 520px) {
  .child-header { grid-template-columns: auto 1fr; }
  .xp { grid-column: 1 / -1; display:flex; gap:.6rem; }
  .metrics-grid { grid-template-columns: 1fr 1fr; }
}
</style>


