<template>
  <div class="parent-dashboard" ref="contentRef" :style="zoomStyle">
    <div class="hero">
      <div class="hero-content">
        <div class="hero-header">
          <div class="badge">Espace parents</div>
          <h1>Suivez les progrès de vos enfants</h1>
          <p class="description">Accompagnez leur apprentissage avec une vision claire et pédagogique</p>
        </div>

        <div class="services-info">
          <div class="services-header">
            <h2 class="services-title">Ressources pédagogiques disponibles</h2>
            <p class="services-subtitle">Un accompagnement complet pour la réussite de votre enfant</p>
          </div>
          <div class="services-grid">
            <div class="service-item">
              <div class="service-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                  <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                </svg>
              </div>
              <div class="service-content">
                <div class="service-name">Cours complets</div>
                <div class="service-desc">Leçons détaillées par chapitre</div>
              </div>
            </div>
            <div class="service-item">
              <div class="service-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
              </div>
              <div class="service-content">
                <div class="service-name">Fiches de synthèse</div>
                <div class="service-desc">Révisions ciblées et efficaces</div>
              </div>
            </div>
            <div class="service-item">
              <div class="service-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
              </div>
              <div class="service-content">
                <div class="service-name">Exercices interactifs</div>
                <div class="service-desc">Pratique adaptée au niveau</div>
              </div>
            </div>
            <div class="service-item">
              <div class="service-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <div class="service-content">
                <div class="service-name">Correction personnalisée</div>
                <div class="service-desc">Retours détaillés sur les devoirs</div>
              </div>
            </div>
            <div class="service-item">
              <div class="service-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
              </div>
              <div class="service-content">
                <div class="service-name">Outils intelligents</div>
                <div class="service-desc">Calculateurs mathématiques avancés</div>
              </div>
            </div>
            <div class="service-item">
              <div class="service-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <div class="service-content">
                <div class="service-name">Cours particuliers</div>
                <div class="service-desc">Accompagnement individuel en ligne</div>
              </div>
            </div>
          </div>
        </div>

        <div class="quick-actions">
          <div class="action-card">
            <div class="card-header">
              <div class="icon-wrapper blue">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 10a4 4 0 100-8 4 4 0 000 8zm-5 2a3 3 0 00-3 3v1a1 1 0 001 1h14a1 1 0 001-1v-1a3 3 0 00-3-3H5z" fill="currentColor"/>
                </svg>
              </div>
              <div>
                <h3>Inviter un élève</h3>
                <p>L'élève recevra une invitation à accepter sur son compte</p>
              </div>
            </div>
            <div class="card-body">
              <div class="input-group">
                <input v-model="newChildEmail" type="email" placeholder="email@exemple.com" class="input" />
                <button class="btn primary" :disabled="adding" @click="handleAddChild">
                  <span v-if="!adding">Envoyer</span>
                  <span v-else>...</span>
                </button>
              </div>
              <div v-if="addMessage" class="message" :class="addMessage.includes('✅') ? 'success' : 'error'">
                {{ addMessage }}
              </div>
              <div class="subscription-cta">
                <div class="cta-content">
                  <div class="cta-title"><span class="cta-icon">✨</span> Offrez le meilleur à votre enfant</div>
                  <div class="cta-text">Accès illimité aux cours, exercices et suivi personnalisé</div>
                </div>
                <button class="btn-cta" @click="goToSubscriptions">Découvrir les offres</button>
              </div>
            </div>
          </div>

          <div class="action-card">
            <div class="card-header">
              <div class="icon-wrapper green">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 10a4 4 0 100-8 4 4 0 000 8zm-5 2a3 3 0 00-3 3v1a1 1 0 001 1h14a1 1 0 001-1v-1a3 3 0 00-3-3H5zm13-3a1 1 0 011 1v2a1 1 0 11-2 0v-2a1 1 0 011-1zm-1-3a1 1 0 10-2 0v2a1 1 0 102 0V6z" fill="currentColor"/>
                </svg>
              </div>
              <div>
                <h3>Créer un compte</h3>
                <p>Si l'élève n'a toujours pas de compte</p>
              </div>
            </div>
            <div class="card-body">
              <div class="input-row">
                <input v-model="create.first_name" class="input" placeholder="Prénom" />
                <input v-model="create.last_name" class="input" placeholder="Nom" />
              </div>
              <input v-model="create.email" class="input" placeholder="Email" />
              <button class="btn secondary full" :disabled="creating" @click="handleCreateChild">
                <span v-if="!creating">Créer le compte</span>
                <span v-else>Création...</span>
              </button>
              <div class="note">
                <span>💡</span>
                <span>Si l'élève n'a pas d'email,</span>
                <button class="btn-link" @click="openContactModal">contactez le support</button>
              </div>
              <div v-if="createMessage" class="message" :class="createMessage.includes('✅') ? 'success' : 'error'">
                {{ createMessage }}
              </div>
              <div v-if="tempPassword" class="temp-password">
                <span class="label">Mot de passe :</span>
                <code>{{ tempPassword }}</code>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <span class="spinner"></span>
    </div>

    <div v-else>
      <div v-if="pendingInvitations.length" class="callout">
        <div class="callout-title">Invitations en attente</div>
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

      <div v-if="declinedInvitations.length" class="callout warning">
        <div class="callout-title">Invitations refusées</div>
        <p class="callout-text">Ces élèves ont refusé l'accès. Vous pouvez renvoyer une invitation en saisissant à nouveau leur email.</p>
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

      <div v-else>
        <div class="tabs-container" v-if="children.length > 1">
          <div class="tabs">
            <button 
              v-for="(child, idx) in children" 
              :key="child.id"
              class="tab"
              :class="{ active: selectedChildIndex === idx }"
              @click="selectedChildIndex = idx"
            >
              <span class="tab-avatar">{{ initials(child.display_name) }}</span>
              <span class="tab-name">{{ child.display_name }}</span>
            </button>
          </div>
        </div>

        <div class="child-card" v-if="selectedChild">
          <div class="child-header">
            <div class="avatar">{{ initials(selectedChild.display_name) }}</div>
            <div class="child-info">
              <div class="name-line">
                <span v-if="selectedChild.pays_flag" class="flag">{{ selectedChild.pays_flag }}</span>
                <span class="name">{{ selectedChild.display_name }}</span>
                <span class="status-chip">{{ statusLabel(selectedChild) }}</span>
              </div>
              <div class="tags">
                <span v-if="selectedChild.niveau" class="tag">{{ selectedChild.niveau }}</span>
                <span class="tag muted">Dernière activité {{ lastActivityLabel(selectedChild) }}</span>
              </div>
            </div>
            <div class="xp">
              <div class="xp-value">{{ selectedChild.xp }} XP</div>
              <div class="level">Niveau {{ selectedChild.level }}</div>
            </div>
          </div>

          <section class="block">
            <div class="section-title">Historique des quiz</div>
            <QuizHistory :child-id="selectedChild.id" :key="`quiz-${selectedChild.id}`" />
          </section>

          <section class="block">
            <div class="section-title">Historique des exercices</div>
            <ExercicesHistory :child-id="selectedChild.id" :show-suggestions="false" :key="`exercices-${selectedChild.id}`" />
          </section>

          <div class="actions-minimal">
            <button class="btn-link-danger" @click="askRemoveChild(selectedChild)" :disabled="removingId === selectedChild.id">Retirer cet élève</button>
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

    <ContactModal 
      :isOpen="isContactModalOpen" 
      :initialSubject="contactModalSubject"
      @close="closeContactModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { fetchMyChildren, addChild, removeChild } from '@/api/users'
