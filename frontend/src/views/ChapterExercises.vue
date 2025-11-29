<template>
  <DashboardLayout>
    <section class="exercices-section" ref="exPageRef">
      <div class="nav-header-base">
        <BackButton 
          text="Retour aux chapitres" 
          :customAction="goBackToNotions"
          position="top-left-dashboard"
        />
      </div>

      <div class="exercices-body">
        <!-- Navigation ultra-propre -->
        <div class="clean-navigation">
        <div class="nav-grid">
          <button 
            v-for="t in tabs" 
            :key="t.key"
            :class="['nav-item', { active: t.key === activeTab }]"
            @click="activeTab = t.key; currentPage = 1"
          >
            <span class="nav-icon">{{ t.icon }}</span>
            <span class="nav-label">{{ t.shortLabel }}</span>
            <span class="nav-count">{{ t.count }}</span>
          </button>
        </div>
      </div>

        <div v-if="loading" class="loading-skeleton-container">
        <SkeletonList :count="4" />
        </div>
        <div v-else-if="error" class="exercices-error">{{ error }}</div>
        <div v-else>
          <div v-if="exercices.length > 0" class="exercices-content-outer" :style="zoomStyle" ref="exOuterRef">
            <div class="exercices-controls">
              <div class="controls-row">
                <div class="filter-cta">
                  <span class="filter-cta-icon" aria-hidden="true">★</span>
                  <span class="filter-cta-text">Utilisez les filtres pour affiner votre sélection d'exercices</span>
                </div>
                <div class="filter-row">
                  <div class="filter-group">
                    <span class="filter-label">Filtrer</span>
                    <div class="filter-buttons type-filter-buttons">
                      <button
                        v-for="opt in typeFilterOptions"
                        :key="opt.value"
                        :class="['filter-btn', 'type-filter-btn', { active: opt.value === selectedTypeFilter }]"
                        @click="selectedTypeFilter = opt.value; handleTypeFilterChange()"
                      >
                        {{ opt.label }}
                      </button>
                    </div>
                  </div>

                  <div class="filter-divider"></div>

                  <div class="filter-item">
                    <span class="filter-label">Difficulté</span>
                      <div class="filter-buttons">
                        <button
                          v-for="d in difficultyOptions"
                          :key="d"
                          :class="['filter-btn', { active: d === selectedDifficulty }]"
                          @click="selectedDifficulty = d; currentPage = 1"
                        >
                          <span v-if="d === 'all'" class="difficulty-text">Toutes</span>
                          <span v-else class="difficulty-stars">
                            {{ d === 'easy' ? '⭐' : d === 'medium' ? '⭐⭐' : '⭐⭐⭐' }}
                          </span>
                        </button>
                      </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="exercices-list">
              <div
                v-for="exercice in paginated"
                :key="exercice.id"
                :id="`ex-${exercice.id}`"
                class="exercice-item-wrapper"
                @click="setLastExerciceId(exercice.id)"
              >
                <ExerciceQCM
                  :eid="exercice.id"
                  :titre="exercice.titre || exercice.nom"
                  :instruction="exercice.instruction || exercice.contenu || exercice.question"
                  :solution="exercice.solution || exercice.reponse_correcte || ''"
                  :etapes="exercice.etapes || ''"
                  :difficulty="exercice.difficulty || exercice.difficulte || 'medium'"
                  :current="statusMap[exercice.id]?.status"
                  @status-changed="handleStatus"
                />
              </div>
              <Pagination :total="filteredExercices.length" :perPage="perPage" :page="currentPage" @update:page="handlePageChange" />
            </div>
          </div>
          <div v-else class="empty-coming">
            <div class="empty-card">
              <div class="empty-icon">🧮</div>
              <h2 class="empty-title">Exercices — bientôt disponibles</h2>
              <p class="empty-text">
                Les exercices pour cette notion arrivent très prochainement.
              </p>
              <div class="empty-actions">
                <button class="empty-btn" @click="goBackToNotions">Retour aux chapitres</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, onActivated, onDeactivated, onBeforeUnmount, nextTick, watch, computed } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import SkeletonList from '@/components/common/SkeletonList.vue'
import { getExercices, getStatuses, createStatus, updateStatus, deleteStatus } from '@/api'
import { useUserStore } from '@/stores/user'
import { useSubjectsStore } from '@/stores/subjects/index'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import Pagination from '@/components/common/Pagination.vue'
import Tabs from '@/components/common/Tabs.vue'
import BackButton from '@/components/common/BackButton.vue'
import { useZoom } from '@/composables/useZoom'

defineOptions({ name: 'ExercisesByNotion' })

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const subjectsStore = useSubjectsStore()
const notionId = ref(route.params.notionId)
const exPageRef = ref(null)
const exOuterRef = ref(null)

// Utiliser le composable de zoom
const {
  viewportWidth,
  contentHeight,
  detectMobileAndZoomSupport,
  createZoomStyle,
  updateViewportWidth,
  measureContentHeight,
  setupViewportListener,
  cleanupViewportListener
} = useZoom()

const exercices = ref([])
const perPage = ref(5)
const currentPage = ref(1)

// Filtre par type (configurable par niveau)
const typeFilterOptions = ref([])
const selectedTypeFilter = ref('all')

// Filtre difficulté
const difficultyOptions = ['all','easy','medium','hard']
const selectedDifficulty = ref('all')

// Recherche
const searchQuery = ref('')

