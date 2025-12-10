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
      <div v-if="pendingInvitations.length" class="pending-section">
        <h2>Invitations en attente</h2>
        <div class="pending-list">
          <div class="pending-card" v-for="invite in pendingInvitations" :key="invite.link_id">
            <div class="pending-info">
              <div class="name">{{ invite.first_name }} {{ invite.last_name }}</div>
              <div class="email">{{ invite.email }}</div>
              <div class="meta">Envoyée le {{ formatDateTime(invite.invited_at) }}</div>
            </div>
            <button class="btn tertiary" :disabled="removingId === invite.child_id" @click="handleRemoveChild(invite.child_id)">
              Annuler
            </button>
          </div>
        </div>
      </div>

      <div v-if="declinedInvitations.length" class="declined-section">
        <h2>Invitations refusées</h2>
        <p class="declined-hint">Ces élèves ont refusé l'accès. Vous pouvez renvoyer une invitation en saisissant à nouveau leur email.</p>
        <ul class="declined-list">
          <li v-for="invite in declinedInvitations" :key="invite.link_id">
            {{ invite.first_name }} {{ invite.last_name }} — refusé le {{ formatDateTime(invite.responded_at) || '—' }}
          </li>
        </ul>
      </div>

      <div v-if="children.length === 0" class="empty">
        <p v-if="pendingInvitations.length">Aucun accès validé pour le moment. Dès que l'élève accepte, il apparaîtra ici.</p>
        <p v-else>Aucun enfant rattaché pour le moment.</p>
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
              <div class="status-chip">{{ statusLabel(c) }}</div>
            </div>
            <div class="xp">
              <div class="xp-value">{{ c.xp }} XP</div>
              <div class="level">Niveau {{ c.level }}</div>
            </div>
          </div>

          <div class="child-body">
            <section class="block help">
              <div class="section-title">Comment aider {{ firstName(c.display_name) }} aujourd'hui ?</div>
              <ul class="help-list">
                <li v-for="(suggestion, idx) in helpActions(c)" :key="idx">{{ suggestion }}</li>
              </ul>
            </section>

            <section class="block tutoring">
              <div class="tutoring-text">
                <div class="section-title">Besoin d'un coup de pouce ?</div>
                <p>OptiTAB propose aussi des cours particuliers en ligne pour débloquer un chapitre précis.</p>
              </div>
              <button class="btn tertiary">Demander un cours ciblé</button>
            </section>

            <section class="block">
              <div class="section-title">Derniers exercices réalisés</div>
              <ul class="activity-list" v-if="recentActivity(c).length">
                <li v-for="(a, idx) in recentActivity(c)" :key="idx" class="activity-row">
                  <span class="icon">{{ activityIcon(a.type) }}</span>
                  <div class="activity-text">
                    <div class="primary">{{ a.title }}</div>
                    <div class="secondary">
                      <span v-if="a.chapter">{{ a.chapter }}</span>
                      <span v-if="a.when">• {{ humanizeDate(a.when) }}</span>
                      <span v-if="a.duration">• {{ a.duration }}</span>
                    </div>
                  </div>
                </li>
              </ul>
              <div class="empty" v-else>
                <div>Aucun exercice enregistré pour le moment.</div>
                <div class="empty-hint">Les 5 derniers exercices apparaîtront ici dès la première séance.</div>
              </div>
            </section>

            <section class="block history history-embed">
              <ExercicesHistory :child-id="c.id" :show-suggestions="false" />
            </section>

            <div class="actions">
              <button class="btn secondary" @click="askRemoveChild(c)" :disabled="removingId === c.id">Retirer cet élève</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="confirmOpen" class="modal-backdrop">
      <div class="modal">
        <div class="modal-title">Retirer l'accès parent pour {{ childToRemove?.display_name || 'cet élève' }} ?</div>
        <p class="modal-text">L'élève ne sera plus rattaché à ce compte parent. Voulez-vous continuer ?</p>
        <div class="modal-actions">
          <button class="btn secondary" @click="cancelRemove" :disabled="removingId">Annuler</button>
          <button class="btn danger" @click="confirmRemoveChild" :disabled="removingId">Oui, retirer</button>
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
import ExercicesHistory from './ExercicesHistory.vue'

