<template>
  <BaseHistory
    title="🧠 Historique des Quiz"
    list-title="📝 Quiz effectués"
    loading-text="Chargement des quiz..."
    api-endpoint="/api/suivis/quiz/stats/"
    :extra-params="{ limit: 6 }"
    :custom-filters="[]"
    :navigation-handler="navigateToQuiz"
    :items-per-page="6"
    :matiere-notion-stats-override="matiereNotionStats"
    :disable-collapse="true"
    :filtered-items="filteredQuizList"
    @data-loaded="onDataLoaded"
    @filter-changed="onFilterChanged"
  >
    <!-- Actions en-tête: bouton Voir l'historique complet -->
    <template #header-actions>
      <button class="view-history-btn" @click="goToFullHistory" title="Archive" aria-label="Archive">
        Archive
      </button>
    </template>
    <!-- Statistiques globales -->
    <template #global-stats="{ stats }">
      <div class="stats-grid">
        <div class="stat-card quiz-completed">
          <span class="stat-label">Quiz effectués</span>
          <span class="stat-value">{{ combinedStats.completed }}</span>
        </div>
        <div class="stat-card quiz-average">
          <span class="stat-label">Note moyenne</span>
          <span class="stat-value">{{ combinedStats.average }}/10</span>
        </div>
        <div class="stat-card quiz-notions">
          <span class="stat-label">Notions maîtrisées</span>
          <span class="stat-value">{{ combinedStats.masteredNotions }}</span>
        </div>
      </div>
    </template>

    <!-- Tableau récapitulatif matière / notion -->
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
          <div class="sortable-header" @click="sortBy('average_on_20')">
            Moyenne
            <span class="sort-icon" :class="{ active: sortField === 'average_on_20' }">
              {{ sortField === 'average_on_20' && sortDirection === 'asc' ? '↑' : '↓' }}
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
            <div class="cell average">
              <span class="avg-badge" :class="getAverageOn20Class(row.average_on_20)">{{ formatAverageOn20(row.average_on_20) }}</span>
            </div>
          </div>
        </template>

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
      </div>
    </template>

    <!-- Statistiques par matière -->
    <template #matiere-stats="{ stats }">
      <h4 class="section-subtitle">📊 Moyennes par matière</h4>
      <div class="matiere-grid">
        <div v-for="matiere in stats" :key="matiere.id" class="matiere-card">
          <div class="matiere-name">{{ matiere.titre }}</div>
          <div class="matiere-info">
            <span class="matiere-average">{{ matiere.average }}/10</span>
            <span class="matiere-count">{{ matiere.quiz_count }} quiz</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Liste des quiz -->
    <template #items-list="{ items, navigateToItem }">
      <div
        v-for="quiz in items"
        :key="quiz.id"
        class="quiz-card"
        :class="{ 'manual-quiz': quiz.is_manual }"
        @click="navigateToItem(quiz)"
      >
        <div class="quiz-card-content">
          <div class="quiz-info">
            <h5 class="quiz-card-title">{{ quiz.quiz_titre }}</h5>
            <div class="quiz-meta">
              {{ quiz.matiere.titre }} • {{ quiz.notion.titre }}
            </div>
          </div>
          <div class="quiz-score" :class="getScoreClass(getScoreOn10(quiz))">
            {{ formatScoreDisplay(quiz) }}
          </div>
        </div>
      </div>
    </template>

    <!-- État vide -->
    <template #empty-state>
      <p>Aucun quiz trouvé avec ces filtres</p>
    </template>
  </BaseHistory>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseHistory from './BaseHistory.vue'
import apiClient from '@/api/client'
import { getQuizSubmissions } from '@/api/quizSubmissions'
import { useUserStore } from '@/stores/user'

// Router
const router = useRouter()
const userStore = useUserStore()

const currentQuizList = ref([])
const matiereNotionStats = ref([])
const sortField = ref('count')
const sortDirection = ref('desc')
const SUMMARY_PER_PAGE = 5
const summaryPage = ref(1)

const roundToOneDecimal = (value) => Math.round(Number(value || 0) * 10) / 10

const sortByDateDesc = (list = []) => {
  return [...list].sort((a, b) => {
    const da = new Date(a?.date_creation || a?.created_at || 0).getTime()
    const db = new Date(b?.date_creation || b?.created_at || 0).getTime()
    return db - da
  })
}

const getScoreOn10 = (quiz) => {
  if (quiz?.manual_note != null) {
    return Number(quiz.manual_note) / 2
  }
  return Number(quiz?.score_on_10 || 0)
}

