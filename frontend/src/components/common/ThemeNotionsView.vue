<template>
  <div class="tnv-wrapper">
    <!-- Loading with Skeleton -->
    <div v-if="loading" class="tnv-loading-skeleton">
      <div class="tnv-loading-spinner">
        <div class="tnv-spinner" aria-hidden="true"></div>
        <p class="tnv-loading-text">Chargement des chapitres...</p>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="tnv-state tnv-error">
      <div class="tnv-error-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
          <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2"/>
          <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>
      <p>{{ error }}</p>
      <button class="tnv-retry" @click="load(matiereId)">Réessayer</button>
    </div>

    <!-- Content -->
    <div v-else class="tnv-content">
      <!-- No active subject -->
      <div v-if="!matiereId" class="tnv-state">
        <template v-if="isTablesFormulesMode">
          <div class="tnv-coming-soon-badge">Nouveau</div>
          <p class="tnv-coming-soon-title">Arrive bientôt</p>
          <p class="tnv-coming-soon-text">Les premiers tableaux et formules essentiels seront disponibles très bientôt.</p>
        </template>
        <template v-else>
          <div class="tnv-error-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 7v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <circle cx="12" cy="16.5" r="1" fill="currentColor"/>
            </svg>
          </div>
          <p>Aucune matière active</p>
          <p style="color:#6b7280;margin-top:4px">Sélectionnez une matière dans la barre latérale pour afficher les concepts.</p>
          <div class="tnv-left-hint">
            <span class="arrow">←</span>
            <span>Dans la colonne de gauche, cliquez sur <strong>+ New Matière</strong> pour en choisir une.</span>
          </div>
        </template>
      </div>
      <template v-else>
        <div v-if="notionsLocked" class="tnv-lock-banner">
          <div class="tnv-lock-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="11" width="18" height="10" rx="2" stroke="currentColor" stroke-width="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <circle cx="12" cy="16" r="1.5" fill="currentColor"/>
            </svg>
          </div>
          <div class="tnv-lock-texts">
            <p class="tnv-lock-title">Niveau verrouillé</p>
            <p class="tnv-lock-text">
              {{ currentLevelLabel || 'Ce niveau' }} est verrouillé. Abonnez-vous pour débloquer tous les chapitres.
            </p>
          </div>
          <router-link to="/billing#plans" class="tnv-lock-cta">
            Voir les offres
          </router-link>
        </div>
      <!-- Search Bar -->
      <div v-if="showSearch" class="tnv-search">
        <div class="tnv-search-inner">
          <svg class="tnv-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
            <line x1="20" y1="20" x2="16" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <input
            v-model="query"
            :placeholder="searchPlaceholder"
            class="tnv-search-input"
            type="search"
            @keydown.enter.prevent="openFirstMatch"
          />
        </div>
        <div v-if="showSearch && query && filteredTotalCount === 0" class="tnv-no-results">
          Aucun résultat pour « {{ query }} »
        </div>
        <!-- Résultats inline (liste complète) -->
        <div v-if="showSearch && query && matchedNotions.length > 0" class="tnv-inline-results">
          <span class="tnv-inline-label">Trouvé dans:</span>
          <button
            v-for="n in matchedNotions"
            :key="`inline-${n.id}`"
            class="tnv-inline-chip"
            type="button"
            :disabled="false"
            @click="goToNotion(n.id)"
          >
            <span v-if="themeNameFor(n)" class="tnv-inline-theme">{{ themeNameFor(n) }}</span>
            <span class="tnv-inline-title" v-html="highlightQuery(n.nom)"></span>
          </button>
        </div>
      </div>
      <!-- Themes with their notions -->
      <div v-if="themes.length > 0" class="tnv-themes">
        <div v-for="theme in filteredThemes" :key="theme.id" class="tnv-theme-block">
          <div class="tnv-theme-header">
            <h2 class="tnv-theme-title">{{ theme.nom }}</h2>
            <div class="tnv-theme-count">
              {{ (notionsForTheme(theme.id)).length }} concept{{ (notionsForTheme(theme.id)).length > 1 ? 's' : '' }}
            </div>
          </div>
          <div class="tnv-notions-grid">
            <NotionCard
              v-for="notion in notionsForTheme(theme.id)"
              :key="notion.id"
              :notion-id="notion.id"
              :title="notion.nom"
              :description="notion.description || ''"
              :locked="isNotionLocked(notion.id)"
              @click="goToNotion(notion.id)"
              @locked-click="goToNotion(notion.id)"
            />
            <div v-if="!(themeToNotions[theme.id] && themeToNotions[theme.id].length)" class="tnv-no-notions">
              <div class="tnv-empty-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <p>Aucun concept disponible</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Fallback: show notions directly or CTA if empty -->
      <div v-else class="tnv-fallback">
        <template v-if="(filteredDirectNotions || []).length === 0">
          <template v-if="isTablesFormulesMode">
            <div class="tnv-fallback-header">
              <div class="tnv-coming-soon-badge">Nouveau</div>
              <h3>Arrive bientôt</h3>
              <p>Les tableaux et formules de ce niveau sont en préparation.</p>
            </div>
          </template>
          <template v-else>
            <div class="tnv-fallback-header">
              <h3>Aucune matière active</h3>
              <p>Sélectionnez une matière dans la barre latérale pour afficher les concepts.</p>
            </div>
            <div class="tnv-left-hint">
              <span class="arrow">←</span>
              <span>Regardez à gauche et cliquez sur <strong>+ New Matière</strong> pour sélectionner une matière.</span>
            </div>
          </template>
        </template>
        <template v-else>
          <div class="tnv-fallback-header">
            <h3>Concepts disponibles</h3>
            <p>Explorez les concepts fondamentaux de cette matière</p>
          </div>
          <div class="tnv-notions-grid">
            <NotionCard
              v-for="notion in filteredDirectNotions"
              :key="notion.id"
              :notion-id="notion.id"
              :title="notion.nom"
              :description="notion.description || ''"
              :locked="isNotionLocked(notion.id)"
              @click="goToNotion(notion.id)"
              @locked-click="goToNotion(notion.id)"
            />
          </div>
        </template>
      </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount, nextTick, computed, onActivated } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { getNotionsPourUtilisateur } from '@/api'