// Construire les options de filtre selon le niveau utilisateur
function refreshTypeFilterOptions() {
  const niveau = userStore.niveau_pays
  const rawOptions = Array.isArray(niveau?.exercice_filter_options)
    ? niveau.exercice_filter_options
    : []
  const cleaned = rawOptions
    .map(o => (typeof o === 'string' || typeof o === 'number') ? String(o).trim() : '')
    .filter(Boolean)
  const unique = Array.from(new Set(cleaned))
  const defaultLabel = (niveau?.exercice_filter_default || 'Tous').trim() || 'Tous'
  const baseOption = { value: 'all', label: defaultLabel }
  typeFilterOptions.value = [baseOption, ...unique.map(val => ({ value: val, label: val }))]

  if (!typeFilterOptions.value.find(o => o.value === selectedTypeFilter.value)) {
    selectedTypeFilter.value = baseOption.value
  }
}

watch(() => userStore.niveau_pays, () => {
  refreshTypeFilterOptions()
}, { immediate: true })

// Status filtering tabs avec design amélioré
const tabs = computed(() => [
  { 
    key: 'all', 
    label: 'Exercices restants',
    shortLabel: 'À faire',
    icon: '📝',
    count: exercices.value.filter(e => !statusMap.value[e.id]).length
  },
  { 
    key: 'done', 
    label: 'Exercices réalisés',
    shortLabel: 'Fait',
    icon: '📋',
    count: exercices.value.filter(e => statusMap.value[e.id]).length
  },
  { 
    key: 'acquired', 
    label: 'Acquis',
    shortLabel: 'Acquis',
    icon: '✅',
    count: exercices.value.filter(e => statusMap.value[e.id]?.status === 'acquired').length
  },
  { 
    key: 'not_acquired', 
    label: 'À revoir',
    shortLabel: 'À revoir',
    icon: '❌',
    count: exercices.value.filter(e => statusMap.value[e.id]?.status === 'not_acquired').length
  }
])
const activeTab = ref('all')

// --- Persistence (sessionStorage) ---
const storageKey = computed(() => `optitab_page_exercices_${notionId.value}`)
const focusKey = computed(() => `optitab_last_exercice_${notionId.value}`)

let isRestoringState = false

function readSavedViewState() {
  try {
    const raw = sessionStorage.getItem(storageKey.value)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    return parsed && typeof parsed === 'object' ? parsed : null
  } catch (_) {
    return null
  }
}

function applyInitialScrollFromStorage() {
  const saved = readSavedViewState()
  if (saved && typeof saved.scrollY === 'number') {
    scrollToPosition({ top: saved.scrollY, behavior: 'auto' })
  } else {
    scrollToTop({ behavior: 'auto' })
  }
}

// (supprimé: fonction dupliquée)

function saveViewState(extra = {}) {
  if (isRestoringState && typeof extra.scrollY === 'undefined') {
    return
  }
  try {
    const container = getScrollContainer(exPageRef.value)
    const scrollY = typeof extra.scrollY === 'number'
      ? extra.scrollY
      : readScrollTop(container)

  const state = {
    perPage: perPage.value,
    currentPage: currentPage.value,
    selectedDifficulty: selectedDifficulty.value,
    selectedTypeFilter: selectedTypeFilter.value,
    activeTab: activeTab.value,
      searchQuery: searchQuery.value,
      scrollY,
      t: Date.now(),
      ...extra
    }
    sessionStorage.setItem(storageKey.value, JSON.stringify(state))
  } catch (_) {}
}

function restoreViewState() {
  isRestoringState = true
  try {
    const raw = sessionStorage.getItem(storageKey.value)
    if (!raw) return null
    const s = JSON.parse(raw)
    if (s && typeof s === 'object') {
  if (typeof s.perPage === 'number') perPage.value = s.perPage
  if (typeof s.currentPage === 'number') currentPage.value = Math.max(1, s.currentPage)
  if (typeof s.selectedDifficulty === 'string') selectedDifficulty.value = s.selectedDifficulty
  if (typeof s.selectedTypeFilter === 'string') selectedTypeFilter.value = s.selectedTypeFilter
  if (typeof s.activeTab === 'string') activeTab.value = s.activeTab
      if (typeof s.searchQuery === 'string') searchQuery.value = s.searchQuery
      return s
    }
  } catch (_) {
    return null
  } finally {
    setTimeout(() => { isRestoringState = false }, 0)
  }
  return null
}

// Fonction pour télécharger tous les exercices en PDF
const downloadAllPDF = async () => {
  try {
    console.log('Download all PDF clicked')
    console.log('Exercices data:', filteredExercices.value)
    
    // Import dynamique pour éviter les erreurs
    const { generateExercicesListPDF } = await import('@/utils/pdfGenerator')
    await generateExercicesListPDF(filteredExercices.value, `Exercices_${notionNom.value}`)
    alert('PDF généré avec succès !')
  } catch (error) {
    console.error('Erreur PDF:', error)
    alert('Erreur lors de la génération du PDF: ' + error.message)
  }
}

const statusMap = ref({}) // exerciceId -> { status, id }

const notionNom = ref('')
const loading = ref(true)
const error = ref('')
const chapitres = ref([])

