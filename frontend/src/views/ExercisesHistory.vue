<template>
  <DashboardLayout>
    <div class="history-page">
      <h2 class="page-title">Historique complet des exercices</h2>

      <BaseHistory
        title="🧭 Historique des Exercices"
        list-title="📝 Tous mes exercices"
        loading-text="Chargement de l'historique..."
        api-endpoint="/api/suivis/exercices/stats/"
        :items-per-page="20"
        :navigation-handler="navigateToExercice"
      >
        <!-- Tableau résumé matière/notion (identique au dashboard, avec tri + détails chapitres) -->
        <template #matiere-notion-stats="{ stats }">
          <div class="summary-table">
            <div class="summary-header">
              <div>Matière</div>
              <div>Notion</div>
              <div class="sortable-header" @click="sortBy('exercice_count')">
                Faits
                <span class="sort-icon" :class="{ active: sortField === 'exercice_count' }">{{ sortField === 'exercice_count' && sortDirection === 'asc' ? '↑' : '↓' }}</span>
              </div>
              <div class="sortable-header" @click="sortBy('correct_count')">
                Réussis
                <span class="sort-icon" :class="{ active: sortField === 'correct_count' }">{{ sortField === 'correct_count' && sortDirection === 'asc' ? '↑' : '↓' }}</span>
              </div>
              <div class="sortable-header" @click="sortBy('incorrect_count')">
                Ratés
                <span class="sort-icon" :class="{ active: sortField === 'incorrect_count' }">{{ sortField === 'incorrect_count' && sortDirection === 'asc' ? '↑' : '↓' }}</span>
              </div>
              <div class="sortable-header" @click="sortBy('average')">
                Moyenne
                <span class="sort-icon" :class="{ active: sortField === 'average' }">{{ sortField === 'average' && sortDirection === 'asc' ? '↑' : '↓' }}</span>
              </div>
            </div>

            <template v-for="row in sortStats(stats)" :key="`${row.matiere.id}-${row.notion.id}`">
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
                <div class="cell count">{{ row.exercice_count }}</div>
                <div class="cell correct">{{ row.correct_count }}</div>
                <div class="cell incorrect">{{ row.incorrect_count }}</div>
                <div class="cell average" :class="getAverageClass(row.average)">{{ formatAverage(row.average) }}</div>
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
                        <div class="cell count">{{ ch.exercice_count }}</div>
                        <div class="cell correct">{{ ch.correct_count }}</div>
                        <div class="cell incorrect">{{ ch.incorrect_count }}</div>
                        <div class="cell ratio">{{ Math.round(ch.ratio_percent) }}%</div>
                        <div class="cell average" :class="getAverageClass(ch.average_10 * 10)">{{ ch.average_10 }}/10</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </template>

        <!-- Liste des items (même rendu que dashboard) -->
        <template #items-list="{ items, toggleDetails, isExpanded, navigateToItem }">
          <div v-for="exercice in items" :key="exercice.id" class="exercice-card" :class="{ 'correct': exercice.est_correct, 'incorrect': !exercice.est_correct }">
            <div class="exercice-card-header" @click="toggleDetails(exercice.id)">
              <div class="exercice-card-title-section">
                <h5 class="exercice-card-title clickable-title" @click.stop="navigateToExercice(exercice)" :title="'Accéder à l\'exercice: ' + exercice.exercice_titre">
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
                <span class="exercice-time" v-if="exercice.temps_seconde">{{ formatTime(exercice.temps_seconde) }}</span>
                <span class="exercice-points" v-if="exercice.points_obtenus">{{ exercice.points_obtenus }} points</span>
              </div>
            </div>
          </div>
        </template>
      </BaseHistory>
    </div>
  </DashboardLayout>
  
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import BaseHistory from '@/components/dashboard/BaseHistory.vue'
import apiClient from '@/api/client'

const router = useRouter()

const navigateToExercice = (exercice) => {
  router.push({ name: 'ExerciceDetail', params: { exerciceId: String(exercice.exercice_id) } })
}

// Tri et détails pour le tableau résumé (identique au dashboard)
const sortField = ref('exercice_count')
const sortDirection = ref('desc')
const expandedNotions = ref(new Set())
const notionDetails = ref({})

