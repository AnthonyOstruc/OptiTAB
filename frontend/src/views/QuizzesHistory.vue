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
        :filtered-items="filteredQuizList"
        @data-loaded="onDataLoaded"
      >
        <!-- Tableau résumé matière/notion -->
        <template #matiere-notion-stats>
          <!-- Version Desktop : Tableau -->
          <div class="summary-table desktop-only">
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
            <template v-for="row in pagedSummaryRows" :key="`${row.matiere.id}-${row.notion.id}`">
              <div class="summary-row">
                <div class="cell matiere">{{ row.matiere.titre }}</div>
                <div class="cell notion">
                  <span class="notion-label">{{ row.notion.titre }}</span>
                </div>
                <div class="cell count">{{ row.count }}</div>
                <div class="cell correct">{{ row.correct_count }}</div>
                <div class="cell incorrect">{{ row.incorrect_count }}</div>
                <div class="cell average" :class="getAverageClass(row.average_percent)">{{ formatAverage(row.average_percent) }}</div>
              </div>
            </template>
          </div>

          <!-- Version Mobile : Cartes -->
          <div class="summary-cards mobile-only">
            <div class="sort-controls">
              <span class="sort-label">Trier par :</span>
              <select v-model="sortField" @change="sortDirection = 'desc'" class="sort-select">
                <option value="count">Faits</option>
                <option value="correct_count">Réussis</option>
                <option value="incorrect_count">Ratés</option>
                <option value="average_percent">Moyenne</option>
              </select>
              <button class="sort-direction-btn" @click="sortDirection = sortDirection === 'asc' ? 'desc' : 'asc'" :title="sortDirection === 'asc' ? 'Croissant' : 'Décroissant'">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </button>
            </div>
            <template v-for="row in pagedSummaryRows" :key="`${row.matiere.id}-${row.notion.id}`">
              <div class="summary-card">
                <div class="card-header">
                  <div class="card-title">{{ row.notion.titre }}</div>
                  <div class="card-subtitle">{{ row.matiere.titre }}</div>
                </div>
                <div class="card-stats">
                  <div class="stat-item">
                    <span class="stat-label">Faits</span>
                    <span class="stat-value">{{ row.count }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Réussis</span>
                    <span class="stat-value success">{{ row.correct_count }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Ratés</span>
                    <span class="stat-value error">{{ row.incorrect_count }}</span>
                  </div>
                  <div class="stat-item highlight" :class="getAverageClass(row.average_percent)">
                    <span class="stat-label">Moyenne</span>
                    <span class="stat-value">{{ formatAverage(row.average_percent) }}</span>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- Pagination (partagée) -->
          <div v-if="summaryTotalPages > 1" class="summary-pagination">
            <button class="pg-btn" :disabled="summaryPage <= 1" @click="goToSummaryPage(summaryPage-1)">‹ Précédent</button>
            <button
              v-for="p in summaryVisiblePages"
              :key="p + '-p'"
              class="pg-page"
              :class="{ active: p === summaryPage, dots: p === '...' }"
              :disabled="p === '...'"
              @click="p !== '...' && goToSummaryPage(p)"
            >
              {{ p }}
            </button>
            <button class="pg-btn" :disabled="summaryPage >= summaryTotalPages" @click="goToSummaryPage(summaryPage+1)">Suivant ›</button>
          </div>
        </template>

        <!-- Liste des items -->
        <template #items-list="{ items, toggleDetails, isExpanded, navigateToItem }">
          <div 
            v-for="quiz in items" 
            :key="quiz.id" 
            class="quiz-card" 
            :class="{ 'multiple-attempts': quiz.total_attempts > 1 }"
            @click="navigateToItem(quiz)"
          >
            <div class="quiz-card-header">
              <div class="quiz-card-title-section">
                <h5 class="quiz-card-title clickable-title" :title="'Accéder au quiz: ' + quiz.quiz_titre">
                  {{ quiz.quiz_titre }}
                  <svg class="navigation-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M7 17l9.2-9.2M17 17V7H7"></path>
                  </svg>
                </h5>
                <div class="quiz-breadcrumb-compact">
                  {{ quiz.matiere?.titre || 'Matière' }} → {{ quiz.notion?.titre || 'Notion' }}
                </div>
              </div>
              <div class="quiz-card-actions">
                <div class="quiz-score" :class="getScoreClass(quiz.score_on_10)">
                  {{ quiz.score_on_10 }}/10
                  <span v-if="quiz.total_attempts > 1" class="retry-indicator">↻</span>
                </div>
                <button class="expand-toggle" :class="{ expanded: isExpanded(quiz.id) }" @click.stop="toggleDetails(quiz.id)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="6,9 12,15 18,9"></polyline>
                  </svg>
                </button>
              </div>
            </div>

            <div v-if="isExpanded(quiz.id)" class="quiz-card-details">
              <div class="quiz-breadcrumb">
                <span class="breadcrumb-item">{{ quiz.matiere?.titre || quiz.matiere?.nom || 'Matière' }}</span>
                <span class="breadcrumb-separator">→</span>
                <span class="breadcrumb-item">{{ quiz.theme?.titre || quiz.theme?.nom || 'Thème' }}</span>
                <span class="breadcrumb-separator">→</span>
                <span class="breadcrumb-item">{{ quiz.notion?.titre || quiz.notion?.nom || 'Notion' }}</span>
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

const router = useRouter()

const navigateToQuiz = (quiz) => {
  const chapitreId = quiz?.chapitre?.id
  const quizId = quiz?.quiz_id
  if (!chapitreId) return
  router.push({ path: `/quiz-exercices/${chapitreId}`, query: { quizId, autoStart: 'true' } })
}

// Données pour le tableau résumé
const currentQuizList = ref([])
const matiereNotionStats = ref([])
const sortField = ref('count')
const sortDirection = ref('desc')

// Pagination pour le tableau récapitulatif
const SUMMARY_PER_PAGE = 5
const summaryPage = ref(1)

const onDataLoaded = (data) => {
  const list = Array.isArray(data.quiz_list) ? data.quiz_list : []
  console.log('📊 Quiz data loaded:', data)
  console.log('📝 Quiz list:', list)
  if (list.length > 0) {
    console.log('🔍 Sample quiz:', list[0])
  }
  currentQuizList.value = list
  matiereNotionStats.value = computeMatiereNotionFromQuizList(list)
  console.log('📈 Matiere/Notion stats:', matiereNotionStats.value)
}

// Liste complète (pas de filtre de maîtrise)
const filteredQuizList = computed(() => {
  return currentQuizList.value
})

const sortedStats = computed(() => {
  const rows = matiereNotionStats.value || []
  return [...rows].sort((a, b) => {
    const aVal = a[sortField.value] || 0
    const bVal = b[sortField.value] || 0
    return sortDirection.value === 'asc' ? aVal - bVal : bVal - aVal
  })
})

const summaryTotalPages = computed(() => Math.ceil(sortedStats.value.length / SUMMARY_PER_PAGE) || 1)

const pagedSummaryRows = computed(() => {
  const start = (summaryPage.value - 1) * SUMMARY_PER_PAGE
  return sortedStats.value.slice(start, start + SUMMARY_PER_PAGE)
})

const summaryVisiblePages = computed(() => {
  const total = summaryTotalPages.value
  const current = summaryPage.value
  const pages = []
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else if (current <= 4) {
    pages.push(1,2,3,4,5,'...', total)
  } else if (current >= total - 3) {
    pages.push(1,'...', total-4, total-3, total-2, total-1, total)
  } else {
    pages.push(1,'...', current-1, current, current+1, '...', total)
  }
  return pages
})

const goToSummaryPage = (p) => {
  const t = Math.max(1, Math.min(summaryTotalPages.value, Number(p)))
  summaryPage.value = t
}

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

// Score badge style on list items
const getScoreClass = (score) => {
  if (score >= 7) return 'score-good'
  if (score >= 5) return 'score-average'
  return 'score-poor'
}

// Calculs d'agrégats
const computeMatiereNotionFromQuizList = (quizList) => {
  console.log('🔄 computeMatiereNotionFromQuizList called with', quizList.length, 'items')
  const map = new Map()
  for (const item of quizList) {
    const mat = item?.matiere || {}
    const not = item?.notion || {}
    console.log('📌 Item matiere:', mat, 'notion:', not)
    const key = `${mat.id}-${not.id}`
    if (!map.has(key)) {
      map.set(key, {
        matiere: { id: mat.id, titre: mat.titre || mat.nom || 'Matière' },
        notion: { id: not.id, titre: not.titre || not.nom || 'Notion' },
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
  console.log('📊 Computed rows:', rows)
  return rows
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

/* Affichage conditionnel Desktop/Mobile */
.desktop-only { display: block; }
.mobile-only { display: none; }

@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: block; }
}

/* Tableau résumé matière/notion Desktop */
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

/* Cartes Mobile */
.summary-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.sort-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.sort-select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 0.875rem;
  color: #1f2937;
}

.sort-direction-btn {
  padding: 0.5rem 0.75rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-direction-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.summary-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.summary-card .card-header {
  margin-bottom: 0.75rem;
}

.summary-card .card-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.summary-card .card-subtitle {
  font-size: 0.8rem;
  color: #6b7280;
}

.summary-card .card-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.summary-card .stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
  background: #f9fafb;
  border-radius: 6px;
}

.summary-card .stat-item.highlight {
  border: 2px solid;
  padding: 0.4rem;
}

.summary-card .stat-item.excellent {
  border-color: #16a34a;
  background: #dcfce7;
}

.summary-card .stat-item.good {
  border-color: #2563eb;
  background: #dbeafe;
}

.summary-card .stat-item.average {
  border-color: #d97706;
  background: #fef3c7;
}

.summary-card .stat-item.poor {
  border-color: #dc2626;
  background: #fee2e2;
}

.summary-card .stat-label {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.summary-card .stat-value {
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
}

.summary-card .stat-value.success {
  color: #059669;
}

.summary-card .stat-value.error {
  color: #dc2626;
}

/* Pagination */
.summary-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.pg-btn,
.pg-page {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.pg-btn:hover:not(:disabled),
.pg-page:hover:not(:disabled):not(.dots) {
  background: #f9fafb;
  border-color: #3b82f6;
  color: #3b82f6;
}

.pg-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pg-page.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
  font-weight: 600;
}

.pg-page.dots {
  border: none;
  background: transparent;
  cursor: default;
}

/* Cartes de quiz (identique au dashboard) */
.quiz-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; transition: all 0.2s; }
.quiz-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.quiz-card.multiple-attempts { border-left: 3px solid #f59e0b; }
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


