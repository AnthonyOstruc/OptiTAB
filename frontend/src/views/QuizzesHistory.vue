<template>
  <DashboardLayout>
    <div class="history-page">
      <h2 class="page-title">Historique complet des quiz</h2>

      <BaseHistory
        title="🧠 Historique des Quiz"
        list-title="📝 Tous mes quiz"
        loading-text="Chargement de l'historique..."
        api-endpoint="/api/suivis/quiz/stats/"
        :items-per-page="20"
        :navigation-handler="navigateToQuiz"
        :custom-filters="masteryFilters"
        :filtered-items="filteredQuizList"
        @data-loaded="onDataLoaded"
      >
        <!-- Tableau résumé matière/notion -->
        <template #matiere-notion-stats>
          <div class="summary-table">
            <div class="summary-header">
              <div>Matière</div>
              <div>Notion</div>
              <div class="sortable-header" @click="sortBy('count')">
                Faits
                <span class="sort-icon" :class="{ active: sortField === 'count' }">
                  {{ sortField === 'count' && sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </div>
              <div class="sortable-header" @click="sortBy('correct_count')">
                Réussis
                <span class="sort-icon" :class="{ active: sortField === 'correct_count' }">
                  {{ sortField === 'correct_count' && sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </div>
              <div class="sortable-header" @click="sortBy('incorrect_count')">
                Ratés
                <span class="sort-icon" :class="{ active: sortField === 'incorrect_count' }">
                  {{ sortField === 'incorrect_count' && sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </div>
              <div class="sortable-header" @click="sortBy('average_percent')">
                Moyenne
                <span class="sort-icon" :class="{ active: sortField === 'average_percent' }">
                  {{ sortField === 'average_percent' && sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </div>
            </div>

            <template v-for="row in sortedStats" :key="`${row.matiere.id}-${row.notion.id}`">
              <div class="summary-row">
                <div class="cell matiere">{{ row.matiere.titre }}</div>
                <div class="cell notion">
                  <button class="notion-toggle" @click="toggleNotionDetails(row)">
                    <span class="notion-label">{{ row.notion.titre }}</span>
                    <svg class="chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ expanded: isNotionExpanded(row) }">
                      <polyline points="6,9 12,15 18,9"></polyline>
                    </svg>
                  </button>
                </div>
                <div class="cell count">{{ row.count }}</div>
                <div class="cell correct">{{ row.correct_count }}</div>
                <div class="cell incorrect">{{ row.incorrect_count }}</div>
                <div class="cell average" :class="getAverageClass(row.average_percent)">{{ formatAverage(row.average_percent) }}</div>
              </div>

              <div v-if="isNotionExpanded(row)" class="summary-details-row">
                <div class="details-cell">
                  <div class="chapter-table">
                    <div class="chapter-header">
                      <div>Chapitre</div>
                      <div>Faits</div>
                      <div>Réussis</div>
                      <div>Ratés</div>
                      <div>Réussite</div>
                      <div>Moyenne</div>
                    </div>
                    <div v-if="getNotionDetails(row).loading" class="chapter-loading">Chargement des détails...</div>
                    <div v-else-if="getNotionDetails(row).error" class="chapter-error">{{ getNotionDetails(row).error }}</div>
                    <div v-else>
                      <div v-for="ch in getNotionDetails(row).chapters" :key="ch.chapitre.id" class="chapter-row">
                        <div class="cell chapitre">{{ ch.chapitre.titre }}</div>
                        <div class="cell count">{{ ch.count }}</div>
                        <div class="cell correct">{{ ch.correct_count }}</div>
                        <div class="cell incorrect">{{ ch.incorrect_count }}</div>
                        <div class="cell ratio">{{ Math.round(ch.ratio_percent) }}%</div>
                        <div class="cell average" :class="getAverageClass(ch.average_percent)">{{ (Math.round(ch.average_10 * 10) / 10) }}/10</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </template>

        <!-- Filtres personnalisés (même UI que dashboard) -->
        <template #custom-filters="{ filters, selected }">
          <button 
            v-for="filter in filters" 
            :key="filter.value"
            @click="updateSelectedMastery(filter.value)"
            :class="['inline-mastery-btn', { active: selectedMastery === filter.value }, filter.class]"
          >
            <span v-if="filter.icon" class="inline-mastery-icon">{{ filter.icon }}</span>
            <span class="inline-mastery-label">{{ filter.label }}</span>
          </button>
        </template>

        <!-- Liste des items (même rendu que sur le dashboard) -->
        <template #items-list="{ items, toggleDetails, isExpanded, navigateToItem }">
          <div v-for="quiz in items" :key="quiz.id" class="quiz-card" :class="{ 'multiple-attempts': quiz.total_attempts > 1, locked: isQuizLocked(quiz) }">
            <div class="quiz-card-header" @click="toggleDetails(quiz.id)">
              <div class="quiz-card-title-section">
                <h5 class="quiz-card-title clickable-title" :class="{ locked: isQuizLocked(quiz) }" @click.stop="onNavigate(quiz)" :title="isQuizLocked(quiz) ? 'Verrouillé' : ('Accéder au quiz: ' + quiz.quiz_titre)">
                  {{ quiz.quiz_titre }}
                  <svg class="navigation-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M7 17l9.2-9.2M17 17V7H7"></path>
                  </svg>
                </h5>
                <div class="quiz-breadcrumb-compact">
                  {{ quiz.matiere.titre }} → {{ quiz.notion.titre }}
                </div>
              </div>
              <div class="quiz-card-actions">
                <div v-if="isQuizLocked(quiz)" class="lock-badge" :title="getCooldownLabel(quiz)">🔒 {{ getCooldownLabel(quiz) }}</div>
                <div v-else class="quiz-score" :class="getScoreClass(quiz.score_on_10)">
                  {{ quiz.score_on_10 }}/10
                  <span v-if="quiz.total_attempts > 1" class="retry-indicator">↻</span>
                </div>
                <button class="expand-toggle" :class="{ expanded: isExpanded(quiz.id) }">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="6,9 12,15 18,9"></polyline>
                  </svg>
                </button>
              </div>
            </div>

            <div v-if="isExpanded(quiz.id)" class="quiz-card-details">
              <div class="quiz-breadcrumb">
                <span class="breadcrumb-item">{{ quiz.matiere.titre }}</span>
                <span class="breadcrumb-separator">→</span>
                <span class="breadcrumb-item">{{ quiz.notion.titre }}</span>
                <span class="breadcrumb-separator">→</span>
                <span class="breadcrumb-item">{{ quiz.chapitre.titre }}</span>
              </div>
              <div class="quiz-meta">
                <span class="quiz-attempt">
                  Tentative #{{ quiz.tentative_numero }}
                  <span v-if="quiz.total_attempts > 1" class="total-attempts">({{ quiz.total_attempts }} au total)</span>
                </span>
                <span class="quiz-date">{{ formatDate(quiz.date_creation) }}</span>
                <span class="quiz-time" v-if="quiz.temps_total_seconde">{{ formatTime(quiz.temps_total_seconde) }}</span>
              </div>
            </div>
          </div>
        </template>
      </BaseHistory>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BaseHistory from '@/components/dashboard/BaseHistory.vue'
import apiClient from '@/api/client'
import { checkQuizCooldown } from '@/api/quiz'

const router = useRouter()

// Filtres de maîtrise comme sur le dashboard
const selectedMastery = ref('all')
const masteryFilters = [
  { value: 'all', label: 'Tous', icon: '', class: 'all' },
  { value: 'mastered', label: 'Maîtrisés', icon: '✅', class: 'mastered' },
  { value: 'average', label: 'Moyens', icon: '⚠️', class: 'average' },
  { value: 'poor', label: 'Non maîtrisés', icon: '❌', class: 'poor' }
]

const navigateToQuiz = (quiz) => {
  const chapitreId = quiz?.chapitre?.id
  const quizId = quiz?.quiz_id
  if (!chapitreId) return
  router.push({ path: `/quiz-exercices/${chapitreId}`, query: { quizId, autoStart: 'true' } })
}

// Données pour le tableau résumé et les détails
const currentQuizList = ref([])
const matiereNotionStats = ref([])
const sortField = ref('count')
const sortDirection = ref('desc')
const expandedNotions = ref(new Set())
const notionDetails = ref({})
const cooldownByQuizId = ref(new Map())

const onDataLoaded = (data) => {
  const list = Array.isArray(data.quiz_list) ? data.quiz_list : []
  currentQuizList.value = list
  matiereNotionStats.value = computeMatiereNotionFromQuizList(list)
  loadCooldowns(list)
}

// Liste filtrée selon la maîtrise (pour 20/page)
const filteredQuizList = computed(() => {
  let filtered = currentQuizList.value
  if (selectedMastery.value !== 'all') {
    filtered = filtered.filter(quiz => {
      const score = Number(quiz.score_on_10 || 0)
      switch (selectedMastery.value) {
        case 'mastered':
          return score >= 7
        case 'average':
          return score >= 5 && score < 7
        case 'poor':
          return score < 5
        default:
          return true
      }
    })
  }
  return filtered
})

const sortedStats = computed(() => {
  const rows = matiereNotionStats.value || []
  return [...rows].sort((a, b) => {
    const aVal = a[sortField.value] || 0
    const bVal = b[sortField.value] || 0
    return sortDirection.value === 'asc' ? aVal - bVal : bVal - aVal
  })
})

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
}

const formatAverage = (average) => {
  if (average === 0) return '0%'
  return `${Math.round(average)}%`
}

const getAverageClass = (average) => {
  if (average >= 90) return 'excellent'
  if (average >= 75) return 'good'
  if (average >= 50) return 'average'
  return 'poor'
}

const loadCooldowns = async (list) => {
  const map = new Map(cooldownByQuizId.value)
  await Promise.all((list || []).map(async (q) => {
    try {
      const info = await checkQuizCooldown(q.quiz_id)
      map.set(q.quiz_id, info)
    } catch (_) {}
  }))
  cooldownByQuizId.value = map
}

const isQuizLocked = (quiz) => {
  const info = cooldownByQuizId.value.get(quiz.quiz_id)
  return info && info.can_attempt === false
}

const getCooldownLabel = (quiz) => {
  const info = cooldownByQuizId.value.get(quiz.quiz_id)
  if (!info || info.can_attempt !== false) return ''
  return info.time_remaining_formatted || info.message || 'Verrouillé'
}

const onNavigate = (quiz) => {
  if (isQuizLocked(quiz)) {
    alert(getCooldownLabel(quiz) || 'Quiz verrouillé')
    return
  }
  navigateToQuiz(quiz)
}

const updateSelectedMastery = (value) => {
  selectedMastery.value = value
}

// Score badge style on list items
const getScoreClass = (score) => {
  if (score >= 7) return 'score-good'
  if (score >= 5) return 'score-average'
  return 'score-poor'
}

// Expansion notion → chapitres
const buildNotionKey = (row) => `${row.matiere.id}-${row.notion.id}`
const isNotionExpanded = (row) => expandedNotions.value.has(buildNotionKey(row))
const getNotionDetails = (row) => {
  const key = buildNotionKey(row)
  if (!notionDetails.value[key]) {
    notionDetails.value[key] = { loading: false, error: '', chapters: [] }
  }
  return notionDetails.value[key]
}
const toggleNotionDetails = async (row) => {
  const key = buildNotionKey(row)
  if (expandedNotions.value.has(key)) {
    expandedNotions.value.delete(key)
    return
  }
  expandedNotions.value.add(key)
  const details = getNotionDetails(row)
  if (details.chapters && details.chapters.length > 0) return
  await fetchNotionChapterDetails(row.matiere.id, row.notion.id)
}
const fetchNotionChapterDetails = async (matiereId, notionId) => {
  const key = `${matiereId}-${notionId}`
  notionDetails.value[key] = { loading: true, error: '', chapters: [] }
  try {
    const response = await apiClient.get('/api/suivis/quiz/stats/', { params: { matiere: matiereId, notion: notionId } })
    const list = Array.isArray(response?.data?.quiz_list) ? response.data.quiz_list : []
    const chapters = computeChapterStats(list)
    notionDetails.value[key] = { loading: false, error: '', chapters }
  } catch (error) {
    const message = (error?.response?.data?.error) || 'Erreur lors du chargement des détails'
    notionDetails.value[key] = { loading: false, error: message, chapters: [] }
  }
}

// Calculs d'agrégats
const computeMatiereNotionFromQuizList = (quizList) => {
  const map = new Map()
  for (const item of quizList) {
    const mat = item?.matiere || {}
    const not = item?.notion || {}
    const key = `${mat.id}-${not.id}`
    if (!map.has(key)) {
      map.set(key, {
        matiere: { id: mat.id, titre: mat.titre || '' },
        notion: { id: not.id, titre: not.titre || '' },
        count: 0,
        correct_count: 0,
        incorrect_count: 0,
      })
    }
    const agg = map.get(key)
    agg.count += 1
    if ((item.score_on_10 || 0) >= 7) agg.correct_count += 1
    else agg.incorrect_count += 1
  }
  const rows = Array.from(map.values()).map(r => ({
    ...r,
    average_percent: r.count > 0 ? (r.correct_count / r.count) * 100 : 0
  }))
  rows.sort((a, b) => String(a.matiere.titre).localeCompare(String(b.matiere.titre), 'fr', { sensitivity: 'base' }) || String(a.notion.titre).localeCompare(String(b.notion.titre), 'fr', { sensitivity: 'base' }))
  return rows
}

const computeChapterStats = (quizList) => {
  const map = new Map()
  for (const item of quizList) {
    const chap = item?.chapitre || {}
    const chapId = chap?.id
    if (!chapId) continue
    if (!map.has(chapId)) {
      map.set(chapId, {
        chapitre: { id: chapId, titre: chap?.titre || 'Chapitre' },
        count: 0,
        correct_count: 0,
        incorrect_count: 0,
        sum_score_10: 0,
      })
    }
    const agg = map.get(chapId)
    agg.count += 1
    agg.sum_score_10 += Number(item.score_on_10 || 0)
    if ((item.score_on_10 || 0) >= 7) agg.correct_count += 1
    else agg.incorrect_count += 1
  }
  const chapters = Array.from(map.values()).map(ch => {
    const ratio = ch.count > 0 ? (ch.correct_count / ch.count) : 0
    const avg10 = ch.count > 0 ? ch.sum_score_10 / ch.count : 0
    return {
      ...ch,
      ratio_percent: ratio * 100,
      average_10: Math.round(avg10 * 10) / 10,
      average_percent: ratio * 100,
    }
  })
  chapters.sort((a, b) => String(a.chapitre.titre).localeCompare(String(b.chapitre.titre), 'fr', { sensitivity: 'base' }))
  return chapters
}

// Formatting helpers for list metadata
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.history-page { padding: 1rem 0; }
.page-title { font-weight: 800; margin-bottom: 1rem; }

/* Tableau résumé matière/notion (comme dashboard) */
.summary-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  margin-bottom: 1.25rem;
}
.summary-header,
.summary-row {
  display: grid;
  grid-template-columns: 1.5fr 2fr 0.8fr 0.8fr 0.8fr 0.8fr;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  align-items: center;
}
.summary-header { background: #f9fafb; font-weight: 700; color: #374151; }
.summary-row:not(:last-child) { border-bottom: 1px solid #f3f4f6; }
.summary-row .cell { font-size: 0.875rem; color: #374151; }
.summary-row .cell.count,
.summary-row .cell.correct,
.summary-row .cell.incorrect { text-align: center; font-weight: 600; }
.summary-row .cell.correct { color: #059669; }
.summary-row .cell.incorrect { color: #dc2626; }

.summary-row .cell.average { font-weight: 700; text-align: center; padding: 0.25rem 0.5rem; border-radius: 4px; }
.summary-row .cell.average.excellent { color: #16a34a; background: #dcfce7; }
.summary-row .cell.average.good { color: #2563eb; background: #dbeafe; }
.summary-row .cell.average.average { color: #d97706; background: #fef3c7; }
.summary-row .cell.average.poor { color: #dc2626; background: #fee2e2; }

.sortable-header { display: flex; align-items: center; justify-content: center; cursor: pointer; user-select: none; padding: 0.25rem; border-radius: 4px; gap: 0.35rem; }
.sortable-header:hover { background-color: #f3f4f6; }
.sort-icon { font-size: 1rem; color: #6b7280; font-weight: 700; }
.sort-icon.active { color: #2563eb; font-weight: 700; }

@media (max-width: 768px) {
  .summary-header, .summary-row { grid-template-columns: 1fr 1fr 0.7fr 0.7fr 0.7fr 0.7fr; padding: 0.5rem 0.75rem; }
}

/* Notion toggle + détails */
.notion-toggle { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.15rem 0.4rem; border: 1px solid transparent; border-radius: 6px; background: transparent; cursor: pointer; color: #1f2937; }
.notion-toggle:hover { background: #f3f4f6; }
.notion-toggle .chevron { transition: transform 0.2s; color: #6b7280; }
.notion-toggle .chevron.expanded { transform: rotate(180deg); color: #374151; }

.summary-details-row { display: block; padding: 0 0.5rem 0.75rem 0.5rem; border-bottom: 1px solid #f3f4f6; }
.summary-details-row .details-cell { grid-column: 1 / -1; }
.chapter-table { border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb; overflow: hidden; }
.chapter-header, .chapter-row { display: grid; grid-template-columns: 2fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr; gap: 0.75rem; padding: 0.5rem 0.75rem; align-items: center; }
.chapter-header { background: #eef2f7; font-weight: 600; color: #374151; }
.chapter-row { background: #fff; border-top: 1px solid #f3f4f6; }
.chapter-loading { padding: 0.75rem; color: #6b7280; font-size: 0.85rem; }
.chapter-error { padding: 0.75rem; color: #dc2626; font-size: 0.85rem; }
.chapter-row .cell { font-size: 0.85rem; }
.chapter-row .cell.count, .chapter-row .cell.correct, .chapter-row .cell.incorrect, .chapter-row .cell.ratio, .chapter-row .cell.average { text-align: center; font-weight: 600; }
.chapter-row .cell.correct { color: #16a34a; }
.chapter-row .cell.incorrect { color: #dc2626; }

@media (max-width: 768px) {
  .chapter-header, .chapter-row { grid-template-columns: 1.4fr 0.7fr 0.7fr 0.7fr 0.7fr 0.7fr; padding: 0.45rem 0.5rem; }
}

/* Filtres personnalisés */
.inline-mastery-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  color: #6b7280;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  min-height: 28px;
}
.inline-mastery-btn:hover { border-color: #d1d5db; background: #f9fafb; }
.inline-mastery-btn.active { background: #3b82f6; border-color: #3b82f6; color: white; font-weight: 600; }
.inline-mastery-icon { font-size: 0.75rem; }
.inline-mastery-label { font-size: 0.75rem; }

/* Cartes de quiz (identique au dashboard) */
.quiz-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; transition: all 0.2s; }
.quiz-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.quiz-card.multiple-attempts { border-left: 3px solid #f59e0b; }
.quiz-card.locked { opacity: .75; cursor: not-allowed; border-left: 3px solid #f59e0b; }
.clickable-title.locked { cursor: not-allowed; }
.lock-badge { font-size: .8rem; font-weight: 700; color: #92400e; background: #fef3c7; padding: .25rem .4rem; border-radius: 4px; }
.quiz-card-header { display: flex; justify-content: space-between; align-items: flex-start; cursor: pointer; padding: 0.5rem; margin: -0.5rem -0.5rem 0.75rem -0.5rem; border-radius: 6px; transition: background-color 0.2s; }
.quiz-card-header:hover { background-color: #f8fafc; }
.quiz-card-title-section { flex: 1; }
.quiz-card-actions { display: flex; align-items: center; gap: 0.5rem; }
.quiz-card-title { font-size: 0.9rem; font-weight: 600; color: #1f2937; margin: 0 0 0.25rem 0; }
.clickable-title { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; padding: 0.25rem; margin: -0.25rem; border-radius: 4px; transition: all 0.2s; }
.clickable-title:hover { color: #3b82f6; background: #f0f9ff; }
.navigation-icon { opacity: 0; transition: opacity 0.2s; flex-shrink: 0; }
.clickable-title:hover .navigation-icon { opacity: 1; }
.quiz-breadcrumb-compact { font-size: 0.7rem; color: #6b7280; font-weight: 500; }
.quiz-score { font-size: 0.9rem; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 4px; }
.expand-toggle { background: none; border: none; cursor: pointer; padding: 0.25rem; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #6b7280; transition: all 0.2s; }
.expand-toggle:hover { background-color: #e5e7eb; color: #374151; }
.expand-toggle svg { transition: transform 0.2s; }
.expand-toggle.expanded svg { transform: rotate(180deg); }
.quiz-score.score-good { background: #dcfce7; color: #166534; }
.quiz-score.score-average { background: #fef3c7; color: #92400e; }
.quiz-score.score-poor { background: #fecaca; color: #991b1b; }
.retry-indicator { margin-left: 0.25rem; font-size: 0.8rem; opacity: 0.7; }
.quiz-card-details { border-top: 1px solid #f3f4f6; padding-top: 0.75rem; margin-top: 0.5rem; animation: slideDown 0.2s ease-out; }
@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
.quiz-breadcrumb { font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; }
.breadcrumb-item { font-weight: 500; }
.breadcrumb-separator { margin: 0 0.25rem; }
.quiz-meta { display: flex; gap: 1rem; font-size: 0.75rem; color: #9ca3af; }

</style>


