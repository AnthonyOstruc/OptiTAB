<template>
  <div class="quiz-history-wrapper">
    <BaseHistory
      ref="baseHistoryRef"
      title="🎯 Historique des Quiz"
      list-title="📝 Quiz effectués"
      loading-text="Chargement des quiz..."
      api-endpoint="/api/suivis/quiz/stats/"
      :extra-params="historyParams"
      :navigation-handler="navigateToQuiz"
      :items-per-page="6"
      :filtered-items="filteredQuizList"
      @data-loaded="onDataLoaded"
      @filter-changed="onFilterChanged"
    >
      <!-- Actions en-tête: bouton Archive -->
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
            <span class="stat-value">{{ stats.completed || 0 }}</span>
          </div>
          <div class="stat-card quiz-average">
            <span class="stat-label">Score moyen</span>
            <span class="stat-value">{{ formatScore(stats.average_score) }}</span>
          </div>
          <div class="stat-card quiz-best">
            <span class="stat-label">Meilleur score</span>
            <span class="stat-value">{{ formatScore(stats.best_score) }}</span>
          </div>
          <div class="stat-card quiz-notions">
            <span class="stat-label">Notions testées</span>
            <span class="stat-value">{{ stats.notionsTested || 0 }}</span>
          </div>
        </div>
      </template>

      <!-- Tableau récapitulatif matière / notion -->
      <template #matiere-notion-stats="{ stats }">
        <!-- Version Desktop : Tableau -->
        <div class="summary-table desktop-only">
          <div class="summary-header">
            <div>Matière</div>
            <div>Notion</div>
            <div class="sortable-header" @click="sortBy('quiz_count')">
              Faits
              <span class="sort-icon" :class="{ active: sortField === 'quiz_count' }">
                {{ sortField === 'quiz_count' && sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </div>
            <div class="sortable-header" @click="sortBy('average_score')">
              Score moyen
              <span class="sort-icon" :class="{ active: sortField === 'average_score' }">
                {{ sortField === 'average_score' && sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </div>
            <div class="sortable-header" @click="sortBy('best_score')">
              Meilleur
              <span class="sort-icon" :class="{ active: sortField === 'best_score' }">
                {{ sortField === 'best_score' && sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </div>
          </div>
          <template v-for="row in pagedSummaryRows" :key="`${row.matiere.id}-${row.notion.id}`">
            <div class="summary-row">
              <div class="cell matiere">{{ row.matiere.titre }}</div>
              <div class="cell notion">
                <span class="notion-label">{{ row.notion.titre }}</span>
              </div>
              <div class="cell count">{{ row.quiz_count }}</div>
              <div class="cell average" :class="getScoreClass(row.average_score)">{{ formatScore(row.average_score) }}</div>
              <div class="cell best" :class="getScoreClass(row.best_score)">{{ formatScore(row.best_score) }}</div>
            </div>
          </template>
        </div>

        <!-- Version Mobile : Cartes -->
        <div class="summary-cards mobile-only">
          <div class="sort-controls">
            <span class="sort-label">Trier par :</span>
            <select v-model="sortField" @change="sortDirection = 'desc'" class="sort-select">
              <option value="quiz_count">Faits</option>
              <option value="average_score">Score moyen</option>
              <option value="best_score">Meilleur</option>
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
                  <span class="stat-value">{{ row.quiz_count }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Score moyen</span>
                  <span class="stat-value" :class="getScoreClass(row.average_score)">{{ formatScore(row.average_score) }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Meilleur</span>
                  <span class="stat-value" :class="getScoreClass(row.best_score)">{{ formatScore(row.best_score) }}</span>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Pagination pour le tableau récapitulatif -->
        <div v-if="totalSummaryPages > 1" class="summary-pagination">
          <button :disabled="summaryPage === 1" @click="summaryPage--" class="pagination-btn">Précédent</button>
          <span class="pagination-info">Page {{ summaryPage }} / {{ totalSummaryPages }}</span>
          <button :disabled="summaryPage === totalSummaryPages" @click="summaryPage++" class="pagination-btn">Suivant</button>
        </div>
      </template>

      <!-- Filtres personnalisés pour quiz -->
      <template #filters>
        <div class="filter-group">
          <div class="filter-label">Score:</div>
          <div class="filter-buttons">
            <button
              v-for="filter in scoreFilters"
              :key="filter.value"
              :class="['filter-btn', filter.class, { active: selectedScore === filter.value }]"
              @click="selectedScore = filter.value"
            >
              {{ filter.icon }} {{ filter.label }}
            </button>
          </div>
        </div>
      </template>

      <!-- Élément de liste personnalisé pour quiz -->
      <template #list-item="{ item }">
        <div class="quiz-item" @click="navigateToQuiz(item)">
          <div class="quiz-header">
            <div class="quiz-title-section">
              <h4 class="quiz-title">
                {{ item.quiz_titre || 'Quiz' }}
                <span v-if="item.is_manual" class="manual-badge">Noté par prof</span>
              </h4>
              <span class="quiz-notion">{{ item.notion?.titre || 'Notion' }}</span>
            </div>
            <div class="quiz-score" :class="getScoreClass(item.score_percentage)">
              {{ formatScore(item.score_percentage) }}
            </div>
          </div>
          <div class="quiz-meta">
            <span class="quiz-date">{{ formatDate(item.date_creation || item.created_at) }}</span>
            <span class="quiz-details">{{ item.score || 0 }}/{{ item.total_points || 0 }} points</span>
            <span v-if="!item.is_manual && item.tentative_numero > 1" class="quiz-attempt">Tentative #{{ item.tentative_numero }}</span>
          </div>
        </div>
      </template>
    </BaseHistory>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseHistory from '@/components/dashboard/BaseHistory.vue'

const props = defineProps({
  childId: {
    type: [Number, String],
    default: null
  }
})

const router = useRouter()
const baseHistoryRef = ref(null)

// Filtres de score pour quiz
const scoreFilters = [
  { value: 'all', label: 'Tous', icon: '', class: 'all' },
  { value: 'excellent', label: 'Excellents (≥16)', icon: '🌟', class: 'excellent' },
  { value: 'good', label: 'Bons (≥12)', icon: '✅', class: 'good' },
  { value: 'average', label: 'Moyens (<12)', icon: '⚠️', class: 'average' }
]

// État des filtres
const selectedScore = ref('all')
const currentQuizList = ref([])

// État du tri pour le tableau matière/notion
const sortField = ref('quiz_count')
const sortDirection = ref('desc')
const matiereNotionStats = ref([])

// Pagination pour le tableau récapitulatif
const SUMMARY_PER_PAGE = 5
const summaryPage = ref(1)

const historyParams = computed(() => {
  const params = {}
  if (props.childId) params.child_id = props.childId
  return params
})

// Computed pour filtrer les quiz selon le score
const filteredQuizList = computed(() => {
  let filtered = currentQuizList.value

  // Filtrer par score
  if (selectedScore.value !== 'all') {
    filtered = filtered.filter(quiz => {
      const scorePercentage = quiz.score_percentage || 0
      switch (selectedScore.value) {
        case 'excellent':
          return scorePercentage >= 16
        case 'good':
          return scorePercentage >= 12 && scorePercentage < 16
        case 'average':
          return scorePercentage < 12
        default:
          return true
      }
    })
  }

  // Trier par date décroissante
  filtered = [...filtered].sort((a, b) => {
    const da = new Date(a.date_creation || a.created_at || a.date || 0).getTime()
    const db = new Date(b.date_creation || b.created_at || b.date || 0).getTime()
    return db - da
  })

  return filtered.slice(0, 6)
})

// Tri du tableau matière/notion
const sortedMatiereNotionStats = computed(() => {
  const sorted = [...matiereNotionStats.value].sort((a, b) => {
    const aVal = a[sortField.value] || 0
    const bVal = b[sortField.value] || 0
    return sortDirection.value === 'asc' ? aVal - bVal : bVal - aVal
  })
  return sorted
})

const totalSummaryPages = computed(() => Math.ceil(sortedMatiereNotionStats.value.length / SUMMARY_PER_PAGE))

const pagedSummaryRows = computed(() => {
  const start = (summaryPage.value - 1) * SUMMARY_PER_PAGE
  const end = start + SUMMARY_PER_PAGE
  return sortedMatiereNotionStats.value.slice(start, end)
})

// Méthodes
const onDataLoaded = async (data) => {
  // 1. Charger les tentatives automatiques
  const automaticList = Array.isArray(data.quiz_list) ? data.quiz_list : []
  
  // 2. Charger aussi les soumissions manuelles notées
  let manualSubmissions = []
  try {
    const { getQuizSubmissions } = await import('@/api/quizSubmissions')
    const submissionsResponse = await getQuizSubmissions({ status: 'graded' })
    manualSubmissions = Array.isArray(submissionsResponse) ? submissionsResponse : []
  } catch (error) {
    console.warn('[QuizHistory] Erreur chargement soumissions manuelles:', error)
  }
  
  // 3. Transformer les soumissions manuelles au même format
  const manualList = manualSubmissions.map(sub => ({
    id: `manual-${sub.id}`,
    quiz_id: sub.quiz?.id,
    quiz_titre: sub.quiz?.titre || 'Quiz manuel',
    score: sub.note,
    total_points: 20,
    score_percentage: sub.note, // Note déjà sur 20
    score_on_10: sub.note / 2, // Convertir en /10
    tentative_numero: 1,
    date_creation: sub.date_correction || sub.date_creation,
    is_manual: true,
    notion: sub.quiz?.notion || { id: null, titre: 'Non spécifié' },
    theme: sub.quiz?.notion?.theme || { id: null, titre: 'Non spécifié' },
    matiere: sub.quiz?.notion?.theme?.matiere || { id: null, titre: 'Non spécifié' }
  }))
  
  // 4. Transformer les tentatives automatiques pour avoir score_percentage
  const automaticListFormatted = automaticList.map(quiz => ({
    ...quiz,
    score_percentage: quiz.score_on_10 * 2, // Convertir /10 en /20
    is_manual: false
  }))
  
  // 5. Fusionner et trier par date
  const allQuiz = [...automaticListFormatted, ...manualList].sort((a, b) => {
    const da = new Date(a.date_creation).getTime()
    const db = new Date(b.date_creation).getTime()
    return db - da
  })
  
  currentQuizList.value = allQuiz
  matiereNotionStats.value = Array.isArray(data.matiere_notion_stats) ? data.matiere_notion_stats : []
}

const onFilterChanged = (filters) => {
  console.log('Filtres changés:', filters)
}

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
  summaryPage.value = 1
}

const formatScore = (score) => {
  if (score == null || score === undefined) return '-'
  return `${parseFloat(score).toFixed(1)}/20`
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const getScoreClass = (score) => {
  if (score == null) return ''
  if (score >= 16) return 'score-excellent'
  if (score >= 12) return 'score-good'
  if (score >= 10) return 'score-average'
  return 'score-low'
}

const navigateToQuiz = async (quiz) => {
  try {
    console.log(`[QuizHistory] 🚀 Navigation vers quiz: ${quiz.quiz_titre}`)

    const notionId = quiz?.notion?.id || quiz?.notion_id
    const quizId = quiz?.quiz_id || quiz?.id

    // Naviguer vers la page notion avec le quiz
    if (notionId) {
      await router.push({
        name: 'QuizByNotion',
        params: { notionId: String(notionId) }
      })
      console.log(`[QuizHistory] ✅ Navigation complétée (notion ${notionId})`)
      return
    }

    console.warn('[QuizHistory] Impossible de naviguer: notionId manquant')
  } catch (error) {
    console.error(`[QuizHistory] ❌ Erreur de navigation:`, error)
  }
}

const goToFullHistory = () => {
  router.push({ name: 'QuizzesHistory' })
}
</script>

<style scoped>
.quiz-history-wrapper {
  margin: 2rem 0;
}

/* Stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
}

.quiz-completed .stat-value {
  color: #3b82f6;
}

.quiz-average .stat-value {
  color: #10b981;
}

.quiz-best .stat-value {
  color: #f59e0b;
}

.quiz-notions .stat-value {
  color: #8b5cf6;
}

/* Filtres */
.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.filter-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

/* Élément de quiz */
.quiz-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.quiz-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
  transform: translateY(-2px);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.quiz-title-section {
  flex: 1;
}

.quiz-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.quiz-notion {
  font-size: 0.875rem;
  color: #6b7280;
}

.quiz-score {
  font-size: 1.5rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
}

.score-excellent {
  color: #059669;
  background: #d1fae5;
}

.score-good {
  color: #0891b2;
  background: #cffafe;
}

.score-average {
  color: #d97706;
  background: #fef3c7;
}

.score-low {
  color: #dc2626;
  background: #fee2e2;
}

.quiz-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
  flex-wrap: wrap;
}

.manual-badge {
  display: inline-block;
  background: #8b5cf6;
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.5rem;
}

.quiz-attempt {
  color: #9ca3af;
  font-style: italic;
}

/* Tableau récapitulatif */
.summary-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}

.summary-header {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 1.5fr 1.5fr;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.summary-row {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 1.5fr 1.5fr;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.2s;
}

.summary-row:hover {
  background: #f9fafb;
}

.sortable-header {
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.sortable-header:hover {
  color: #3b82f6;
}

.sort-icon {
  opacity: 0.3;
  transition: opacity 0.2s;
}

.sort-icon.active {
  opacity: 1;
  color: #3b82f6;
}

.cell {
  display: flex;
  align-items: center;
}

.notion-label {
  font-weight: 500;
  color: #374151;
}

/* Cartes mobile */
.summary-cards {
  display: none;
}

.desktop-only {
  display: block;
}

.mobile-only {
  display: none;
}

/* Pagination */
.summary-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #3b82f6;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 500;
  color: #6b7280;
}

.view-history-btn {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.view-history-btn:hover {
  background: #2563eb;
}

/* Responsive */
@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }

  .mobile-only {
    display: block;
  }

  .summary-cards {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .sort-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: #f9fafb;
    border-radius: 8px;
  }

  .sort-label {
    font-weight: 500;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .sort-select {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.875rem;
  }

  .sort-direction-btn {
    padding: 0.5rem 0.75rem;
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 1.25rem;
    cursor: pointer;
  }

  .summary-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1rem;
  }

  .card-header {
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #f3f4f6;
  }

  .card-title {
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.25rem;
  }

  .card-subtitle {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .card-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .stat-item .stat-label {
    font-size: 0.75rem;
    color: #9ca3af;
  }

  .stat-item .stat-value {
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-buttons {
    flex-direction: column;
    width: 100%;
  }

  .filter-btn {
    width: 100%;
  }
}
</style>
      


      <!-- Filtres -->
      <div class="quiz-filters">
        <select v-model="selectedMatiere" @change="onMatiereChange" class="filter-select" :key="'matieres-' + matieresComputed.length">
          <option value="">Toutes les matières</option>
          <option v-for="matiere in matieresComputed" :key="`matiere-${matiere.id}`" :value="matiere.id">
            {{ matiere.titre || matiere.nom }}
          </option>
        </select>
        
        <select v-model="selectedNotion" @change="onNotionChange" class="filter-select" :disabled="!selectedMatiere">
          <option value="">Toutes les notions</option>
          <option v-for="notion in filteredNotions" :key="notion.id" :value="notion.id">
            {{ notion.titre }}
          </option>
        </select>
        
        <select v-model="selectedChapitre" @change="onChapitreChange" class="filter-select" :disabled="!selectedNotion">
          <option value="">Tous les chapitres</option>
          <option v-for="chapitre in filteredChapitres" :key="chapitre.id" :value="chapitre.id">
            {{ chapitre.titre }}
          </option>
        </select>
      </div>


    </div>

    <!-- Statistiques globales -->
    <div v-if="!loading" class="stats-section">
      <div class="stats-grid">
        <div class="stat-card quiz-completed">
          <span class="stat-label">Quiz effectués</span>
          <span class="stat-value">{{ globalStats.completed }}</span>
        </div>
        <div class="stat-card quiz-average">
          <span class="stat-label">Note moyenne</span>
          <span class="stat-value">{{ globalStats.average }}/10</span>
        </div>
        <div class="stat-card quiz-notions">
          <span class="stat-label">Notions maîtrisées</span>
          <span class="stat-value">{{ globalStats.masteredNotions }}</span>
        </div>
      </div>
    </div>

    <!-- Statistiques par matière -->
    <div v-if="!loading && matiereStats.length > 0" class="matiere-stats">
      <h4 class="section-subtitle">📊 Moyennes par matière</h4>
      <div class="matiere-grid">
        <div v-for="matiere in matiereStats" :key="matiere.id" class="matiere-card">
          <div class="matiere-name">{{ matiere.titre }}</div>
          <div class="matiere-info">
            <span class="matiere-average">{{ matiere.average }}/10</span>
            <span class="matiere-count">{{ matiere.quiz_count }} quiz</span>
          </div>
        </div>
      </div>
    </div>

                    <!-- Liste des quiz -->
                <div v-if="!loading" class="quiz-list-section">
                  <div class="quiz-list-header" @click="toggleQuizListSection">
                    <h4 class="section-subtitle">📝 Quiz effectués ({{ filteredQuizList.length }})</h4>
                    
                    <!-- Filtres de maîtrise inline -->
                    <div class="inline-mastery-filters">
                      <button 
                        v-for="filter in masteryFilters" 
                        :key="filter.value"
                        @click.stop="selectedMastery = filter.value"
                        :class="['inline-mastery-btn', { active: selectedMastery === filter.value }, filter.class]"
                        :title="filter.label"
                        :aria-label="filter.label"
                      >
                        <span v-if="filter.icon" class="inline-mastery-icon">{{ filter.icon }}</span>
                        <span class="inline-mastery-label">{{ filter.label }}</span>
                      </button>
                    </div>
                    
                    <button class="section-toggle" :class="{ expanded: isQuizListExpanded }">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6,9 12,15 18,9"></polyline>
                      </svg>
                    </button>
                  </div>
      
      <div v-if="isQuizListExpanded" class="quiz-list-content">
        <div v-if="filteredQuizList.length === 0" class="empty-state">
          <p>Aucun quiz trouvé avec ces filtres</p>
        </div>
        
        <div v-else class="quiz-grid">
         <div v-for="quiz in paginatedQuizList" :key="quiz.id" class="quiz-card" :class="{ 'multiple-attempts': quiz.total_attempts > 1 }">
           <div class="quiz-card-header" @click="toggleQuizDetails(quiz.id)">
             <div class="quiz-card-title-section">
               <h5 class="quiz-card-title clickable-title" 
                   @click.stop="navigateToQuiz(quiz)" 
                   :title="'Accéder au quiz: ' + quiz.quiz_titre">
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
               <button class="expand-toggle" :class="{ expanded: isQuizExpanded(quiz.id) }">
                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                   <polyline points="6,9 12,15 18,9"></polyline>
                 </svg>
               </button>
             </div>
           </div>
           
           <div v-if="isQuizExpanded(quiz.id)" class="quiz-card-details">
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
        </div>
        
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-container">
          <button 
            @click="goToPage(currentPage - 1)" 
            :disabled="currentPage <= 1"
            class="pagination-btn prev"
            :title="'Précédent'"
            aria-label="Précédent"
          >
            <span class="pagination-icon">‹</span>
            <span class="pagination-label">Précédent</span>
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page)"
              :class="['pagination-page', { active: page === currentPage }]"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="goToPage(currentPage + 1)" 
            :disabled="currentPage >= totalPages"
            class="pagination-btn next"
            :title="'Suivant'"
            aria-label="Suivant"
          >
            <span class="pagination-label">Suivant</span>
            <span class="pagination-icon">›</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des quiz...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getMatieres, getNotions } from '@/api'
import apiClient from '@/api/client'
import { useUserStore } from '@/stores/user'

// Store utilisateur
const userStore = useUserStore()
const router = useRouter()

// État
const loading = ref(true)
const globalStats = ref({ completed: 0, average: 0, masteredNotions: 0 })
const quizList = ref([])
const matiereStats = ref([])

// Données de référence
const matieres = ref([])
const notions = ref([])
const chapitres = ref([])
// Mapping thème -> matière pour un filtrage fiable même quand notion.theme est un ID
const themesById = ref({})

// Filtres
const selectedMatiere = ref('')
const selectedNotion = ref('')
const selectedChapitre = ref('')

// Filtre par niveau de maîtrise
const selectedMastery = ref('all')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 6

// État d'expansion des détails
const expandedQuizzes = ref(new Set())

// État d'expansion de la section quiz
const isQuizListExpanded = ref(true)

// Responsive helper (mobile detection)
const isMobile = ref(false)
const updateIsMobile = () => {
  if (typeof window !== 'undefined') {
    isMobile.value = window.innerWidth <= 768
  }
}

// Computed
const filteredNotions = computed(() => {
  if (!selectedMatiere.value) return []

  const selectedMatiereId = parseInt(selectedMatiere.value)

  const filtered = notions.value.filter(notion => {
    // Récupérer l'ID du thème (objet ou nombre)
    const themeId = typeof notion.theme === 'object' ? notion.theme?.id : notion.theme

    // Tenter de récupérer la matière directement depuis la notion (si le thème est imbriqué)
    let matiereId = null
    if (typeof notion.theme === 'object') {
      matiereId = notion.theme?.matiere_id || notion.theme?.matiere?.id || null
    }

    // Sinon, utiliser la table de correspondance thème -> matière
    if (!matiereId && themeId && themesById.value[themeId]) {
      matiereId = themesById.value[themeId].matiere_id || themesById.value[themeId].matiere
    }

    return parseInt(matiereId) === selectedMatiereId
  })

  return filtered
})

const filteredChapitres = computed(() => [])

const filteredQuizList = computed(() => {
  let filtered = quizList.value

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

// Computed pour la pagination
const totalPages = computed(() => Math.ceil(filteredQuizList.value.length / itemsPerPage))

const paginatedQuizList = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredQuizList.value.slice(start, end)
})

// Computed pour forcer la réactivité des matières
const matieresComputed = computed(() => {
  return matieres.value || []
})

// Computed pour les pages visibles dans la pagination
const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  // Mode mobile: n'afficher que 1 … total
  if (isMobile.value) {
    if (total <= 1) {
      return [1]
    }
    return [1, '...', total]
  }
  
  if (total <= 7) {
    // Si 7 pages ou moins, afficher toutes les pages
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Logique pour afficher les pages avec ellipses
    if (current <= 4) {
      // Début : 1, 2, 3, 4, 5, ..., total
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      if (total > 5) pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      // Fin : 1, ..., total-4, total-3, total-2, total-1, total
      pages.push(1)
      if (total > 6) pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        if (i > 1) pages.push(i)
      }
    } else {
      // Milieu : 1, ..., current-1, current, current+1, ..., total
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    }
  }
  
  return pages
})

// Filtres de maîtrise
const masteryFilters = [
  { value: 'all', label: 'Tous', icon: '', class: 'all' },
  { value: 'mastered', label: 'Maîtrisés', icon: '✅', class: 'mastered' },
  { value: 'average', label: 'Moyens', icon: '⚠️', class: 'average' },
  { value: 'poor', label: 'Non maîtrisés', icon: '❌', class: 'poor' }
]

// Méthodes
const loadReferenceData = async () => {
  try {
    // Utiliser les endpoints spécialisés qui filtrent automatiquement selon l'utilisateur
    const [mResponse, tnResponse, nResponse, cResponse] = await Promise.all([
      // Matières pour l'utilisateur (endpoint spécialisé)
      apiClient.get('/api/matieres/user_matieres/', { timeout: 20000 }).catch(() => apiClient.get('/api/matieres/user_matieres/')),
      // Thèmes + Notions pour utilisateur (donne le lien thème -> matière)
      apiClient.get('/api/themes/notions-pour-utilisateur/', { timeout: 20000 }).catch(() => apiClient.get('/api/themes/notions-pour-utilisateur/')),
      // Notions - essayer d'abord l'endpoint spécialisé, puis l'endpoint général
      getNotions({}).catch(() => apiClient.get('/api/notions/pour-utilisateur/', { timeout: 20000 })),
      // Chapitres supprimés: plus de chargement
    ])
    
    // Extraire les données des réponses - gestion spécifique pour user_matieres
    let matieresData = []
    if (mResponse?.data?.matieres_disponibles) {
      // Structure spécifique de user_matieres
      matieresData = mResponse.data.matieres_disponibles
    } else if (mResponse?.data?.data) {
      matieresData = mResponse.data.data
    } else if (Array.isArray(mResponse?.data)) {
      matieresData = mResponse.data
    }
    
    // Gestion spécifique pour les notions
    let notionsData = []
    if (nResponse?.data?.notions_disponibles) {
      notionsData = nResponse.data.notions_disponibles
    } else if (nResponse?.data?.data) {
      notionsData = nResponse.data.data
    } else if (Array.isArray(nResponse?.data)) {
      notionsData = nResponse.data
    } else if (nResponse?.data?.results) {
      notionsData = nResponse.data.results
    }

    // Récupérer thèmes + notions depuis l'endpoint combiné si disponible
    const themesData = tnResponse?.data?.themes || []
    const notionsFromThemesEndpoint = tnResponse?.data?.notions || []

    // Construire la table thème -> matière
    const map = {}
    themesData.forEach(t => {
      const matId = t.matiere_id || (t.matiere && (t.matiere.id || t.matiere))
      map[t.id] = { matiere_id: matId, matiere: matId }
    })
    themesById.value = map

    // Si l'endpoint combiné retourne des notions, l'utiliser en priorité
    if (Array.isArray(notionsFromThemesEndpoint) && notionsFromThemesEndpoint.length > 0) {
      notionsData = notionsFromThemesEndpoint
    }
    
    const chapitresData = Array.isArray(cResponse?.data) ? cResponse.data : (cResponse?.results || [])
    
    matieres.value = Array.isArray(matieresData) ? matieresData : []
    notions.value = Array.isArray(notionsData) ? notionsData : []
    chapitres.value = Array.isArray(chapitresData) ? chapitresData : []
    
    // Forcer la réactivité Vue
    await nextTick()
  } catch (error) {
    console.error('Erreur lors du chargement des données de référence:', error)
    // Fallback vers les données générales si les endpoints spécialisés échouent
    try {
      const [mResponse, nResponse, cResponse] = await Promise.all([
        getMatieres({}),
        getNotions({})
      ])
      
      matieres.value = Array.isArray(mResponse?.data) ? mResponse.data : (mResponse?.results || [])
      notions.value = Array.isArray(nResponse?.data) ? nResponse.data : (nResponse?.results || [])
      chapitres.value = Array.isArray(cResponse?.data) ? cResponse.data : (cResponse?.results || [])
      
      // Forcer la réactivité Vue
      await nextTick()
    } catch (fallbackError) {
      console.error('Erreur fallback:', fallbackError)
    }
  }
}

const loadQuizData = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedMatiere.value) params.matiere = selectedMatiere.value
    if (selectedNotion.value) params.notion = selectedNotion.value
    if (selectedChapitre.value) params.chapitre = selectedChapitre.value
    
    const response = await apiClient.get('/api/suivis/quiz/stats/', { params, timeout: 20000 })
    const data = response.data
    
    globalStats.value = data.global_stats || { completed: 0, average: 0, masteredNotions: 0 }
    quizList.value = data.quiz_list || []
    matiereStats.value = data.matiere_stats || []
    
  } catch (error) {
    console.error('Erreur lors du chargement des quiz:', error)
  } finally {
    loading.value = false
  }
}