const formatScoreDisplay = (quiz) => {
  if (quiz?.is_manual && quiz?.manual_note != null) {
    return `${roundToOneDecimal(quiz.manual_note)}/20`
  }
  return `${roundToOneDecimal(getScoreOn10(quiz))}/10`
}

const buildMatiereFromQuiz = (quiz = {}) => {
  const mat = quiz?.notion?.theme?.matiere || quiz?.matiere
  if (mat && typeof mat === 'object') {
    return { id: mat.id ?? null, titre: mat.titre || mat.nom || 'Matière' }
  }
  if (mat) {
    return { id: mat, titre: 'Matière' }
  }
  return { id: null, titre: 'Matière' }
}

const buildNotionFromQuiz = (quiz = {}) => {
  const notion = quiz?.notion
  if (notion && typeof notion === 'object') {
    return { id: notion.id ?? null, titre: notion.titre || notion.nom || 'Notion' }
  }
  if (quiz?.notion_id) {
    return { id: quiz.notion_id, titre: 'Notion' }
  }
  return { id: null, titre: 'Notion' }
}

const buildChapitreFromQuiz = (quiz = {}) => {
  const chapitre = quiz?.chapitre
  if (chapitre && typeof chapitre === 'object') {
    return { id: chapitre.id ?? null, titre: chapitre.titre || 'Chapitre' }
  }
  if (quiz?.chapitre_id) {
    return { id: quiz.chapitre_id, titre: 'Chapitre' }
  }
  return { id: null, titre: 'Quiz' }
}

const mapManualSubmission = (submission = {}) => {
  const quiz = submission.quiz || {}
  const manualNote = submission?.note
  const fallbackDate = submission?.date_correction || submission?.date_creation || submission?.created_at || submission?.updated_at || new Date().toISOString()

  // Construire matiere avec le titre depuis la submission si disponible
  let matiere = buildMatiereFromQuiz(quiz)
  if (submission?.quiz_matiere_titre) {
    matiere = {
      id: quiz?.notion?.theme?.matiere?.id || matiere.id,
      titre: submission.quiz_matiere_titre
    }
  }

  // Construire notion avec le titre depuis la submission si disponible
  let notion = buildNotionFromQuiz(quiz)
  if (submission?.quiz_notion_titre) {
    notion = {
      id: quiz?.notion?.id || submission?.quiz?.notion?.id || notion.id,
      titre: submission.quiz_notion_titre
    }
  }

  return {
    id: `manual-${submission.id}`,
    quiz_id: quiz?.id || submission?.quiz_id || submission?.quizId,
    quiz_titre: submission?.quiz_titre || quiz?.titre || 'Quiz rendu',
    matiere: matiere,
    notion: notion,
    chapitre: buildChapitreFromQuiz(quiz),
    score_on_10: manualNote != null ? Number(manualNote) / 2 : 0,
    manual_note: manualNote != null ? Number(manualNote) : null,
    tentative_numero: 1,
    total_attempts: 1,
    date_creation: fallbackDate,
    temps_total_seconde: null,
    is_manual: true,
    commentaire_admin: submission?.commentaire || submission?.notes_admin || ''
  }
}

// Derniers quiz (6 plus récents)
const filteredQuizList = computed(() => {
  const sorted = sortByDateDesc(currentQuizList.value)
  return sorted.slice(0, 6)
})

// Stats combinées (auto + notes admin)
const combinedStats = computed(() => {
  const list = currentQuizList.value || []
  const completed = list.length
  const average = completed ? roundToOneDecimal(list.reduce((sum, quiz) => sum + getScoreOn10(quiz), 0) / completed) : 0
  const masteredNotions = new Set(
    list
      .filter(quiz => getScoreOn10(quiz) >= 7)
      .map(quiz => quiz?.notion?.id)
      .filter(Boolean)
  ).size

  return {
    completed,
    average,
    masteredNotions
  }
})

// Tri du tableau récapitulatif
const sortedStats = computed(() => {
  const rows = matiereNotionStats.value || []
  const sorted = [...rows].sort((a, b) => {
    const aVal = a[sortField.value] || 0
    const bVal = b[sortField.value] || 0
    return sortDirection.value === 'asc' ? aVal - bVal : bVal - aVal
  })
  return sorted
})

const summaryTotalPages = computed(() => Math.ceil((sortedStats.value.length || 0) / SUMMARY_PER_PAGE))

const summaryVisiblePages = computed(() => {
  const pages = []
  const total = summaryTotalPages.value
  const current = summaryPage.value

  if (total <= 1) return [1]
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        if (i > 1) pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    }
  }
  return pages
})

