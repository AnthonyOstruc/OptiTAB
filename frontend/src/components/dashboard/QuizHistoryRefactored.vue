<template>
  <BaseHistory
    title="🧠 Historique des Quiz"
    list-title="📝 Quiz effectués"
    loading-text="Chargement des quiz..."
    api-endpoint="/api/suivis/quiz/stats/"
    :extra-params="{ limit: 6 }"
    :custom-filters="masteryFilters"
    :navigation-handler="navigateToQuiz"
    :items-per-page="6"
    :filtered-items="filteredQuizList"
    @data-loaded="onDataLoaded"
    @filter-changed="onFilterChanged"
  >
    <!-- Actions en-tête: bouton Voir l'historique complet -->
    <template #header-actions>
      <button class="view-history-btn" @click="goToFullHistory" title="Voir tout l'historique" aria-label="Voir tout l'historique">
        Voir l'historique
      </button>
    </template>
    <!-- Statistiques globales -->
    <template #global-stats="{ stats }">
      <div class="stats-grid">
        <div class="stat-card quiz-completed">
          <span class="stat-label">Quiz effectués</span>
          <span class="stat-value">{{ stats.completed || 0 }}</span>
        </div>
        <div class="stat-card quiz-average">
          <span class="stat-label">Note moyenne</span>
          <span class="stat-value">{{ stats.average || 0 }}/10</span>
        </div>
        <div class="stat-card quiz-notions">
          <span class="stat-label">Notions maîtrisées</span>
          <span class="stat-value">{{ stats.masteredNotions || 0 }}</span>
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

    <!-- Filtres personnalisés -->
    <template #custom-filters="{ filters, selected }">
      <button 
        v-for="filter in filters" 
        :key="filter.value"
        @click="updateSelectedMastery(filter.value)"
        :class="['inline-mastery-btn', { active: selected === filter.value }, filter.class]"
      >
        <span v-if="filter.icon" class="inline-mastery-icon">{{ filter.icon }}</span>
        <span class="inline-mastery-label">{{ filter.label }}</span>
      </button>
    </template>

    <!-- Liste des quiz -->
    <template #items-list="{ items, toggleDetails, isExpanded, navigateToItem }">
      <div v-for="quiz in items" :key="quiz.id" class="quiz-card" :class="{ 'multiple-attempts': quiz.total_attempts > 1 }">
        <div class="quiz-card-header" @click="toggleDetails(quiz.id)">
          <div class="quiz-card-title-section">
            <h5 class="quiz-card-title clickable-title" @click.stop="navigateToItem(quiz)" :title="'Accéder au quiz: ' + quiz.quiz_titre">
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
            <div class="quiz-score" :class="getScoreClass(quiz.score_on_10)">
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
              <span v-if="quiz.total_attempts > 1" class="total-attempts">
                ({{ quiz.total_attempts }} au total)
              </span>
            </span>
            <span class="quiz-date">{{ formatDate(quiz.date_creation) }}</span>
            <span class="quiz-time" v-if="quiz.temps_total_seconde">
              {{ formatTime(quiz.temps_total_seconde) }}
            </span>
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

// Router
const router = useRouter()

// État
const selectedMastery = ref('all')
const currentQuizList = ref([])
const matiereNotionStats = ref([])
const sortField = ref('count')
const sortDirection = ref('desc')
const expandedNotions = ref(new Set())
const notionDetails = ref({})

// Filtres de maîtrise pour quiz
const masteryFilters = [
  { value: 'all', label: 'Tous', icon: '', class: 'all' },
  { value: 'mastered', label: 'Maîtrisés', icon: '✅', class: 'mastered' },
  { value: 'average', label: 'Moyens', icon: '⚠️', class: 'average' },
  { value: 'poor', label: 'Non maîtrisés', icon: '❌', class: 'poor' }
]

