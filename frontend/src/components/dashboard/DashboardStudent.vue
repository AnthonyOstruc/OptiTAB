<template>
  <div class="dashboard-content">
    <div v-if="showInvitationModal && activeInvitation" class="parent-invite-overlay">
      <div class="parent-invite-modal">
        <h2>Invitation parent</h2>
        <p class="invite-lead">
          <strong>{{ activeInvitation.parent_display_name }}</strong> souhaite accéder à votre progression.
        </p>
        <p class="invitation-email">Email parent : <span>{{ activeInvitation.parent_email }}</span></p>
        <p v-if="activeInvitation.invited_at" class="invitation-date">
          Invitation envoyée le {{ formatInvitationDate(activeInvitation.invited_at) }}
        </p>
        <p class="invitation-question">Autorisez-vous cet accès ?</p>
        <div class="invitation-actions">
          <button class="btn accept" :disabled="!!processingAction" @click="respondToInvitation('accept')">Accepter</button>
          <button class="btn decline" :disabled="!!processingAction" @click="respondToInvitation('decline')">Refuser</button>
        </div>
        <div v-if="invitationFeedback" :class="['invitation-feedback', { error: invitationError }]">
          {{ invitationFeedback }}
        </div>
      </div>
    </div>

    <!-- Notification de reset gamification désactivée -->
    
    <div class="dashboard-center-top">
      <div v-if="userStore.isLoading" class="dashboard-spinner">
        <span class="spinner"></span>
      </div>
      <h1 v-else>
        Bienvenue {{ userStore.firstName }} sur votre tableau de bord
      </h1>
    </div>

    <!-- Notifications de corrections en attente -->
    <PendingCorrections />
    
    <!-- Classement + Niveau + Objectifs -->
    <div class="section leaderboard-section">
      <div class="leaderboard-grid">
        <div class="leaderboard-container">
          <LeaderboardWidget />
        </div>
        <div class="level-container">
          <XPBadges />
          <LoginStreak />
          <PrivateTutorCTA />
        </div>
      </div>
    </div>



    <!-- Mini-jeux -->
    <div v-if="userStore.isAdmin" class="section games-section">
      <router-link to="/jeux/math-run" class="math-run-card">
        <div class="math-run-card-left">
          <span class="math-run-card-emoji">🏃</span>
          <div>
            <div class="math-run-card-title">Math Run</div>
            <div class="math-run-card-sub">Runner mathématique — réponds vite !</div>
          </div>
        </div>
        <span class="math-run-card-badge">Jouer →</span>
      </router-link>
    </div>

    <!-- Historique des quiz -->
    <QuizHistory />

    <!-- Historique des exercices avec filtres → rendu immédiat -->
    <ExercicesHistory />

    <!-- Modal d'abonnement (niveaux bloqués) -->
    <SubscriptionPromptModal
      :is-open="showSubscriptionPrompt"
      @close="handleSubscriptionPromptClose"
    />

    
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import { lockBodyScroll, unlockBodyScroll } from '@/utils/bodyScrollLock'
import { useSubjectsStore } from '@/stores/subjects/index'
import { getStatuses, getMatieres } from '@/api'
import {
  fetchUserGamification,
  fetchMyOverview,
  fetchParentInvitations,
  respondParentInvitation
} from '@/api/users'
// Verification disabled: no imports
import LeaderboardWidget from '@/components/dashboard/LeaderboardWidget.vue'





import XPBadges from '@/components/dashboard/XPBadges.vue'
import LoginStreak from '@/components/dashboard/LoginStreak.vue'
import PrivateTutorCTA from '@/components/dashboard/PrivateTutorCTA.vue'
import QuizHistory from '@/components/dashboard/QuizHistoryRefactored.vue'
import ExercicesHistory from '@/components/dashboard/ExercicesHistory.vue'
import PendingCorrections from '@/components/dashboard/PendingCorrections.vue'
import SubscriptionPromptModal from '@/components/modals/SubscriptionPromptModal.vue'
import { useSubscriptionStore } from '@/stores/subscription'

// StreakTestButton supprimé

const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const subscriptionStore = useSubscriptionStore()
const router = useRouter()

