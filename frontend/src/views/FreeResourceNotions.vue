<script setup>
import { ref, computed, onMounted, watch, nextTick, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import NotionCard from '@/components/UI/NotionCard.vue'
import BackButton from '@/components/common/BackButton.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import { getFreeResources } from '@/api/free-content'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useZoom } from '@/composables/useZoom'

const props = defineProps({
  resourceType: {
    type: String,
    default: 'course'
  }
})

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const error = ref(null)
const resources = ref([]) // liste courante (page)
const allResources = ref([]) // fallback si pas de pagination serveur
const totalCount = ref(0)
const totalExercisesCount = ref(0)
const totalChaptersCount = ref(0)
const levelOptions = ref([])
const levelOptionsLoaded = ref(false)
const isServerPaginated = ref(true)
const selectedLevels = ref([])
const showLevelFilter = ref(false)
const filterDropdownRef = ref(null)
const filterButtonRef = ref(null)
const currentPage = ref(1)
const itemsPerPage = 12
const searchQuery = ref('')
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()
const { openModal } = useModalManager()
let searchTimeoutId = null

const contentRef = ref(null)
const notionGridRef = ref(null)
const ctaMaxWidthPx = ref(null)

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

const zoomStyle = createZoomStyle({
  cssVar: '--content-zoom',
  heightVar: '--content-height',
  mobileZoomAdjustment: (z) => Math.max(0.6, z - 0.08)
})

function measureContentHeightForFreeResources() {
  measureContentHeight(contentRef)
}

function updateCtaMaxWidthToMatchGrid() {
  const gridEl = notionGridRef.value
  if (!gridEl) {
    ctaMaxWidthPx.value = null
    return
  }

  const children = Array.from(gridEl.children || [])
  if (children.length === 0) {
    ctaMaxWidthPx.value = null
    return
  }

  const gridRect = gridEl.getBoundingClientRect()
  const firstRect = children[0].getBoundingClientRect()
  const rowTop = firstRect.top
  const tolerance = 2

  let maxRight = firstRect.right
  for (const child of children) {
    const rect = child.getBoundingClientRect()
    if (Math.abs(rect.top - rowTop) <= tolerance) {
      maxRight = Math.max(maxRight, rect.right)
    }
  }

  const width = maxRight - gridRect.left
  ctaMaxWidthPx.value = Number.isFinite(width) && width > 0 ? Math.round(width) : null
}

const ctaWidthStyle = computed(() => {
  if (!ctaMaxWidthPx.value) return undefined
  return { maxWidth: `${ctaMaxWidthPx.value}px` }
})

const typeConfig = computed(() => {
  if (props.resourceType === 'exercise') {
    return {
      slugRoute: 'FreeExerciseDetail',
      fallback: 'Exercices à découvrir',
      emptyLabel: 'Aucun exercice gratuit disponible pour le moment.',
      counterLabel: 'exercice',
      chapterLabel: 'Chapitre'
    }
  }
  if (props.resourceType === 'summary') {
    return {
      slugRoute: 'FreeSummaryDetail',
      fallback: 'Fiches à découvrir',
      emptyLabel: 'Aucune fiche de synthèse gratuite disponible pour le moment.',
      counterLabel: 'fiche',
      chapterLabel: 'Niveau'
    }
  }
  return {
    slugRoute: 'FreeCourseDetail',
    fallback: 'Chapitres à découvrir',
    emptyLabel: 'Aucun chapitre gratuit disponible pour le moment.',
    counterLabel: 'chapitre',
    chapterLabel: 'Chapitre'
  }
})

const isExerciseMode = computed(() => props.resourceType === 'exercise')
const isSummaryMode = computed(() => props.resourceType === 'summary')
const isCourseMode = computed(() => props.resourceType === 'course')

const pageIntro = computed(() => {
  if (isExerciseMode.value) {
    return {
      title: 'Exercices corrigés gratuits de maths',
      subtitle: 'Collège • Seconde • Première • Terminale • Prépa (MPSI) • Grandes Écoles — corrections et méthode pas à pas.'
    }
  }

  if (isSummaryMode.value) {
    return {
      title: 'Fiches de synthèse gratuites (maths)',
      subtitle: 'Collège • Seconde • Première • Terminale • Prépa (MPSI) • Grandes Écoles — fiches de synthèse : formules et méthodes.'
    }
  }

  return {
    title: 'Cours de maths en ligne gratuits',
    subtitle: 'Collège • Seconde • Première • Terminale • Prépa (MPSI) • Grandes Écoles — cours clairs, méthodes et exemples.'
  }
})

const getCardTitle = (resource) => {
  if (!resource) return 'Chapitre'
  if (isExerciseMode.value && resource?.notion_nom) {
    return resource.notion_nom
  }
  return resource?.titre || resource?.notion_nom || 'Chapitre'
}

const getCardDescription = (resource) => {
  if (!resource) return 'Cliquez pour explorer'
  if (isExerciseMode.value) {
    return 'Cliquez pour explorer les exercices'
  }
  if (isSummaryMode.value) {
    return 'Cliquez pour explorer les chapitres'
  }
  if (isCourseMode.value) {
    return 'Cliquez pour explorer le cours'
  }
  return resource?.accroche || resource?.excerpt || 'Cliquez pour explorer ce chapitre'
}

const getSummaryLevel = (resource) => {
  return resource?.niveau_nom || resource?.tag_secondaire || resource?.matiere_nom || ''
}

const extractLevels = (list) => {
  const levels = new Set()
  ;(list || []).forEach((resource) => {
    const level = resource?.niveau_nom || resource?.tag_secondaire
    if (level) {
      levels.add(level)
    }
  })
  return Array.from(levels).sort()
}

const sortByLockStatus = (list) => {
  return [...(list || [])].sort((a, b) => {
    const aLocked = Boolean(a?.is_locked)
    const bLocked = Boolean(b?.is_locked)
    if (aLocked === bLocked) return 0
    return aLocked ? 1 : -1
  })
}

const SEARCH_STOPWORDS = new Set([
  'cours',
  'course',
  'en',
  'lign',
  'ligne',
  'online',
  'de',
  'des',
  'du',
  'la',
  'le',
  'les',
  'un',
  'une',
  'et',
  'a',
  'au',
  'aux',
  'pour',
  'avec',
  'sur',
  'dans',
  'd',
  'l'
])

function stripHtml(text) {
  return String(text || '').replace(/<[^>]*>/g, ' ')
}

function normalizeText(text) {
  return String(text || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[’']/g, ' ')
    .replace(/[^a-z0-9]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function expandToken(token) {
  const t = String(token || '').trim()
  if (!t) return []
  const set = new Set([t])

  if (t === 'maths' || t.includes('math')) {
    set.add('math')
    set.add('mathematique')
    set.add('mathematiques')
  }

  if (t === 'mathematique' || t === 'mathematiques') {
    set.add('math')
  }

  if (t === 'terminale' || t.startsWith('terminal')) {
    set.add('terminale')
    set.add('terminal')
  }

  if (t === 'premiere' || t === '1ere' || t === '1re') {
    set.add('premiere')
    set.add('1ere')
    set.add('1re')
  }

  if (t === 'seconde' || t === '2nde' || t === '2de') {
    set.add('seconde')
    set.add('2nde')
    set.add('2de')
  }

  return Array.from(set)
}

function queryTokenGroups(query) {
  const normalized = normalizeText(query)
  if (!normalized) return []
  const rawTokens = normalized.split(' ').filter(Boolean).filter((t) => t.length >= 2)
  const base = rawTokens.filter((t) => !SEARCH_STOPWORDS.has(t))
  if (base.length === 0) return []
  return base.map((t) => expandToken(t)).filter((group) => group.length > 0)
}

function groupMatches(text, group) {
  if (!text || !group || !group.length) return false
  return group.some((variant) => variant && text.includes(variant))
}

function groupsAllMatch(text, groups) {
  if (!groups || groups.length === 0) return false
  return groups.every((group) => groupMatches(text, group))
}

function groupsScore(text, groups) {
  if (!groups || groups.length === 0) return 0
  let score = 0
  for (const group of groups) {
    if (groupMatches(text, group)) score += 1
  }
  return score
}

const fetchResources = async (page = 1, retried = false) => {
  loading.value = true
  error.value = null
  try {
    const filtersActive = selectedLevels.value.length > 0 || Boolean(searchQuery.value.trim())
    const useServerPagination = !filtersActive
    const effectivePage = useServerPagination ? page : 1
    const effectivePageSize = useServerPagination ? itemsPerPage : 500

    const params = {
      type: props.resourceType,
      page: effectivePage,
      page_size: effectivePageSize
    }
    if (isExerciseMode.value) {
      params.group_by = 'notion'
    }
    if (selectedLevels.value.length > 0) {
      params.niveau_nom = selectedLevels.value.join(',')
    }
    if (searchQuery.value.trim()) {
      params.q = searchQuery.value.trim()
    }
    const data = await getFreeResources(params)
    const list = Array.isArray(data?.results) ? data.results : data
    const count = Number(data?.count) || 0
    const totalExercises = Number(data?.total_exercises || data?.totalExercises || 0)
    allResources.value = list || []
    // Ne pas écraser la liste complète des niveaux; elle est chargée séparément
    if (isExerciseMode.value) {
      totalExercisesCount.value = totalExercises || list?.reduce((acc, item) => acc + (Number(item?.count) || 1), 0) || 0
      totalChaptersCount.value = useServerPagination ? (count || (list ? list.length : 0)) : (list ? list.length : 0)
      totalCount.value = totalChaptersCount.value
      isServerPaginated.value = useServerPagination && count > 0
      resources.value = list || []
      currentPage.value = useServerPagination ? page : 1
      return
    } else {
      totalExercisesCount.value = 0
      totalChaptersCount.value = 0
      totalCount.value = useServerPagination ? count : (list ? list.length : 0)
    }
    isServerPaginated.value = useServerPagination && count > 0

    if (isServerPaginated.value) {
      resources.value = list || []
      currentPage.value = page
    } else {
      // Pas de pagination serveur: fallback client (filtre actif)
      currentPage.value = 1
      const start = 0
      resources.value = (list || []).slice(start, start + itemsPerPage)
    }
  } catch (err) {
    console.error('Erreur chargement ressources gratuites', err)
    if (!retried) {
      // Fallback: certains endpoints n'acceptent pas page/page_size -> tenter sans pagination serveur
      try {
        const fallbackParams = { type: props.resourceType }
        if (isExerciseMode.value) {
          fallbackParams.group_by = 'notion'
        }
        if (selectedLevels.value.length > 0) {
          fallbackParams.niveau_nom = selectedLevels.value.join(',')
        }
        if (searchQuery.value.trim()) {
          fallbackParams.q = searchQuery.value.trim()
        }
        const data = await getFreeResources(fallbackParams)
        const list = Array.isArray(data?.results) ? data.results : data
        allResources.value = list || []
        if (isExerciseMode.value) {
          totalExercisesCount.value = list?.reduce((acc, item) => acc + (Number(item?.count) || 1), 0) || 0
          totalChaptersCount.value = list ? list.length : 0
          totalCount.value = totalChaptersCount.value
          isServerPaginated.value = false
          currentPage.value = page
          const start = (page - 1) * itemsPerPage
          resources.value = (list || []).slice(start, start + itemsPerPage)
          return
        } else {
          totalCount.value = 0
          totalExercisesCount.value = 0
          totalChaptersCount.value = 0
          isServerPaginated.value = false
          currentPage.value = page
          const start = (page - 1) * itemsPerPage
          resources.value = (list || []).slice(start, start + itemsPerPage)
          return
        }
      } catch (fallbackErr) {
        console.error('Erreur fallback ressources gratuites', fallbackErr)
      }
    }
    error.value = err?.message || "Impossible de charger ces ressources gratuites."
  } finally {
    loading.value = false
    nextTick(() => {
      measureContentHeightForFreeResources()
      updateCtaMaxWidthToMatchGrid()
    })
    // Charger la liste complète des niveaux en arrière-plan si pas encore fait
    if (!levelOptionsLoaded.value) {
      fetchLevelOptions()
    }
  }
}

const fetchLevelOptions = async () => {
  try {
    const params = {
      type: props.resourceType,
      page: 1,
      page_size: 500
    }
    if (isExerciseMode.value) {
      params.group_by = 'notion'
    }
    const data = await getFreeResources(params)
    const list = Array.isArray(data?.results) ? data.results : data
    levelOptions.value = extractLevels(list)
    levelOptionsLoaded.value = true
  } catch (_) {
    // si erreur, on garde les options existantes
  }
}

onMounted(() => {
  detectMobileAndZoomSupport()
  updateViewportWidth()
  setupViewportListener()
  fetchResources(1)
  fetchLevelOptions()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  cleanupViewportListener()
  if (searchTimeoutId) {
    clearTimeout(searchTimeoutId)
  }
  document.removeEventListener('click', handleClickOutside)
})

watch(() => props.resourceType, () => {
  fetchResources(1)
  selectedLevels.value = []
  levelOptions.value = []
  levelOptionsLoaded.value = false
  currentPage.value = 1
  searchQuery.value = ''
  fetchLevelOptions()
})

watch(() => selectedLevels.value.length, () => {
  currentPage.value = 1
  fetchResources(1)
})

watch(() => searchQuery.value, () => {
  currentPage.value = 1
  if (searchTimeoutId) {
    clearTimeout(searchTimeoutId)
  }
  searchTimeoutId = setTimeout(() => {
    fetchResources(1)
  }, 250)
})

watch(viewportWidth, () => {
  nextTick(() => {
    measureContentHeightForFreeResources()
    updateCtaMaxWidthToMatchGrid()
  })
})

const handleClickOutside = (event) => {
  if (!showLevelFilter.value) return
  const dropdownEl = filterDropdownRef.value
  const buttonEl = filterButtonRef.value
  const target = event.target
  if (dropdownEl && dropdownEl.contains(target)) return
  if (buttonEl && buttonEl.contains(target)) return
  showLevelFilter.value = false
}

const availableLevels = computed(() => {
  if (levelOptions.value.length > 0) {
    return levelOptions.value
  }
  const baseList = hasServerPagination.value ? resources.value : allResources.value
  return extractLevels(baseList)
})

const hasServerPagination = computed(() => isServerPaginated.value && totalCount.value > 0)

const filteredResources = computed(() => {
  const baseList = hasServerPagination.value ? resources.value : allResources.value
  // Si pagination serveur active, on applique juste un tri pour mettre les gratuits devant
  if (hasServerPagination.value) {
    return sortByLockStatus(baseList)
  }

  let filtered = [...(baseList || [])]

  // Filter by level
  if (selectedLevels.value.length > 0) {
    filtered = filtered.filter((resource) => {
      const level = resource?.niveau_nom || resource?.tag_secondaire
      return level && selectedLevels.value.includes(level)
    })
  }

  // Filter by search query and mark if match is in content
  if (searchQuery.value.trim()) {
    const groups = queryTokenGroups(searchQuery.value)

    // RequÃªte trop gÃ©nÃ©rique (ex: "cours en ligne") -> ne pas filtrer
    if (groups.length === 0) {
      filtered.forEach((resource) => { resource._matchInContent = false })
      return sortByLockStatus(filtered)
    }

    const sortScored = (a, b) => {
      const aLocked = Boolean(a.resource?.is_locked)
      const bLocked = Boolean(b.resource?.is_locked)
      if (aLocked !== bLocked) return aLocked ? 1 : -1
      if (b.score !== a.score) return b.score - a.score
      if (b.titleScore !== a.titleScore) return b.titleScore - a.titleScore
      return String(a.resource?.titre || a.resource?.notion_nom || '').localeCompare(String(b.resource?.titre || b.resource?.notion_nom || ''))
    }

    const scored = filtered.map((resource) => {
      const titleText = normalizeText(`${resource?.titre || ''} ${resource?.notion_nom || ''}`)
      const metaText = normalizeText(`${resource?.matiere_nom || ''} ${resource?.niveau_nom || ''} ${resource?.pays_nom || ''} ${resource?.tag_secondaire || ''}`)
      const bodyText = normalizeText(`${resource?.accroche || ''} ${resource?.excerpt || ''} ${resource?.question || ''} ${stripHtml(resource?.contenu || '')}`)
      const fullText = `${titleText} ${metaText} ${bodyText}`.trim()

      const titleScore = groupsScore(titleText, groups)
      const bodyScore = groupsScore(`${metaText} ${bodyText}`.trim(), groups)
      const score = groupsScore(fullText, groups)

      resource._matchInContent = titleScore === 0 && bodyScore > 0

      return { resource, score, titleScore, bodyScore, fullText }
    })

    const strictMatches = scored.filter(({ fullText }) => groupsAllMatch(fullText, groups))
    if (strictMatches.length > 0) {
      return strictMatches
        .sort(sortScored)
        .map(({ resource }) => resource)
    }

    // Fallback (OR): afficher les meilleurs rÃ©sultats si aucun match strict
    return scored
      .filter(({ score }) => score > 0)
      .sort(sortScored)
      .map(({ resource }) => resource)
    /* filtered = filtered.filter((resource) => {
      // Chercher dans le titre
      const title = (resource?.titre || resource?.notion_nom || '').toLowerCase()
      
      // Chercher dans le contenu texte (champ principal du cours)
      const content = (resource?.contenu || '').toLowerCase()
      
      // Chercher dans les autres champs textuels
      const accroche = (resource?.accroche || '').toLowerCase()
      const excerpt = (resource?.excerpt || '').toLowerCase()
      const question = (resource?.question || '').toLowerCase()
      
      // Enlever les balises HTML du contenu pour une meilleure recherche
      const cleanContent = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ')
      
      const titleMatch = title.includes(query)
      const contentMatch = cleanContent.includes(query)
      const otherMatch = accroche.includes(query) || excerpt.includes(query) || question.includes(query)
      
      // Marquer si le match provient du contenu
      resource._matchInContent = !titleMatch && (contentMatch || otherMatch)
      
      return titleMatch || contentMatch || otherMatch
    }) */
  } else {
    // Réinitialiser le marqueur si pas de recherche
    filtered.forEach(resource => {
      resource._matchInContent = false
    })
  }

  return sortByLockStatus(filtered)
})

const toggleLevel = (level) => {
  const index = selectedLevels.value.indexOf(level)
  if (index > -1) {
    selectedLevels.value.splice(index, 1)
  } else {
    selectedLevels.value.push(level)
  }
}

const clearFilters = () => {
  selectedLevels.value = []
}

const flatList = computed(() => {
  if (!filteredResources.value.length) {
    return []
  }

  if (isExerciseMode.value) {
    const chaptersMap = new Map()
    filteredResources.value.filter(Boolean).forEach((item, index) => {
      const chapterKey = item.notion || item.notion_nom || `chapitre-${index}`
      const chapterName = item?.notion_nom || item?.titre || item?.nom || typeConfig.value.fallback || 'Chapitre'
      if (!chaptersMap.has(chapterKey)) {
        chaptersMap.set(chapterKey, {
          id: chapterKey,
          notionId: item.notion || chapterKey,
          name: chapterName,
          description: item?.notion_description || item?.accroche || item?.excerpt || '',
          exercises: [],
          displayTag: '',
          totalCount: 0
        })
      }
      const chapterEntry = chaptersMap.get(chapterKey)
      chapterEntry.exercises = chapterEntry.exercises || []
      chapterEntry.exercises.push(item)
      chapterEntry.totalCount = (chapterEntry.totalCount || 0) + (Number(item?.count) || 1)
      const tag = item.tag_secondaire || item.niveau_nom || item.matiere_nom || ''
      if (!chapterEntry.displayTag && tag) {
        chapterEntry.displayTag = tag
      }
    })
    return Array.from(chaptersMap.values())
      .map((chapter) => {
        const exercisesList = Array.isArray(chapter.exercises) ? chapter.exercises : []
        return {
          ...chapter,
          count: typeof chapter.totalCount === 'number' ? chapter.totalCount : exercisesList.length,
          isLocked: exercisesList.length > 0 && exercisesList.every((exercise) => Boolean(exercise.is_locked))
        }
      })
      .sort((a, b) => {
        if (a.isLocked !== b.isLocked) {
          return a.isLocked ? 1 : -1
        }
        return (a.name || '').localeCompare(b.name || '')
      })
  }

  const sorted = [...filteredResources.value].sort((a, b) => {
    const aLocked = Boolean(a.is_locked)
    const bLocked = Boolean(b.is_locked)
    if (aLocked === bLocked) return 0
    return aLocked ? 1 : -1
  })

  return sorted
})

const totalResourceCount = computed(() => {
  if (isExerciseMode.value) {
    // Pour les exercices, afficher "X exercices" et "Y chapitres" (chapitres globaux)
    const exercisesCount = totalExercisesCount.value || totalCount.value || filteredResources.value.length
    const chapterCount = totalChaptersCount.value || flatList.value.length
    return {
      count: exercisesCount,
      chapterCount
    }
  }
  const count = totalCount.value || filteredResources.value.length
  return {
    count,
    chapterCount: 0
  }
})

const totalPages = computed(() => {
  if (hasServerPagination.value) {
    const totalForPagination = isExerciseMode.value
      ? (totalChaptersCount.value || flatList.value.length)
      : (totalCount.value || filteredResources.value.length)
    return Math.max(1, Math.ceil(totalForPagination / itemsPerPage))
  }
  const listLength = isExerciseMode.value ? flatList.value.length : filteredResources.value.length
  return Math.max(1, Math.ceil(listLength / itemsPerPage))
})

const paginatedList = computed(() => {
  const sourceList = isExerciseMode.value ? flatList.value : filteredResources.value
  if (hasServerPagination.value) {
    return sourceList
  }
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return sourceList.slice(start, end)
})

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  if (hasServerPagination.value) {
    fetchResources(page).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    })
  } else {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const formatCount = (count, overrideLabel) => {
  const label = overrideLabel || typeConfig.value.counterLabel || 'ressource'
  return `${count} ${label}${count > 1 ? 's' : ''}`
}

const getExerciseCount = (chapter) => {
  if (!chapter) return 0
  if (typeof chapter.count === 'number') return chapter.count
  return Array.isArray(chapter.exercises) ? chapter.exercises.length : 0
}

const openResource = (resource) => {
  if (!resource) return
  if (resource.is_locked) {
    onLockedResource(resource)
    return
  }
  if (!resource.slug) return
  router.push({ name: typeConfig.value.slugRoute, params: { slug: resource.slug } })
}

const openExerciseChapter = (chapter) => {
  if (!chapter) return
  if (chapter.isLocked) {
    onLockedExercise(chapter)
    return
  }
  const notionId = chapter?.notionId || chapter?.id
  if (!notionId) return
  router.push({
    name: 'FreeExerciseChapter',
    params: { notionId },
    query: { title: chapter?.name || undefined }
  })
}

const premiumRoutes = {
  course: 'CourseByNotion',
  exercise: 'ExercicesByNotion',
  summary: 'SynthesisByNotion'
}

const subscriptionCtaLabel = computed(() => (subscriptionStore.hasAccess ? 'Gérer mon abonnement' : "S'abonner"))

const onSubscriptionCtaClick = () => {
  if (!userStore.isAuthenticated) {
    openModal(MODAL_IDS.REGISTER)
    return
  }

  if (subscriptionStore.hasAccess) {
    router.push({ name: 'Subscription' })
    return
  }

  router.push({
    name: 'Billing',
    query: {
      redirect: route.fullPath,
      reason: 'free_resources_cta'
    }
  })
}

const handleLockedAccess = ({ resourceType, notionId }) => {
  if (subscriptionStore.hasAccess && notionId && premiumRoutes[resourceType]) {
    router.push({ name: premiumRoutes[resourceType], params: { notionId } })
    return
  }

  if (!userStore.isAuthenticated) {
    openModal(MODAL_IDS.REGISTER)
    return
  }

  router.push({
    name: 'Billing',
    query: {
      redirect: route.fullPath,
      reason: `${resourceType}_premium`
    }
  })
}

const onLockedResource = (resource) => {
  if (!resource?.notion) {
    handleLockedAccess({ resourceType: props.resourceType, notionId: null })
    return
  }
  handleLockedAccess({ resourceType: props.resourceType, notionId: resource.notion })
}

const onLockedExercise = (chapter) => {
  handleLockedAccess({ resourceType: 'exercise', notionId: chapter?.notionId })
}
</script>

<template>
  <MainLayout>
    <div class="free-course-page">
      <div class="header-row">
        <BackButton text="Retour à l'accueil" :custom-action="() => router.push({ name: 'Home' })" position="top-left" />
        <div v-if="!loading && totalResourceCount.count > 0" class="resource-count-badge">
          <template v-if="isExerciseMode && totalResourceCount.chapterCount > 0">
            {{ totalResourceCount.count }} {{ typeConfig.counterLabel }}{{ totalResourceCount.count > 1 ? 's' : '' }}
            <span class="badge-separator">+</span>
            {{ totalResourceCount.chapterCount }} chapitre{{ totalResourceCount.chapterCount > 1 ? 's' : '' }}
          </template>
          <template v-else>
            {{ totalResourceCount.count }} {{ typeConfig.counterLabel }}{{ totalResourceCount.count > 1 ? 's' : '' }}
          </template>
        </div>
      </div>

      <header class="page-intro" aria-labelledby="free-resource-title">
        <h1 id="free-resource-title" class="page-title">{{ pageIntro.title }}</h1>
        <p class="page-subtitle">{{ pageIntro.subtitle }}</p>
      </header>

      <section class="free-resource-cta" :style="ctaWidthStyle" aria-label="Accès professeur ou plateforme">
        <div class="free-resource-cta__copy">
          <p class="free-resource-cta__title">Besoin d’un professeur ou d’un accès complet&nbsp;?</p>
          <p class="free-resource-cta__subtitle">Cours particuliers de maths en ligne • Abonnement plateforme OptiTAB</p>
        </div>
        <div class="free-resource-cta__actions">
          <router-link
            :to="{ name: 'CoursParticuliers' }"
            class="free-resource-cta__btn free-resource-cta__btn--primary"
            data-track="nav"
            data-nav-name="tutoring"
            data-nav-location="free_resources_banner"
          >
            Cours particuliers
          </router-link>
          <button
            type="button"
            class="free-resource-cta__btn free-resource-cta__btn--secondary"
            data-cta-name="subscribe"
            data-cta-location="free_resources_banner"
            @click="onSubscriptionCtaClick"
          >
            {{ subscriptionCtaLabel }}
          </button>
        </div>
      </section>

      <div v-if="availableLevels.length > 0" class="filter-section" :style="ctaWidthStyle">
        <div class="filter-bar">
          <div class="filter-toggle-wrapper">
            <button class="filter-toggle" ref="filterButtonRef" @click="showLevelFilter = !showLevelFilter">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="filter-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
              </svg>
              Filtrer par niveau
              <span v-if="selectedLevels.length > 0" class="filter-badge">{{ selectedLevels.length }}</span>
            </button>

            <div v-if="showLevelFilter" class="filter-dropdown" ref="filterDropdownRef">
              <div class="filter-header">
                <span class="filter-title">Niveaux</span>
                <button v-if="selectedLevels.length > 0" class="clear-btn" @click="clearFilters">Effacer</button>
              </div>
              <div class="filter-options">
                <label
                  v-for="level in availableLevels"
                  :key="level"
                  class="filter-option"
                >
                  <input
                    type="checkbox"
                    :checked="selectedLevels.includes(level)"
                    @change="toggleLevel(level)"
                  />
                  <span class="filter-label">{{ level }}</span>
                </label>
              </div>
            </div>
          </div>

          <div class="search-box">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="search-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher un chapitre ou une méthode..."
              class="search-input"
            />
            <button
              v-if="searchQuery"
              class="clear-search-btn"
              @click="searchQuery = ''"
              aria-label="Effacer la recherche"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="clear-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="state-card">
        <div class="state-card__spinner" aria-hidden="true"></div>
        <p>Chargement des ressources gratuites...</p>
      </div>
      <div v-else-if="error" class="state-card">
        <p>{{ error }}</p>
        <button @click="fetchResources">Réessayer</button>
      </div>
      <div v-else-if="flatList.length === 0" class="state-card">
        {{ typeConfig.emptyLabel }}
      </div>
      <template v-else>
        <div class="content-wrapper" :style="zoomStyle" ref="contentRef">
          <div class="notion-grid" ref="notionGridRef">
          <template v-if="isExerciseMode">
            <NotionCard
              v-for="chapter in paginatedList"
              :key="chapter.id"
              :title="chapter.name || typeConfig.fallback || 'Chapitre'"
              description="Cliquez pour explorer les exercices"
              :notion-id="chapter.notionId"
              :to="
                chapter.isLocked
                  ? null
                  : {
                      name: 'FreeExerciseChapter',
                      params: { notionId: chapter?.notionId || chapter?.id },
                      query: { title: chapter?.name || undefined }
                    }
              "
              :disable-prefetch="true"
              :locked="Boolean(chapter.isLocked)"
              @locked-click="() => onLockedExercise(chapter)"
            >
              <template #meta>
                <span
                  v-if="chapter.isLocked"
                  class="resource-locked-pill"
                >
                  Premium
                </span>
                <span class="resource-chapter-pill">
                  {{ formatCount(getExerciseCount(chapter), 'exercice') }}
                </span>
                <span
                  v-if="chapter.displayTag"
                  class="resource-tag-pill"
                >
                  {{ chapter.displayTag }}
                </span>
              </template>
            </NotionCard>
          </template>

          <template v-else>
            <NotionCard
              v-for="resource in paginatedList"
              :key="resource.slug"
              :title="getCardTitle(resource)"
              :description="getCardDescription(resource)"
              :notion-id="resource.notion"
              :to="
                resource.is_locked || !resource.slug
                  ? null
                  : { name: typeConfig.slugRoute, params: { slug: resource.slug } }
              "
              :disable-prefetch="true"
              :locked="Boolean(resource.is_locked)"
              @locked-click="() => onLockedResource(resource)"
            >
              <template v-if="isSummaryMode" #meta>
                <span
                  v-if="resource._matchInContent"
                  class="resource-match-pill"
                >
                  🔍 Trouvé dans le contenu
                </span>
                <span
                  v-if="resource.is_locked"
                  class="resource-locked-pill"
                >
                  Premium
                </span>
                <span
                  v-if="getSummaryLevel(resource)"
                  class="resource-chapter-pill"
                >
                  {{ getSummaryLevel(resource) }}
                </span>
              </template>
              <template v-else #meta>
                <span
                  v-if="resource._matchInContent"
                  class="resource-match-pill"
                >
                  🔍 Trouvé dans le contenu
                </span>
                <span
                  v-if="resource.is_locked"
                  class="resource-locked-pill"
                >
                  Premium
                </span>
                <span v-if="resource.tag_secondaire" class="resource-tag-pill">
                  {{ resource.tag_secondaire }}
                </span>
              </template>
            </NotionCard>
          </template>
        </div>

        <div v-if="totalPages > 1" class="pagination">
          <button
            class="pagination-btn"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="pagination-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
          </button>
          
          <div class="pagination-info">
            <span class="pagination-text">Page {{ currentPage }} sur {{ totalPages }}</span>
          </div>
          
          <button
            class="pagination-btn"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="pagination-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
        </div>
      </template>
    </div>

    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur OptiTAB !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
  </MainLayout>
</template>

<style scoped>
.free-course-page {
  min-height: 100vh;
  background: #ffffff;
  padding: 140px 32px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-wrapper {
  transform-origin: top left;
  transition: transform 0.2s ease, zoom 0.2s ease;
  overflow: visible;
  /* Les styles (zoom ou transform) seront appliqués dynamiquement via JS selon le support du zoom */
}

/* Sur mobile, assurer que le conteneur ne crée pas de problèmes de scroll */
@media (max-width: 768px) {
  .content-wrapper {
    min-height: auto;
    overflow: visible;
  }
}

.header-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.page-intro {
  margin: 0 0 18px 0;
  max-width: 980px;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.page-subtitle {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #475569;
  line-height: 1.6;
}

.free-resource-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border-radius: 18px;
  border: 1px solid rgba(59, 130, 246, 0.25);
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.10), rgba(99, 102, 241, 0.07));
  margin: 0 0 22px 0;
}

.free-resource-cta__copy {
  min-width: 0;
}

.free-resource-cta__title {
  margin: 0;
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.free-resource-cta__subtitle {
  margin: 4px 0 0 0;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  line-height: 1.45;
}

.free-resource-cta__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
  white-space: nowrap;
}

.free-resource-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  min-height: 40px;
  padding: 10px 18px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 13px;
  letter-spacing: -0.01em;
  border: 1px solid transparent;
  text-decoration: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  user-select: none;
  transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.free-resource-cta__btn--primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 55%, #1d4ed8 100%);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.18);
  box-shadow: 0 14px 32px rgba(59, 130, 246, 0.24);
}

.free-resource-cta__btn--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 18px 38px rgba(59, 130, 246, 0.3);
}

.free-resource-cta__btn--primary::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0) 52%);
  transform: translateX(-70%);
  transition: transform 0.55s ease;
}