// Computed pour filtrer les quiz selon le niveau de maîtrise
const filteredQuizList = computed(() => {
  let filtered = currentQuizList.value

  // Filtrer par niveau de maîtrise
  if (selectedMastery.value !== 'all') {
    filtered = filtered.filter(quiz => {
      const score = quiz.score_on_10
      switch (selectedMastery.value) {
        case 'mastered':
          return score >= 7 // Maîtrisé
        case 'average':
          return score >= 5 && score < 7 // Moyen
        case 'poor':
          return score < 5 // Non maîtrisé
        default:
          return true
      }
    })
  }

  return filtered
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

// Méthodes
const onDataLoaded = (data) => {
  const fullList = Array.isArray(data.quiz_list) ? data.quiz_list : []
  // Limiter visuellement à 6 pour le dashboard
  currentQuizList.value = fullList.slice(0, 6)
  // Construire l'agrégat matière/notion côté client
  matiereNotionStats.value = computeMatiereNotionFromQuizList(fullList)
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
    const chapters = await computeChapterStats(list)
    notionDetails.value[key] = { loading: false, error: '', chapters }
  } catch (error) {
    const message = (error?.response?.data?.error) || 'Erreur lors du chargement des détails'
    notionDetails.value[key] = { loading: false, error: message, chapters: [] }
  }
}

const computeChapterStats = async (quizList) => {
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

const navigateToQuiz = async (quiz) => {
  try {
    console.log(`[QuizHistory] 🚀 Navigation rapide vers quiz: ${quiz.quiz_titre}`)
    
    const chapitreId = quiz.chapitre.id
    const quizId = quiz.quiz_id
    
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

const updateSelectedMastery = (value) => {
  selectedMastery.value = value
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
  updateSelectedMastery
})
</script>

<style scoped>
/* Bouton voir l'historique */
.view-history-btn {
  background: #111827;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  cursor: pointer;
}
.view-history-btn:hover { background: #1f2937; }
/* Tableau résumé matière/notion - aligné avec Exercices */
.summary-table {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  margin-bottom: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.summary-header,
.summary-row {
  display: grid;
  grid-template-columns: 1.5fr 2fr 0.8fr 0.8fr 0.8fr 0.8fr;
  gap: 1rem;
  padding: 0.75rem 1rem;
  align-items: center;
}
.summary-header {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  border-bottom: 1px solid #e5e7eb;
}
.summary-row { border-bottom: 1px solid #f3f4f6; }
.summary-row:last-child { border-bottom: none; }
.summary-row .cell { font-size: 0.875rem; color: #374151; }
.summary-row .cell.count,
.summary-row .cell.correct,
.summary-row .cell.incorrect { text-align: center; font-weight: 600; }
.summary-row .cell.correct { color: #16a34a; }
.summary-row .cell.incorrect { color: #dc2626; }

.summary-row .cell.average { font-weight: 600; text-align: center; padding: 0.25rem 0.5rem; border-radius: 4px; }
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
/* Stats globales */
.stats-grid {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.stat-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  min-width: 140px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 800;
}

.stat-card.quiz-completed {
  border-color: #8b5cf6;
}
.stat-card.quiz-completed .stat-value {
  color: #8b5cf6;
}

.stat-card.quiz-average {
  border-color: #f59e0b;
}
.stat-card.quiz-average .stat-value {
  color: #d97706;
}

.stat-card.quiz-notions {
  border-color: #10b981;
}
.stat-card.quiz-notions .stat-value {
  color: #059669;
}

/* Stats par matière */
.section-subtitle {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.matiere-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.matiere-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
}

.matiere-name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.matiere-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.matiere-average {
  font-size: 1.1rem;
  font-weight: 700;
  color: #059669;
}

.matiere-count {
  font-size: 0.8rem;
  color: #6b7280;
}

/* Filtres personnalisés */
.inline-mastery-btn {
  display: flex;
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

.inline-mastery-btn:hover {
  border-color: #d1d5db;
  background: #f9fafb;
}

.inline-mastery-btn.active {
  font-weight: 600;
  color: white;
  border-width: 1px;
}

.inline-mastery-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
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
  padding: 1rem;
  transition: all 0.2s;
}

.quiz-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.quiz-card.multiple-attempts {
  border-left: 3px solid #f59e0b;
}

.quiz-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  cursor: pointer;
  padding: 0.5rem;
  margin: -0.5rem -0.5rem 0.75rem -0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.quiz-card-header:hover {
  background-color: #f8fafc;
}

.quiz-card-title-section {
  flex: 1;
}

.quiz-card-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quiz-card-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.clickable-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem;
  margin: -0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.clickable-title:hover {
  color: #3b82f6;
  background: #f0f9ff;
}

.navigation-icon {
  opacity: 0;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.clickable-title:hover .navigation-icon {
  opacity: 1;
}

.quiz-breadcrumb-compact {
  font-size: 0.7rem;
  color: #6b7280;
  font-weight: 500;
}

.quiz-score {
  font-size: 0.9rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.expand-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s;
}

.expand-toggle:hover {
  background-color: #e5e7eb;
  color: #374151;
}

.expand-toggle svg {
  transition: transform 0.2s;
}

.expand-toggle.expanded svg {
  transform: rotate(180deg);
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
  background: #fecaca;
  color: #991b1b;
}

.retry-indicator {
  margin-left: 0.25rem;
  font-size: 0.8rem;
  opacity: 0.7;
}

.quiz-card-details {
  border-top: 1px solid #f3f4f6;
  padding-top: 0.75rem;
  margin-top: 0.5rem;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.quiz-breadcrumb {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.breadcrumb-item {
  font-weight: 500;
}

.breadcrumb-separator {
  margin: 0 0.25rem;
}

.quiz-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #9ca3af;
}

.quiz-attempt {
  font-weight: 600;
}

.total-attempts {
  color: #6b7280;
  font-weight: 400;
  font-size: 0.7rem;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .matiere-grid {
    grid-template-columns: 1fr;
  }
  
  .quiz-meta {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .quiz-card-header {
    align-items: flex-start;
  }
  
  .quiz-card-actions {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.25rem;
  }
  
  .quiz-breadcrumb-compact {
    font-size: 0.65rem;
  }
}
</style>