const loading = ref(true)
const children = ref([])
const pendingInvitations = ref([])
const declinedInvitations = ref([])
const router = useRouter()
const newChildEmail = ref('')
const adding = ref(false)
const addMessage = ref('')
const removingId = ref(null)
const creating = ref(false)
const createMessage = ref('')
const tempPassword = ref('')
const create = ref({ first_name: '', last_name: '', email: '' })
const confirmOpen = ref(false)
const childToRemove = ref(null)

function applyChildrenPayload(payload = {}) {
  children.value = payload.children || []
  pendingInvitations.value = payload.pending_invitations || []
  declinedInvitations.value = payload.declined_invitations || []
}

function initials(name) {
  if (!name) return 'E'
  const parts = String(name).trim().split(/\s+/)
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase()
  return (parts[0].substring(0, 1) + parts[1].substring(0, 1)).toUpperCase()
}

function firstName(name) {
  if (!name) return "l'élève"
  return String(name).trim().split(/\s+/)[0]
}

function attendanceLabel(child) {
  const done = child.metrics?.weekly_done ?? 0
  const goal = child.metrics?.weekly_goal
  if (!goal || goal <= 0) return "Objectif hebdo non défini (ex. 4 séances/semaine)"
  if (goal >= 10) return `${done} séance(s) cette semaine • pensez à fixer un objectif réaliste`
  const plural = done > 1 ? 's' : ''
  return `${done} séance${plural} sur ${goal} prévues`
}

function attendanceSub(child) {
  const progress = child.metrics?.weekly_progress
  if (typeof progress === 'number') return `Progression: ${Math.round(progress)}%`
  return 'Cet indicateur se mettra à jour après les premières séances.'
}

function attendanceTone(child) {
  const done = child.metrics?.weekly_done ?? 0
  const goal = child.metrics?.weekly_goal
  if (!goal) return 'neutral'
  const ratio = goal ? done / goal : 0
  if (ratio >= 0.75) return 'ok'
  if (ratio >= 0.4) return 'warn'
  return 'danger'
}

function toneClass(tone) {
  return tone ? `tone-${tone}` : ''
}

function formatMinutes(minutes) {
  const total = Number(minutes)
  if (!Number.isFinite(total) || total <= 0) return '0 min'
  const h = Math.floor(total / 60)
  const m = Math.round(total % 60)
  if (h && m) return `${h}h${m}`
  if (h) return `${h}h`
  return `${m} min`
}

function timeWorkedLabel(child) {
  const minutes = child.metrics?.time_spent_minutes_7d ?? child.metrics?.time_spent_minutes
  if (!Number.isFinite(minutes) || minutes <= 0) return '0 min pour le moment'
  return formatMinutes(minutes)
}

function timeWorkedDelta(child) {
  const delta = child.metrics?.time_spent_delta_minutes
  if (Number.isFinite(delta) && delta !== 0) {
    const sign = delta > 0 ? '+' : '-'
    return `${sign}${formatMinutes(Math.abs(delta))} vs semaine dernière`
  }
  return 'Planifiez une première séance cette semaine'
}

function chaptersLabel(child) {
  const raw = child.metrics?.recent_chapters || child.metrics?.chapters_worked || child.metrics?.chapters || []
  if (Array.isArray(raw) && raw.length) return raw.slice(0, 3).join(', ')
  if (typeof raw === 'string' && raw.trim()) return raw
  if (child.last_activity?.chapitre_title) return child.last_activity.chapitre_title
  return 'Pas encore de chapitre travaillé. Cette zone se remplira dès les premières séances.'
}

function globalLevelLabel(child) {
  const acquired = child.metrics?.acquired_count ?? 0
  const toReview = child.metrics?.not_acquired_count ?? 0
  if (toReview >= acquired + 2) return 'Niveau général : à renforcer'
  if (acquired >= 5 && toReview <= 1) return 'Niveau général : en bonne voie'
  return 'Niveau général : en cours de consolidation'
}