const onMatiereChange = async () => {
  selectedNotion.value = ''
  selectedChapitre.value = ''
  resetPagination()
  
  // Recharger les notions pour la matière sélectionnée si nécessaire
  if (selectedMatiere.value && filteredNotions.value.length === 0) {
    console.log('🔄 Rechargement des notions pour matière:', selectedMatiere.value)
    try {
      // Rafraîchir les thèmes + notions pour la matière sélectionnée (met à jour aussi themesById)
      const tnResponse = await apiClient.get('/api/themes/notions-pour-utilisateur/', { params: { matiere: selectedMatiere.value } })
      const themesData = tnResponse?.data?.themes || []
      const notionsFromThemesEndpoint = tnResponse?.data?.notions || []

      const map = {}
      themesData.forEach(t => {
        const matId = t.matiere_id || (t.matiere && (t.matiere.id || t.matiere))
        map[t.id] = { matiere_id: matId, matiere: matId }
      })
      themesById.value = { ...themesById.value, ...map }
      
      let newNotionsData = notionsFromThemesEndpoint
      // Si pas de notions via l'endpoint combiné, fallback sur l'endpoint notions
      if (!Array.isArray(newNotionsData) || newNotionsData.length === 0) {
        const nResponse = await apiClient.get('/api/notions/pour-utilisateur/', { params: { matiere: selectedMatiere.value } })
        if (nResponse?.data?.notions_disponibles) newNotionsData = nResponse.data.notions_disponibles
        else if (nResponse?.data?.data) newNotionsData = nResponse.data.data
        else if (Array.isArray(nResponse?.data)) newNotionsData = nResponse.data
        else if (nResponse?.data?.results) newNotionsData = nResponse.data.results
      }
      
      // Fusionner avec les notions existantes (éviter les doublons)
      const existingIds = notions.value.map(n => n.id)
      const newNotions = newNotionsData.filter(n => !existingIds.includes(n.id))
      notions.value = [...notions.value, ...newNotions]
      

    } catch (error) {
      console.error('Erreur lors du rechargement des notions:', error)
    }
  }
  
  loadQuizData()
}