onMounted(async () => {
  detectMobileAndZoomSupport()
  updateViewportWidth()
  setupViewportListener()
  applyInitialScrollFromStorage()
  // Synchroniser la recherche locale avec l'URL (barre globale)
  const q0 = route.query?.q
  if (typeof q0 !== 'undefined' && q0 !== null) {
    try { searchQuery.value = String(q0) } catch {}
  }
  await loadData()
})

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  detectMobileAndZoomSupport()
  updateViewportWidth()
  applyInitialScrollFromStorage()
  // Forcer le rendu MathJax à chaque réactivation pour éviter les problèmes de cache
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
    }, 100)

    // Restaurer la position de scroll sauvegardée (comme Cours/Sheets)
    const saved = restoreViewState()
    if (saved && typeof saved.scrollY === 'number') {
      scrollToPosition({ top: saved.scrollY, behavior: 'auto' })
    } else {
      scrollToTop({ behavior: 'auto' })
    }
  })
})

async function loadData() {
  loading.value = true
  try {
    const niveauId = userStore.niveau_pays?.id

    // Reset data when notion changes
    exercices.value = []
    statusMap.value = {}

    const [exercicesData, statusesResp] = await Promise.all([
      getExercices({ notion: notionId.value, niveau: niveauId }),
      getStatuses()
    ])

    notionNom.value = 'Notion'

    exercices.value = Array.isArray(exercicesData) ? exercicesData : []
    console.log(`[ExercisesByNotion] Exercices chargés pour niveau ${niveauId}:`, exercices.value.length)

    const stats = statusesResp?.data || []
    const list = Array.isArray(stats) ? stats : (stats?.results || [])
    statusMap.value = Object.fromEntries(
      list.map(s => [
        s.exercice,
        { status: s.est_correct ? 'acquired' : 'not_acquired', id: s.id }
      ])
    )

    // Restaurer l'état de vue
    restoreViewState()

    const total = Math.max(1, Math.ceil((filteredExercices?.value?.length || 0) / Math.max(1, perPage.value)))
    if (currentPage.value > total) currentPage.value = total
    error.value = ''
  } catch (e) {
    console.error('[ExercisesByNotion] Erreur chargement:', e)
    error.value = "Impossible de charger les exercices."
  } finally {
    loading.value = false
    await nextTick()

    // Installer l'écouteur de scroll
    setupScrollListener()
    measureContentHeightForExercices()

    // Forcer le rendu MathJax après le chargement des exercices
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        try {
          if (window.MathJax.typesetClear) {
            window.MathJax.typesetClear()
          }
          window.MathJax.typesetPromise()
        } catch (error) {
          console.warn('[MathJax] Erreur:', error)
        }
      }
      measureContentHeightForExercices()

      // Restaurer la position de scroll si disponible (comme Cours/Sheets)
      const saved = restoreViewState()
      if (saved && typeof saved.scrollY === 'number') {
        scrollToPosition({ top: saved.scrollY, behavior: 'auto' })
      } else {
        scrollToTop({ behavior: 'auto' })
      }
    }, 150)
  }
}

// Recharger si l'ID de notion change sous KeepAlive
watch(() => route.params.notionId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    notionId.value = newId
    await loadData()
  }
})

// Sur changement de hash, tenter de scroller vers l'exercice ciblé
watch(() => route.hash, (newHash, oldHash) => {
  if (newHash && newHash !== oldHash && newHash.startsWith('#ex-')) {
    tryScrollToHashExercice()
  }
})

const totalPages = computed(() => Math.ceil(exercices.value.length / perPage.value))

const filteredExercices = computed(() => {
  let list = exercices.value
  
  // Filtre par recherche
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    list = list.filter(e => {
      const title = (e.titre || e.nom || '').toLowerCase()
      const content = (e.instruction || e.contenu || e.question || '').toLowerCase()
      return title.includes(query) || content.includes(query)
    })
  }

  // Filtre par type (configurable par niveau)
  if (selectedTypeFilter.value !== 'all') {
    const target = selectedTypeFilter.value.toLowerCase().trim()
    list = list.filter(e => {
      const fields = [
        e.exercice_type,
        e.type,
        e.titre,
        e.nom
      ]
      return fields
        .filter(Boolean)
        .some(field => String(field).toLowerCase().includes(target))
    })
  }

  // Filtre par difficulté
  if (selectedDifficulty.value !== 'all') {
    list = list.filter(e => e.difficulty === selectedDifficulty.value)
  }
  
  // Filtre par statut
  if (activeTab.value === 'done') {
    // Tous les exercices déjà traités (peu importe le résultat)
    list = list.filter(e => statusMap.value[e.id])
  } else if (activeTab.value === 'all') {
    // Exercices restants : ceux sans statut enregistré
    list = list.filter(e => !statusMap.value[e.id])
  } else {
    // Filtre par statut précis (acquired ou not_acquired)
    list = list.filter(e => statusMap.value[e.id]?.status === activeTab.value)
  }
  
  // Trier les exercices par ID pour avoir l'ordre 1, 2, 3, etc.
  return list.sort((a, b) => {
    const idA = parseInt(a.id) || 0
    const idB = parseInt(b.id) || 0
    return idA - idB
  })
})

const paginated = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return filteredExercices.value.slice(start, start + perPage.value)
})

const zoomStyle = createZoomStyle({
  cssVar: '--exercices-zoom',
  heightVar: '--exercices-content-height',
  mobileZoomAdjustment: (z) => Math.max(0.45, z * 0.75)
})


function measureContentHeightForExercices() {
  measureContentHeight(exOuterRef)
}

function handlePageChange(page) {
  currentPage.value = page
  // scroll to top of exercises (dans le bon conteneur)
  scrollToTop({ behavior: 'smooth' })
  // Sauvegarder l'état
  saveViewState()
  // Forcer le rendu MathJax après le changement de page
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  })
}