import { getThemesWithNotionsForUser } from '@/api/themes'
import { getCours } from '@/api/cours'
import { getSynthesisSheets, getSynthesisSheet } from '@/api/synthesis'
import { getExercices } from '@/api/exercices'
import NotionCard from '@/components/UI/NotionCard.vue'
import SkeletonCard from '@/components/common/SkeletonCard.vue'
import { useDataPrefetch } from '@/composables/useDataPrefetch'
import { useRequireSubscription } from '@/composables/useRequireSubscription'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  matiereId: { type: [Number, String], required: true },
  notionRouteName: { type: String, required: true },
  showSearch: { type: Boolean, default: false },
  searchPlaceholder: { type: String, default: 'Rechercher un concept, un mot-clé…' },
  deepSearchInCourses: { type: Boolean, default: false },
  deepSearchInSheets: { type: Boolean, default: false },
  synthesisSheetType: { type: String, default: 'summary' },
  filterNotionsBySheets: { type: Boolean, default: false },
  excludeNotionsBySheetType: { type: String, default: '' },
  deepSearchInExercises: { type: Boolean, default: false },
  showInlineResults: { type: Boolean, default: true }
})

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const { prefetchNotionContent } = useDataPrefetch()
const { ensureAccess } = useRequireSubscription()
const { showToast } = useToast()

const loading = ref(false)
const error = ref('')
const themes = ref([])
const themeToNotions = ref({})
const directNotions = ref([])
const query = ref('')
// Deep search index: notionId -> { raw: string, norm: string }
const deepIndex = ref(new Map())
let deepAbortToken = 0
const deepIndexingNotions = new Set()

const isTablesFormulesMode = computed(() => {
  const type = String(props.synthesisSheetType || '').toLowerCase()
  return props.filterNotionsBySheets && type === 'table'
})

// Accès pratique à toutes les notions (ordre stable)
const allNotions = computed(() => {
  const out = []
  for (const theme of themes.value) {
    const arr = themeToNotions.value[theme.id] || []
    out.push(...arr)
  }
  if (themes.value.length === 0 && Array.isArray(directNotions.value)) out.push(...directNotions.value)
  return out
})

function rankForNotion(n) {
  const q = normalize(query.value)
  if (!q) return Number.POSITIVE_INFINITY
  // 1) Nom/description
  const nameIdx = normalize(n.nom || '').indexOf(q)
  if (nameIdx !== -1) return nameIdx
  const descIdx = normalize(n.description || '').indexOf(q)
  if (descIdx !== -1) return 1000 + descIdx
  // 2) Deep index
  const text = deepIndex.value.get(n.id)
  if (typeof text === 'string') {
    const contentIdx = normalize(text).indexOf(q)
    if (contentIdx !== -1) return 100000 + contentIdx
  }
  return Number.POSITIVE_INFINITY
}

const matchedNotions = computed(() => {
  if (!hasQuery()) return []
  const list = allNotions.value.filter(notionMatches)
  return list.sort((a, b) => rankForNotion(a) - rankForNotion(b))
})

const firstMatchNotion = computed(() => matchedNotions.value[0] || null)