const onNotionChange = async () => {
  selectedChapitre.value = ''
  resetPagination()
  // Plus de chapitres: recharger uniquement les quiz
  loadQuizData()
}

const onChapitreChange = () => {
  resetPagination()
  loadQuizData()
}

const getScoreClass = (score) => {
  if (score >= 7) return 'score-good'
  if (score >= 5) return 'score-average'
  return 'score-poor'
}

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

const toggleQuizDetails = (quizId) => {
  if (expandedQuizzes.value.has(quizId)) {
    expandedQuizzes.value.delete(quizId)
  } else {
    expandedQuizzes.value.add(quizId)
  }
}

const isQuizExpanded = (quizId) => {
  return expandedQuizzes.value.has(quizId)
}

const toggleQuizListSection = () => {
  isQuizListExpanded.value = !isQuizListExpanded.value
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

// Méthodes de pagination
const goToPage = (page) => {
  if (typeof page === 'number' && page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const resetPagination = () => {
  currentPage.value = 1
}

// Lifecycle
onMounted(async () => {
  updateIsMobile()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateIsMobile)
  }
  
  // Si l'utilisateur n'est pas encore chargé, attendre un peu
  if (userStore.isLoading || (!userStore.isAuthenticated && !userStore.id)) {
    // Attendre que l'utilisateur soit chargé (max 3 secondes)
    let attempts = 0
    while ((userStore.isLoading || !userStore.isAuthenticated) && attempts < 30) {
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
    }
  }
  
  await loadReferenceData()
  await loadQuizData()
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateIsMobile)
  }
})
</script>