function handleTypeFilterChange() {
  currentPage.value = 1
  saveViewState()
}

async function handleStatus({ exerciceId, status }) {
  try {
    if (status) {
      // Vérifier si un statut existe déjà pour cet exercice
      const existingStatus = statusMap.value[exerciceId]
      
      if (existingStatus) {
        // Si un statut existe déjà, le mettre à jour
        await updateStatus(existingStatus.id, {
          exercice: exerciceId,
          reponse_donnee: status,
          est_correct: status === 'acquired'
        })
        // Mettre à jour le statut local
        statusMap.value[exerciceId] = { status, id: existingStatus.id }
        
        // Objectifs journaliers supprimés
      } else {
        // Si aucun statut n'existe, en créer un nouveau
        const response = await createStatus({
          exercice: exerciceId,
          reponse_donnee: status,
          est_correct: status === 'acquired',
          points_obtenus: status === 'acquired' ? 1 : 0,
          temps_seconde: 0
        })
        // Mettre à jour le statut local avec l'ID retourné
        const newId = response?.data?.id || response?.id
        statusMap.value[exerciceId] = { status, id: newId }
      }
      
      // Objectifs journaliers supprimés
    } else {
      // Supprimer le statut de la base de données
      const existingStatus = statusMap.value[exerciceId]
      
      if (existingStatus) {
        await deleteStatus(existingStatus.id)
      }
      
      // Supprimer du statut local
      delete statusMap.value[exerciceId]
    }

    // Mémoriser le dernier exercice touché (pour retour via onglet)
    setLastExerciceId(exerciceId)
  } catch (error) {
    console.error('Erreur lors de la sauvegarde du statut:', error)
    // En cas d'erreur, on peut quand même mettre à jour le statut local
    if (status) {
      statusMap.value[exerciceId] = { status, id: null }
    } else {
      delete statusMap.value[exerciceId]
    }
  }
}

function goBackToNotions() {
  // Rediriger vers exercicies/id (liste des notions d'exercices)
  const matiereId = route.params.matiereId || subjectsStore.activeMatiereId
  if (matiereId) {
    router.push({ 
      name: 'Themes', 
      params: { 
        matiereId: matiereId
      } 
    })
  } else {
    router.back()
  }
}

// Sauvegarder à chaque changement significatif
watch([perPage, currentPage, selectedDifficulty, selectedTypeFilter, activeTab, searchQuery], () => {
  saveViewState()
})

// Garder l'URL en phase quand on saisit dans le champ local
let updateUrlTimer = null
watch(searchQuery, (val) => {
  if (updateUrlTimer) clearTimeout(updateUrlTimer)
  updateUrlTimer = setTimeout(() => {
    const q = (val || '').trim()
    const currentQ = route.query?.q ? String(route.query.q) : ''
    if (q !== currentQ) {
      const newQuery = { ...route.query }
      if (q) newQuery.q = q
      else delete newQuery.q
      router.replace({ query: newQuery }).catch(() => {})
    }
  }, 150)
})

// Suivre la recherche globale (depuis la sidebar) -> mettre à jour le filtre
watch(() => route.query.q, (val) => {
  const incoming = val ? String(val) : ''
  if (incoming !== (searchQuery.value || '')) {
    searchQuery.value = incoming
    currentPage.value = 1
  }
})

watch(viewportWidth, () => {
  nextTick(() => {
    if (typeof window !== 'undefined' && window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
    measureContentHeightForExercices()
  })
}, { immediate: true })

// Forcer le rendu MathJax quand les exercices affichés changent
watch(paginated, () => {
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
    measureContentHeight()
  })
}, { deep: true })

onBeforeUnmount(() => {
  saveViewState()
  cleanupViewportListener()
})

onDeactivated(() => {
  // Sauvegarder la position au moment de quitter via onglets
  saveViewState()
})

// Sauvegarder aussi juste avant de quitter la route (sécurité)
onBeforeRouteLeave((_to, _from, next) => {
  try { saveViewState() } catch (_) {}
  next()
})

function setLastExerciceId(id) {
  try {
    if (!id) return
    sessionStorage.setItem(focusKey.value, String(id))
  } catch (_) {}
}

// Essayer de scroller jusqu'à l'ancre ex-<id> si présente dans l'URL
async function tryScrollToHashExercice() {
  try {
    const h = route.hash || ''
    if (!h.startsWith('#ex-')) return false
    const id = Number(h.replace('#ex-', ''))
    if (!id) return false

    // S'assurer que l'exercice est visible: retirer filtres qui pourraient le masquer
    const ex = exercices.value.find(e => Number(e.id) === id)
    if (!ex) return false
    setLastExerciceId(id)

    // Adapter l'onglet selon le statut connu
    const st = statusMap.value[id]?.status
    if (st === 'acquired' || st === 'not_acquired') {
      activeTab.value = st
    } else if (statusMap.value[id]) {
      activeTab.value = 'done'
    } else {
      activeTab.value = 'all'
    }
    selectedDifficulty.value = 'all'
    selectedTypeFilter.value = 'all'
    searchQuery.value = ''

    await nextTick()
    // Calculer la page qui contient cet exercice dans la liste filtrée
    const idx = filteredExercices.value.findIndex(e => Number(e.id) === id)
    if (idx >= 0) {
      const page = Math.floor(idx / Math.max(1, perPage.value)) + 1
      if (page !== currentPage.value) {
        currentPage.value = page
        await nextTick()
      }
    }

    // Scroller jusqu'à l'élément (avec fallback retardé)
    const elId = `ex-${id}`
    const doScroll = () => {
      const el = document.getElementById(elId)
      if (el) {
        el.scrollIntoView({ behavior: 'auto', block: 'start' })
        return true
      }
      return false
    }
    if (!doScroll()) {
      setTimeout(doScroll, 50)
      setTimeout(doScroll, 150)
    }
    return true
  } catch (_) {
    return false
  }
}

