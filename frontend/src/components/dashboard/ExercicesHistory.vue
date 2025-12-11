<template>
  <BaseHistory
    ref="baseHistoryRef"
    title="🧭 Historique des Exercices"
      list-title="📝 Exercices effectués"
      loading-text="Chargement des exercices..."
      api-endpoint="/api/suivis/exercices/stats/"
      :extra-params="historyParams"
      :navigation-handler="navigateToExercice"
      :items-per-page="6"
      :filtered-items="filteredExercicesList"
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
        <div class="stat-card exercice-completed">
          <span class="stat-label">Exercices effectués</span>
          <span class="stat-value">{{ stats.completed || 0 }}</span>
        </div>
        <div class="stat-card exercice-correct">
          <span class="stat-label">Exercices réussis</span>
          <span class="stat-value">{{ stats.correct || 0 }}</span>
        </div>
        <div class="stat-card exercice-percentage">
          <span class="stat-label">Taux de réussite</span>
          <span class="stat-value">{{ stats.percentage || 0 }}%</span>
        </div>
        <div class="stat-card exercice-notions">
          <span class="stat-label">Chapitres maîtrisés</span>
          <span class="stat-value">{{ stats.masteredNotions || 0 }}</span>
        </div>
      </div>
    </template>

    

    <!-- Tableau récapitulatif matière / notion -->
    <template #matiere-notion-stats="{ stats }">
      <!-- Version Desktop : Tableau -->
      <div class="summary-table desktop-only">
        <div class="summary-header">
          <div>Matière</div>
          <div>Chapitre</div>
          <div class="sortable-header" @click="sortBy('exercice_count')">
            Faits
            <span class="sort-icon" :class="{ active: sortField === 'exercice_count' }">
              {{ sortField === 'exercice_count' && sortDirection === 'asc' ? '↑' : '↓' }}
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
          <div class="sortable-header" @click="sortBy('average')">
            Moyenne
            <span class="sort-icon" :class="{ active: sortField === 'average' }">
              {{ sortField === 'average' && sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </div>
        </div>
        <template v-for="row in pagedSummaryRows" :key="`${row.matiere.id}-${row.notion.id}`">
          <div class="summary-row">
            <div class="cell matiere">{{ row.matiere.titre }}</div>
            <div class="cell notion">
              <span class="notion-label">{{ row.notion.titre }}</span>
            </div>
            <div class="cell count">{{ row.exercice_count }}</div>
            <div class="cell correct">{{ row.correct_count }}</div>
            <div class="cell incorrect">{{ row.incorrect_count }}</div>
            <div class="cell average" :class="getAverageClass(row.average)">{{ formatAverage(row.average) }}</div>
          </div>
        </template>
      </div>

      <!-- Version Mobile : Cartes -->
      <div class="summary-cards mobile-only">
        <div class="sort-controls">
          <span class="sort-label">Trier par :</span>
          <select v-model="sortField" @change="sortDirection = 'desc'" class="sort-select">
            <option value="exercice_count">Faits</option>
            <option value="correct_count">Réussis</option>
            <option value="incorrect_count">Ratés</option>
            <option value="average">Moyenne</option>
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
                <span class="stat-value">{{ row.exercice_count }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Réussis</span>
                <span class="stat-value success">{{ row.correct_count }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Ratés</span>
                <span class="stat-value error">{{ row.incorrect_count }}</span>
              </div>
              <div class="stat-item highlight" :class="getAverageClass(row.average)">
                <span class="stat-label">Moyenne</span>
                <span class="stat-value">{{ formatAverage(row.average) }}</span>
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


    <!-- Liste des exercices -->
        <template #items-list="{ items, toggleDetails, isExpanded, navigateToItem }">
             <div
          v-for="exercice in items"
          :key="exercice.exercice_id || exercice.id"
          :id="`ex-${exercice.exercice_id || exercice.id}`"
          class="exercice-card"
          :class="{ 'correct': exercice.est_correct, 'incorrect': !exercice.est_correct }"
          @click="navigateToItem(exercice)"
        >
        <div class="exercice-card-header">
          <div class="exercice-card-title-section">
            <h5 class="exercice-card-title clickable-title" :title="'Accéder à l\'exercice: ' + exercice.exercice_titre">
              {{ exercice.exercice_titre }}
              <svg class="navigation-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 17l9.2-9.2M17 17V7H7"></path>
              </svg>
            </h5>
            <div class="exercice-breadcrumb-compact">
              {{ exercice.matiere.titre }} → {{ exercice.notion.titre }}
            </div>
          </div>
            <div class="exercice-card-actions">
              <div class="exercice-status" :class="getStatusClass(exercice.est_correct)">
                {{ exercice.est_correct ? '✅' : '❌' }}
              </div>
            <button class="expand-toggle" :class="{ expanded: isExpanded(exercice.id) }" @click.stop="toggleDetails(exercice.id)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </button>
          </div>
        </div>
        
        <div v-if="isExpanded(exercice.id)" class="exercice-card-details">
          <div class="exercice-breadcrumb">
            <span class="breadcrumb-item">{{ exercice.matiere.titre }}</span>
            <span class="breadcrumb-separator">→</span>
            <span class="breadcrumb-item">{{ exercice.notion.titre }}</span>
            <span class="breadcrumb-separator">→</span>
            <span class="breadcrumb-item">{{ exercice.chapitre.titre }}</span>
          </div>
          
          <div class="exercice-meta">
            <span class="exercice-date">{{ formatDate(exercice.date_creation) }}</span>
            <span class="exercice-time" v-if="exercice.temps_seconde">
              {{ formatTime(exercice.temps_seconde) }}
            </span>
            <span class="exercice-points" v-if="exercice.points_obtenus">
              {{ exercice.points_obtenus }} points
            </span>
          </div>
        </div>
             </div>
     </template>

    <!-- État vide -->
    <template #empty-state>
      <p>Aucun exercice trouvé avec ces filtres</p>
      <p class="empty-hint">Essayez de modifier vos filtres ou commencez à faire des exercices !</p>
    </template>
  </BaseHistory>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import BaseHistory from './BaseHistory.vue'
import apiClient from '@/api/client'

const props = defineProps({
  childId: {
    type: [Number, String],
    default: null
  },
  showSuggestions: {
    type: Boolean,
    default: true
  }
})

// Router
const router = useRouter()

// État
const baseHistoryRef = ref(null)

// Filtres de maîtrise pour exercices
const masteryFilters = [
  { value: 'all', label: 'Tous', icon: '', class: 'all' },
  { value: 'correct', label: 'Réussis', icon: '✅', class: 'correct' },
  { value: 'incorrect', label: 'Ratés', icon: '❌', class: 'incorrect' }
]

// État des filtres
const selectedMastery = ref('all')
const currentExercicesList = ref([])

// État du tri pour le tableau matière/notion
const sortField = ref('exercice_count')
const sortDirection = ref('desc')
const matiereNotionStats = ref([])
// Pagination pour le tableau récapitulatif
const SUMMARY_PER_PAGE = 5
const summaryPage = ref(1)

const sortedRecent = computed(() => {
  return [...currentExercicesList.value].sort((a, b) => {
    const da = new Date(a.date_creation || a.created_at || a.date || 0).getTime()
    const db = new Date(b.date_creation || b.created_at || b.date || 0).getTime()
    return db - da
  })
})

const lastDone = computed(() => sortedRecent.value[0] || null)
const lastIncorrect = computed(() => sortedRecent.value.find((e) => e.est_correct === false) || null)

const historyParams = computed(() => {
  const params = {}
  if (props.childId) params.child_id = props.childId
  return params
})

const suggestionCards = computed(() => {
  const cards = []

  if (lastIncorrect.value?.notion?.id) {
    const notionId = lastIncorrect.value.notion.id
    const exerciceId = lastIncorrect.value.exercice_id || lastIncorrect.value.id
    cards.push({
      key: `retry-${lastIncorrect.value.notion.id}`,
      badge: 'À revoir',
      badgeClass: 'badge-warning',
      notionLabel: lastIncorrect.value.notion.titre || 'Notion',
      title: 'Reprends où tu t’es arrêté',
      subtitle: `Revois l’exercice “${lastIncorrect.value.exercice_titre || 'Dernier exercice'}”.`,
      cta: 'Réessayer cet exercice',
      notionId,
      exerciceId
    })
  }

  if (lastDone.value?.notion?.id) {
    const notionId = lastDone.value.notion.id
    const exerciceId = lastDone.value.exercice_id || lastDone.value.id
    cards.push({
      key: `practice-${lastDone.value.notion.id}`,
      badge: 'Entraînement',
      badgeClass: 'badge-info',
      notionLabel: lastDone.value.notion.titre || 'Notion',
      title: 'Poursuis là où tu t’es arrêté',
      subtitle: `Continue “${lastDone.value.exercice_titre || 'Dernier exercice'}” ou un exercice proche.`,
      cta: 'Reprendre cet exercice',
      notionId,
      exerciceId
    })
  }

  return cards.slice(0, 2)
})

const openSuggestion = async (card) => {
  try {
    const notionId = card?.notionId || card?.notion?.id || card?.notion_id
    const exerciceId = card?.exerciceId || card?.exercice_id || card?.id

    if (notionId && exerciceId) {
      await router.push({
        name: 'ExercicesByNotion',
        params: { notionId: String(notionId) },
        hash: `#ex-${exerciceId}`
      })
      return
    }

    if (exerciceId) {
      await router.push({
        name: 'ExerciceDetail',
        params: { exerciceId: String(exerciceId) }
      })
      return
    }
  } catch (error) {
    console.error('[ExercicesHistory] Navigation suggestion échouée:', error)
  }
}

// Chapitres supprimés: plus de tri dédié

// Chapitres supprimés: plus d'expansion/détails

// Chapitres supprimés: plus de cache

// Computed pour filtrer les exercices selon le niveau de maîtrise
const filteredExercicesList = computed(() => {
  let filtered = currentExercicesList.value

  // Filtrer par statut de réussite
  if (selectedMastery.value !== 'all') {
    filtered = filtered.filter(exercice => {
      switch (selectedMastery.value) {
        case 'correct':
          return exercice.est_correct === true
        case 'incorrect':
          return exercice.est_correct === false
        default:
          return true
      }
    })
  }

  // Trier par date décroissante (derniers réalisés en premier)
  filtered = [...filtered].sort((a, b) => {
    const da = new Date(a.date_creation || a.created_at || a.date || 0).getTime()
    const db = new Date(b.date_creation || b.created_at || b.date || 0).getTime()
    return db - da
  })
  // Ne garder que les 6 derniers
  return filtered.slice(0, 6)
})

// Méthodes
const onDataLoaded = (data) => {
  // Le backend peut limiter la payload avec ?limit=6, sinon on tronque côté front
  const list = Array.isArray(data.exercice_list) ? data.exercice_list : []
  currentExercicesList.value = list.slice(0, 6)
  
  // Sauvegarder les stats matière/notion pour le tri
  matiereNotionStats.value = Array.isArray(data.matiere_notion_stats) ? data.matiere_notion_stats : []
}

const onFilterChanged = (filters) => {
  console.log('Filtres changés:', filters)
}

const getStatusClass = (estCorrect) => {
  return estCorrect ? 'status-correct' : 'status-incorrect'
}

const navigateToExercice = async (exercice) => {
  try {
    console.log(`[ExercicesHistory] 🚀 Navigation vers exercice: ${exercice.exercice_titre}`)

    const notionId = exercice?.notion?.id || exercice?.notion_id || exercice?.notion?.notion_id
    const exerciceId = exercice?.exercice_id || exercice?.id

    // Préférer la page notion avec ancre vers l'exercice
    if (notionId && exerciceId) {
      await router.push({
        name: 'ExercicesByNotion',
        params: { notionId: String(notionId) },
        hash: `#ex-${exerciceId}`
      })
      console.log(`[ExercicesHistory] ✅ Navigation complétée (notion ${notionId} -> ex-${exerciceId})`)
      return
    }

    // Fallback: page détail
    if (exerciceId) {
      await router.push({
        name: 'ExerciceDetail',
        params: { exerciceId: String(exerciceId) }
      })
      console.log(`[ExercicesHistory] ✅ Navigation complétée (fallback détail)`)
      return
    }

    console.warn('[ExercicesHistory] Impossible de naviguer: notionId ou exerciceId manquant')
  } catch (error) {
    console.error(`[ExercicesHistory] ❌ Erreur de navigation:`, error)
  }
}

const goToFullHistory = () => {
  router.push({ name: 'ExercisesHistory' })
}

// Computed pour le tri des stats matière/notion
const sortedStats = computed(() => {
  if (!matiereNotionStats.value.length) return []
  
  // Ajouter la moyenne calculée à chaque ligne (sur 20)
  const statsWithAverage = matiereNotionStats.value.map(row => ({
    ...row,
    average: row.exercice_count > 0 ? Math.round((row.correct_count / row.exercice_count) * 20 * 10) / 10 : 0
  }))
  
  const sorted = [...statsWithAverage].sort((a, b) => {
    const aValue = a[sortField.value] || 0
    const bValue = b[sortField.value] || 0
    
    if (sortDirection.value === 'asc') {
      return aValue - bValue
    } else {
      return bValue - aValue
    }
  })
  
  return sorted
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

// Méthode pour changer le tri
const sortBy = (field) => {
  if (sortField.value === field) {
    // Inverser la direction si c'est le même champ
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Nouveau champ, commencer par décroissant
    sortField.value = field
    sortDirection.value = 'desc'
  }
}

// Chapitres supprimés: plus de tri

// Méthodes utilitaires pour la moyenne
const formatAverage = (average) => {
  if (average === 0) return '0/20'
  return `${average}/20`
}

const getAverageClass = (average) => {
  if (average >= 15) return 'excellent'  // ≥ 15/20 = vert
  if (average >= 10) return 'good'       // 10-14.9/20 = orange
  return 'poor'                          // < 10/20 = rouge
}


// Chapitres supprimés: plus d’expansion/prefetch/observer

onBeforeUnmount(() => {})

// Chapitres supprimés: plus de stats chapitres

// Fonction pour trier les chapitres selon le champ et la direction sélectionnés
// Chapitres supprimés: plus de tri



// Méthodes utilitaires (à récupérer du composant de base)
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

// Watcher pour synchroniser le filtre personnalisé
const updateSelectedMastery = (value) => {
  selectedMastery.value = value
}

// Exposer la méthode pour le slot
defineExpose({
  updateSelectedMastery
})
</script>

<style scoped>
.practice-suggestions {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px 16px 14px;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.suggestion-header {
  margin-bottom: 10px;
}

.suggestion-title {
  font-weight: 800;
  color: #1d4ed8;
}

.suggestion-subtitle {
  color: #475569;
  font-size: 0.95rem;
}

.suggestion-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}

.suggestion-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}

.suggestion-card-head {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.suggestion-notion {
  font-weight: 700;
  color: #0f172a;
  font-size: 1rem;
  text-align: right;
}

.badge {
  padding: 4px 8px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.8rem;
}

.badge-warning {
  background: #fef3c7;
  color: #9a3412;
  border: 1px solid #fcd34d;
}

.badge-info {
  background: #e0f2fe;
  color: #0ea5e9;
  border: 1px solid #bae6fd;
}

.suggestion-body {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.suggestion-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  color: #1f2937;
}

.suggestion-title-line {
  font-weight: 800;
  font-size: 0;
}

.suggestion-cta {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  min-width: 150px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.15);
}

.suggestion-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
}

.suggestion-cta:active {
  transform: translateY(0);
}

@media (max-width: 640px) {
  .practice-suggestions {
    padding: 12px 12px 14px;
  }

  .suggestion-cards {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .suggestion-card {
    padding: 12px;
    flex-direction: column;
    align-items: flex-start;
  }

  .suggestion-card-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }

  .suggestion-notion {
    text-align: left;
    font-size: 0.9rem;
  }

  .suggestion-body {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .suggestion-cta {
    width: 100%;
    text-align: center;
    align-self: stretch;
  }

  .suggestion-title-line {
    font-size: 1rem;
  }

  .suggestion-desc {
    font-size: 0.9rem;
  }
}

/* Stats globales - Design épuré (identique à QuizHistory) */
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

/* Couleurs des valeurs - même palette que QuizHistory */
.stat-card.exercice-completed .stat-value { color: #3b82f6; }
.stat-card.exercice-correct .stat-value { color: #10b981; }
.stat-card.exercice-percentage .stat-value { color: #10b981; }
.stat-card.exercice-notions .stat-value { color: #8b5cf6; }

/* Statistiques par matière */
.section-subtitle {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1e293b;
  margin: 1.25rem 0 0.75rem;
}

.matiere-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.matiere-card {
  background: transparent;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 0.25rem;
  text-align: center;
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
  color: #10b981;
}

.matiere-count {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* Filtres de maîtrise inline */
.inline-mastery-filters {
  display: flex;
  gap: 0.25rem;
  align-items: center;
  width: 100%;
}

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

/* Cartes d'exercices - Design épuré */
.exercice-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.exercice-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
}

.exercice-card.correct {
  border-left: 3px solid #10b981;
}

.exercice-card.incorrect {
  border-left: 3px solid #ef4444;
}

.exercice-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.exercice-card-header:hover {
  background-color: #f8fafc;
}

.exercice-card-title-section {
  flex: 1;
  min-width: 0;
}

.exercice-card-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.clickable-title {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s;
}

.clickable-title:hover {
  color: #3b82f6;
}

.navigation-icon {
  flex-shrink: 0;
  color: #64748b;
  transition: color 0.2s;
}

.clickable-title:hover .navigation-icon {
  color: #3b82f6;
}

.exercice-breadcrumb-compact {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
  line-height: 1.3;
}

.exercice-card-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.exercice-status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 1rem;
  font-weight: 600;
}

.status-correct {
  background: #d1fae5;
  color: #059669;
}

.status-incorrect {
  background: #fee2e2;
  color: #dc2626;
}

.expand-toggle {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.expand-toggle:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1;
  color: #334155;
}

.expand-toggle svg {
  transition: transform 0.2s;
}

.expand-toggle.expanded svg {
  transform: rotate(180deg);
}

.exercice-card-details {
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.exercice-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.75rem;
  flex-wrap: wrap;
}

.breadcrumb-item {
  color: #334155;
  font-weight: 500;
}

.breadcrumb-separator {
  color: #94a3b8;
}

.exercice-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #64748b;
  flex-wrap: wrap;
}

.exercice-date,
.exercice-time,
.exercice-points {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}



/* État vide */
.empty-hint {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

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

/* Tableau résumé matière/notion - Design épuré */
.summary-table {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1rem;
}

/* Utilitaires responsive */
.desktop-only {
  display: block;
}

.mobile-only {
  display: none;
}

/* Desktop : afficher uniquement le tableau */
@media (min-width: 769px) {
  .desktop-only {
    display: block !important;
  }

  .mobile-only {
    display: none !important;
  }
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

.summary-row .cell.average .avg-badge,
.summary-row .cell.average {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 56px;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.8125rem;
}

.summary-row .cell.average.excellent { 
  background: #dcfce7; 
  color: #166534; 
}
.summary-row .cell.average.good { 
  background: #fef3c7; 
  color: #92400e; 
}
.summary-row .cell.average.poor { 
  background: #fee2e2; 
  color: #991b1b; 
}

/* Pagination du tableau récapitulatif */
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

/* En-têtes triables */
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


/* Notion toggle */
.notion-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.15rem 0.4rem;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  color: #1f2937;
}
.notion-toggle:hover { background: #f3f4f6; }
.notion-toggle.active { 
  background: #dbeafe; 
  color: #1e40af; 
  border-color: #3b82f6;
  font-weight: 600;
}
.notion-toggle.active:hover { 
  background: #bfdbfe; 
  border-color: #2563eb;
}
.notion-toggle .chevron { transition: transform 0.2s; color: #6b7280; }
.notion-toggle .chevron.expanded { transform: rotate(180deg); color: #374151; }
.notion-toggle.active .chevron { color: #1e40af; }
.notion-toggle.active .chevron.expanded { color: #1e40af; }

/* Details row under notion */
.summary-details-row {
  display: block;
  padding: 0 0.5rem 0.75rem 0.5rem;
  border-bottom: 1px solid #f3f4f6;
}
.summary-details-row .details-cell {
  grid-column: 1 / -1;
}
.chapter-table {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
  overflow: hidden;
}
.chapter-header,
.chapter-row {
  display: grid;
  grid-template-columns: 2fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  align-items: center;
}
.chapter-header { 
  background: #eef2f7; 
  font-weight: 600; 
  color: #374151; 
  font-size: 0.875rem;
}
.chapter-row { background: #fff; border-top: 1px solid #f3f4f6; }
.chapter-loading { padding: 0.75rem; color: #6b7280; font-size: 0.85rem; }
.chapter-error { padding: 0.75rem; color: #dc2626; font-size: 0.85rem; }
.chapter-row .cell { font-size: 0.85rem; }
.chapter-row .cell.count,
.chapter-row .cell.correct,
.chapter-row .cell.incorrect,
.chapter-row .cell.ratio,
.chapter-row .cell.average { text-align: center; font-weight: 600; }
.chapter-row .cell.correct { color: #16a34a; }
.chapter-row .cell.incorrect { color: #dc2626; }

/* Couleurs des moyennes pour les chapitres - même système que les notions */
.chapter-row .cell.average.excellent { 
  color: #16a34a; 
  background: #dcfce7;
}
.chapter-row .cell.average.good { 
  color: #d97706; 
  background: #fef3c7;
}
.chapter-row .cell.average.poor { 
  color: #dc2626; 
  background: #fee2e2;
}

/* En-têtes triables pour les chapitres - même style que les notions */
.chapter-header .sortable-header {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  padding: 0.25rem;
  border-radius: 4px;
  gap: 0.35rem;
}
.chapter-header .sortable-header:hover {
  background-color: #d1d5db;
}
.chapter-header .sort-icon {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 700;
}
.chapter-header .sort-icon.active {
  color: #2563eb;
  font-weight: 700;
}

@media (max-width: 768px) {
  .chapter-header, .chapter-row {
    grid-template-columns: 1.4fr 0.7fr 0.7fr 0.7fr 0.7fr 0.7fr;
    padding: 0.45rem 0.5rem;
  }
}

/* Version Mobile : Cartes - Design professionnel et épuré */
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
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  background: #ffffff;
  font-size: 1.125rem;
  font-weight: 600;
  color: #3b82f6;
  cursor: pointer;
  min-width: 48px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sort-direction-btn:hover {
  background: #f8fafc;
  border-color: #94a3b8;
  transform: scale(1.02);
}

.sort-direction-btn:active {
  transform: scale(0.98);
}

.summary-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899);
  opacity: 0;
  transition: opacity 0.25s ease;
}

.summary-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
  border-color: #cbd5e1;
}

.summary-card:hover::before {
  opacity: 1;
}

.card-header {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
  position: relative;
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

.stat-item.highlight.excellent {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #86efac;
}

.stat-item.highlight.good {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border-color: #fcd34d;
}

.stat-item.highlight.poor {
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

.stat-item.highlight.excellent .stat-value {
  color: #047857;
  background: rgba(16, 185, 129, 0.1);
}

.stat-item.highlight.good .stat-value {
  color: #d97706;
  background: rgba(251, 191, 36, 0.15);
}

.stat-item.highlight.poor .stat-value {
  color: #b91c1c;
  background: rgba(239, 68, 68, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  /* Masquer tableau desktop, afficher cartes mobile */
  .desktop-only {
    display: none !important;
  }

  .mobile-only {
    display: block !important;
  }

  /* Stats grid : 2 colonnes sur mobile */
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }
  
  .stats-grid .stat-card {
    min-width: 0;
    padding: 0.75rem 0.5rem;
  }

  .stats-grid .stat-label {
    font-size: 0.7rem;
  }

  .stats-grid .stat-value {
    font-size: 1.15rem;
  }

  .summary-pagination {
    flex-wrap: wrap;
    gap: 0.25rem;
    padding: 0.5rem 0.25rem 0.75rem;
  }

  .pg-btn,
  .pg-page {
    padding: 0.25rem 0.4rem;
    font-size: 0.75rem;
    min-width: 30px;
    height: 30px;
  }
  
  .matiere-grid {
    grid-template-columns: 1fr;
  }
  
  .inline-mastery-filters {
    align-self: stretch !important;
    justify-content: space-between !important;
    gap: 0 !important;
    width: 100% !important;
  }
  
  .inline-mastery-btn {
    flex: 1 !important;
    justify-content: center !important;
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
  
  .exercice-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}

/* Très petits écrans */
@media (max-width: 480px) {
  /* Garder 2 colonnes pour .stats-grid jusqu'à 350px */
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .stats-grid .stat-card {
    padding: 0.65rem 0.5rem;
  }

  /* Entre 351px et 480px : 4 colonnes en ligne */
  .card-stats {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 0.375rem !important;
  }

  .stat-item.highlight {
    grid-column: auto !important;
  }

  .sort-controls {
    flex-wrap: wrap;
    padding: 0.75rem;
    gap: 0.5rem;
  }

  .sort-label {
    width: 100%;
    font-size: 0.75rem;
  }

  .sort-select {
    flex: 1;
    min-width: 0;
    font-size: 0.8125rem;
    padding: 0.5625rem 0.875rem;
  }

  .sort-direction-btn {
    min-width: 44px;
    height: 38px;
    font-size: 1rem;
  }

  .summary-card {
    padding: 1rem;
    border-radius: 14px;
  }

  .card-title {
    font-size: 1rem;
  }

  .card-subtitle {
    font-size: 0.75rem;
    padding: 0.1875rem 0.5rem;
  }

  /* Les règles pour 4 colonnes sont déjà définies plus haut dans cette media query */

  .summary-cards .stat-item {
    padding: 0.625rem 0.375rem;
    border-radius: 8px;
  }

  .summary-cards .stat-item.highlight {
    grid-column: auto !important;
    padding: 0.625rem 0.375rem;
    border-radius: 8px;
  }

  .summary-cards .stat-item .stat-label {
    font-size: 0.5625rem;
  }

  .summary-cards .stat-item .stat-value {
    font-size: 1.0625rem;
  }

  .summary-cards .stat-item.highlight .stat-value {
    font-size: 0.9375rem;
    padding: 0.1875rem 0.25rem;
  }
}

/* Petits écrans (jusqu'à 350px inclus) - grille 2x2 */
@media screen and (max-width: 350px) {
  /* Forcer 2 colonnes pour .stats-grid jusqu'à 350px */
  .stats-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.5rem !important;
  }

  .card-stats {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    grid-template-rows: repeat(2, auto) !important;
    gap: 0.5rem !important;
    min-width: 0 !important;
  }

  .summary-cards .stat-item {
    padding: 0.625rem 0.375rem !important;
    border-radius: 8px !important;
    min-width: 0 !important;
  }

  .summary-cards .stat-item.highlight {
    grid-column: auto !important;
    grid-row: auto !important;
    padding: 0.625rem 0.375rem !important;
  }

  .summary-cards .stat-item .stat-label {
    font-size: 0.5625rem !important;
    letter-spacing: 0.03em !important;
  }

  .summary-cards .stat-item .stat-value {
    font-size: 1rem !important;
  }

  .summary-cards .stat-item.highlight .stat-value {
    font-size: 0.9375rem !important;
    padding: 0.1875rem 0.25rem !important;
  }
}

/* Skeleton loader pour chapitres */
.chapter-skeleton { padding: 0.5rem; background: #fff; border-top: 1px solid #f3f4f6; }
.skeleton-row { display: grid; grid-template-columns: 2fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr; gap: 0.75rem; padding: 0.4rem 0.25rem; align-items: center; }
.skeleton-cell { height: 12px; border-radius: 6px; background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 37%, #f3f4f6 63%); background-size: 400% 100%; animation: skeleton-shimmer 1.2s ease-in-out infinite; }
.skeleton-cell.title { height: 14px; }
.skeleton-cell.num { width: 60%; justify-self: center; }
@keyframes skeleton-shimmer { 0% { background-position: 100% 0 } 100% { background-position: -100% 0 } }
</style>