const sortStats = (statsArray) => {
  const rows = Array.isArray(statsArray) ? statsArray : []
  const withAverage = rows.map(r => ({
    ...r,
    average: r.exercice_count > 0 ? (r.correct_count / r.exercice_count) * 100 : 0
  }))
  return [...withAverage].sort((a, b) => {
    const aValue = a[sortField.value] || 0
    const bValue = b[sortField.value] || 0
    return sortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
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

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
}

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
    const response = await apiClient.get('/api/suivis/exercices/stats/', { params: { matiere: matiereId, notion: notionId } })
    const list = Array.isArray(response?.data?.exercice_list) ? response.data.exercice_list : []
    const chapters = computeChapterStats(list)
    notionDetails.value[key] = { loading: false, error: '', chapters }
  } catch (error) {
    const message = (error?.response?.data?.error) || 'Erreur lors du chargement des détails'
    notionDetails.value[key] = { loading: false, error: message, chapters: [] }
  }
}

const computeChapterStats = (exerciceList) => {
  const map = new Map()
  for (const item of exerciceList) {
    const chap = item?.chapitre || {}
    const chapId = chap?.id
    if (!chapId) continue
    if (!map.has(chapId)) {
      map.set(chapId, { chapitre: { id: chapId, titre: chap?.titre || 'Chapitre' }, exercice_count: 0, correct_count: 0, incorrect_count: 0 })
    }
    const agg = map.get(chapId)
    agg.exercice_count += 1
    if (item.est_correct) agg.correct_count += 1
    else agg.incorrect_count += 1
  }
  const chapters = Array.from(map.values()).map(ch => {
    const ratio = ch.exercice_count > 0 ? (ch.correct_count / ch.exercice_count) : 0
    const average10 = Math.round(ratio * 10 * 10) / 10
    return { ...ch, ratio_percent: ratio * 100, average_10: average10 }
  })
  chapters.sort((a, b) => String(a.chapitre.titre).localeCompare(String(b.chapitre.titre), 'fr', { sensitivity: 'base' }))
  return chapters
}

const getStatusClass = (estCorrect) => (estCorrect ? 'status-correct' : 'status-incorrect')

// Utils copied from base for the details panel
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
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

/* Résumé matière/notion (comme dashboard) */
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

/* Détails sous notion */
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

/* Cartes d'exercices (liste) */
.exercice-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.exercice-card:hover { box-shadow: 0 4px 6px rgba(0,0,0,0.1); transform: translateY(-1px); }
.exercice-card.correct { border-color: #10b981; }
.exercice-card.incorrect { border-color: #ef4444; }
.exercice-card-header { display: flex; justify-content: space-between; align-items: flex-start; padding: 1rem; cursor: pointer; transition: background-color 0.2s; }
.exercice-card-header:hover { background-color: #f9fafb; }
.exercice-card-title-section { flex: 1; min-width: 0; }
.exercice-card-title { font-size: 0.875rem; font-weight: 600; color: #1f2937; margin: 0 0 0.25rem 0; line-height: 1.4; }
.clickable-title { cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: color 0.2s; }
.clickable-title:hover { color: #3b82f6; }
.navigation-icon { flex-shrink: 0; color: #6b7280; transition: color 0.2s; }
.clickable-title:hover .navigation-icon { color: #3b82f6; }
.exercice-breadcrumb-compact { font-size: 0.75rem; color: #6b7280; line-height: 1.3; }
.exercice-card-actions { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.exercice-status { display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%; font-size: 1rem; font-weight: 600; }
.status-correct { background: #d1fae5; color: #059669; }
.status-incorrect { background: #fee2e2; color: #dc2626; }
.expand-toggle { background: none; border: 1px solid #e5e7eb; border-radius: 6px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #6b7280; transition: all 0.2s; }
.expand-toggle:hover { background-color: #f9fafb; border-color: #d1d5db; color: #374151; }
.expand-toggle svg { transition: transform 0.2s; }
.expand-toggle.expanded svg { transform: rotate(180deg); }
.exercice-card-details { padding: 1rem; border-top: 1px solid #e5e7eb; background-color: #f9fafb; }
.exercice-breadcrumb { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem; font-size: 0.75rem; flex-wrap: wrap; }
.breadcrumb-item { color: #374151; font-weight: 500; }
.breadcrumb-separator { color: #9ca3af; }
.exercice-meta { display: flex; gap: 1rem; font-size: 0.75rem; color: #6b7280; flex-wrap: wrap; }
.exercice-date, .exercice-time, .exercice-points { display: flex; align-items: center; gap: 0.25rem; }
</style>


