<template>
  <BaseHistory
    ref="baseHistoryRef"
    title="🧭 Historique des Exercices"
    list-title="📝 Exercices effectués"
    loading-text="Chargement des exercices..."
    api-endpoint="/api/suivis/exercices/stats/"
    :custom-filters="masteryFilters"
    :navigation-handler="navigateToExercice"
    :items-per-page="12"
    :filtered-items="filteredExercicesList"
    @data-loaded="onDataLoaded"
    @filter-changed="onFilterChanged"
  >
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
          <span class="stat-label">Notions maîtrisées</span>
          <span class="stat-value">{{ stats.masteredNotions || 0 }}</span>
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
            <span class="matiere-count">{{ matiere.exercice_count }} exercices</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Filtres personnalisés -->
    <template #custom-filters="{ filters, selected }">
      <div class="inline-mastery-filters">
        <button
          v-for="filter in filters"
          :key="filter.value"
          @click.stop="updateSelectedMastery(filter.value)"
          :class="['inline-mastery-btn', filter.class, { active: selectedMastery === filter.value }]"
        >
          <span class="inline-mastery-icon">{{ filter.icon }}</span>
          <span class="inline-mastery-label">{{ filter.label }}</span>
        </button>
      </div>
    </template>

    <!-- Liste des exercices -->
    <template #items-list="{ items, toggleDetails, isExpanded, navigateToItem }">
             <div v-for="exercice in items" :key="exercice.id" class="exercice-card" :class="{ 'correct': exercice.est_correct, 'incorrect': !exercice.est_correct }">
        <div class="exercice-card-header" @click="toggleDetails(exercice.id)">
          <div class="exercice-card-title-section">
            <h5 class="exercice-card-title clickable-title" @click.stop="navigateToItem(exercice)" :title="'Accéder à l\'exercice: ' + exercice.exercice_titre">
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
            <button class="expand-toggle" :class="{ expanded: isExpanded(exercice.id) }">
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseHistory from './BaseHistory.vue'

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

  return filtered
})

// Méthodes
const onDataLoaded = (data) => {
  currentExercicesList.value = data.exercice_list || []
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

    const exerciceId = exercice.exercice_id

    // Navigation directe vers la page détail de l'exercice
    await router.push({
      name: 'ExerciceDetail',
      params: { exerciceId: String(exerciceId) }
    })

    console.log(`[ExercicesHistory] ✅ Navigation complétée`)
  } catch (error) {
    console.error(`[ExercicesHistory] ❌ Erreur de navigation:`, error)
  }
}



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

.stat-card.exercice-completed {
  border-color: #8b5cf6;
}
.stat-card.exercice-completed .stat-value {
  color: #8b5cf6;
}

.stat-card.exercice-correct {
  border-color: #10b981;
}
.stat-card.exercice-correct .stat-value {
  color: #059669;
}

.stat-card.exercice-percentage {
  border-color: #f59e0b;
}
.stat-card.exercice-percentage .stat-value {
  color: #d97706;
}

.stat-card.exercice-notions {
  border-color: #3b82f6;
}
.stat-card.exercice-notions .stat-value {
  color: #2563eb;
}

/* Statistiques par matière */
.section-subtitle {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
  text-align: center;
}

.matiere-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.matiere-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.matiere-name {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.matiere-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.matiere-average {
  font-weight: 600;
  color: #059669;
}

.matiere-count {
  color: #6b7280;
}

/* Filtres de maîtrise inline */
.inline-mastery-filters {
  display: flex;
  gap: 0.25rem;
  align-items: center;
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

.inline-mastery-btn.all.active {
  background: #3b82f6;
  border-color: #3b82f6;
}

.inline-mastery-btn.correct.active {
  background: #3b82f6;
  border-color: #3b82f6;
}

.inline-mastery-btn.incorrect.active {
  background: #3b82f6;
  border-color: #3b82f6;
}

.inline-mastery-icon {
  font-size: 0.75rem;
}

.inline-mastery-label {
  font-size: 0.75rem;
}

/* Cartes d'exercices */
.exercice-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.exercice-card:hover {
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transform: translateY(-1px);
}

.exercice-card.correct {
  border-color: #10b981;
}

.exercice-card.incorrect {
  border-color: #ef4444;
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
  background-color: #f9fafb;
}

.exercice-card-title-section {
  flex: 1;
  min-width: 0;
}

.exercice-card-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
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
  color: #6b7280;
  transition: color 0.2s;
}

.clickable-title:hover .navigation-icon {
  color: #3b82f6;
}

.exercice-breadcrumb-compact {
  font-size: 0.75rem;
  color: #6b7280;
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
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.expand-toggle:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
  color: #374151;
}

.expand-toggle svg {
  transition: transform 0.2s;
}

.expand-toggle.expanded svg {
  transform: rotate(180deg);
}

.exercice-card-details {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background-color: #f9fafb;
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
  color: #374151;
  font-weight: 500;
}

.breadcrumb-separator {
  color: #9ca3af;
}

.exercice-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
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
  color: #9ca3af;
  margin-top: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .stat-card {
    min-width: 200px;
  }
  
  .matiere-grid {
    grid-template-columns: 1fr;
  }
  
  .inline-mastery-filters {
    align-self: stretch;
    justify-content: space-between;
  }
  
  .inline-mastery-btn {
    flex: 1;
    justify-content: center;
  }
  
  .exercice-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  

}
</style>