function normalizeActivity(item = {}) {
  return {
    type: item.type || item.content_type || 'exercise',
    title: item.exercice_title || item.title || 'Activité',
    chapter: item.chapitre_title || item.chapter || '',
    matiere: item.matiere?.titre || item.matiere || '',
    notion: item.notion?.titre || item.notion || '',
    when: item.when || item.created_at || item.date || '',
    duration: item.duration ? formatMinutes(item.duration) : item.duration_minutes ? formatMinutes(item.duration_minutes) : '',
    est_correct: item.est_correct ?? item.correct ?? item.success ?? null,
    score: item.score ?? item.note ?? item.average ?? null
  }
}

function recentActivity(child) {
  const list = Array.isArray(child.recent_activities) ? child.recent_activities : []
  const source = list.length ? list : (child.last_activity ? [child.last_activity] : [])
  const normalized = source.map(normalizeActivity)
  const exercises = normalized.filter(a => (a.type || '').toLowerCase().includes('exercice') || (a.type || '').toLowerCase().includes('exercise'))
  const chosen = exercises.length ? exercises : normalized
  return chosen.slice(0, 5)
}

function activityIcon(type) {
  const key = String(type || '').toLowerCase()
  if (key.includes('course')) return '📘'
  if (key.includes('resum') || key.includes('resume')) return '📝'
  return '✅'
}

function humanizeDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
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

function chaptersProgress(child) {
  const raw = child.metrics?.chapters_progress || child.metrics?.chapters || []
  const list = Array.isArray(raw) ? raw : []
  const normalized = list.map(item => {
    const percent = clampPercent(item.percent ?? item.progress ?? item.mastery)
    const state = stateFromPercent(percent)
    return {
      name: item.name || item.title || item.chapitre || 'Chapitre',
      percent,
      state,
      stateLabel: stateLabel(state)
    }
  }).filter(item => item.name)
  if (!normalized.length && child.last_activity?.chapitre_title) {
    normalized.push({
      name: child.last_activity.chapitre_title,
      percent: 30,
      state: 'progress',
      stateLabel: stateLabel('progress')
    })
  }
  return normalized.slice(0, 4)
}

function clampPercent(value) {
  const n = Number(value)
  if (!Number.isFinite(n)) return 0
  return Math.min(100, Math.max(0, Math.round(n)))
}

function stateFromPercent(percent) {
  if (percent >= 70) return 'ok'
  if (percent >= 40) return 'warn'
  return 'progress'
}

function stateLabel(state) {
  if (state === 'ok') return 'maîtrisé'
  if (state === 'warn') return 'à renforcer'
  return 'en cours'
}

function progressHint(child) {
  const list = chaptersProgress(child)
  if (!list.length) return 'Point fort à venir dès les premières séances.'
  const sorted = [...list].sort((a, b) => b.percent - a.percent)
  const top = sorted[0]
  const lows = sorted.filter(item => item.percent < 50).map(item => item.name).slice(0, 2)
  if (!lows.length) return `Point fort actuel : ${top.name}`
  return `Point fort actuel : ${top.name} • À travailler : ${lows.join(', ')}`
}

function alertData(child) {
  const alerts = []
  const recent = recentActivity(child)
  const last = recent.find(a => a.when)?.when || child.last_activity?.when || child.last_activity?.created_at || child.last_activity?.date
  if (last) {
    const d = new Date(last)
    if (!Number.isNaN(d.getTime())) {
      const days = Math.floor((Date.now() - d.getTime()) / 86400000)
      if (days >= 7) alerts.push('Aucune activité depuis 7 jours.')
      else if (days >= 4) alerts.push('Aucune activité depuis 4 jours.')
    }
  } else {
    alerts.push("Aucune activité depuis la création de l'accès.")
  }
  const toReview = child.metrics?.not_acquired_count ?? 0
  if (toReview >= 3) alerts.push('Plusieurs exercices sous 40 % récemment.')
  const tone = alerts.length === 0 ? 'ok' : (toReview >= 3 || alerts.some(a => a.includes('7 jours')) ? 'danger' : 'warn')
  const message = alerts[0] || `Tout va bien, ${firstName(child.display_name)} travaille régulièrement.`
  return { tone, message }
}

