<template>
  <div class="base-history">
    <div class="history-header">
      <h3 class="history-title">{{ title }}</h3>
      <!-- Zone d'actions dans l'en-tête (ex: lien "Voir l'historique") -->
      <div class="history-actions">
        <slot name="header-actions" />
      </div>
      
      <!-- Filtres -->
      <div class="history-filters">
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

    <!-- Slot pour les statistiques globales -->
    <div v-if="!loading" class="stats-section">
      <slot name="global-stats" :stats="globalStats" :loading="loading" />
    </div>

    <!-- Slot pour les statistiques par matière -->
    <div v-if="!loading && matiereStats.length > 0" class="matiere-stats">
      <slot name="matiere-stats" :stats="matiereStats" />
    </div>

    <!-- Slot supplémentaire: stats matière/notion -->
    <div v-if="!loading && matiereNotionStats.length > 0" class="matiere-stats">
      <slot name="matiere-notion-stats" :stats="matiereNotionStats" />
    </div>

    <!-- Section principale (liste des items) -->
    <div v-if="!loading" class="items-list-section">
      <div class="items-list-header" @click="toggleItemsListSection">
        <h4 class="section-subtitle">{{ listTitle }} ({{ filteredItemsList.length }})</h4>
        
        <!-- Filtres personnalisés -->
        <div class="inline-filters" v-if="customFilters && customFilters.length > 0">
          <slot name="custom-filters" :filters="customFilters" :selected="selectedCustomFilter" />
        </div>
        
        <button class="section-toggle" :class="{ expanded: isItemsListExpanded }">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6,9 12,15 18,9"></polyline>
          </svg>
        </button>
      </div>

      <div v-if="isItemsListExpanded" class="items-list-content">
        <div v-if="filteredItemsList.length === 0" class="empty-state">
          <slot name="empty-state">
            <p>Aucun élément trouvé avec ces filtres</p>
          </slot>
        </div>
        
        <div v-else class="items-grid">
          <slot name="items-list" :items="paginatedItemsList" :toggle-details="toggleItemDetails" :is-expanded="isItemExpanded" :navigate-to-item="navigateToItem" />
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
      <p>{{ loadingText }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getMatieres, getNotions, getChapitres, getChapitresByNotion } from '@/api'
import apiClient from '@/api/client'
import { useUserStore } from '@/stores/user'

// Props
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  listTitle: {
    type: String,
    required: true
  },
  loadingText: {
    type: String,
    default: 'Chargement...'
  },
  apiEndpoint: {
    type: String,
    required: true
  },
  customFilters: {
    type: Array,
    default: () => []
  },
  // Paramètres additionnels à envoyer avec la requête (ex: { limit: 7 })
  extraParams: {
    type: Object,
    default: () => ({})
  },
  navigationHandler: {
    type: Function,
    default: null
  },
  itemsPerPage: {
    type: Number,
    default: 12
  },
  filteredItems: {
    type: Array,
    default: null
  }
})

// Emits
const emit = defineEmits(['data-loaded', 'filter-changed'])

// Store et router
const userStore = useUserStore()
const router = useRouter()

// État
const loading = ref(true)
const globalStats = ref({})
const itemsList = ref([])
const matiereStats = ref([])
const matiereNotionStats = ref([])

// Données de référence
const matieres = ref([])
const notions = ref([])
const chapitres = ref([])
const themesById = ref({})

// Filtres
const selectedMatiere = ref('')
const selectedNotion = ref('')
const selectedChapitre = ref('')
const selectedCustomFilter = ref('all')

// Pagination
const currentPage = ref(1)

// État d'expansion des détails
const expandedItems = ref(new Set())
const isItemsListExpanded = ref(true)

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

const filteredChapitres = computed(() => {
  if (!selectedNotion.value) return []
  
  const selectedNotionId = parseInt(selectedNotion.value)
  
  return chapitres.value.filter(chapitre => {
    const chapNotionId = chapitre.notion_id ?? chapitre.notion?.id ?? (typeof chapitre.notion === 'number' ? chapitre.notion : null)
    return parseInt(chapNotionId) === selectedNotionId
  })
})

const filteredItemsList = computed(() => {
  // Si le composant parent fournit une liste filtrée, l'utiliser
  if (props.filteredItems) {
    return props.filteredItems
  }
  
  // Sinon, retourner la liste complète
  return itemsList.value
})

// Computed pour la pagination
const totalPages = computed(() => Math.ceil(filteredItemsList.value.length / props.itemsPerPage))

const paginatedItemsList = computed(() => {
  const start = (currentPage.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return filteredItemsList.value.slice(start, end)
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
// Responsive helper (mobile detection)
const isMobile = ref(false)
const updateIsMobile = () => {
  if (typeof window !== 'undefined') {
    isMobile.value = window.innerWidth <= 768
  }
}
onMounted(() => {
  updateIsMobile()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateIsMobile)
  }
})
onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateIsMobile)
  }
})

const matieresComputed = computed(() => {
  return matieres.value || []
})