const pagedSummaryRows = computed(() => {
  const start = (summaryPage.value - 1) * SUMMARY_PER_PAGE
  const end = start + SUMMARY_PER_PAGE
  return sortedStats.value.slice(start, end)
})

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
  summaryPage.value = 1
}

const formatAverage = (average) => {
  if (average === 0) return '0%'
  return `${Math.round(average)}%`
}

const formatAverageOn20 = (value) => `${roundToOneDecimal(value || 0)}/20`

const getAverageClass = (average) => {
  if (average >= 90) return 'excellent'
  if (average >= 75) return 'good'
  if (average >= 50) return 'average'
  return 'poor'
}

const getAverageOn20Class = (average) => {
  if (average >= 16) return 'avg-good'
  if (average >= 10) return 'avg-medium'
  return 'avg-poor'
}

// Méthodes
const onDataLoaded = async (data) => {
  const automaticList = Array.isArray(data.quiz_list) ? data.quiz_list : []
  let manualList = []

  // Ne charger que les soumissions de l'utilisateur courant
  const userId = userStore?.id
  if (userId) {
    try {
      const submissionsResponse = await getQuizSubmissions({ status: 'graded', user: userId })
      manualList = Array.isArray(submissionsResponse) ? submissionsResponse : []
    } catch (error) {
      console.warn('[QuizHistory] Impossible de charger les notes admin:', error)
    }
  }

  const manualFormatted = manualList.map(mapManualSubmission)

  const fullList = sortByDateDesc([...automaticList, ...manualFormatted])
  currentQuizList.value = fullList
  // Construire l'agrégat matière/notion côté client
  matiereNotionStats.value = computeMatiereNotionFromQuizList(fullList)
  summaryPage.value = 1
}

const onFilterChanged = (filters) => {
  console.log('Filtres changés:', filters)
}

const getScoreClass = (score) => {
  if (score >= 7) return 'score-good'
  if (score >= 5) return 'score-average'
  return 'score-poor'
}

const goToFullHistory = () => {
  router.push({ name: 'QuizzesHistory' })
}

const goToSummaryPage = (page) => {
  if (typeof page === 'number' && page >= 1 && page <= summaryTotalPages.value) {
    summaryPage.value = page
  }
}

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
        sum_score_10: 0,
      })
    }
    const agg = map.get(key)
    agg.count += 1
    agg.sum_score_10 += getScoreOn10(item)
    if ((item.score_on_10 || 0) >= 7) agg.correct_count += 1
    else agg.incorrect_count += 1
  }
  const rows = Array.from(map.values()).map(r => ({
    ...r,
    average_percent: r.count > 0 ? (r.correct_count / r.count) * 100 : 0,
    average_on_20: r.count > 0 ? roundToOneDecimal((r.sum_score_10 / r.count) * 2) : 0
  }))
  rows.sort((a, b) => String(a.matiere.titre).localeCompare(String(b.matiere.titre), 'fr', { sensitivity: 'base' }) || String(a.notion.titre).localeCompare(String(b.notion.titre), 'fr', { sensitivity: 'base' }))
  return rows
}

const navigateToQuiz = async (quiz) => {
  try {
    console.log(`[QuizHistory] 🚀 Navigation rapide vers quiz: ${quiz.quiz_titre}`)
    
    const chapitreId = quiz?.chapitre?.id
    const quizId = quiz?.quiz_id
    if (!chapitreId || !quizId) {
      console.warn('[QuizHistory] Navigation impossible: identifiants manquants', { chapitreId, quizId })
      return
    }
    
    // Navigation optimisée avec remplacement de l'historique pour éviter les allers-retours
    await router.push({
      path: `/quiz-exercices/${chapitreId}`,
      query: { quizId: quizId, autoStart: 'true' }
    })
    
    console.log(`[QuizHistory] ✅ Navigation complétée`)
  } catch (error) {
    console.error(`[QuizHistory] ❌ Erreur de navigation:`, error)
  }
}

// Méthodes utilitaires
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

// Exposer les méthodes pour le template
defineExpose({
})
</script>