const firstMatchThemeName = computed(() => {
  const n = firstMatchNotion.value
  if (!n) return ''
  const tId = n.theme
  if (!tId) return ''
  const t = themes.value.find(t => t.id === tId)
  return t?.nom || ''
})

function openFirstMatch() {
  const n = firstMatchNotion.value
  if (n?.id) {
    goToNotion(n.id)
  }
}

// Helpers de filtrage
function normalize(str) {
  return (str || '')
    .toString()
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
}

const qNorm = computed(() => normalize(query.value))
const hasQuery = () => qNorm.value.length > 0

function notionMatches(notion) {
  if (!hasQuery()) return true
  const q = qNorm.value
  const basic = (
    normalize(notion.nom).includes(q) ||
    normalize(notion.description || '').includes(q)
  )
  if (basic) return true
  // Deep search in content (courses, sheets, exercises) if enabled and query has enough length
  if ((props.deepSearchInCourses || props.deepSearchInSheets || props.deepSearchInExercises) && q.length >= 3) {
    const idx = deepIndex.value
    const entry = idx.get(notion.id)
    if (entry && typeof entry.norm === 'string') {
      return entry.norm.includes(q)
    } else {
      // Pas d'index encore: laisser scheduleDeepIndexing gérer (debounced)
    }
  }
  return false
}

async function goToNotion(notionId) {
  if (isNotionLocked(notionId)) {
    router.push({ name: 'Billing', hash: '#plans' })
    return
  }
  // Effacer le filtre de recherche de l'URL avant de naviguer
  try {
    const newQuery = { ...route.query }
    delete newQuery.q
    router.replace({ query: newQuery })
  } catch (_) {}
  const target = { name: props.notionRouteName, params: { notionId } }
  const isDemoNotion = demoNotionId.value && Number(notionId) === demoNotionId.value
  if (isDemoNotion || await ensureAccess(target)) {
    router.push(target)
  }
}

// Cache hybride mémoire + localStorage pour accélérer l'affichage (5 minutes)
const CACHE_TTL_MS = 300000
const cache = new Map()

function storageKey(matiereId) {
  return `tnv_cache:${cacheKey(matiereId)}`
}

function readFromStorage(matiereId) {
  try {
    const raw = localStorage.getItem(storageKey(matiereId))
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed || !parsed.t || !parsed.v) return null
    if (Date.now() - parsed.t > CACHE_TTL_MS) return null
    return parsed
  } catch (_) {
    return null
  }
}

function writeToStorage(matiereId, value) {
  try {
    const payload = JSON.stringify({ t: Date.now(), v: value })
    localStorage.setItem(storageKey(matiereId), payload)
  } catch (_) {
    // ignore quota or serialization errors
  }
}

function cacheKey(matiereId) {
  const niveauId = userStore.niveau_pays?.id || 'n'
  const paysId = userStore.pays?.id || 'p'
  const excludedType = (props.excludeNotionsBySheetType || '').trim().toLowerCase()
  const notionsScope = props.filterNotionsBySheets
    ? `sheets:${props.synthesisSheetType || 'summary'}`
    : (excludedType ? `exclude-sheets:${excludedType}` : 'all-notions')
  return `${matiereId}|${niveauId}|${paysId}|${notionsScope}`
}

let currentAbortController = null

