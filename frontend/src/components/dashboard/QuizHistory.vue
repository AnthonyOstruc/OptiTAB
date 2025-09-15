<template>
  <div class="quiz-history">
    <div class="quiz-header">
      <h3 class="quiz-title">🧠 Historique des Quiz</h3>
      


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
         <div v-for="quiz in paginatedQuizList" :key="quiz.id" class="quiz-card" :class="{ 'multiple-attempts': quiz.total_attempts > 1, 'cooldown': isQuizInCooldown(quiz.quiz_id) }">
           <div class="quiz-card-header" @click="toggleQuizDetails(quiz.id)">
             <div class="quiz-card-title-section">
               <h5 class="quiz-card-title clickable-title" 
                   @click.stop="navigateToQuiz(quiz)" 
                   :title="isQuizInCooldown(quiz.quiz_id) ? 'Quiz en cooldown - Accès temporairement bloqué' : 'Accéder au quiz: ' + quiz.quiz_titre"
                   :class="{ 'cooldown-title': isQuizInCooldown(quiz.quiz_id) }">
                 <span v-if="isQuizInCooldown(quiz.quiz_id)" class="cooldown-lock" title="Quiz en cooldown">🔒</span>
                 {{ quiz.quiz_titre }}
                 <svg v-if="!isQuizInCooldown(quiz.quiz_id)" class="navigation-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
             
             <!-- Affichage du cooldown si le quiz est en cooldown -->
             <div v-if="isQuizInCooldown(quiz.quiz_id)" class="quiz-cooldown-info">
               <div class="cooldown-warning">
                 <span class="cooldown-icon">⏰</span>
                 <span class="cooldown-text">
                   Prochaine tentative possible dans {{ getQuizCooldown(quiz.quiz_id).time_remaining_formatted }}
                 </span>
               </div>
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
import { getMatieres, getNotions, getChapitres, getChapitresByNotion } from '@/api'
import apiClient from '@/api/client'
import { useUserStore } from '@/stores/user'
import { checkQuizCooldown } from '@/api/quiz'

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

// Cooldown des quiz
const quizCooldowns = ref(new Map())
const cooldownLoading = ref(false)

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

const filteredChapitres = computed(() => {
  if (!selectedNotion.value) return []
  
  const selectedNotionId = parseInt(selectedNotion.value)
  
  return chapitres.value.filter(chapitre => {
    const chapNotionId = chapitre.notion_id ?? chapitre.notion?.id ?? (typeof chapitre.notion === 'number' ? chapitre.notion : null)
    return parseInt(chapNotionId) === selectedNotionId
  })
})

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

// Fonctions de cooldown
const loadQuizCooldowns = async () => {
  if (!quizList.value.length) return
  
  cooldownLoading.value = true
  
  try {
    for (const quiz of quizList.value) {
      try {
        const cooldownInfo = await checkQuizCooldown(quiz.quiz_id)
        quizCooldowns.value.set(quiz.quiz_id, cooldownInfo)
      } catch (error) {
        console.warn(`Erreur cooldown pour quiz ${quiz.quiz_id}:`, error)
        // En cas d'erreur, autoriser la tentative
        quizCooldowns.value.set(quiz.quiz_id, { can_attempt: true })
      }
    }
  } catch (error) {
    if (import.meta.env && import.meta.env.DEV) {
      console.error('Erreur lors du chargement des cooldowns:', error)
    }
  } finally {
    cooldownLoading.value = false
  }
}

const getQuizCooldown = (quizId) => {
  return quizCooldowns.value.get(quizId) || { can_attempt: true }
}

const isQuizInCooldown = (quizId) => {
  const cooldown = getQuizCooldown(quizId)
  return !cooldown.can_attempt
}

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
    
    // Charger les cooldowns des quiz après avoir chargé les données
    if (quizList.value.length > 0) {
      await loadQuizCooldowns()
    }
    
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
      
      // Si pas de résultats, essayer l'endpoint général  je veux pour a prmeiere fois sauvgarder dans un repersortryavec paramètre
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
    // Vérifier le cooldown avant de naviguer
    if (isQuizInCooldown(quiz.quiz_id)) {
      const cooldownInfo = getQuizCooldown(quiz.quiz_id)
      alert(`⏰ Ce quiz est en cooldown. ${cooldownInfo.message}`)
      return
    }
    
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

.quiz-card.cooldown {
  opacity: 0.7;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border-color: #f59e0b;
}

.quiz-card.cooldown .quiz-card-header {
  cursor: default;
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

.cooldown-title {
  color: #92400e !important;
  cursor: not-allowed !important;
}

.cooldown-lock {
  margin-right: 0.5rem;
  font-size: 1.1em;
  animation: cooldown-pulse 2s ease-in-out infinite;
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

.quiz-cooldown-info {
  margin-top: 1rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 2px solid #f59e0b;
  border-radius: 8px;
}

.cooldown-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #92400e;
}

.cooldown-icon {
  font-size: 1.2rem;
  animation: cooldown-pulse 2s ease-in-out infinite;
}

.cooldown-text {
  font-size: 0.9rem;
  font-weight: 600;
}

@keyframes cooldown-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
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
