<template>
  <BaseHistory
    ref="baseHistoryRef"
    title="🧭 Historique des Exercices"
    list-title="📝 Exercices effectués"
    loading-text="Chargement des exercices..."
    api-endpoint="/api/suivis/exercices/stats/"
    :extra-params="{ limit: 6 }"
    :custom-filters="masteryFilters"
    :navigation-handler="navigateToExercice"
    :items-per-page="6"
    :filtered-items="filteredExercicesList"
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

    <!-- Tableau récapitulatif matière / notion -->
    <template #matiere-notion-stats="{ stats }">
      <div class="summary-table">
        <div class="summary-header">
          <div>Matière</div>
          <div>Notion</div>
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
        <template v-for="row in sortedStats" :key="`${row.matiere.id}-${row.notion.id}`">
          <div class="summary-row" :ref="el => setSummaryRowRef(row, el)">
            <div class="cell matiere">{{ row.matiere.titre }}</div>
            <div class="cell notion">
              <button
                class="notion-toggle"
                :class="{ active: isNotionExpanded(row) }"
                @click="toggleNotionDetails(row)"
                @mouseenter="prefetchNotionDetails(row)"
                @focus="prefetchNotionDetails(row)"
              >
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
                  <div class="sortable-header" @click="sortChapterBy('exercice_count')">
                    Faits
                    <span class="sort-icon" :class="{ active: chapterSortField === 'exercice_count' }">
                      {{ chapterSortField === 'exercice_count' && chapterSortDirection === 'asc' ? '↑' : '↓' }}
                    </span>
                  </div>
                  <div class="sortable-header" @click="sortChapterBy('correct_count')">
                    Réussis
                    <span class="sort-icon" :class="{ active: chapterSortField === 'correct_count' }">
                      {{ chapterSortField === 'correct_count' && chapterSortDirection === 'asc' ? '↑' : '↓' }}
                    </span>
                  </div>
                  <div class="sortable-header" @click="sortChapterBy('incorrect_count')">
                    Ratés
                    <span class="sort-icon" :class="{ active: chapterSortField === 'incorrect_count' }">
                      {{ chapterSortField === 'incorrect_count' && chapterSortDirection === 'asc' ? '↑' : '↓' }}
                    </span>
                  </div>
                  <div class="sortable-header" @click="sortChapterBy('ratio_percent')">
                    Réussite
                    <span class="sort-icon" :class="{ active: chapterSortField === 'ratio_percent' }">
                      {{ chapterSortField === 'ratio_percent' && chapterSortDirection === 'asc' ? '↑' : '↓' }}
                    </span>
                  </div>
                  <div class="sortable-header" @click="sortChapterBy('average_20')">
                    Moyenne
                    <span class="sort-icon" :class="{ active: chapterSortField === 'average_20' }">
                      {{ chapterSortField === 'average_20' && chapterSortDirection === 'asc' ? '↑' : '↓' }}
                    </span>
                  </div>
                </div>
                <div v-if="getNotionDetails(row).loading" class="chapter-skeleton">
                  <div class="skeleton-row" v-for="n in 3" :key="n">
                    <div class="skeleton-cell title"></div>
                    <div class="skeleton-cell num"></div>
                    <div class="skeleton-cell num"></div>
                    <div class="skeleton-cell num"></div>
                    <div class="skeleton-cell num"></div>
                    <div class="skeleton-cell num"></div>
                  </div>
                </div>
                <div v-else-if="getNotionDetails(row).error" class="chapter-error">{{ getNotionDetails(row).error }}</div>
                <div v-else>
                  <div v-for="ch in getNotionDetails(row).chapters" :key="ch.chapitre.id" class="chapter-row">
                    <div class="cell chapitre">{{ ch.chapitre.titre }}</div>
                    <div class="cell count">{{ ch.exercice_count }}</div>
                    <div class="cell correct">{{ ch.correct_count }}</div>
                    <div class="cell incorrect">{{ ch.incorrect_count }}</div>
                    <div class="cell ratio">{{ Math.round(ch.ratio_percent) }}%</div>
                    <div class="cell average" :class="getAverageClass(ch.average_20)">{{ ch.average_20 }}/20</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
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
          :title="filter.label"
          :aria-label="filter.label"
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import BaseHistory from './BaseHistory.vue'
import apiClient from '@/api/client'

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

// État du tri pour le tableau des chapitres
const chapterSortField = ref('exercice_count')
const chapterSortDirection = ref('desc')

// État d'expansion et détails par notion (clé: "matiereId-notionId")
const expandedNotions = ref(new Set())
const notionDetails = ref({})
const notionFetchControllers = new Map()

