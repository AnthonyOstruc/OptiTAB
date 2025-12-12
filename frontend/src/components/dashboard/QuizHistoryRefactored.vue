<template>
  <BaseHistory
    title="🧠 Historique des Quiz"
    list-title="📝 Quiz effectués"
    loading-text="Chargement des quiz..."
    api-endpoint="/api/suivis/quiz/stats/"
    :extra-params="extraParams"
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
          <span class="stat-value">{{ combinedStats.average.toFixed(1) }}/20</span>
        </div>
        <div class="stat-card quiz-notions">
          <span class="stat-label">Chapitres maîtrisés</span>
          <span class="stat-value">{{ combinedStats.masteredNotions }}</span>
        </div>
      </div>
    </template>

    <!-- Tableau récapitulatif matière / notion -->
    <template #matiere-notion-stats>
      <!-- Version Desktop : Tableau -->
      <div class="summary-table desktop-only">
        <div class="summary-header">
          <div>Matière</div>
          <div>Chapitre</div>
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

        <template v-for="row in pagedSummaryRows" :key="`${row.matiere.id}-${row.notion.id}-${row.quiz_id || ''}`">
          <div class="summary-row">
            <div class="cell matiere">{{ row.matiere.titre }}</div>
            <div class="cell notion">
              <span class="notion-label">{{ row.quiz_titre || row.notion.quiz_titre || row.notion.titre }}</span>
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

      <!-- Version Mobile : Cartes -->
      <div class="summary-cards mobile-only">
        <div class="sort-controls">
          <span class="sort-label">Trier par :</span>
          <select v-model="sortField" @change="sortDirection = 'desc'" class="sort-select">
            <option value="count">Faits</option>
            <option value="correct_count">Réussis</option>
            <option value="incorrect_count">Ratés</option>
            <option value="average_on_20">Moyenne</option>
          </select>
          <button class="sort-direction-btn" @click="sortDirection = sortDirection === 'asc' ? 'desc' : 'asc'" :title="sortDirection === 'asc' ? 'Croissant' : 'Décroissant'">
            {{ sortDirection === 'asc' ? '↑' : '↓' }}
          </button>
        </div>
        <template v-for="row in pagedSummaryRows" :key="`${row.matiere.id}-${row.notion.id}-${row.quiz_id || ''}`">
          <div class="summary-card">
            <div class="card-header">
              <div class="card-title">{{ row.quiz_titre || row.notion.quiz_titre || row.notion.titre }}</div>
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
              <div class="stat-item highlight" :class="getAverageOn20Class(row.average_on_20)">
                <span class="stat-label">Moyenne</span>
                <span class="stat-value">{{ formatAverageOn20(row.average_on_20) }}</span>
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

// Props
const props = defineProps({
  childId: {
    type: Number,
    default: null
  }
})

// Router
const router = useRouter()
const userStore = useUserStore()

// Paramètres pour l'API (inclure user_id si childId est fourni)
const extraParams = computed(() => {
  const params = { limit: 6 }
  if (props.childId) {
    params.user_id = props.childId
  }
  return params
})

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
  const average = completed ? roundToOneDecimal(list.reduce((sum, quiz) => sum + (getScoreOn10(quiz) * 2), 0) / completed) : 0
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

  // Utiliser childId si fourni (pour les parents), sinon userStore.id (pour l'élève)
  const userId = props.childId || userStore?.id
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
    const quizId = item?.quiz_id || item?.id
    const quizTitre = item?.quiz_titre || ''
    
    // Clé unique par quiz (pas par notion) pour avoir des lignes séparées par quiz
    const key = `${mat.id}-${not.id}-${quizId}`
    if (!map.has(key)) {
      map.set(key, {
        matiere: { id: mat.id, titre: mat.titre || '' },
        notion: { id: not.id, titre: not.titre || '', quiz_titre: quizTitre },
        quiz_id: quizId,
        quiz_titre: quizTitre,
        count: 0,
        correct_count: 0,
        incorrect_count: 0,
        sum_score_10: 0,
      })
    }
    const agg = map.get(key)
    agg.count += 1
    agg.sum_score_10 += getScoreOn10(item)
    if (getScoreOn10(item) >= 7) agg.correct_count += 1
    else agg.incorrect_count += 1
  }
  const rows = Array.from(map.values()).map(r => ({
    ...r,
    average_percent: r.count > 0 ? (r.correct_count / r.count) * 100 : 0,
    average_on_20: r.count > 0 ? roundToOneDecimal((r.sum_score_10 / r.count) * 2) : 0
  }))
  rows.sort((a, b) => 
    String(a.matiere.titre).localeCompare(String(b.matiere.titre), 'fr', { sensitivity: 'base' }) || 
    String(a.notion.titre).localeCompare(String(b.notion.titre), 'fr', { sensitivity: 'base' }) ||
    String(a.quiz_titre || '').localeCompare(String(b.quiz_titre || ''), 'fr', { sensitivity: 'base' })
  )
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
/* ═══════════════════════════════════════════════════════════════
   DESIGN ÉPURÉ - Quiz History
   ═══════════════════════════════════════════════════════════════ */