.free-resource-cta__btn--primary:hover::after {
  transform: translateX(-15%);
}

.free-resource-cta__btn--secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #2563eb;
  border-color: rgba(59, 130, 246, 0.25);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.free-resource-cta__btn--secondary:hover {
  transform: translateY(-1px);
  background: rgba(59, 130, 246, 0.08);
  border-color: rgba(59, 130, 246, 0.32);
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.08);
}

.free-resource-cta__btn:active {
  transform: translateY(0);
}

.free-resource-cta__btn:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}

.resource-count-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background: #eef2ff;
  color: #3730a3;
  font-size: 14px;
  font-weight: 700;
  border-radius: 999px;
  border: 1px solid rgba(59, 130, 246, 0.3);
  white-space: nowrap;
}

.badge-separator {
  margin: 0 8px;
  color: #6366f1;
  font-weight: 600;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 22px;
  }

  .page-subtitle {
    font-size: 14px;
  }
}

@media (max-width: 640px) {
  .free-resource-cta {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    width: 100%;
  }

  .free-resource-cta__actions {
    justify-content: stretch;
  }

  .free-resource-cta__btn {
    width: 100%;
  }
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 48px;
  padding: 20px 0;
}

.pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #3b82f6;
  color: #3b82f6;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-icon {
  width: 20px;
  height: 20px;
}