async function load(matiereId) {
  if (!matiereId) return
  error.value = ''
  loading.value = true

  const key = cacheKey(matiereId)
  const entry = cache.get(key) || readFromStorage(matiereId)
  if (entry && Date.now() - entry.t < CACHE_TTL_MS) {
    themes.value = entry.v.themes
    themeToNotions.value = entry.v.themeToNotions
    directNotions.value = entry.v.directNotions
    setTimeout(() => { loading.value = false }, 120)
  } else {
    loading.value = true
  }

  try {
    // Annuler l'appel précédent si toujours en vol
    if (currentAbortController) {
      try { currentAbortController.abort() } catch (_) {}
    }
    currentAbortController = new AbortController()
    const requestParams = { matiere: matiereId, signal: currentAbortController.signal }
    const excludedType = (props.excludeNotionsBySheetType || '').trim().toLowerCase()
    if (excludedType) requestParams.exclude_sheet_type = excludedType
    const { data } = await getThemesWithNotionsForUser(requestParams)
    
    // Les données sont déjà triées par le backend - pas besoin de re-trier
    let themesList = Array.isArray(data?.themes) ? data.themes : []
    let notions = Array.isArray(data?.notions) ? data.notions : []

    if (props.filterNotionsBySheets) {
      const sheetType = props.synthesisSheetType || 'summary'
      const sheetsResp = await getSynthesisSheets({
        matiere: matiereId,
        sheet_type: sheetType
      })
      const sheetsRaw = sheetsResp?.data
      const sheetsList = Array.isArray(sheetsRaw)
        ? sheetsRaw
        : (Array.isArray(sheetsRaw?.results) ? sheetsRaw.results : [])

      const allowedNotionIds = new Set(
        sheetsList
          .map(sheet => Number(sheet?.notion))
          .filter(notionId => Number.isFinite(notionId))
      )

      notions = notions.filter(n => allowedNotionIds.has(Number(n.id)))

      if (themesList.length > 0) {
        const themeIdsWithNotions = new Set(
          notions
            .map(n => Number(n.theme))
            .filter(themeId => Number.isFinite(themeId))
        )
        themesList = themesList.filter(theme => themeIdsWithNotions.has(Number(theme.id)))
      }
    }

    // Grouper les notions par thème (notions déjà triées par theme_id, ordre, titre)
    const grouped = {}
    for (const n of notions) {
      if (!grouped[n.theme]) grouped[n.theme] = []
      grouped[n.theme].push(n)
    }

    themes.value = themesList
    themeToNotions.value = grouped
    directNotions.value = themesList.length === 0 ? notions.filter(n => !n.theme) : []

    const cachePayload = { themes: themes.value, themeToNotions: themeToNotions.value, directNotions: directNotions.value }
    cache.set(key, { t: Date.now(), v: cachePayload })
    writeToStorage(matiereId, cachePayload)
    
    // Précharger automatiquement les 3 premières notions en arrière-plan (non-bloquant)
    await nextTick()
    prefetchTopNotions()
  } catch (e) {
    if (e?.name === 'CanceledError' || e?.name === 'AbortError') {
      // navigation rapide: ignorer l'erreur annulée
      return
    }
    error.value = 'Erreur lors du chargement des concepts'
  } finally {
    loading.value = false
  }
}

/**
 * Précharge les 3 premières notions en arrière-plan
 * pour accélérer la navigation utilisateur
 */
function prefetchTopNotions() {
  // Collecter les 3 premières notions de tous les thèmes
  const topNotions = []
  for (const theme of themes.value) {
    const notionsInTheme = themeToNotions.value[theme.id] || []
    topNotions.push(...notionsInTheme.slice(0, 1)) // 1ère notion de chaque thème
    if (topNotions.length >= 3) break
  }
  
  // Précharger en arrière-plan (fire and forget)
  topNotions.slice(0, 3).forEach(notion => {
    if (notion?.id) {
      setTimeout(() => {
        prefetchNotionContent(notion.id).catch(() => {
          // Ignorer les erreurs silencieusement
        })
      }, 500) // Délai de 500ms pour ne pas bloquer l'UI
    }
  })
}

onMounted(() => {
  load(props.matiereId)
  subscriptionStore.fetchStatus({ force: true }).catch(() => {})
})
watch(() => props.matiereId, (id) => load(id))

onBeforeUnmount(() => {
  if (currentAbortController) {
    try { currentAbortController.abort() } catch (_) {}
  }
})
// Données filtrées dérivées
const filteredThemeToNotions = computed(() => {
  if (!hasQuery()) return themeToNotions.value
  const out = {}
  for (const [themeId, arr] of Object.entries(themeToNotions.value || {})) {
    out[themeId] = (arr || []).filter(notionMatches)
  }
  return out
})

const filteredThemes = computed(() => {
  if (!hasQuery()) return themes.value
  return themes.value.filter(t => (filteredThemeToNotions.value[t.id] || []).length > 0)
})

function notionsForTheme(themeId) {
  return (hasQuery() ? filteredThemeToNotions.value[themeId] : themeToNotions.value[themeId]) || []
}

const filteredDirectNotions = computed(() => {
  return hasQuery() ? (directNotions.value || []).filter(notionMatches) : directNotions.value
})

const filteredTotalCount = computed(() => {
  let total = 0
  if (themes.value.length > 0) {
    for (const t of filteredThemes.value) total += notionsForTheme(t.id).length
  } else {
    total = (filteredDirectNotions.value || []).length
  }
  return total
})

const selectedNiveauId = computed(() => {
  const rawId = userStore.niveau_pays?.id
  if (rawId == null) return null
  const parsed = Number(rawId)
  return Number.isNaN(parsed) ? null : parsed
})
const hasSelectedLevelAccess = computed(() => {
  if (userStore.isAdmin) return true
  return subscriptionStore.accessForLevel(selectedNiveauId.value)
})
const notionsLocked = computed(() => !hasSelectedLevelAccess.value)
const demoNotionId = computed(() => {
  const id = userStore.niveau_pays?.demo_notion
  return id ? Number(id) : null
})
function isNotionLocked(notionId) {
  if (!notionsLocked.value) return false
  if (demoNotionId.value && Number(notionId) === demoNotionId.value) return false
  return true
}
const currentLevelLabel = computed(() => {
  const level = userStore.niveau_pays
  if (!level) return ''
  const paysName = level.pays?.nom || userStore.pays?.nom
  return paysName ? `${level.nom} · ${paysName}` : level.nom
})