<style scoped>
.quiz-history {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem 0;
}

.quiz-header {
  margin-bottom: 1.5rem;
}

.quiz-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.quiz-filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  min-width: 160px;
  font-size: 0.875rem;
}

.filter-select:disabled {
  background: #f9fafb;
  color: #9ca3af;
}

/* Filtres de maîtrise inline */

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

/* Stats globales */
.stats-section {
  margin-bottom: 1.5rem;
}

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
.matiere-stats {
  margin-bottom: 1.5rem;
}

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

/* Liste des quiz */
.quiz-list-section {
  margin-top: 2rem;
}

.quiz-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 0.75rem;
  margin: -0.75rem -0.75rem 1rem -0.75rem;
  border-radius: 8px;
  transition: background-color 0.2s;
  gap: 1rem;
}

.quiz-list-header .section-subtitle {
  margin: 0;
  align-self: center;
}

.inline-mastery-filters {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.quiz-list-header:hover {
  background-color: #f8fafc;
}

.section-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s;
}

.section-toggle:hover {
  background-color: #e5e7eb;
  color: #374151;
}

.section-toggle svg {
  transition: transform 0.2s;
}

.section-toggle.expanded svg {
  transform: rotate(180deg);
}

.quiz-list-content {
  animation: slideDown 0.3s ease-out;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}