import apiClient from '@/api/client'
import ExercicesHistory from './ExercicesHistory.vue'
import QuizHistory from './QuizHistoryRefactored.vue'
import ContactModal from '@/components/common/ContactModal.vue'
import { useZoom } from '@/composables/useZoom'

// Zoom responsive
const contentRef = ref(null)
const {
  viewportWidth,
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom()

const zoomStyle = createZoomStyle({
  cssVar: '--parent-zoom',
  heightVar: '--parent-height',
  mobileZoomAdjustment: (z) => Math.max(0.65, z - 0.05)
})

function measureContentHeightForParent() {
  measureContentHeight(contentRef)
}

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
const isContactModalOpen = ref(false)
const contactModalSubject = ref('')
const selectedChildIndex = ref(0)
const selectedChild = computed(() => children.value[selectedChildIndex.value] || null)

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

function lastActivityLabel(child) {
  const recent = recentActivity(child)
  const entry = recent.find(a => a.when) || child.last_activity || {}
  const when = entry.when || entry.created_at || entry.date
  const label = humanizeDate(when)
  return label || '—'
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
  // Setup zoom responsive
  detectMobileAndZoomSupport()
  updateViewportWidth()
  setupViewportListener()
  
  try {
    const res = await fetchMyChildren()
    const data = res?.data?.data || {}
    applyChildrenPayload(data)
  } catch (e) {
    applyChildrenPayload()
  } finally {
    loading.value = false
    nextTick(() => measureContentHeightForParent())
  }
})