// (plus de limite topN, on affiche tout en inline)

// Sync recherche <-> URL (partage/retour)
onMounted(() => {
  // Toujours synchroniser la première valeur depuis l'URL
  if (typeof route.query?.q !== 'undefined' && route.query?.q !== null) {
    try { query.value = String(route.query.q) } catch { /* ignore */ }
  }
})

// Synchroniser depuis l'URL quand on revient via KeepAlive
onActivated(() => {
  const q = route.query?.q ? String(route.query.q) : ''
  if (q !== (query.value || '')) {
    query.value = q
  }
})

// Synchroniser quand l'URL est modifiée par un parent
watch(() => route.query.q, (val) => {
  const incoming = val ? String(val) : ''
  if (incoming !== (query.value || '')) {
    query.value = incoming
  }
})

let deepScheduleTimer = null
watch(query, (val) => {
  if (!props.showSearch) return
  const q = (val || '').trim()
  const newQuery = { ...route.query }
  if (q) newQuery.q = q
  else delete newQuery.q
  router.replace({ query: newQuery }).catch(() => {})
  // Kick off deep indexing when user searches
  if ((props.deepSearchInCourses || props.deepSearchInSheets || props.deepSearchInExercises) && q.length >= 3) {
    if (deepScheduleTimer) clearTimeout(deepScheduleTimer)
    deepScheduleTimer = setTimeout(() => {
      scheduleDeepIndexing()
    }, 250)
  }
})

// Déclencher l'indexation aussi quand la source est la recherche globale (showSearch=false)
let deepScheduleTimerFromUrl = null
watch(qNorm, (val) => {
  if (!(props.deepSearchInCourses || props.deepSearchInSheets || props.deepSearchInExercises)) return
  if (val.length < 3) return
  if (deepScheduleTimerFromUrl) clearTimeout(deepScheduleTimerFromUrl)
  deepScheduleTimerFromUrl = setTimeout(() => {
    scheduleDeepIndexing()
  }, 250)
})

// Helpers deep indexing
function allNotionIds() {
  const ids = new Set()
  Object.values(themeToNotions.value || {}).forEach(arr => {
    (arr || []).forEach(n => ids.add(n.id))
  })
  ;(directNotions.value || []).forEach(n => ids.add(n.id))
  return Array.from(ids)
}

function scheduleIndexForNotion(notionId) {
  if (deepIndexingNotions.has(notionId)) return
  deepIndexingNotions.add(notionId)
  // index single notion in background
  buildDeepIndexForNotion(notionId).finally(() => {
    deepIndexingNotions.delete(notionId)
  })
}

async function buildDeepIndexForNotion(notionId) {
  try {
    const parts = []
    if (props.deepSearchInCourses) {
      const { data } = await getCours(props.matiereId, notionId, null)
      const list = Array.isArray(data) ? data : (data ? [data] : [])
      for (const c of list) {
        if (c?.titre) parts.push(String(c.titre))
        if (c?.description) parts.push(String(c.description))
        if (c?.contenu) parts.push(String(c.contenu))
      }
    }
    if (props.deepSearchInSheets) {
      const resp = await getSynthesisSheets({
        notion: notionId,
        sheet_type: props.synthesisSheetType || 'summary'
      })
      const raw = resp?.data
      const list = Array.isArray(raw) ? raw : (Array.isArray(raw?.results) ? raw.results : [])
      for (const s of list) {
        let pushed = false
        try {
          if (s?.id) {
            const detail = await getSynthesisSheet(s.id)
            const d = detail?.data || detail
            if (d?.titre) { parts.push(String(d.titre)); pushed = true }
            if (d?.summary) { parts.push(String(d.summary)); pushed = true }
          }
        } catch (_) { /* ignore */ }
        if (!pushed) {
          if (s?.titre) parts.push(String(s.titre))
          if (s?.summary) parts.push(String(s.summary))
        }
      }
    }
    if (props.deepSearchInExercises) {
      try {
        const resp = await getExercices({ notion: notionId, limit: 200 })
        const exoList = Array.isArray(resp?.data) ? resp.data : (resp?.data?.results || [])
        for (const e of exoList) {
          if (e?.titre) parts.push(String(e.titre))
          if (e?.question) parts.push(String(e.question))
          if (e?.instruction) parts.push(String(e.instruction))
          if (e?.contenu) parts.push(String(e.contenu))
          if (e?.etapes) parts.push(String(e.etapes))
          if (e?.solution) parts.push(String(e.solution))
          if (e?.reponse_correcte) parts.push(String(e.reponse_correcte))
        }
      } catch (_) {}
    }
    const text = parts.join('\n\n')
    const entry = { raw: text, norm: normalize(text) }
    const map = new Map(deepIndex.value)
    map.set(notionId, entry)
    deepIndex.value = map
  } catch (_) {
    // ignore errors for deep indexing
  }
}