const stats = ref({ done: 0, acquired: 0, not_acquired: 0 })
// Supprimé: indicateur de chargement bas de page devenu inutile
const statuses = ref([])

const matieres = ref([])
const overview = ref(null)
// Verification disabled: no code-handling functions

const invitations = ref([])
const activeInvitationIndex = ref(0)
const showInvitationModal = ref(false)
const invitationFeedback = ref('')
const invitationError = ref(false)
const processingAction = ref('')

const activeInvitation = computed(() => invitations.value[activeInvitationIndex.value] || null)
const isAuthenticated = computed(() => userStore.isAuthenticated)

// --- Modal abonnement (réapparait toutes les 2 min si niveaux bloqués) ---
const showSubscriptionPrompt = ref(false)
let subscriptionPromptTimer = null
const SUBSCRIPTION_PROMPT_INTERVAL = 2 * 60 * 1000 // 2 minutes
const hasLearningProfile = computed(() => Boolean(userStore.pays && userStore.niveau_pays))
const hasUnlockedCurrentLevel = computed(() => {
  const currentLevelId = userStore.niveau_pays?.id
  if (!currentLevelId) return false
  return subscriptionStore.levelUnlocked(currentLevelId)
})

const shouldShowSubscriptionPrompt = computed(() => {
  if (!isAuthenticated.value) return false
  if (userStore.isAdmin) return false
  // Ne jamais afficher la promo abonnement tant que le profil d'apprentissage n'est pas configuré.
  if (!hasLearningProfile.value) return false
  // Attendre que le statut soit chargé avant de décider
  if (subscriptionStore.loading || !subscriptionStore.status) return false
  if (subscriptionStore.hasAccess || hasUnlockedCurrentLevel.value) return false
  // L'utilisateur n'a pas d'accès → niveaux bloqués
  return true
})

function openSubscriptionPrompt() {
  if (shouldShowSubscriptionPrompt.value) {
    showSubscriptionPrompt.value = true
  }
}

function handleSubscriptionPromptClose() {
  showSubscriptionPrompt.value = false
  // Relancer le timer pour réapparition dans 2 min
  clearSubscriptionPromptTimer()
  if (shouldShowSubscriptionPrompt.value) {
    subscriptionPromptTimer = setTimeout(openSubscriptionPrompt, SUBSCRIPTION_PROMPT_INTERVAL)
  }
}

function clearSubscriptionPromptTimer() {
  if (subscriptionPromptTimer) {
    clearTimeout(subscriptionPromptTimer)
    subscriptionPromptTimer = null
  }
}

function initSubscriptionPrompt() {
  clearSubscriptionPromptTimer()
  if (shouldShowSubscriptionPrompt.value) {
    // Afficher immédiatement au chargement du dashboard
    showSubscriptionPrompt.value = true
  }
}

const lastActivity = computed(() => {
  if (!statuses.value.length) return null
  const sorted = [...statuses.value].sort((a, b) => new Date(b.date_creation) - new Date(a.date_creation))
  return sorted[0]
})

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

function goToLastChapter() {
  if (!lastActivity.value || !lastActivity.value.chapitreId) return
  router.push({ name: 'Exercices', params: { chapitreId: String(lastActivity.value.chapitreId) } })
}

function formatInvitationDate(iso) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString('fr-FR', {
      day: '2-digit',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return ''
  }
}

async function respondToInvitation(action) {
  if (!activeInvitation.value || processingAction.value) return
  processingAction.value = action
  invitationError.value = false
  invitationFeedback.value = ''
  try {
    const res = await respondParentInvitation(activeInvitation.value.link_id, action)
    invitationFeedback.value = res?.data?.message || (action === 'accept' ? 'Invitation acceptée' : 'Invitation refusée')
    const targetIndex = activeInvitationIndex.value
    setTimeout(() => {
      invitations.value.splice(targetIndex, 1)
      if (!invitations.value.length) {
        showInvitationModal.value = false
      } else if (activeInvitationIndex.value >= invitations.value.length) {
        activeInvitationIndex.value = 0
      }
      invitationFeedback.value = ''
      processingAction.value = ''
    }, 1200)
  } catch (error) {
    invitationError.value = true
    invitationFeedback.value = error?.response?.data?.message || "Action impossible pour le moment"
    processingAction.value = ''
  }
}