// Trouver le conteneur scrollable le plus proche
function getScrollContainer(el) {
  if (typeof window === 'undefined' || typeof document === 'undefined') return null
  let parent = el ? el.parentElement : null
  while (parent) {
    const style = window.getComputedStyle(parent)
    const overflowY = style.overflowY
    const canScroll = (overflowY === 'auto' || overflowY === 'scroll') && parent.scrollHeight > parent.clientHeight
    if (canScroll) return parent
    parent = parent.parentElement
  }
  return document.scrollingElement || document.documentElement
}

function readScrollTop(container) {
  if (typeof document === 'undefined') return 0
  if (!container) return 0
  if (container === document.documentElement || container === document.body) {
    if (typeof window === 'undefined') return 0
    return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
  }
  return container.scrollTop || 0
}

function scrollToPosition({ top = 0, behavior = 'auto', targetEl } = {}) {
  if (typeof document === 'undefined') return
  const container = getScrollContainer(targetEl ?? exPageRef.value) || document.documentElement || document.body
  if (!container) return
  if (container === document.documentElement || container === document.body) {
    if (typeof window !== 'undefined') {
      window.scrollTo({ top, behavior })
    }
  } else {
    container.scrollTo({ top, behavior })
  }
}

function scrollToTop(options = {}) {
  scrollToPosition({ ...options, top: 0 })
}

let scrollCleanup = null
function setupScrollListener() {
  try {
    if (scrollCleanup) {
      try { scrollCleanup() } catch (_) {}
      scrollCleanup = null
    }
    const container = getScrollContainer(exPageRef.value)
    if (!container) return
    const handleScroll = () => {
      saveViewState({ scrollY: readScrollTop(container) })
    }
    if (container === document.documentElement || container === document.body) {
      if (typeof window === 'undefined') return
      window.addEventListener('scroll', handleScroll, { passive: true })
      scrollCleanup = () => window.removeEventListener('scroll', handleScroll)
    } else {
      container.addEventListener('scroll', handleScroll, { passive: true })
      scrollCleanup = () => container.removeEventListener('scroll', handleScroll)
    }
  } catch (_) {}
}