async function scheduleDeepIndexing() {
  const token = ++deepAbortToken
  const ids = allNotionIds()
  for (const id of ids) {
    if (token !== deepAbortToken) return
    if (!deepIndex.value.has(id) && !deepIndexingNotions.has(id)) {
      deepIndexingNotions.add(id)
      await buildDeepIndexForNotion(id)
      deepIndexingNotions.delete(id)
    }
  }
}

// Utilitaires pour thème/snippet/highlight affichés dans la ribbon
function themeNameFor(n) {
  const t = themes.value.find(t => t.id === n.theme)
  return t?.nom || ''
}

function snippetForNotion(n) {
  const q = normalize(query.value)
  if (!q) return ''
  let source = n.nom || ''
  let idx = normalize(source).indexOf(q)
  if (idx === -1) {
    source = n.description || ''
    idx = normalize(source).indexOf(q)
  }
  if (idx === -1) {
    const entry = deepIndex.value.get(n.id)
    const text = entry?.raw || ''
    source = text
    idx = normalize(source).indexOf(q)
  }
  if (idx === -1) return ''
  const start = Math.max(0, idx - 30)
  const end = Math.min(source.length, idx + q.length + 30)
  let snippet = source.slice(start, end)
  if (start > 0) snippet = '…' + snippet
  if (end < source.length) snippet = snippet + '…'
  return snippet
}

function escapeHtml(s) {
  return (s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function highlightQuery(text) {
  const q = normalize(query.value)
  if (!q) return escapeHtml(text)
  const source = text || ''
  const idx = normalize(source).indexOf(q)
  if (idx === -1) return escapeHtml(source)
  const before = escapeHtml(source.slice(0, idx))
  const match = escapeHtml(source.slice(idx, idx + q.length))
  const after = escapeHtml(source.slice(idx + q.length))
  return `${before}<mark class="hl">${match}</mark>${after}`
}
</script>

<style scoped>
/* (Reverted) Removed compact spacing overrides */
.tnv-wrapper {
  width: 100%;
  max-width: 100%;
  /* left align content within dashboard main */
  margin: 0;
  box-sizing: border-box;
  overflow-x: hidden;
  min-height: 60vh;
}

.tnv-lock-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #fef3c7;
  border-radius: 0.85rem;
  background: #fffbeb;
  margin-bottom: 1.25rem;
  width: 100%;
  box-sizing: border-box;
  max-width: 100%;
  overflow: hidden;
}

.tnv-lock-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #fef3c7;
  color: #d97706;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tnv-lock-texts {
  flex: 1;
}

.tnv-lock-title {
  margin: 0;
  font-weight: 600;
  color: #92400e;
}

.tnv-lock-text {
  margin: 0.15rem 0 0;
  color: #b45309;
  font-size: 0.9rem;
}

.tnv-lock-cta {
  padding: 0.6rem 1.25rem;
  border-radius: 999px;
  border: 1px solid #fbbf24;
  color: #92400e;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease;
}

.tnv-lock-cta:hover {
  background: rgba(251, 191, 36, 0.15);
}

/* Responsive - Mobile pour la bannière de verrouillage */
@media (max-width: 768px) {
  .tnv-lock-banner {
    flex-direction: row;
    align-items: center;
    gap: 0.625rem;
    padding: 0.65rem;
    border-radius: 0.65rem;
    margin-bottom: 0.875rem;
  }

  .tnv-lock-icon {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
  }

  .tnv-lock-icon svg {
    width: 16px;
    height: 16px;
  }

  .tnv-lock-texts {
    flex: 1;
    min-width: 0; /* Permet au texte de se rétrécir si nécessaire */
    overflow-wrap: break-word;
    word-wrap: break-word;
  }

  .tnv-lock-title {
    font-size: 0.8rem;
    line-height: 1.25;
    margin-bottom: 0.1rem;
    font-weight: 600;
  }

  .tnv-lock-text {
    font-size: 0.7rem;
    line-height: 1.35;
    margin: 0;
    overflow-wrap: break-word;
    word-wrap: break-word;
  }

  .tnv-lock-cta {
    padding: 0.4rem 0.75rem;
    font-size: 0.7rem;
    white-space: nowrap;
    flex-shrink: 0;
  }
}