// Cache chapitres en sessionStorage (TTL)
const CHAPTER_CACHE_TTL = 5 * 60 * 1000 // 5 minutes
const chaptersCacheKey = (matiereId, notionId) => `ex_hist:${matiereId}:${notionId}`
const readChaptersCache = (matiereId, notionId) => {
  try {
    const raw = sessionStorage.getItem(chaptersCacheKey(matiereId, notionId))
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed || !Array.isArray(parsed.chapters)) return null
    if (Date.now() - (parsed.ts || 0) > CHAPTER_CACHE_TTL) return null
    return parsed
  } catch (e) { return null }
}
const writeChaptersCache = (matiereId, notionId, chapters) => {
  try {
    sessionStorage.setItem(chaptersCacheKey(matiereId, notionId), JSON.stringify({ ts: Date.now(), chapters }))
  } catch (e) {}
}

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

// Méthode pour changer le tri des chapitres
const sortChapterBy = (field) => {
  if (chapterSortField.value === field) {
    // Inverser la direction si c'est le même champ
    chapterSortDirection.value = chapterSortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Nouveau champ, commencer par décroissant
    chapterSortField.value = field
    chapterSortDirection.value = 'desc'
  }
  
  // Recalculer les stats des chapitres pour tous les détails ouverts
  Object.keys(notionDetails.value).forEach(key => {
    const details = notionDetails.value[key]
    if (details.chapters && details.chapters.length > 0) {
      details.chapters = sortChapters(details.chapters)
    }
  })
}

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


// Gestion de l'expansion des notions dans le tableau récapitulatif
const buildNotionKey = (row) => `${row.matiere.id}-${row.notion.id}`

const isNotionExpanded = (row) => {
  return expandedNotions.value.has(buildNotionKey(row))
}

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
  // Charger les détails si pas déjà chargés
  const details = getNotionDetails(row)
  if (details.chapters && details.chapters.length > 0) return
  await fetchNotionChapterDetails(row.matiere.id, row.notion.id)
}

const fetchNotionChapterDetails = async (matiereId, notionId, options = {}) => {
  const key = `${matiereId}-${notionId}`

  // 1) Utiliser le cache si disponible et valable
  const cached = readChaptersCache(matiereId, notionId)
  if (cached && cached.chapters && cached.chapters.length > 0) {
    // Afficher instantanément depuis le cache
    notionDetails.value[key] = { loading: false, error: '', chapters: sortChapters(cached.chapters) }
    // Si c'est un prefetch et que le cache est valide, on s'arrête là
    if (options.prefetch) return
  }

  // Pour le prefetch, éviter d'afficher l'état de chargement visuellement
  if (!options.prefetch) {
    notionDetails.value[key] = { loading: true, error: '', chapters: cached?.chapters || [] }
  }

  // Annuler une requête précédente pour cette notion si nécessaire
  if (notionFetchControllers.has(key)) {
    try { notionFetchControllers.get(key).abort() } catch (e) {}
  }
  const controller = new AbortController()
  notionFetchControllers.set(key, controller)

  try {
    const response = await apiClient.get('/api/suivis/exercices/stats/', {
      params: { matiere: matiereId, notion: notionId },
      signal: controller.signal
    })
    const list = Array.isArray(response?.data?.exercice_list) ? response.data.exercice_list : []
    const chapters = computeChapterStats(list)
    // Écrire dans le cache (non trié à nouveau plus tard)
    writeChaptersCache(matiereId, notionId, chapters)
    notionDetails.value[key] = { loading: false, error: '', chapters }
  } catch (error) {
    // Ignorer si annulé (Axios/AbortController)
    if (error?.name === 'CanceledError' || error?.name === 'AbortError' || error?.code === 'ERR_CANCELED' || error?.message === 'canceled') return
    const message = (error?.response?.data?.error) || 'Erreur lors du chargement des détails'
    notionDetails.value[key] = { loading: false, error: message, chapters: [] }
  } finally {
    notionFetchControllers.delete(key)
  }
}

// Prefetch au survol / focus
const prefetchNotionDetails = (row) => {
  const details = getNotionDetails(row)
  if (details.chapters && details.chapters.length > 0) return
  fetchNotionChapterDetails(row.matiere.id, row.notion.id, { prefetch: true })
}

// Prefetch quand la ligne entre dans le viewport
const rowElToMeta = new Map()
const summaryRowObserver = ref(null)
const setSummaryRowRef = (row, el) => {
  if (!el || typeof IntersectionObserver === 'undefined') return
  const key = buildNotionKey(row)
  rowElToMeta.set(el, { key, matiereId: row.matiere.id, notionId: row.notion.id })
  if (!summaryRowObserver.value) {
    summaryRowObserver.value = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const meta = rowElToMeta.get(entry.target)
          if (meta) {
            fetchNotionChapterDetails(meta.matiereId, meta.notionId, { prefetch: true })
            summaryRowObserver.value.unobserve(entry.target)
            rowElToMeta.delete(entry.target)
          }
        }
      })
    }, { rootMargin: '200px' })
  }
  summaryRowObserver.value.observe(el)
}

onBeforeUnmount(() => {
  if (summaryRowObserver.value) {
    try { summaryRowObserver.value.disconnect() } catch (e) {}
  }
  notionFetchControllers.forEach(ctrl => { try { ctrl.abort() } catch (e) {} })
  notionFetchControllers.clear()
})