// Méthodes
const loadReferenceData = async () => {
  try {
    // Utiliser les endpoints spécialisés qui filtrent automatiquement selon l'utilisateur
    const [mResponse, tnResponse, nResponse, cResponse] = await Promise.all([
      // Matières pour l'utilisateur (endpoint spécialisé)
      apiClient.get('/api/matieres/user_matieres/'),
      // Thèmes + Notions pour utilisateur (donne le lien thème -> matière)
      apiClient.get('/api/themes/notions-pour-utilisateur/', { timeout: 20000 }).catch(() => apiClient.get('/api/themes/notions-pour-utilisateur/')),
      // Notions - essayer d'abord l'endpoint spécialisé, puis l'endpoint général
      getNotions({}).catch(() => apiClient.get('/api/notions/pour-utilisateur/', { timeout: 20000 })),
      // Chapitres via l'endpoint général mais on filtrera côté client
      getChapitres({})
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
        getNotions({}),
        getChapitres({})
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

const loadData = async () => {
  loading.value = true
  try {
    const params = { ...(props.extraParams || {}) }
    if (selectedMatiere.value) params.matiere = selectedMatiere.value
    if (selectedNotion.value) params.notion = selectedNotion.value
    if (selectedChapitre.value) params.chapitre = selectedChapitre.value
    
    const response = await apiClient.get(props.apiEndpoint, { params })
    const data = response.data
    
    globalStats.value = data.global_stats || {}
    itemsList.value = data.quiz_list || data.exercice_list || []
    matiereStats.value = data.matiere_stats || []
    matiereNotionStats.value = data.matiere_notion_stats || []
    
    emit('data-loaded', data)
    
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error)
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
    try {
      // Rafraîchir les thèmes + notions pour la matière sélectionnée
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
  
  loadData()
  emit('filter-changed', { matiere: selectedMatiere.value, notion: selectedNotion.value, chapitre: selectedChapitre.value })
}

const onNotionChange = async () => {
  selectedChapitre.value = ''
  resetPagination()
  
  // Recharger les chapitres pour la notion sélectionnée
  if (selectedNotion.value) {
    try {
      // Essayer getChapitresByNotion
      let cResponse = await getChapitresByNotion(selectedNotion.value)
      
      let newChapitresData = []
      if (Array.isArray(cResponse?.data)) {
        newChapitresData = cResponse.data
      } else if (cResponse?.data?.results) {
        newChapitresData = cResponse.data.results
      }
      
      // Si pas de résultats, essayer l'endpoint général avec paramètre
      if (newChapitresData.length === 0) {
        const cResponse2 = await getChapitres({ notion: selectedNotion.value })
        
        if (Array.isArray(cResponse2?.data)) {
          newChapitresData = cResponse2.data
        } else if (cResponse2?.data?.results) {
          newChapitresData = cResponse2.data.results
        }
      }
      
      // Si toujours pas de résultats, essayer l'endpoint direct du backend
      if (newChapitresData.length === 0) {
        const cResponse3 = await apiClient.get(`/api/notions/${selectedNotion.value}/chapitres/`)
        
        if (Array.isArray(cResponse3?.data)) {
          newChapitresData = cResponse3.data
        } else if (cResponse3?.data?.results) {
          newChapitresData = cResponse3.data.results
        }
      }
      
      // Mettre à jour les chapitres si on a trouvé quelque chose
      if (newChapitresData.length > 0) {
        // Fusionner avec les chapitres existants (éviter les doublons)
        const existingIds = chapitres.value.map(c => c.id)
        const newChapitres = newChapitresData.filter(c => !existingIds.includes(c.id))
        chapitres.value = [...chapitres.value, ...newChapitres]
      }
      
    } catch (error) {
      console.error('Erreur lors du rechargement des chapitres:', error)
    }
  }
  
  loadData()
  emit('filter-changed', { matiere: selectedMatiere.value, notion: selectedNotion.value, chapitre: selectedChapitre.value })
}

const onChapitreChange = () => {
  resetPagination()
  loadData()
  emit('filter-changed', { matiere: selectedMatiere.value, notion: selectedNotion.value, chapitre: selectedChapitre.value })
}

const toggleItemDetails = (itemId) => {
  if (expandedItems.value.has(itemId)) {
    expandedItems.value.delete(itemId)
  } else {
    expandedItems.value.add(itemId)
  }
}

const isItemExpanded = (itemId) => {
  return expandedItems.value.has(itemId)
}

const toggleItemsListSection = () => {
  isItemsListExpanded.value = !isItemsListExpanded.value
}

const navigateToItem = (item) => {
  if (props.navigationHandler) {
    props.navigationHandler(item)
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

// Méthodes utilitaires exposées
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

// Lifecycle
onMounted(async () => {
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
  await loadData()
})

// Expose des méthodes utilitaires pour les slots
defineExpose({
  formatDate,
  formatTime,
  toggleItemDetails,
  isItemExpanded,
  navigateToItem,
  selectedCustomFilter,
  resetPagination
})
</script>

<style scoped>
.base-history {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem 0;
}

.history-header {
  margin-bottom: 1.5rem;
}

.history-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.history-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.history-filters {
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

/* Stats sections */
.stats-section {
  margin-bottom: 1.5rem;
}

.matiere-stats {
  margin-bottom: 1.5rem;
}

/* Liste des items */
.items-list-section {
  margin-top: 2rem;
}

.items-list-header {
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

.items-list-header .section-subtitle {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  align-self: center;
}

.inline-filters {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.items-list-header:hover {
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

.items-list-content {
  animation: slideDown 0.3s ease-out;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
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

/* Pagination responsive: icônes seules en mobile */
@media (max-width: 768px) {
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

/* Responsive */
@media (max-width: 1024px) {
  .items-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .history-filters {
    flex-direction: column;
  }

  .filter-select {
    min-width: 100%;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .items-list-header {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }

  .inline-filters {
    align-self: stretch;
    justify-content: space-between;
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
}
</style>