@media (max-width: 480px) {
  .tnv-lock-banner {
    flex-direction: row;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.55rem;
    border-radius: 0.55rem;
  }

  .tnv-lock-icon {
    width: 28px;
    height: 28px;
    margin-top: 0.1rem; /* Alignement avec le texte */
  }

  .tnv-lock-icon svg {
    width: 14px;
    height: 14px;
  }

  .tnv-lock-texts {
    flex: 1;
    min-width: 0;
    overflow-wrap: break-word;
    word-wrap: break-word;
  }

  .tnv-lock-title {
    font-size: 0.75rem;
    line-height: 1.25;
    margin-bottom: 0.15rem;
    font-weight: 600;
  }

  .tnv-lock-text {
    font-size: 0.65rem;
    line-height: 1.3;
    overflow-wrap: break-word;
    word-wrap: break-word;
  }

  .tnv-lock-cta {
    padding: 0.35rem 0.65rem;
    font-size: 0.65rem;
    white-space: nowrap;
    align-self: flex-start;
    margin-top: 0.1rem;
  }
}

/* Barre de recherche */
.tnv-search {
  margin: 0 0 1rem 0;
}

.tnv-search-inner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
}

.tnv-search-icon {
  color: #9ca3af;
  flex-shrink: 0;
}

.tnv-search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.95rem;
  color: #111827;
}

.tnv-no-results {
  margin-top: 0.5rem;
  color: #6b7280;
  font-size: 0.9rem;
}

.tnv-search-suggestion {
  margin-top: 0.5rem;
  color: #374151;
  font-size: 0.9rem;
}