async function generatePDF(includeCorrection = false) {
  try {
    // Dynamically import PDF libraries
    const { default: jsPDF } = await import('jspdf')
    
    // Create a new PDF document with better configuration
    const pdf = new jsPDF({
      orientation: 'p',
      unit: 'mm',
      format: 'a4',
      putOnlyUsedFonts: true,
      floatPrecision: 16
    })
    
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 20
    const contentWidth = pageWidth - (2 * margin)
    
    // Enhanced header
    pdf.setFillColor(240, 248, 255)
    pdf.rect(0, 0, pageWidth, 40, 'F')
    
    // Title
    pdf.setFontSize(18)
    pdf.setFont('helvetica', 'bold')
    pdf.setTextColor(30, 64, 175)
    const title = includeCorrection ? 
      `Exercices de ${notionNom.value}` : 
      `Feuille d'exercices - ${notionNom.value}`
    
    const titleWidth = pdf.getTextWidth(title)
    pdf.text(title, (pageWidth - titleWidth) / 2, 20)
    
    // Subtitle
    pdf.setFontSize(10)
    pdf.setFont('helvetica', 'normal')
    pdf.setTextColor(100, 116, 139)
    const subtitle = includeCorrection ? 'Exercices avec corrections détaillées' : 'Énoncés des exercices'
    const subtitleWidth = pdf.getTextWidth(subtitle)
    pdf.text(subtitle, (pageWidth - subtitleWidth) / 2, 28)
    
    // Metadata
    pdf.setTextColor(0, 0, 0)
    pdf.setFontSize(8)
    const date = new Date().toLocaleDateString('fr-FR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
    pdf.text(`Généré le ${date}`, margin, 36)
    pdf.text(`${filteredExercices.value.length} exercice(s)`, pageWidth - margin - 30, 36)
    
    let yPosition = 50
    let exerciseNumber = 1
    
    // Process each exercise with enhanced formatting
    for (const exercice of filteredExercices.value) {
      // Check if we need a new page
      if (yPosition > pageHeight - 100) {
        pdf.addPage()
        yPosition = margin
      }
      
      // Exercise number box
      pdf.setFillColor(59, 130, 246)
      pdf.setTextColor(255, 255, 255)
      pdf.roundedRect(margin, yPosition - 5, 15, 10, 2, 2, 'F')
      pdf.setFontSize(10)
      pdf.setFont('helvetica', 'bold')
      pdf.text(`${exerciseNumber}`, margin + 4, yPosition + 2)
      
      // Exercise title
      pdf.setTextColor(0, 0, 0)
      pdf.setFontSize(12)
      pdf.setFont('helvetica', 'bold')
      if (exercice.titre) {
        pdf.text(exercice.titre, margin + 20, yPosition + 2)
      }
      
      yPosition += 15
      
      // Difficulty indicator
      const difficulty = exercice.difficulty || 'medium'
      const difficultyText = difficulty === 'easy' ? '★☆☆ Facile' : 
                            difficulty === 'medium' ? '★★☆ Moyen' : '★★★ Difficile'
      const difficultyColor = difficulty === 'easy' ? [34, 197, 94] : 
                             difficulty === 'medium' ? [245, 158, 11] : [239, 68, 68]
      
      pdf.setFontSize(8)
      pdf.setFont('helvetica', 'normal')
      pdf.setTextColor(...difficultyColor)
      pdf.text(difficultyText, margin, yPosition)
      
      yPosition += 10
      pdf.setTextColor(0, 0, 0)
      
      // Exercise content (énoncé)
      const question = exercice.question || exercice.contenu || ''
      if (question) {
        pdf.setFontSize(11)
        pdf.setFont('helvetica', 'bold')
        pdf.text('Énoncé :', margin, yPosition)
        yPosition += 8
        
        yPosition = formatScientificContent(
          cleanTextForPDF(question), 
          pdf, 
          yPosition, 
          contentWidth, 
          margin
        )
        yPosition += 10
      }
      
      // If including corrections, add steps and solution
      if (includeCorrection) {
        // Steps if available
        if (exercice.etapes && exercice.etapes.trim()) {
          // Check for page break
          if (yPosition > pageHeight - 60) {
            pdf.addPage()
            yPosition = margin
          }
          
          pdf.setFontSize(11)
          pdf.setFont('helvetica', 'bold')
          pdf.setTextColor(139, 69, 19)
          pdf.text('🔢 Méthode de résolution :', margin, yPosition)
          yPosition += 10
          
          pdf.setTextColor(0, 0, 0)
          yPosition = formatScientificContent(
            cleanTextForPDF(exercice.etapes), 
            pdf, 
            yPosition, 
            contentWidth, 
            margin
          )
          yPosition += 10
        }
        
        // Solution
        const solution = exercice.reponse_correcte || ''
        if (solution) {
          // Check for page break
          if (yPosition > pageHeight - 40) {
            pdf.addPage()
            yPosition = margin
          }
          
          pdf.setFillColor(240, 253, 244)
          pdf.roundedRect(margin - 5, yPosition - 5, contentWidth + 10, 8, 2, 2, 'F')
          
          pdf.setFontSize(11)
          pdf.setFont('helvetica', 'bold')
          pdf.setTextColor(21, 128, 61)
          pdf.text('✅ Réponse :', margin, yPosition)
          yPosition += 10
          
          pdf.setTextColor(0, 0, 0)
          yPosition = formatScientificContent(
            cleanTextForPDF(solution), 
            pdf, 
            yPosition, 
            contentWidth, 
            margin
          )
          yPosition += 5
        }
      }
      
      // Add separator line
      yPosition += 10
      pdf.setDrawColor(229, 231, 235)
      pdf.setLineWidth(0.5)
      pdf.line(margin, yPosition, pageWidth - margin, yPosition)
      yPosition += 20
      
      exerciseNumber++
    }
    
    // Footer on each page
    const pageCount = pdf.internal.getNumberOfPages()
    for (let i = 1; i <= pageCount; i++) {
      pdf.setPage(i)
      pdf.setFontSize(8)
      pdf.setTextColor(107, 114, 128)
      pdf.text(`Page ${i} sur ${pageCount}`, pageWidth - margin - 20, pageHeight - 10)
      
      if (includeCorrection) {
        pdf.text('Document avec corrections', margin, pageHeight - 10)
      } else {
        pdf.text('Document d\'énoncés', margin, pageHeight - 10)
      }
    }
    
    // Generate filename
    const sanitizedChapterName = notionNom.value
      .replace(/[^a-zA-Z0-9\sàâäéèêëïîôöùûüÿç]/g, '')
      .replace(/\s+/g, '_')
      .toLowerCase()
    const suffix = includeCorrection ? '_avec_corrections' : '_enonces'
    const dateStr = new Date().toISOString().split('T')[0]
    const filename = `exercices_${sanitizedChapterName}${suffix}_${dateStr}.pdf`
    
    // Save the PDF
    pdf.save(filename)
    
    // Success notification
    const message = includeCorrection ? 
      'PDF avec corrections généré avec succès !' : 
      'PDF des énoncés généré avec succès !'
    
    // You can replace this with a proper toast notification
    setTimeout(() => {
      alert(message)
    }, 500)
    
  } catch (error) {
    console.error('Erreur lors de la génération du PDF:', error)
    alert('Erreur lors de la génération du PDF. Veuillez vérifier que les données sont chargées et réessayer.')
  }
}

function cleanTextForPDF(text) {
  if (!text) return ''
  
  return text
    // Remove HTML tags but preserve structure
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<p[^>]*>/gi, '')
    .replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**')
    .replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*')
    .replace(/<[^>]*>/g, '')
    // Replace common HTML entities
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    // Handle LaTeX math notation better
    .replace(/\$\$([^$]+)\$\$/g, '\n[$1]\n')  // Display math
    .replace(/\$([^$]+)\$/g, '($1)')          // Inline math
    .replace(/\\ge/g, '≥')
    .replace(/\\le/g, '≤')
    .replace(/\\cdot/g, '·')
    .replace(/\\times/g, '×')
    .replace(/\\div/g, '÷')
    .replace(/\\pm/g, '±')
    .replace(/\\infty/g, '∞')
    .replace(/\\alpha/g, 'α')
    .replace(/\\beta/g, 'β')
    .replace(/\\gamma/g, 'γ')
    .replace(/\\delta/g, 'δ')
    .replace(/\\pi/g, 'π')
    .replace(/\\theta/g, 'θ')
    .replace(/\\lambda/g, 'λ')
    .replace(/\\mu/g, 'μ')
    .replace(/\\sigma/g, 'σ')
    .replace(/\\sum/g, 'Σ')
    .replace(/\\prod/g, 'Π')
    .replace(/\\int/g, '∫')
    .replace(/\\partial/g, '∂')
    .replace(/\\nabla/g, '∇')
    .replace(/\\sqrt/g, '√')
    // Replace common math patterns
    .replace(/\^(\d+)/g, '⁽$1⁾')
    .replace(/\_(\d+)/g, '₍$1₎')
    // Clean up formatting
    .replace(/\*\*([^*]+)\*\*/g, (match, p1) => p1.toUpperCase())  // Bold to uppercase
    .replace(/\*([^*]+)\*/g, '$1')  // Remove italic markers
    // Clean up multiple spaces and newlines
    .replace(/\s+/g, ' ')
    .replace(/\n\s*\n\s*\n/g, '\n\n')
    .replace(/^\s+|\s+$/g, '')
    .trim()
}