.quiz-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* Styles des quiz cards */
.quiz-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s;
}

.quiz-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
}

.quiz-score.score-good {
  background: #d1fae5;
  color: #065f46;
}

.quiz-score.score-average {
  background: #fef3c7;
  color: #92400e;
}

.quiz-score.score-poor {
  background: #fee2e2;
  color: #991b1b;
}

.retry-indicator {
  margin-left: 0.25rem;
  font-size: 0.7rem;
}

.expand-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.expand-toggle:hover {
  background: #f3f4f6;
}

.expand-toggle.expanded svg {
  transform: rotate(180deg);
}

.expand-toggle svg {
  transition: transform 0.2s;
}

.quiz-card-details {
  border-top: 1px solid #e5e7eb;
  padding-top: 0.75rem;
  margin-top: 0.5rem;
}

.quiz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.8rem;
  color: #6b7280;
}

.breadcrumb-item {
  font-weight: 500;
}

.breadcrumb-separator {
  color: #d1d5db;
}

.quiz-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.quiz-attempt {
  font-weight: 600;
}

.total-attempts {
  color: #9ca3af;
}

/* Loading */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding: 1rem 0;
}

.pagination-btn {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #374151;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-pages {
  display: flex;
  gap: 0.25rem;
}

.pagination-page {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s;
}