.tnv-match-theme { color: #1f2937; }
.tnv-match-notion { color: #1d4ed8; }

/* Résultats inline collés à la recherche */
.tnv-inline-results {
  margin-top: 0.35rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.35rem 0.5rem;
}
.tnv-inline-label { color: #6b7280; font-size: 0.9rem; }
.tnv-inline-chip {
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 999px;
  padding: 0.2rem 0.6rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
}
.tnv-inline-chip:hover { background: #f9fafb; border-color: #93c5fd; }
.tnv-inline-chip:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  border-color: #e5e7eb;
  background: #f8fafc;
}
.tnv-inline-theme { color: #1f2937; font-size: 0.8rem; }
.tnv-inline-title { color: #1d4ed8; font-weight: 600; font-size: 0.9rem; }
.tnv-inline-more { color: #6b7280; font-size: 0.9rem; }

/* États de chargement et d'erreur */
/* Loading Skeleton */
.tnv-loading-skeleton {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  text-align: center;
  gap: 12px;
  position: relative;
}

.tnv-loading-spinner {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 0;
}

.tnv-spinner {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 4px solid #e5ecff;
  border-top-color: #2563eb;
  animation: tnv-spin 0.9s linear infinite;
}

.tnv-loading-text {
  margin: 0;
  font-weight: 700;
  color: #1d3b8b;
  font-size: 15px;
  letter-spacing: 0.2px;
}

@keyframes tnv-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.tnv-theme-skeleton {
  background: transparent;
  border-radius: 0;
}

.skeleton-theme-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f3f4f6;
}

.skeleton-line {
  height: 12px;
  background: linear-gradient(
    90deg,
    #f3f4f6 0%,
    #e5e7eb 50%,
    #f3f4f6 100%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-theme-title {
  height: 24px;
  width: 200px;
}

.tnv-skeleton-grid {
  display: grid;
  grid-template-columns: repeat(4, 280px);
  gap: 1rem;
  justify-content: start;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.tnv-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.tnv-error-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  background: #fef2f2;
  border-radius: 12px;
  color: #ef4444;
  margin-bottom: 1rem;
}

.tnv-retry {
  background: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 1rem;
}

.tnv-retry:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

/* Blocs de thèmes */
.tnv-theme-block {
  background: transparent;
  border-radius: 0;
  padding: 1rem 0;
  margin-bottom: 1.25rem;
  box-shadow: none;
  border: none;
}

.tnv-theme-block:first-child {
  padding-top: 0.5rem;
}

.tnv-theme-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f3f4f6;
}

.tnv-theme-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  text-align: left;
}

.tnv-theme-count {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.4rem 0.65rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Grille des notions - EXACTEMENT 4 CARTES PAR LIGNE */
.tnv-notions-grid {
  display: grid;
  /* 4 colonnes fixes, espace constant, alignées à gauche */
  grid-template-columns: repeat(4, 280px);
  gap: 1rem;
  justify-content: start;
  align-items: stretch; /* Toutes les cartes ont la même hauteur dans leur ligne */
}

/* État vide */
.tnv-no-notions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  color: #6b7280;
  text-align: center;
  grid-column: 1 / -1;
}

.tnv-empty-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #f9fafb;
  border-radius: 16px;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.tnv-no-notions p {
  margin: 0;
  font-size: 0.875rem;
}

/* Ribbon des résultats (défilement horizontal) */
.tnv-results-ribbon {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding: 0.5rem 0.5rem;
  margin: 0.25rem 0 0.5rem 0;
  scroll-snap-type: x proximity;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f8fafc;
}

.tnv-chip {
  flex: 0 0 auto;
  max-width: 320px;
  scroll-snap-align: start;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  border-radius: 999px;
  padding: 0.4rem 0.75rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.tnv-chip:hover {
  border-color: #93c5fd;
  background: #f9fbff;
}

.tnv-chip-theme {
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 999px;
  padding: 0.1rem 0.5rem;
  font-size: 0.75rem;
}

.tnv-chip-title {
  font-weight: 600;
  color: #111827;
  white-space: nowrap;
}

.tnv-chip-snippet {
  color: #6b7280;
  font-size: 0.85rem;
  white-space: nowrap;
}

.hl { background: #fff3b0; padding: 0 .1rem; border-radius: 2px; }

/* Fallback */
.tnv-fallback {
  background: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.tnv-fallback-header {
  text-align: center;
  margin-bottom: 2rem;
}

.tnv-fallback-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.tnv-fallback-header p {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

/* Hint to the left sidebar */
.tnv-left-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #374151;
  margin-top: 8px;
}
.tnv-left-hint .arrow {
  font-size: 1.4rem;
  color: #3b82f6;
  animation: nudge-left 1.2s ease-in-out infinite;
}

.tnv-coming-soon-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  margin: 0 auto 0.75rem;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 0.75rem;
  font-weight: 600;
}

.tnv-coming-soon-title {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  color: #111827;
}

.tnv-coming-soon-text {
  margin: 0.45rem 0 0;
  color: #6b7280;
  font-size: 0.95rem;
}
@keyframes nudge-left {
  0% { transform: translateX(0); }
  50% { transform: translateX(-4px); }
  100% { transform: translateX(0); }
}

/* Responsive - ADAPTATION POUR 4 CARTES PAR LIGNE */
@media (max-width: 1500px) {
  .tnv-notions-grid {
    grid-template-columns: repeat(3, 280px);
    gap: 1rem;
    justify-content: start;
  }
  
  .tnv-skeleton-grid {
    grid-template-columns: repeat(3, 280px);
  }
}

@media (max-width: 1200px) {
  .tnv-notions-grid {
    grid-template-columns: repeat(2, 280px);
    gap: 1rem;
    justify-content: start;
  }
  
  .tnv-skeleton-grid {
    grid-template-columns: repeat(2, 280px);
  }
  
  .tnv-theme-block {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .tnv-wrapper {
    margin-top: 0;
    padding: 0.85rem;
  }
  
  .tnv-notions-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    justify-content: center;
    padding: 0;
  }
  
  .tnv-skeleton-grid {
    grid-template-columns: 1fr;
    justify-content: center;
  }

  .tnv-theme-block {
    padding: 0;
    margin-bottom: 2rem;
    background: transparent;
  }
  
  .tnv-theme-block:first-child {
    padding-top: 0;
    margin-top: 0;
  }

  .tnv-theme-header {
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding: 0;
    border-bottom: 2.5px solid #3b82f6;
    padding-bottom: 0.6rem;
  }
  
  .tnv-theme-title {
    font-size: 1.15rem;
    color: #111827;
    text-align: left;
    font-weight: 700;
    letter-spacing: -0.01em;
  }
  
  .tnv-notions-grid {
    padding: 0;
  }
  
  /* Cacher le badge de concepts en mode mobile */
  .tnv-theme-count {
    display: none;
  }
}

@media (max-width: 650px) {
  .tnv-wrapper {
    padding: 0.75rem;
  }
  
  .tnv-notions-grid {
    grid-template-columns: 1fr;
    gap: 0.65rem;
    justify-content: center;
    padding: 0;
  }
  
  .tnv-skeleton-grid {
    grid-template-columns: 1fr;
    justify-content: center;
  }

  .tnv-theme-block {
    padding: 0;
    margin-bottom: 1.85rem;
  }

  .tnv-theme-header {
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 0.5rem;
    padding: 0;
    padding-bottom: 0.55rem;
    margin-bottom: 0.9rem;
  }
  
  .tnv-theme-title {
    font-size: 1.05rem;
  }
}

</style>