function alertTone(child) {
  return `tone-${alertData(child).tone}`
}

function alertMessage(child) {
  return alertData(child).message
}

function helpActions(child) {
  const name = firstName(child.display_name)
  const actions = []
  const toReview = child.metrics?.not_acquired_count ?? 0
  const lastChapter = child.last_activity?.chapitre_title
  const alert = alertData(child)
  if (alert.tone === 'danger') actions.push(`Proposer à ${name} une séance de 20 minutes dès aujourd'hui pour relancer le rythme.`)
  if (alert.tone !== 'ok' && toReview > 0) actions.push(`Encourager ${name} à refaire 1 série d'exercices sur un chapitre à revoir.`)
  if (lastChapter) actions.push(`Suggérer à ${name} de consolider "${lastChapter}".`)
  actions.push(`Inviter ${name} à lancer une première courte séance sur OptiTAB cette semaine.`)
  actions.push('Si besoin, demander un cours ciblé.')
  return actions.slice(0, 3)
}

function askRemoveChild(child) {
  childToRemove.value = child
  confirmOpen.value = true
}

function cancelRemove() {
  confirmOpen.value = false
  childToRemove.value = null
}

async function confirmRemoveChild() {
  if (!childToRemove.value) return
  await handleRemoveChild(childToRemove.value.id)
  cancelRemove()
}

function openChild(childId) {
  router.push({ name: 'ChildOverview', params: { childId: String(childId) } })
}

onMounted(async () => {
  try {
    const res = await fetchMyChildren()
    const data = res?.data?.data || {}
    applyChildrenPayload(data)
  } catch (e) {
    applyChildrenPayload()
  } finally {
    loading.value = false
  }
})