const computeChapterStats = (exerciceList) => {
  const map = new Map()
  for (const item of exerciceList) {
    const chap = item?.chapitre || {}
    const chapId = chap?.id
    if (!chapId) continue
    if (!map.has(chapId)) {
      map.set(chapId, {
        chapitre: { id: chapId, titre: chap?.titre || 'Chapitre' },
        exercice_count: 0,
        correct_count: 0,
        incorrect_count: 0,
      })
    }
    const agg = map.get(chapId)
    agg.exercice_count += 1
    if (item.est_correct) agg.correct_count += 1
    else agg.incorrect_count += 1
  }
  const chapters = Array.from(map.values()).map(ch => {
    const ratio = ch.exercice_count > 0 ? (ch.correct_count / ch.exercice_count) : 0
    const average20 = Math.round(ratio * 20 * 10) / 10 // arrondi 0.1 sur 20
    return {
      ...ch,
      ratio_percent: ratio * 100,
      average_20: average20
    }
  })
  // Trier les chapitres selon le champ sélectionné
  return sortChapters(chapters)
}

// Fonction pour trier les chapitres selon le champ et la direction sélectionnés
const sortChapters = (chapters) => {
  const sorted = [...chapters].sort((a, b) => {
    let aValue, bValue
    
    switch (chapterSortField.value) {
      case 'exercice_count':
        aValue = a.exercice_count || 0
        bValue = b.exercice_count || 0
        break
      case 'correct_count':
        aValue = a.correct_count || 0
        bValue = b.correct_count || 0
        break
      case 'incorrect_count':
        aValue = a.incorrect_count || 0
        bValue = b.incorrect_count || 0
        break
      case 'ratio_percent':
        aValue = a.ratio_percent || 0
        bValue = b.ratio_percent || 0
        break
      case 'average_20':
        aValue = a.average_20 || 0
        bValue = b.average_20 || 0
        break
      default:
        // Par défaut, trier par titre de chapitre
        aValue = String(a.chapitre.titre).toLowerCase()
        bValue = String(b.chapitre.titre).toLowerCase()
        return aValue.localeCompare(bValue, 'fr', { sensitivity: 'base' })
    }
    
    if (chapterSortDirection.value === 'asc') {
      return aValue - bValue
    } else {
      return bValue - aValue
    }
  })
  
  return sorted
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

/* Bouton voir l'historique */
.view-history-btn {
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(59, 130, 246, 0.3);
}
.view-history-btn:hover { 
  background: #2563eb; 
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);
}

/* Tableau résumé matière/notion - Version simple et pédagogique */
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
.summary-row {
  border-bottom: 1px solid #f3f4f6;
}
.summary-row:last-child {
  border-bottom: none;
}
.summary-row .cell {
  font-size: 0.875rem;
  color: #374151;
}
.summary-row .cell.count,
.summary-row .cell.correct,
.summary-row .cell.incorrect { 
  text-align: center;
  font-weight: 600;
}
.summary-row .cell.correct { 
  color: #16a34a; 
}
.summary-row .cell.incorrect { 
  color: #dc2626; 
}

/* Moyenne simple et claire */
.summary-row .cell.average {
  font-weight: 600;
  text-align: center;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}
.summary-row .cell.average.excellent { 
  color: #16a34a; 
  background: #dcfce7;
}
.summary-row .cell.average.good { 
  color: #d97706; 
  background: #fef3c7;
}
.summary-row .cell.average.poor { 
  color: #dc2626; 
  background: #fee2e2;
}

/* En-têtes triables - Version simple */
.sortable-header {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  padding: 0.25rem;
  border-radius: 4px;
  gap: 0.35rem;
}
.sortable-header:hover {
  background-color: #f3f4f6;
}
.sort-icon {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 700;
}
.sort-icon.active {
  color: #2563eb;
  font-weight: 700;
}

@media (max-width: 768px) {
  .summary-header, .summary-row {
    grid-template-columns: 1fr 1fr 0.7fr 0.7fr 0.7fr 0.7fr;
    padding: 0.5rem 0.75rem;
  }
}

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

/* Skeleton loader pour chapitres */
.chapter-skeleton { padding: 0.5rem; background: #fff; border-top: 1px solid #f3f4f6; }
.skeleton-row { display: grid; grid-template-columns: 2fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr; gap: 0.75rem; padding: 0.4rem 0.25rem; align-items: center; }
.skeleton-cell { height: 12px; border-radius: 6px; background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 37%, #f3f4f6 63%); background-size: 400% 100%; animation: skeleton-shimmer 1.2s ease-in-out infinite; }
.skeleton-cell.title { height: 14px; }
.skeleton-cell.num { width: 60%; justify-self: center; }
@keyframes skeleton-shimmer { 0% { background-position: 100% 0 } 100% { background-position: -100% 0 } }
</style>