function formatScientificContent(text, pdf, startY, contentWidth, margin, isTitle = false) {
  if (!text) return startY
  
  const fontSize = isTitle ? 12 : 10
  const lineHeight = fontSize * 0.4
  
  pdf.setFontSize(fontSize)
  pdf.setFont('helvetica', isTitle ? 'bold' : 'normal')
  
  // Split content into paragraphs
  const paragraphs = text.split('\n\n').filter(p => p.trim())
  let currentY = startY
  
  for (const paragraph of paragraphs) {
    if (paragraph.trim()) {
      // Handle special formatting
      let formattedParagraph = paragraph
      
      // Detect if it's a step or numbered item
      const isStep = /^(🔵|Étape \d+|Question \d+|Réponse)/i.test(paragraph)
      
      if (isStep) {
        pdf.setFont('helvetica', 'bold')
        pdf.setFontSize(fontSize)
      } else {
        pdf.setFont('helvetica', 'normal')
        pdf.setFontSize(fontSize - 1)
      }
      
      const lines = pdf.splitTextToSize(formattedParagraph, contentWidth)
      
      // Check for page break
      if (currentY + (lines.length * lineHeight) > pdf.internal.pageSize.getHeight() - 20) {
        pdf.addPage()
        currentY = margin
      }
      
      pdf.text(lines, margin, currentY)
      currentY += lines.length * lineHeight + (isStep ? 8 : 5)
    }
  }
  
  return currentY
}
</script>

<style scoped>
.exercices-section {
  background: #f8fafc;
  min-height: 100vh;
  padding: 0;
}

:deep(.dashboard-main) {
  padding-top: 0 !important;
  padding-left: 0 !important;
}

:deep(.dashboard-main.with-mobile-nav) {
  padding-top: 0 !important;
}

.nav-header-base {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 0.75rem 0.25rem 0.75rem 0.25rem;
  margin: 0 0 1rem 0;
  display: flex;
  background: #f8fafc;
  box-shadow: none;
}

.exercices-body {
  width: 100%;
  padding: 0 2rem 1.5rem 2rem;
}

@media (max-width: 1200px) {
  .exercices-body {
    padding: 0 1.5rem 1.25rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .exercices-body {
    padding: 0 1rem 0.75rem 1rem;
  }
}

@media (max-width: 480px) {
  .exercices-body {
    padding: 0 0.75rem 0.5rem 0.75rem;
  }
}

@media (max-width: 360px) {
  .exercices-body {
    padding: 0 0.6rem 0.4rem 0.6rem;
  }
}

.exercices-content-outer {
  width: 100%;
  transform-origin: top left;
  transition: transform 0.2s ease, zoom 0.2s ease;
  overflow-x: hidden;
  /* Les styles seront appliqués dynamiquement via JS selon le support du zoom */
}

/* Responsive design pour mobile */
@media (max-width: 768px) {
  .exercices-title {
    font-size: 1.6rem;
    margin-bottom: 30px;
  }

  .exercices-list {
    gap: 24px;
    max-width: 100%;
    margin: 0;
  }
}

@media (max-width: 680px) {
  .exercices-title {
    font-size: 1.4rem;
    margin-bottom: 25px;
  }

  .exercices-list {
    gap: 20px;
  }
}

.exercices-title {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
}
.exercices-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: 100%;
  margin: 0 auto;
  align-items: stretch;
  transition: max-width 0.3s ease;
}

