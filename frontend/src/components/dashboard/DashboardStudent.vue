<template>
  <div class="dashboard-content">
    <!-- Notification de reset gamification -->
    <GameResetNotification />
    
    <div class="dashboard-center-top">
      <div v-if="userStore.isLoading" class="dashboard-spinner">
        <span class="spinner"></span>
      </div>
      <h1 v-else>
        Bienvenue {{ userStore.firstName }} sur votre tableau de bord
      </h1>
    </div>
    
    <!-- Classement + Niveau + Objectifs -->
    <div class="section leaderboard-section">
      <div class="leaderboard-grid">
        <div class="leaderboard-container">
          <LeaderboardWidget />
        </div>
        <div class="level-container">
          <XPBadges />
          <DailyObjectives />
        </div>
      </div>
    </div>



    <!-- Historique des quiz avec filtres -->
    <div v-if="!loadingStats">
      <QuizHistory />
    </div>

    <!-- Historique des exercices avec filtres -->
    <div v-if="!loadingStats">
      <ExercicesHistory />
    </div>
    
    <div v-if="loadingStats" class="dashboard-spinner"><span class="spinner"></span></div>









    <!-- Composant de test pour le système de streak (à supprimer en production) -->
    <div v-if="userStore.isAdmin" class="section">
      <div class="section-header">
        <h3 class="section-title">🧪 Tests (Admin uniquement)</h3>
      </div>
      <StreakTestButton />
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjects/index'
import { getStatuses, getExercices, getChapitres, getMatieres } from '@/api'
import { fetchUserGamification, fetchMyOverview } from '@/api/users'
import LeaderboardWidget from '@/components/dashboard/LeaderboardWidget.vue'





import XPBadges from '@/components/dashboard/XPBadges.vue'
import GameResetNotification from '@/components/notifications/GameResetNotification.vue'
import QuizHistory from '@/components/dashboard/QuizHistory.vue'
import ExercicesHistory from '@/components/dashboard/ExercicesHistory.vue'
import DailyObjectives from '@/components/dashboard/DailyObjectives.vue'


import StreakTestButton from '@/components/debug/StreakTestButton.vue'

const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const router = useRouter()

const stats = ref({ done: 0, acquired: 0, not_acquired: 0 })
const loadingStats = ref(true)
const statuses = ref([])

const exercices = ref([])
const chapitres = ref([])
const exercicesIndex = ref({})
const chapitresIndex = ref({})
const matieres = ref([])
const overview = ref(null)

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

function buildIndexes() {
  exercicesIndex.value = Object.fromEntries(exercices.value.map(e => [e.id, e]))
  chapitresIndex.value = Object.fromEntries(chapitres.value.map(c => [c.id, c]))
}



function goToLastChapter() {
  if (!lastActivity.value || !lastActivity.value.chapitreId) return
  router.push({ name: 'Exercices', params: { chapitreId: String(lastActivity.value.chapitreId) } })
}



onMounted(async () => {
  try {
    const [ex, ch, stResponse, mResponse, gam, ov] = await Promise.all([
      getExercices({}),
      getChapitres({}),
      getStatuses(),
      getMatieres(),
      fetchUserGamification().catch(() => null),
      fetchMyOverview().catch(() => null)
    ])

    const normalizeList = (val) => Array.isArray(val) ? val : (val?.results || [])

    exercices.value = normalizeList(ex)
    chapitres.value = normalizeList(ch)
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

    buildIndexes()

    // Stats fiables basées sur est_correct
    stats.value.done = statuses.value.length
    stats.value.acquired = statuses.value.filter(s => s.est_correct === true).length
    stats.value.not_acquired = statuses.value.filter(s => s.est_correct === false).length


  } catch {}
  loadingStats.value = false
})
</script>

<style scoped>
.dashboard-content {
  margin-bottom: 1.5rem;
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