async function refreshChildren() {
  try {
    const res = await fetchMyChildren()
    const data = res?.data?.data || {}
    applyChildrenPayload(data)
  } catch {
    applyChildrenPayload()
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
    const res = await addChild({ email })
    const responseData = res?.data || {}
    addMessage.value = responseData.message || 'Invitation envoyée ✅'
    newChildEmail.value = ''
    await refreshChildren()
  } catch (e) {
    addMessage.value = e.response?.data?.message || "Impossible d'ajouter cet élève"
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

function formatDateTime(isoString) {
  if (!isoString) return ''
  try {
    return new Date(isoString).toLocaleString('fr-FR', {
      day: '2-digit',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return ''
  }
}

function statusLabel(child) {
  if (child.status === 'accepted') {
    const acceptedAt = formatDateTime(child.responded_at)
    return acceptedAt ? `Accès accordé le ${acceptedAt}` : 'Accès accordé'
  }
  return 'Lien actif'
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

.pending-section { margin-top:1.2rem; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:1rem; }
.pending-section h2 { margin:0 0 .6rem; font-size:1rem; font-weight:700; color:#1f2937; }
.pending-list { display:flex; flex-direction:column; gap:.6rem; }
.pending-card { display:flex; align-items:center; justify-content:space-between; gap:.75rem; background:#fff; border:1px solid #e5e7eb; border-radius:10px; padding:.7rem .9rem; }
.pending-info .name { font-weight:700; color:#1f2937; }
.pending-info .email { color:#475569; font-size:.85rem; }
.pending-info .meta { color:#94a3b8; font-size:.78rem; margin-top:.15rem; }
.btn.tertiary { background:#e0e7ff; color:#4338ca; border:1px solid #c7d2fe; }
.btn.tertiary:hover { background:#c7d2fe; }

.declined-section { margin-top:1.2rem; background:#fff7ed; border:1px dashed #fdba74; border-radius:12px; padding:1rem; }
.declined-section h2 { margin:0; font-size:1rem; font-weight:700; color:#9a3412; }
.declined-hint { margin:.35rem 0 .6rem; color:#9a3412; font-size:.85rem; }
.declined-list { margin:0; padding-left:1.1rem; color:#f97316; font-size:.85rem; }

.loading { display: flex; justify-content: center; align-items: center; height: 80px; }
.spinner { width: 36px; height: 36px; border: 4px solid #e5e7eb; border-top: 4px solid #2563eb; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty { text-align: center; color: #64748b; padding: 1rem; }

.children-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; margin-top: .75rem; }
.child-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: .9rem; box-shadow: 0 2px 6px rgba(30,41,59,0.06); }
.child-header { display: grid; grid-template-columns: auto 1fr auto; gap: .6rem; align-items: center; }
.avatar { width: 38px; height: 38px; border-radius: 50%; background: #eef2ff; color: #4f46e5; display:flex; align-items:center; justify-content:center; font-weight: 800; }
.child-info .name { font-weight: 800; color: #111827; display:flex; align-items:center; gap:.4rem; }
.child-info .meta { color: #64748b; font-size: .85rem; }
.flag { font-size: 1.1rem; }
.xp { text-align: right; }
.xp-value { font-weight: 800; color: #2563eb; }
.level { color: #64748b; font-weight: 700; font-size: .9rem; }

.child-body { margin-top: .6rem; display: flex; flex-direction: column; gap: .75rem; }
.block { background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:.75rem .9rem; }
.section-title { margin:0 0 .35rem; font-size:1rem; font-weight:800; color:#0f172a; }

.grid-2 { display:grid; grid-template-columns: 1fr; gap:.75rem; }
.activity-list { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:.55rem; }
.activity-row { display:flex; gap:.5rem; align-items:flex-start; }
.activity-row .icon { font-size:1.05rem; }
.activity-text .primary { font-weight:700; color:#0f172a; }
.activity-text .secondary { color:#64748b; font-size:.9rem; display:flex; gap:.35rem; flex-wrap:wrap; }
.empty-hint { color:#94a3b8; font-size:.9rem; margin-top:.15rem; }

.watch-help .block { height:100%; }
.alert { border-left:4px solid #f97316; }
.alert-text { margin:0; color:#0f172a; line-height:1.4; }
.help-list { margin:0; padding-left:1.1rem; color:#0f172a; display:flex; flex-direction:column; gap:.3rem; }
.help-list li { color:#475569; }

.tutoring { display:flex; align-items:center; justify-content:space-between; gap:.75rem; flex-wrap:wrap; }
.tutoring-text p { margin:.15rem 0 0; color:#475569; }

.status-chip { display:inline-block; margin-top:.3rem; padding:.2rem .55rem; border-radius:999px; background:#dcfce7; color:#166534; font-size:.75rem; font-weight:600; }

.actions { display:flex; justify-content:flex-end; gap:.5rem; }
.btn { background:#2563eb; color:white; border:none; border-radius:8px; padding:.5rem .9rem; font-weight:700; cursor:pointer; }
.btn:hover { background:#1e40af; }
.btn.secondary { background:#f1f5f9; color:#0f172a; border:1px solid #e2e8f0; }
.btn.secondary:hover { background:#e2e8f0; }
.btn.danger { background:#dc2626; }
.btn.danger:hover { background:#b91c1c; }

@media (max-width: 520px) {
  .child-header { grid-template-columns: auto 1fr; }
  .xp { grid-column: 1 / -1; display:flex; gap:.6rem; }
  .overview-grid { grid-template-columns: 1fr; }
}

.modal-backdrop { position: fixed; inset:0; background: rgba(15,23,42,0.45); display:flex; align-items:center; justify-content:center; z-index: 30; padding:1rem; }
.modal { background:#fff; border-radius:12px; padding:1rem 1.2rem; width:100%; max-width:420px; box-shadow:0 10px 30px rgba(15,23,42,0.2); border:1px solid #e2e8f0; }
.modal-title { margin:0 0 .35rem; font-size:1.1rem; font-weight:800; color:#0f172a; }
.modal-text { margin:0 0 .8rem; color:#475569; }
.modal-actions { display:flex; justify-content:flex-end; gap:.5rem; }
</style>