.pagination-page:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #374151;
}

.pagination-page.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.pagination-page.active:hover {
  background: #2563eb;
  border-color: #2563eb;
}

/* Responsive */
@media (max-width: 1024px) {
  .quiz-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .quiz-filters {
    flex-direction: column;
  }

  .filter-select {
    min-width: 100%;
  }

  .stats-grid {
    flex-direction: column;
    align-items: center;
  }

  .quiz-grid {
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

  .quiz-list-header {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }

  .inline-mastery-filters {
    align-self: stretch;
    justify-content: space-between;
  }

  .inline-mastery-btn {
    flex: 1;
    justify-content: center;
  }

  /* Mobile: icônes seules pour les filtres (sauf "Tous") */
  .inline-mastery-btn:not(.all) .inline-mastery-label {
    display: none;
  }
  .inline-mastery-btn:not(.all) {
    min-width: 36px;
    padding: 0.25rem;
  }
  .inline-mastery-btn:not(.all) .inline-mastery-icon {
    font-size: 1rem;
  }

  .pagination-container {
    gap: 0.25rem;
  }

  .pagination-btn {
    padding: 0.375rem 0.5rem;
    font-size: 0.8rem;
  }

  .pagination-page {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }

  /* Pagination responsive: icônes seules en mobile */
  .pagination-btn .pagination-label {
    display: none;
  }
  .pagination-btn {
    padding: 0.375rem 0.5rem;
    width: 36px;
    height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