/* Bouton Archive */
.view-history-btn {
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}
.view-history-btn:hover { 
  background: #2563eb;
}

/* ─────────────────────────────────────────────────────────────────
   Stats globales - Design minimaliste
   ───────────────────────────────────────────────────────────────── */
.stats-grid {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.stat-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  min-width: 140px;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 500;
  color: #64748b;
  margin-bottom: 0.375rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-card.quiz-completed .stat-value { color: #3b82f6; }
.stat-card.quiz-average .stat-value { color: #10b981; }
.stat-card.quiz-notions .stat-value { color: #8b5cf6; }

/* ─────────────────────────────────────────────────────────────────
   Tableau récapitulatif - Design clean
   ───────────────────────────────────────────────────────────────── */
.summary-table {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.summary-header,
.summary-row {
  display: grid;
  grid-template-columns: 1.5fr 2.5fr 0.75fr 0.75fr 0.75fr 1fr;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  align-items: center;
}

.summary-header {
  background: #f8fafc;
  font-weight: 600;
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  border-bottom: 1px solid #e2e8f0;
}

.summary-row { 
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.15s ease;
}
.summary-row:last-child { border-bottom: none; }
.summary-row:hover { background: #f8fafc; }

.summary-row .cell { 
  font-size: 0.875rem; 
  color: #334155;
}

.summary-row .cell.matiere {
  font-weight: 500;
  color: #475569;
}

.summary-row .cell.notion .notion-label {
  color: #1e293b;
  font-weight: 500;
}

.summary-row .cell.count,
.summary-row .cell.correct,
.summary-row .cell.incorrect { 
  text-align: center; 
  font-weight: 600;
  font-size: 0.875rem;
}

.summary-row .cell.correct { color: #10b981; }
.summary-row .cell.incorrect { color: #ef4444; }

.summary-row .cell.average { text-align: center; }

.avg-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 56px;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.8125rem;
}

.avg-badge.avg-good { 
  background: #dcfce7; 
  color: #166534; 
}
.avg-badge.avg-medium { 
  background: #fef3c7; 
  color: #92400e; 
}
.avg-badge.avg-poor { 
  background: #fee2e2; 
  color: #991b1b; 
}

/* Tri */
.sortable-header { 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  cursor: pointer; 
  user-select: none; 
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  margin: -0.25rem -0.5rem;
  border-radius: 4px;
  transition: background 0.15s;
}
.sortable-header:hover { background: #e2e8f0; }
.sort-icon { 
  font-size: 0.75rem; 
  color: #94a3b8; 
  font-weight: 600;
}
.sort-icon.active { color: #3b82f6; }

/* Pagination du tableau */
.summary-pagination {
  display: flex;
  gap: 0.375rem;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  border-top: 1px solid #f1f5f9;
}

.pg-btn, .pg-page {
  border: 1px solid #e2e8f0;
  background: #fff;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  cursor: pointer;
  min-width: 32px;
  font-weight: 500;
  color: #64748b;
  transition: all 0.15s ease;
}

.pg-btn:hover:not(:disabled), 
.pg-page:hover:not(:disabled):not(.dots) {
  border-color: #cbd5e1;
  background: #f8fafc;
  color: #334155;
}

.pg-page.dots { 
  cursor: default; 
  background: transparent; 
  border: none; 
  color: #94a3b8;
}

.pg-page.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #fff;
  font-weight: 600;
}

.pg-btn:disabled, .pg-page:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ─────────────────────────────────────────────────────────────────
   Stats par matière
   ───────────────────────────────────────────────────────────────── */
.section-subtitle {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1e293b;
  margin: 1.25rem 0 0.75rem;
}

.matiere-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.matiere-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.875rem 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.matiere-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.matiere-name {
  font-weight: 600;
  color: #334155;
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
  color: #3b82f6;
}

.matiere-count {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* ─────────────────────────────────────────────────────────────────
   Cartes de Quiz - Design épuré
   ───────────────────────────────────────────────────────────────── */
.quiz-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.875rem 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.quiz-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
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
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quiz-meta {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.quiz-score {
  font-size: 0.875rem;
  font-weight: 700;
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  white-space: nowrap;
}

.quiz-score.score-good {
  background: #dcfce7;
  color: #166534;
}

.quiz-score.score-average {
  background: #fef3c7;
  color: #92400e;
}

.quiz-score.score-poor {
  background: #fee2e2;
  color: #991b1b;
}

/* ─────────────────────────────────────────────────────────────────
   Filtres personnalisés
   ───────────────────────────────────────────────────────────────── */
.inline-mastery-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #64748b;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.inline-mastery-btn:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.inline-mastery-btn.active {
  font-weight: 600;
  color: white;
  background: #3b82f6;
  border-color: #3b82f6;
}

.inline-mastery-icon {
  font-size: 0.75rem;
}

.inline-mastery-label {
  font-size: 0.75rem;
}

/* ─────────────────────────────────────────────────────────────────
   Version Mobile : Cartes de résumé
   ───────────────────────────────────────────────────────────────── */
.summary-cards {
  margin-top: 1rem;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  padding: 0.875rem 1rem;
  background: linear-gradient(to right, #f8fafc, #f1f5f9);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sort-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #475569;
  white-space: nowrap;
  letter-spacing: -0.01em;
}

.sort-select {
  flex: 1;
  padding: 0.625rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  background: #ffffff;
  font-size: 0.875rem;
  font-weight: 500;
  color: #1e293b;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sort-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.sort-direction-btn {
  padding: 0.625rem 0.875rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 1.125rem;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sort-direction-btn:hover {
  background: #f8fafc;
  border-color: #94a3b8;
  transform: scale(1.02);
}

.summary-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.summary-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
  border-color: #cbd5e1;
}

.card-header {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.card-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.375rem;
  line-height: 1.5;
  letter-spacing: -0.02em;
}

.card-subtitle {
  font-size: 0.8125rem;
  color: #64748b;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.625rem;
  background: #f8fafc;
  border-radius: 6px;
  width: fit-content;
}

.card-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.375rem;
  min-width: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.625rem 0.375rem;
  background: #fafbfc;
  border-radius: 8px;
  border: 1px solid #f1f5f9;
  transition: all 0.2s ease;
  align-items: center;
  text-align: center;
  min-width: 0;
  overflow: hidden;
}

.stat-item:hover {
  background: #f8fafc;
  border-color: #e2e8f0;
  transform: translateY(-1px);
}

.stat-item.highlight {
  grid-column: auto;
  padding: 0.75rem 0.5rem;
  background: linear-gradient(135deg, #fafbfc 0%, #f8fafc 100%);
  border-radius: 10px;
  border: 2px solid #e2e8f0;
}

.stat-item.highlight.avg-good {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #86efac;
}

.stat-item.highlight.avg-medium {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border-color: #fcd34d;
}

.stat-item.highlight.avg-poor {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-color: #fca5a5;
}

.stat-item .stat-label {
  font-size: 0.5625rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 0.1875rem;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.stat-item .stat-value {
  font-size: 1.125rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.1;
  white-space: nowrap;
}

.stat-item .stat-value.success {
  color: #059669;
}

.stat-item .stat-value.error {
  color: #dc2626;
}

.stat-item.highlight .stat-value {
  font-size: 1rem;
  font-weight: 800;
  padding: 0.1875rem 0.25rem;
  border-radius: 6px;
  display: inline-block;
  line-height: 1;
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.stat-item.highlight.avg-good .stat-value {
  color: #047857;
  background: rgba(16, 185, 129, 0.1);
}

.stat-item.highlight.avg-medium .stat-value {
  color: #d97706;
  background: rgba(251, 191, 36, 0.15);
}

.stat-item.highlight.avg-poor .stat-value {
  color: #b91c1c;
  background: rgba(239, 68, 68, 0.1);
}

/* Desktop : masquer les cartes mobiles */
.mobile-only {
  display: none !important;
}

.desktop-only {
  display: block !important;
}

/* ─────────────────────────────────────────────────────────────────
   Responsive
   ───────────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }

  .mobile-only {
    display: block !important;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }
  
  .stat-card {
    min-width: 0;
    padding: 0.75rem 0.5rem;
  }
  
  .stat-label {
    font-size: 0.7rem;
  }
  
  .stat-value {
    font-size: 1.15rem;
  }
  
  .summary-header, 
  .summary-row { 
    grid-template-columns: 1fr 1.5fr 0.6fr 0.6fr 0.6fr 0.9fr; 
    padding: 0.625rem 0.75rem;
    gap: 0.375rem;
  }
  
  .summary-row .cell {
    font-size: 0.8125rem;
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