function lockScroll(lock) {
  if (lock) {
    lockBodyScroll('dashboard-student-invitation', { mode: 'overflow' })
  } else {
    unlockBodyScroll('dashboard-student-invitation')
  }
}

watch(showInvitationModal, (visible) => {
  lockScroll(visible)
  if (!visible) {
    invitationFeedback.value = ''
    invitationError.value = false
  }
})

onBeforeUnmount(() => {
  lockScroll(false)
  clearSubscriptionPromptTimer()
})

onBeforeRouteLeave((to, from, next) => {
  if (showInvitationModal.value) {
    invitationError.value = true
    invitationFeedback.value = 'Répondez à la demande d’accès avant de continuer.'
    next(false)
  } else {
    next()
  }
})

const normalizeList = (val) => Array.isArray(val) ? val : (val?.results || [])

const runDashboardLoad = async () => {
  if (!isAuthenticated.value) {
    return
  }
  try {
    const [stResponse, mResponse, gam, ov, invitationsResponse] = await Promise.all([
      getStatuses(),
      getMatieres(),
      fetchUserGamification().catch(() => null),
      fetchMyOverview().catch(() => null),
      fetchParentInvitations().catch(() => null)
    ])

    statuses.value = normalizeList(stResponse?.data)
    matieres.value = normalizeList(mResponse?.data ?? mResponse)
    overview.value = ov?.data?.data || null

    // Gamification (optionnelle)
    const gamData = gam?.data?.data
    if (gamData) {
      userStore.xp = gamData.xp ?? userStore.xp
      userStore.level = gamData.level ?? userStore.level
      userStore.xp_to_next = gamData.xp_to_next ?? (gamData.next_level_xp - gamData.xp)
    }

    // Stats fiables basées sur est_correct
    stats.value.done = statuses.value.length
    stats.value.acquired = statuses.value.filter(s => s.est_correct === true).length
    stats.value.not_acquired = statuses.value.filter(s => s.est_correct === false).length

    const inviteList = invitationsResponse?.data?.data?.invitations || []
    if (inviteList.length) {
      invitations.value = inviteList
      showInvitationModal.value = true
      activeInvitationIndex.value = 0
    }
  } catch {}
}

onMounted(async () => {
  if (isAuthenticated.value) {
    runDashboardLoad()
    // Forcer le chargement du statut d'abonnement (même si récemment chargé)
    await subscriptionStore.fetchStatus({ force: true })
    initSubscriptionPrompt()
  }
})

watch(isAuthenticated, async (authed) => {
  if (authed) {
    runDashboardLoad()
    await subscriptionStore.fetchStatus()
    initSubscriptionPrompt()
  } else {
    // Nettoyer les données affichées lorsque l'utilisateur se déconnecte
    stats.value = { done: 0, acquired: 0, not_acquired: 0 }
    statuses.value = []
    matieres.value = []
    overview.value = null
    invitations.value = []
    showInvitationModal.value = false
    activeInvitationIndex.value = 0
    clearSubscriptionPromptTimer()
    showSubscriptionPrompt.value = false
  }
})

watch(shouldShowSubscriptionPrompt, (canShow) => {
  if (!canShow) {
    showSubscriptionPrompt.value = false
    clearSubscriptionPromptTimer()
  }
})
</script>

<style scoped>
.dashboard-content {
  margin-bottom: 1.5rem;
  padding-bottom: 40px;
}