/* Coming soon card */
.empty-coming { display:flex; align-items:center; justify-content:center; min-height:50vh; }
.empty-card { background:#fff; border:1px solid #e5e7eb; border-radius:16px; padding:2rem; text-align:center; box-shadow:0 8px 24px rgba(2,6,23,0.06); max-width:720px; }
.empty-icon { font-size:2.2rem; margin-bottom:.25rem; }
.empty-title { margin:0 0 .5rem; color:#0f172a; font-size:1.35rem; }
.empty-text { color:#475569; margin:0; }
.empty-actions { margin-top:1rem; }
.empty-btn { background:linear-gradient(135deg,#3b82f6,#1e40af); color:#fff; border:none; border-radius:10px; padding:.6rem 1rem; font-weight:700; cursor:pointer; }
.empty-btn:hover { filter:brightness(1.05); }

.exercices-list.full-width {
  max-width: 95vw;
}
.exercices-loader, .exercices-error {
  font-size: 1.2rem;
  color: #475569;
  margin: 40px 0;
}

/* Responsive pour les messages de chargement et d'erreur */
@media (max-width: 768px) {
  .exercices-loader, .exercices-error {
    font-size: 1rem;
    margin: 30px 0;
  }
}

@media (max-width: 680px) {
  .exercices-loader, .exercices-error {
    font-size: 0.9rem;
    margin: 25px 0;
  }
}

.exercices-controls {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border-radius: 0;
  border: none;
  max-width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.controls-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: space-between;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.type-filter-buttons {
  flex-wrap: wrap;
}
.filter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 500;
  color: #6b7280;
  font-size: 0.8rem;
  white-space: nowrap;
}

.filter-divider {
  width: 1px;
  height: 16px;
  background-color: #d1d5db;
  flex-shrink: 0;
}

.filter-cta {
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
  border-radius: 999px;
  padding: 0.45rem 1rem;
  box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.15);
  font-weight: 500;
  color: #4338ca;
}

.filter-cta-icon {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #4338ca;
  border-radius: 50%;
  color: white;
}

.filter-cta-icon svg {
  width: 16px;
  height: 16px;
}

.filter-cta-text {
  font-size: 0.85rem;
  white-space: nowrap;
}

.filter-buttons {
  display: flex;
  gap: 0.25rem;
}

.type-filter-btn {
  min-width: 90px;
  padding: 0.35rem 0.8rem;
}

.filter-btn {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.35rem 0.9rem;
  cursor: pointer;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s ease;
  min-width: 2rem;
  text-align: center;
  font-size: 0.85rem;
  line-height: 1.2;
  min-height: 38px;
}

.filter-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

.filter-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
  box-shadow: 0 1px 4px rgba(59, 130, 246, 0.3);
}

.difficulty-stars {
  color: inherit;
  font-size: 0.7rem;
}

.difficulty-text {
  font-weight: 500;
}

.width-toggle-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  min-width: auto !important;
}

.width-toggle-btn span:first-child {
  font-size: 0.875rem;
}

.pdf-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.pdf-btn:hover:not(:disabled) {
  background: #3b82f6;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.pdf-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pdf-btn:disabled:hover {
  background: #f9fafb;
  color: #6b7280;
  transform: none;
  box-shadow: none;
}

/* Responsive design for filters */
@media (max-width: 680px) {
  .exercices-controls {
    padding: 0.5rem;
    margin: 0.5rem;
  }

  .controls-row {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .filter-row {
    flex-direction: row;
    gap: 0.5rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .filter-item {
    flex-direction: row;
    align-items: center;
    gap: 0.4rem;
    flex: 0 1 auto;
  }

  .filter-label {
    font-size: 0.7rem;
  }

  .filter-divider {
    display: block;
    height: auto;
    align-self: stretch;
  }

  .filter-buttons {
    gap: 0.25rem;
  }

  .filter-btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.75rem;
    min-width: 1.8rem;
  }

}

/* Navigation ultra-propre */
.clean-navigation {
  margin: 1.5rem 0 1rem 0;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.4rem;
  width: 100%;
  margin: 0 auto;
}

.nav-item {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  text-align: left;
  min-height: 50px;
}

.nav-item:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-item.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.nav-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.2;
  flex: 1;
  text-align: left;
}

.nav-count {
  font-size: 0.6rem;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  min-width: 1.2rem;
  height: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-item.active .nav-count {
  background: rgba(255, 255, 255, 0.25);
}

/* Style pour les boutons de téléchargement dans les filtres */
.download-enonces-btn {
  background: #3b82f6 !important;
  color: white !important;
  border-color: #3b82f6 !important;
  transition: all 0.2s ease;
}

.download-enonces-btn:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.download-corriges-btn {
  background: #10b981 !important;
  color: white !important;
  border-color: #10b981 !important;
  transition: all 0.2s ease;
}

.download-corriges-btn:hover {
  background: #059669 !important;
  border-color: #059669 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* Responsive */
@media (max-width: 680px) {
  .clean-navigation {
    margin: 1.5rem 0 1rem 0;
    padding: 0 0.5rem;
  }

  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.3rem;
    width: 100%;
  }

  .nav-item {
    padding: 0.4rem 0.4rem;
    min-height: 45px;
  }

  .nav-icon {
    font-size: 0.9rem;
  }

  .nav-label {
    font-size: 0.65rem;
  }

  .nav-count {
    font-size: 0.5rem;
    padding: 0.1rem 0.25rem;
    min-width: 1rem;
    height: 1rem;
  }
}

@media (max-width: 360px) {
  .clean-navigation {
    margin: 1.5rem 0 1rem 0;
  }

  .nav-grid {
    grid-template-columns: 1fr;
    gap: 0.3rem;
    width: 100%;
  }

  .nav-item {
    padding: 0.4rem 0.6rem;
    min-height: 40px;
  }

  .nav-icon {
    font-size: 0.85rem;
  }

  .nav-label {
    font-size: 0.6rem;
  }

  .nav-count {
    font-size: 0.5rem;
    padding: 0.1rem 0.2rem;
    min-width: 0.9rem;
    height: 0.9rem;
  }
}

</style> 