.pagination-info {
  padding: 0 12px;
}

.pagination-text {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.filter-section {
  position: relative;
  margin: 0 0 24px 0;
}

.filter-bar {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
}

.filter-toggle-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.search-box {
  position: relative;
  width: 100%;
  min-width: 0;
  max-width: none;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 44px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  background: #fff;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.search-input::placeholder {
  color: #94a3b8;
}

.clear-search-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.clear-icon {
  width: 16px;
  height: 16px;
}

.filter-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #475569;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.filter-toggle:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.filter-icon {
  width: 18px;
  height: 18px;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #3b82f6;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  border-radius: 999px;
  margin-left: 4px;
}

.filter-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 240px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
  z-index: 100;
  padding: 12px;
}

.filter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 10px;
}

.filter-title {
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.clear-btn {
  padding: 4px 10px;
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.filter-option:hover {
  background: #f8fafc;
}

.filter-option input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #3b82f6;
}

.filter-label {
  flex: 1;
  font-size: 14px;
  color: #334155;
  font-weight: 500;
}

.notion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 320px));
  gap: 16px;
  justify-content: flex-start;
  justify-items: start;
}

.state-card {
  margin-top: 30px;
  padding: 32px;
  border-radius: 18px;
  border: 1px dashed #cbd5f5;
  text-align: center;
  color: #475569;
}