<style scoped>
/* Bouton voir l'historique */
.view-history-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.875rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.view-history-btn:hover { 
  background: #1d4ed8;
}
/* Tableau résumé matière/notion */
.summary-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  margin-bottom: 1rem;
  overflow: hidden;
}
.summary-header,
.summary-row {
  display: grid;
  grid-template-columns: 1.5fr 2fr 0.8fr 0.8fr 0.8fr 0.8fr;
  gap: 0.75rem;
  padding: 0.65rem 0.875rem;
  align-items: center;
}
.summary-header {
  background: #f9fafb;
  font-weight: 600;
  color: #1f2937;
  font-size: 0.8rem;
  border-bottom: 1px solid #e5e7eb;
}
.summary-row { 
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.15s ease;
}
.summary-row:hover {
  background: #f9fafb;
}
.summary-row:last-child { border-bottom: none; }
.summary-row .cell { font-size: 0.825rem; color: #1f2937; }
.summary-row .cell.count,
.summary-row .cell.correct,
.summary-row .cell.incorrect { text-align: center; font-weight: 600; }
.summary-row .cell.correct { color: #059669; }
.summary-row .cell.incorrect { color: #dc2626; }

.summary-row .cell.average { text-align: center; }
.avg-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 64px;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.8rem;
}
.avg-badge.avg-good { background: #d1fae5; color: #065f46; }
.avg-badge.avg-medium { background: #fef08a; color: #854d0e; }
.avg-badge.avg-poor { background: #fecaca; color: #991b1b; }

.summary-pagination {
  display: flex;
  gap: 0.35rem;
  align-items: center;
  justify-content: center;
  margin: 0.75rem 0 0.5rem;
}

.pg-btn, .pg-page {
  border: 1px solid #e5e7eb;
  background: #fff;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  min-width: 32px;
  font-weight: 500;
  transition: all 0.15s ease;
}

.pg-btn:hover:not(:disabled), .pg-page:hover:not(:disabled):not(.dots) {
  border-color: #d1d5db;
  background: #f9fafb;
}

.pg-page.dots { cursor: default; background: transparent; border: none; }
.pg-page.active {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
  font-weight: 600;
}
.pg-btn:disabled, .pg-page:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.sortable-header { display: flex; align-items: center; justify-content: center; cursor: pointer; user-select: none; padding: 0.25rem; border-radius: 4px; gap: 0.35rem; }
.sortable-header:hover { background-color: #f3f4f6; }
.sort-icon { font-size: 1rem; color: #6b7280; font-weight: 700; }
.sort-icon.active { color: #2563eb; font-weight: 700; }

@media (max-width: 768px) {
  .summary-header, .summary-row { grid-template-columns: 1fr 1fr 0.7fr 0.7fr 0.7fr 0.9fr; padding: 0.5rem 0.75rem; }
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
/* Stats globales */
.stats-grid {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.stat-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  min-width: 120px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.stat-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-card.quiz-completed .stat-value {
  color: #2563eb;
}

.stat-card.quiz-average .stat-value {
  color: #059669;
}

.stat-card.quiz-notions .stat-value {
  color: #8b5cf6;
}

/* Stats par matière */
.section-subtitle {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
  margin-top: 1rem;
}

.matiere-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.matiere-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 0.875rem;
  transition: box-shadow 0.2s ease;
}

.matiere-card:hover {
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.matiere-name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.matiere-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.matiere-average {
  font-size: 1rem;
  font-weight: 700;
  color: #2563eb;
}

.matiere-count {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

/* Filtres personnalisés */
.inline-mastery-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.3rem 0.6rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  color: #6b7280;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.inline-mastery-btn:hover {
  border-color: #d1d5db;
  background: #f9fafb;
}

.inline-mastery-btn.active {
  font-weight: 600;
  color: white;
  background: #2563eb;
  border-color: #2563eb;
}

.inline-mastery-icon {
  font-size: 0.75rem;
}

.inline-mastery-label {
  font-size: 0.75rem;
}

/* Cartes de quiz */
.quiz-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 0.875rem;
  transition: all 0.2s;
  cursor: pointer;
}

.quiz-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-color: #2563eb;
}

.quiz-card.manual-quiz {
  border-left: 3px solid #8b5cf6;
}

.quiz-card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.quiz-info {
  flex: 1;
  min-width: 0;
}

.quiz-card-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quiz-meta {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.quiz-score {
  font-size: 0.875rem;
  font-weight: 700;
  padding: 0.35rem 0.7rem;
  border-radius: 6px;
  white-space: nowrap;
}

.quiz-score.score-good {
  background: #d1fae5;
  color: #065f46;
}

.quiz-score.score-average {
  background: #fef08a;
  color: #854d0e;
}

.quiz-score.score-poor {
  background: #fecaca;
  color: #991b1b;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-grid {
    flex-direction: column;
    align-items: stretch;
  }
  
  .matiere-grid {
    grid-template-columns: 1fr;
  }
  
  .quiz-card-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .quiz-score {
    align-self: flex-start;
  }
}
</style>