onBeforeUnmount(() => {
  cleanupViewportListener()
})

watch(viewportWidth, () => {
  nextTick(() => measureContentHeightForParent())
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

function openContactModal() {
  contactModalSubject.value = "Création de compte élève sans email"
  isContactModalOpen.value = true
}

function closeContactModal() {
  isContactModalOpen.value = false
  contactModalSubject.value = ''
}

function goToSubscriptions() {
  router.push('/billing')
}

function viewAsStudent(childId) {
  router.push(`/dashboard/student/${childId}`)
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
/* Layout */
.parent-dashboard { 
  width: 100%;
  padding: 2rem 1rem;
  transform-origin: top left;
}

/* Support zoom natif */
@supports (zoom: 1) {
  .parent-dashboard {
    zoom: var(--parent-zoom, 1);
    transform: none !important;
    width: 100% !important;
  }
}

/* Hero Section */
.hero { 
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: 2rem 1.5rem;
  margin-bottom: 2rem;
}

.hero-content {
  width: 100%;
}

.hero-header {
  margin-bottom: 2rem;
}

.badge {
  display: inline-block;
  background: white;
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.hero-header h1 {
  font-size: 1.875rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  line-height: 1.3;
  color: #0f172a;
}

.description {
  font-size: 0.9375rem;
  margin: 0;
  font-weight: 400;
  color: #64748b;
}

/* Services Info */
.services-info {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 2rem;
}

.services-header {
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid #e2e8f0;
}

.services-title {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 0.25rem;
}

.services-subtitle {
  font-size: 0.8125rem;
  color: #64748b;
  margin: 0;
  font-weight: 400;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.service-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.875rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  transition: background-color 0.15s;
}

.service-item:hover {
  background: #f1f5f9;
}

.service-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  color: #2563eb;
  flex-shrink: 0;
}

.service-content {
  flex: 1;
  min-width: 0;
}

.service-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 0.125rem;
}

.service-desc {
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.4;
}

/* Quick Actions */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.action-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.25rem;
  min-width: 0;
  overflow: hidden;
}

.action-card:hover {
  border-color: #cbd5e0;
}

.card-header {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-wrapper.blue {
  background: #eff6ff;
  color: #2563eb;
}

.icon-wrapper.green {
  background: #f0fdf4;
  color: #16a34a;
}

.card-header h3 {
  margin: 0 0 0.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
}

.card-header p {
  margin: 0;
  font-size: 0.8125rem;
  color: #64748b;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Forms */
.input-group {
  display: flex;
  gap: 0.5rem;
  align-items: stretch;
}

.input-group .input {
  flex: 2;
  min-width: 0;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.input-row .input {
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.input {
  padding: 0.625rem 0.875rem;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.15s;
  background: white;
  min-width: 0;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: #2563eb;
  background: white;
}

.input::placeholder {
  color: #94a3b8;
}

.full {
  width: 100%;
}

/* Buttons */
.btn {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.15s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.btn.primary {
  background: #2563eb;
  color: white;
}

.btn.primary:hover:not(:disabled) {
  background: #1d4ed8;
}

.btn.secondary {
  background: white;
  color: #475569;
  border: 1px solid #cbd5e0;
}

.btn.secondary:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #94a3b8;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Messages */
.message {
  padding: 0.625rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8125rem;
  font-weight: 400;
}

.message.success {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.message.error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.temp-password {
  padding: 0.625rem 0.75rem;
  background: #fffbeb;
  border: 1px solid #fde047;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
}

.temp-password .label {
  font-weight: 500;
  color: #78350f;
}

.temp-password code {
  background: #fef9c3;
  padding: 0.125rem 0.375rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-weight: 500;
  color: #78350f;
}

.note {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 0.75rem;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 4px;
  font-size: 0.8125rem;
  color: #075985;
}

.btn-link {
  background: none;
  border: none;
  color: #2563eb;
  font-size: 0.8125rem;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
}

.btn-link:hover {
  color: #1d4ed8;
}

.subscription-cta {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  margin-top: 0.75rem;
}

.cta-icon {
  font-size: 1.25rem;
  margin-right: 0.375rem;
}

.cta-content {
  flex: 1;
  min-width: 0;
}

.cta-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 0.125rem;
  display: flex;
  align-items: center;
}

.cta-text {
  font-size: 0.75rem;
  color: #475569;
  line-height: 1.4;
}

.btn-cta {
  padding: 0.5rem 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-cta:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}

/* Tabs */
.tabs-container {
  margin-bottom: 1.5rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-bottom: none;
  border-radius: 6px 6px 0 0;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  white-space: nowrap;
}

.tab:hover {
  background: #f8fafc;
  color: #0f172a;
}

.tab.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.tab-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e2e8f0;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}

.tab.active .tab-avatar {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.tab-name {
  font-weight: 600;
}

/* Loading State */
.loading { 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  padding: 4rem;
}

.spinner { 
  width: 48px; 
  height: 48px; 
  border: 4px solid #e2e8f0; 
  border-top: 4px solid #3b82f6; 
  border-radius: 50%; 
  animation: spin 0.8s linear infinite;
}

@keyframes spin { 
  to { transform: rotate(360deg); } 
}

/* Callouts */
.callout { 
  background: white;
  border: 2px solid #e2e8f0; 
  border-radius: 16px; 
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.callout-title { 
  margin: 0 0 1rem; 
  font-weight: 700; 
  font-size: 1.125rem;
  color: #1a202c;
}

.callout-text { 
  margin: 0 0 1rem; 
  color: #4a5568;
  line-height: 1.6;
}

.callout.warning { 
  background: #fffbeb;
  border-color: #fbbf24;
}

.callout.warning .callout-title {
  color: #92400e;
}

.pending-list { 
  display: flex; 
  flex-direction: column; 
  gap: 0.75rem;
}

.pending-card { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  gap: 1rem;
  background: #f7fafc;
  border: 1px solid #e2e8f0; 
  border-radius: 12px; 
  padding: 1rem 1.25rem;
  transition: all 0.2s;
}

.pending-card:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.pending-info .name { 
  font-weight: 700; 
  color: #1a202c;
  margin-bottom: 0.25rem;
}

.pending-info .email { 
  color: #718096;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.pending-info .meta { 
  color: #a0aec0;
  font-size: 0.8rem;
}

.declined-list { 
  margin: 0; 
  padding-left: 1.5rem;
  color: #92400e;
  font-size: 0.9rem;
  line-height: 1.8;
}

.empty { 
  text-align: center; 
  color: #718096;
  padding: 3rem 1rem;
  font-size: 1rem;
}
/* Children Grid */
.children-grid { 
  display: grid; 
  grid-template-columns: 1fr; 
  gap: 1.25rem;
}

.child-card { 
  background: white;
  border: 1px solid #e2e8f0; 
  border-radius: 8px; 
  padding: 1.25rem;
  display: flex; 
  flex-direction: column; 
  gap: 1rem;
}

.child-card:hover {
  border-color: #cbd5e0;
}

.child-header { 
  display: grid; 
  grid-template-columns: auto 1fr auto; 
  gap: 1rem;
  align-items: start;
}

.avatar { 
  width: 48px; 
  height: 48px; 
  border-radius: 50%; 
  background: #f1f5f9;
  color: #475569;
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-weight: 600;
  font-size: 1rem;
  border: 1px solid #e2e8f0;
}

.name-line { 
  display: flex; 
  align-items: center; 
  gap: 0.5rem;
  flex-wrap: wrap;
}

.name { 
  font-weight: 700;
  color: #1a202c;
  font-size: 1.25rem;
}

.tags { 
  display: flex; 
  gap: 0.5rem;
  flex-wrap: wrap; 
  margin-top: 0.5rem;
}

.tag { 
  background: #edf2f7;
  color: #2d3748;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.tag.muted { 
  color: #718096;
  background: #f7fafc;
}

.flag { 
  font-size: 1.25rem;
}

.xp { 
  text-align: right;
}

.xp-value { 
  font-weight: 700;
  font-size: 1.125rem;
  color: #2563eb;
}

.level { 
  color: #718096;
  font-weight: 600;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
/* Metrics */
.mini-metrics { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
  gap: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0; 
  border-radius: 6px; 
  padding: 1rem;
}

.metric { 
  display: flex; 
  flex-direction: column; 
  gap: 0.375rem;
}

.metric-label { 
  color: #64748b;
  font-weight: 500;
  font-size: 0.8125rem;
}

.metric-value { 
  color: #0f172a;
  font-weight: 600;
  font-size: 1.125rem;
}

.metric-sub { 
  color: #94a3b8;
  font-size: 0.8125rem;
}

.child-body { 
  display: flex; 
  flex-direction: column; 
  gap: 1rem;
}

.block { 
  background: #f8fafc;
  border: 1px solid #e2e8f0; 
  border-radius: 6px; 
  padding: 1rem;
}

.section-title { 
  margin: 0 0 0.625rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #0f172a;
}

.help-list { 
  margin: 0; 
  padding-left: 1.5rem;
  color: #4a5568;
  display: flex; 
  flex-direction: column; 
  gap: 0.5rem;
  line-height: 1.6;
}

.tutoring { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  gap: 1rem;
  flex-wrap: wrap;
}

.tutoring-text { 
  margin: 0.25rem 0 0;
  color: #718096;
  line-height: 1.5;
}
/* Activity */
.activity-list { 
  list-style: none; 
  padding: 0; 
  margin: 0; 
  display: flex; 
  flex-direction: column; 
  gap: 0.75rem;
}

.activity-row { 
  display: flex; 
  gap: 0.75rem;
  align-items: flex-start;
  padding: 0.75rem;
  background: white;
  border-radius: 10px;
  transition: background 0.2s;
}

.activity-row:hover {
  background: #edf2f7;
}

.activity-row .icon { 
  font-size: 1.25rem;
}

.activity-text .primary { 
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.25rem;
}

.activity-text .secondary { 
  color: #718096;
  font-size: 0.875rem;
  display: flex; 
  gap: 0.5rem;
  flex-wrap: wrap;
}

.empty-hint { 
  color: #a0aec0;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Status Pills */
.status-chip { 
  display: inline-block; 
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  background: #d1fae5;
  color: #065f46;
  font-size: 0.75rem;
  font-weight: 600;
}

.pill { 
  display: inline-flex; 
  align-items: center; 
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  background: #edf2f7;
  color: #1a202c;
  font-weight: 600;
  font-size: 0.875rem;
}

.pill.tone { 
  background: #eef2ff;
  color: #1e40af;
  border: 1px solid #c7d2fe;
}

.tone-ok { 
  background: #d1fae5;
  color: #065f46;
  border-color: #6ee7b7;
}

.tone-warn { 
  background: #fef3c7;
  color: #92400e;
  border-color: #fbbf24;
}

.tone-danger { 
  background: #fee2e2;
  color: #991b1b;
  border-color: #fca5a5;
}

.history-embed { 
  background: white;
  border: 1px solid #e2e8f0;
}

/* Actions */
.actions-minimal { 
  display: flex; 
  justify-content: flex-end; 
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.btn-link-danger {
  background: none;
  border: none;
  color: #dc2626;
  font-size: 0.8125rem;
  font-weight: 500;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
}

.btn-link-danger:hover:not(:disabled) {
  color: #b91c1c;
}

.btn-link-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.tertiary { 
  background: #edf2f7;
  color: #4a5568;
  border: 1px solid #cbd5e0;
}

.btn.tertiary:hover:not(:disabled) { 
  background: #e2e8f0;
  border-color: #a0aec0;
}

.btn.danger { 
  background: #f56565;
  color: white;
}

.btn.danger:hover:not(:disabled) { 
  background: #e53e3e;
  box-shadow: 0 4px 12px rgba(245, 101, 101, 0.3);
}
/* Modal */
.modal-backdrop { 
  position: fixed; 
  inset: 0; 
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 50;
  padding: 1rem;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal { 
  background: white;
  border-radius: 20px; 
  padding: 2rem;
  width: 100%; 
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-title { 
  margin: 0 0 0.75rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: #1a202c;
}

.modal-text { 
  margin: 0 0 1.5rem;
  color: #4a5568;
  line-height: 1.6;
}

.modal-actions { 
  display: flex; 
  justify-content: flex-end; 
  gap: 0.75rem;
}

/* Responsive */
@media (max-width: 1330px) {
  .subscription-cta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .subscription-cta .btn-cta {
    width: 100%;
    text-align: center;
  }
}

@media (max-width: 1024px) {
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .quick-actions {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .parent-dashboard {
    padding: 1rem 0.75rem;
  }
  
  .hero {
    padding: 1.5rem 1rem;
    border-radius: 12px;
  }

  .hero-header h1 {
    font-size: 1.5rem;
  }
  
  .description {
    font-size: 0.9rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .service-item {
    padding: 0.625rem;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
  }
  
  .service-icon {
    width: 32px;
    height: 32px;
  }
  
  .service-name {
    font-size: 0.75rem;
  }
  
  .service-desc {
    display: none;
  }

  .quick-actions {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .action-card {
    max-width: 100%;
    box-sizing: border-box;
  }

  .input-group {
    flex-direction: column;
  }

  .input-row {
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .input-row .input {
    min-width: 0;
  }

  .child-header {
    grid-template-columns: auto 1fr;
  }

  .xp {
    grid-column: 1 / -1;
    display: flex;
    gap: 1rem;
    padding-top: 0.5rem;
  }

  .mini-metrics {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
  }

  .actions .btn {
    width: 100%;
  }
  
  .tabs {
    gap: 0.25rem;
  }
  
  .tab {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
  
  .tab-avatar {
    width: 24px;
    height: 24px;
    font-size: 0.625rem;
  }
  
  .tab-name {
    display: none;
  }
  
  .child-card {
    padding: 1rem;
  }
  
  .block {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .parent-dashboard {
    padding: 0.75rem 0.5rem;
  }

  .hero {
    border-radius: 8px;
    padding: 1rem 0.75rem;
  }

  .hero-header h1 {
    font-size: 1.25rem;
  }

  .description {
    font-size: 0.85rem;
  }
  
  .badge {
    font-size: 0.625rem;
    padding: 0.25rem 0.5rem;
  }
  
  .services-header {
    margin-bottom: 0.75rem;
  }
  
  .services-title {
    font-size: 0.9rem;
  }
  
  .services-subtitle {
    font-size: 0.75rem;
  }
  
  .services-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.375rem;
  }
  
  .service-item {
    padding: 0.5rem;
  }
  
  .service-icon {
    width: 28px;
    height: 28px;
  }
  
  .service-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .service-name {
    font-size: 0.65rem;
    line-height: 1.2;
  }
  
  .action-card {
    padding: 1rem;
  }
  
  .card-header {
    margin-bottom: 0.875rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
  
  .card-subtitle {
    font-size: 0.75rem;
  }
  
  .input-group input,
  .input-row input {
    font-size: 0.8rem;
    padding: 0.5rem;
    min-width: 0;
  }
  
  .input-row {
    gap: 0.5rem;
  }
  
  .btn {
    font-size: 0.8rem;
    padding: 0.625rem 1rem;
  }
  
  .tabs-container {
    margin-bottom: 1rem;
  }
  
  .tab {
    padding: 0.375rem 0.5rem;
  }
  
  .tab-avatar {
    width: 22px;
    height: 22px;
    font-size: 0.5625rem;
  }
  
  .child-card {
    padding: 0.75rem;
    border-radius: 8px;
  }
  
  .avatar {
    width: 40px;
    height: 40px;
    font-size: 0.875rem;
  }
  
  .name {
    font-size: 1rem;
  }
  
  .tag {
    font-size: 0.625rem;
    padding: 0.125rem 0.375rem;
  }
  
  .xp-value {
    font-size: 1rem;
  }
  
  .level {
    font-size: 0.7rem;
  }
  
  .block {
    padding: 0.75rem;
    border-radius: 8px;
  }
  
  .section-title {
    font-size: 0.875rem;
  }
}

@media (max-width: 360px) {
  .parent-dashboard {
    padding: 0.5rem 0.375rem;
  }
  
  .hero {
    padding: 0.75rem 0.5rem;
  }
  
  .hero-header h1 {
    font-size: 1.125rem;
  }
  
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .service-item {
    padding: 0.375rem;
  }
  
  .service-icon {
    width: 24px;
    height: 24px;
  }
  
  .service-name {
    font-size: 0.6rem;
  }
}
</style>