.state-card__spinner {
  width: 42px;
  height: 42px;
  margin: 0 auto 14px;
  border-radius: 999px;
  border: 4px solid #e0e7ff;
  border-top-color: #2563eb;
  animation: spin 0.9s linear infinite;
}

.state-card button {
  margin-top: 12px;
  padding: 10px 18px;
  border-radius: 12px;
  border: none;
  background: #1d4ed8;
  color: #fff;
  cursor: pointer;
}

.resource-chapter-pill,
.resource-status-pill,
.resource-tag-pill,
.resource-locked-pill,
.resource-match-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.resource-chapter-pill {
  background: #eef2ff;
  color: #3730a3;
  border-color: rgba(59, 130, 246, 0.3);
}

.resource-status-pill {
  background: #e0f2fe;
  color: #0c4a6e;
  border-color: rgba(14, 165, 233, 0.4);
}

.resource-tag-pill {
  background: #dcfce7;
  color: #14532d;
  border-color: rgba(34, 197, 94, 0.35);
}

.resource-locked-pill {
  background: #eef2ff;
  color: #1d4ed8;
  border-color: rgba(99, 102, 241, 0.35);
  text-transform: uppercase;
  font-size: 11px;
}

.resource-match-pill {
  background: #fef3c7;
  color: #92400e;
  border-color: rgba(251, 191, 36, 0.4);
  font-size: 11px;
}

@media (max-width: 768px) {
  .free-course-page {
    padding: 120px 16px 60px;
  }

  .notion-grid {
    grid-template-columns: 1fr;
    justify-content: stretch;
  }
}

@media (max-width: 640px) {
  .free-course-page {
    padding: 110px 14px 56px;
  }

  .header-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 20px;
  }

  .resource-count-badge {
    font-size: 13px;
    padding: 6px 14px;
  }

  .free-resource-cta {
    width: 100%;
    max-width: 100%;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
    width: 100%;
  }

  .search-box {
    max-width: 100%;
    min-width: 100%;
    width: 100%;
  }

  .filter-toggle {
    width: 100%;
  }

  .filter-section {
    width: 100%;
  }

  .notion-grid {
    gap: 12px;
  }

  .pagination {
    margin-top: 32px;
    gap: 12px;
  }

  .pagination-btn {
    width: 36px;
    height: 36px;
  }

  .pagination-icon {
    width: 18px;
    height: 18px;
  }

  .pagination-text {
    font-size: 13px;
  }
}

@media (max-width: 420px) {
  .free-course-page {
    padding: 105px 12px 48px;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