.dashboard-center-top {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.dashboard-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.parent-invite-overlay {
  position: fixed;
  inset: 0;
  z-index: 1200;
  background: rgba(15, 23, 42, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  backdrop-filter: blur(2px);
}

.parent-invite-modal {
  width: min(480px, 92vw);
  background: #fff;
  border-radius: 18px;
  padding: 2rem 1.75rem;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.25);
}

.parent-invite-modal h2 {
  margin: 0 0 .8rem;
  font-size: 1.45rem;
  font-weight: 800;
  color: #0f172a;
}

.invite-lead {
  margin: .5rem 0 .75rem;
  color: #334155;
  line-height: 1.5;
}

.invitation-email {
  margin: .25rem 0;
  color: #475569;
}

.invitation-email span {
  font-weight: 700;
  color: #1d4ed8;
}

.invitation-date {
  margin: .25rem 0 .85rem;
  color: #64748b;
  font-size: .9rem;
}

.invitation-question {
  margin: 1rem 0 .4rem;
  font-weight: 700;
  color: #0f172a;
}

.invitation-actions {
  display: flex;
  gap: .75rem;
  margin-top: 1.25rem;
}

.invitation-actions .btn {
  flex: 1;
  padding: .7rem 1rem;
  border-radius: 10px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: transform .15s ease, background .2s ease;
}

.invitation-actions .btn.accept {
  background: #10b981;
  color: #fff;
}

.invitation-actions .btn.accept:hover {
  background: #0f9d74;
}

.invitation-actions .btn.decline {
  background: #f1f5f9;
  color: #0f172a;
  border: 1px solid #cbd5f5;
}

.invitation-actions .btn.decline:hover {
  background: #e2e8f0;
}

.invitation-actions .btn:disabled {
  opacity: .65;
  cursor: not-allowed;
  transform: none;
}

.invitation-feedback {
  margin-top: 1rem;
  text-align: center;
  font-size: .95rem;
  font-weight: 600;
  color: #047857;
}

.invitation-feedback.error {
  color: #b91c1c;
}



/* Quick actions */
/* Leaderboard section */
.leaderboard-section {
  margin-bottom: 1.5rem;
}

.leaderboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

.leaderboard-container {
  margin: 0;
}

.level-container {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}




.quick-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin-top: 1.25rem;
}

.quick-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 6px rgba(30,41,59,0.06);
}

.quick-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: .75rem;
}

.quick-title {
  font-weight: 700;
  color: #1f2937;
}

.quick-meta {
  font-weight: 700;
  color: #2563eb;
}

.quick-body { margin-top: .5rem; }
.quick-line { display: flex; gap:.5rem; align-items: baseline; }
.quick-label { color:#64748b; font-weight:600; font-size:.9rem; }
.quick-value { color:#334155; font-weight:600; }

.quick-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: .5rem .9rem;
  font-weight: 600;
  cursor: pointer;
}
.quick-btn:hover { background:#1e40af; }

.progress-bar { height: 10px; background:#eef2ff; border-radius: 999px; overflow: hidden; margin-top:.5rem; }
.progress-fill { height: 100%; background:#6366f1; width: 0; transition: width .3s ease; }
.progress-hint { color:#64748b; font-size:.875rem; margin-top:.5rem; }
.progress-bar.small { height: 8px; margin-top: 6px; }

/* Sections */
.section { margin-top: 1.25rem; }
.section-header { display:flex; align-items:center; justify-content:space-between; margin-bottom: .5rem; }
.section-title { margin:0; font-size:1.1rem; font-weight:800; color:#1f2937; }

/* Math Run card */
.math-run-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #0a1628 0%, #1e3a8a 100%);
  border: 1px solid #2563eb;
  border-radius: 14px;
  padding: 16px 20px;
  text-decoration: none;
  transition: transform 0.15s, box-shadow 0.15s;
}
.math-run-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(37,99,235,0.25);
}
.math-run-card-left { display: flex; align-items: center; gap: 14px; }
.math-run-card-emoji { font-size: 32px; }
.math-run-card-title { color: #ffd54f; font-weight: 700; font-size: 15px; }
.math-run-card-sub { color: #93c5fd; font-size: 13px; margin-top: 2px; }
.math-run-card-badge {
  background: #2563eb;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  padding: 6px 16px;
  border-radius: 20px;
}

/* Single card container (pour remplacer quick-grid quand il n'y a qu'un seul élément) */
.single-card-container {
  display: flex;
  width: 100%;
}

/* Activity */


@media (max-width: 1000px) {
  .leaderboard-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .quick-grid { grid-template-columns: 1fr; }
}
</style>
