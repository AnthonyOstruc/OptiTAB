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
          <!-- Version Desktop : Tableau -->
          <div class="summary-table desktop-only">
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
            <template v-for="row in sortStats(stats)" :key="`${row.matiere.id}-${row.notion.id}`">
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
  /* Masquer tableau desktop, afficher cartes mobile */
  .desktop-only {
    display: none !important;
  }

  .mobile-only {
    display: block !important;
  }

  .summary-header, .summary-row { grid-template-columns: 1fr 1fr 0.7fr 0.7fr 0.7fr 0.7fr; padding: 0.5rem 0.75rem; }
}

/* Détails sous notion */
.notion-toggle { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.15rem 0.4rem; border: 1px solid transparent; border-radius: 6px; background: transparent; cursor: pointer; color: #1f2937; }
.notion-toggle:hover { background: #f3f4f6; }
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

.stat-item.highlight.average {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #93c5fd;
}

.stat-item.highlight.poor {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-color: #fca5a5;
}

.stat-label {
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

.stat-value {
  font-size: 1.125rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.1;
  white-space: nowrap;
}

.stat-value.success {
  color: #059669;
}

.stat-value.error {
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

.stat-item.highlight.average .stat-value {
  color: #2563eb;
  background: rgba(59, 130, 246, 0.1);
}

.stat-item.highlight.poor .stat-value {
  color: #b91c1c;
  background: rgba(239, 68, 68, 0.1);
}

/* Très petits écrans */
@media (max-width: 480px) {
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

  .stat-item {
    padding: 0.625rem 0.375rem;
    border-radius: 8px;
  }

  .stat-item.highlight {
    grid-column: auto !important;
    padding: 0.625rem 0.375rem;
    border-radius: 8px;
  }

  .stat-label {
    font-size: 0.5625rem;
  }

  .stat-value {
    font-size: 1.0625rem;
  }

  .stat-item.highlight .stat-value {
    font-size: 0.9375rem;
    padding: 0.1875rem 0.25rem;
  }
}

/* Petits écrans (jusqu'à 350px inclus) - grille 2x2 */
@media screen and (max-width: 350px) {
  .card-stats {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    grid-template-rows: repeat(2, auto) !important;
    gap: 0.5rem !important;
    min-width: 0 !important;
  }

  .stat-item {
    padding: 0.625rem 0.375rem !important;
    border-radius: 8px !important;
    min-width: 0 !important;
  }

  .stat-item.highlight {
    grid-column: auto !important;
    grid-row: auto !important;
    padding: 0.625rem 0.375rem !important;
  }

  .stat-label {
    font-size: 0.5625rem !important;
    letter-spacing: 0.03em !important;
  }

  .stat-value {
    font-size: 1rem !important;
  }

  .stat-item.highlight .stat-value {
    font-size: 0.9375rem !important;
    padding: 0.1875rem 0.25rem !important;
  }
}
</style>
