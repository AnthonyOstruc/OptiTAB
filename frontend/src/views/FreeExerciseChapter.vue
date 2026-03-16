<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getFreeResources } from '@/api/free-content'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'
import { renderMath } from '@/utils/scientificRenderer'
import {
  setPageSeo,
  getRobotsForRoute,
  buildBreadcrumbJsonLd,
  buildCreativeWorkJsonLd
} from '@/services/seo'
import { buildExerciseChapterRouteParams, slugifyText } from '@/utils/freeExerciseSlug'
import { FREE_RESOURCES_AUTHORITY_CONTENT, isKnownBrokenPopularLink } from '@/config/freeResourcesAuthority'
import { useZoom } from '@/composables/useZoom'
import {
  buildDynamicSeo,
  buildCanonicalSeoFields,
  DYNAMIC_SEO_PAGE_TYPES,
  normalizePathname,
  stripHtmlForSeo
} from '@/composables/useDynamicSeo'
import { getManualSeoOverrideByPath } from '@/config/manualSeoOverrides'

const props = defineProps({
  notionIdOverride: {
    type: [String, Number],
    default: null
  },
  notionTitleOverride: {
    type: String,
    default: ''
  }
})

const route = useRoute()
const router = useRouter()
const { openModal } = useModalManager()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()

const loading = ref(false)
const error = ref(null)
const exercises = ref([])
const notionTitle = ref(props.notionTitleOverride || route.query.title || '')
const currentPage = ref(1)
const itemsPerPage = 5

const contentRef = ref(null)

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

function measureContentHeightForFreeExercises() {
  measureContentHeight(contentRef)
}

const notionId = computed(() => props.notionIdOverride || route.params.notionId)

const formatCount = (count) => `${count} exercice${count > 1 ? 's' : ''}`

const formatNiveauLabel = (value) => {
  if (!value) return ''
  const normalized = String(value).trim().toLowerCase()
  if (normalized.includes('terminale') || normalized === 'terminal') {
    return 'Terminale - Bac'
  }
  if (normalized.includes('première') || normalized.includes('premiere')) {
    return 'Première - 1er'
  }
  return value
}

const formatNiveauGroupLabel = (value) => {
  if (!value) return ''
  const normalized = String(value).trim().toLowerCase()
  if (normalized.includes('lycee')) return 'Lycee'
  if (normalized.includes('college')) return 'College'
  if (normalized.includes('prepa')) return 'Prepa'
  return ''
}

const formatMatiereLabel = (value) => {
  if (!value) return ''
  const normalized = String(value).trim().toLowerCase()
  if (normalized.includes('math')) return 'Maths'
  return value
}

function pickChapterSeoSourceText(source) {
  return stripHtmlForSeo(
    source?.accroche ||
    source?.excerpt ||
    source?.question ||
    source?.contenu ||
    source?.contenu_html ||
    ''
  )
}

function getSiteUrl() {
  const fromEnv = String(import.meta?.env?.VITE_SITE_URL || '').trim()
  if (fromEnv) return fromEnv.replace(/\/+$/, '')
  if (typeof window !== 'undefined' && window.location?.origin) return window.location.origin
  return 'https://www.optitab.net'
}

function toAbsoluteUrl(maybeUrlOrPath) {
  const raw = String(maybeUrlOrPath || '').trim()
  if (!raw) return ''
  if (/^https?:\/\//i.test(raw)) return raw
  const base = getSiteUrl()
  return `${base}${raw.startsWith('/') ? '' : '/'}${raw}`
}

function buildCanonicalPath(source) {
  const canonicalParams = buildExerciseChapterRouteParams({
    paysNom: source?.pays_nom,
    matiereNom: source?.matiere_nom,
    niveauNom: source?.niveau_nom,
    niveauGroup: source?.niveau_nom,
    name: source?.notion_nom || source?.name || source?.titre,
    id: source?.notion || source?.id || notionId.value
  })
  if (!canonicalParams?.slug || !canonicalParams?.id) return route.path
  if (canonicalParams.niveauGroup) {
    return `/ressources-gratuites/exercices/${canonicalParams.pays}/${canonicalParams.niveauGroup}/${canonicalParams.matiere}/${canonicalParams.slug}-${canonicalParams.id}`
  }
  return `/ressources-gratuites/exercices/${canonicalParams.pays}/${canonicalParams.matiere}/${canonicalParams.slug}-${canonicalParams.id}`
}

function isCanonicalRoutePath(currentPath, canonicalPath) {
  return normalizePathname(currentPath) === normalizePathname(canonicalPath)
}

function pickSeoImage(list) {
  const first = Array.isArray(list) ? list[0] : null
  const cover = first?.cover_image || first?.image
  if (cover) return cover
  const images = Array.isArray(first?.images) ? first.images : []
  return images[0]?.image || ''
}

const chapterMetaLabel = computed(() => {
  const source = exercises.value.find((item) => item?.pays_nom || item?.niveau_nom || item?.matiere_nom)
  if (!source) return ''
  const pays = source.pays_nom || ''
  const matiere = formatMatiereLabel(source.matiere_nom || '')
  const niveau = formatNiveauLabel(source.niveau_nom || '')
  const groupLabel = formatNiveauGroupLabel(route.params?.niveauGroup || '')
  const niveauLabel = groupLabel && niveau ? `${groupLabel} ${niveau}` : (niveau || groupLabel)
  const parts = [pays, matiere, niveauLabel].filter(Boolean)
  return parts.join(' / ')
})


const displayedExercises = computed(() =>
  exercises.value.map((item, index) => ({
    id: item.id || item.slug || index,
    slug: item.slug,
    titre: item.titre || item.nom || `Exercice ${index + 1}`,
    instruction: item.question || item.contenu || item.accroche || '',
    solution: item.solution || item.reponse_correcte || '',
    etapes: item.etapes || '',
    difficulty: item.difficulty || item.difficulte || 'medium',
    previewImages: item.images || [],
    badge: item.badge,
    tag: item.tag_secondaire,
    _locked: Boolean(item.is_locked)
  }))
)

const exercisesCount = computed(() => displayedExercises.value.length)

const breadcrumbItems = computed(() => [
  { label: 'Accueil', to: '/' },
  { label: 'Exercices gratuits', to: '/ressources-gratuites/exercices' },
  { label: notionTitle.value || 'Chapitre' }
])

const RELATED_LINK_BASE_PATHS = Object.freeze({
  course: '/ressources-gratuites/cours',
  summary: '/ressources-gratuites/syntheses',
  exercise: '/ressources-gratuites/exercices'
})

const RELATED_LINK_STOPWORDS = new Set([
  'cours',
  'course',
  'exercice',
  'exercices',
  'corrige',
  'corriges',
  'corrigees',
  'fiche',
  'fiches',
  'synthese',
  'resume',
  'gratuite',
  'gratuites',
  'math',
  'maths',
  'mathematiques',
  'de',
  'des',
  'du',
  'la',
  'le',
  'les',
  'et',
  'en',
  'pour',
  'sur'
])

function stripTopicPrefix(value) {
  return String(value || '')
    .trim()
    .replace(/^r[eé]sum[eé]\s*:\s*/i, '')
    .replace(/^cours\s*:\s*/i, '')
    .replace(/^exercices?\s+corrig[eé]s?\s*:\s*/i, '')
    .replace(/^exercice\s*:\s*/i, '')
    .trim()
}

function stripQueryFromPath(value) {
  return String(value || '').split('#')[0].split('?')[0]
}

function tokenizeForRelatedMatch(value) {
  return slugifyText(value || '')
    .split('-')
    .filter((token) => token && token.length > 2 && !RELATED_LINK_STOPWORDS.has(token))
}

function scoreAuthorityLinkMatch(link, topicTokens, levelTokens) {
  const searchableText = slugifyText(`${link?.label || ''} ${link?.href || ''}`)
  if (!searchableText) return 0
  let score = 0
  for (const token of topicTokens) {
    if (searchableText.includes(token)) score += 6
  }
  for (const token of levelTokens) {
    if (searchableText.includes(token)) score += 3
  }
  return score
}

function pickAuthorityLinks({ preferredTypes, topicTokens, levelTokens, excludedPaths, limit } = {}) {
  const rows = []

  ;(preferredTypes || []).forEach((type, typeIndex) => {
    const popularLinks = Array.isArray(FREE_RESOURCES_AUTHORITY_CONTENT?.[type]?.popularLinks)
      ? FREE_RESOURCES_AUTHORITY_CONTENT[type].popularLinks
      : []

    popularLinks.forEach((link, itemIndex) => {
      const href = String(link?.href || '').trim()
      const label = String(link?.label || '').trim()
      const normalizedPath = normalizePathname(stripQueryFromPath(href))
      if (!href || !label || !normalizedPath) return
      if (isKnownBrokenPopularLink(href)) return
      if (excludedPaths?.has(normalizedPath)) return

      rows.push({
        href,
        label,
        normalizedPath,
        typeIndex,
        itemIndex,
        score: scoreAuthorityLinkMatch(link, topicTokens || [], levelTokens || [])
      })
    })
  })

  rows.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score
    if (a.typeIndex !== b.typeIndex) return a.typeIndex - b.typeIndex
    return a.itemIndex - b.itemIndex
  })

  const picked = []
  const used = new Set()
  for (const row of rows) {
    if (picked.length >= (limit || 5)) break
    if (used.has(row.normalizedPath)) continue
    used.add(row.normalizedPath)
    picked.push({ label: row.label, href: row.href })
  }

  return picked
}

function hashSeed(value) {
  const text = String(value || '')
  let hash = 2166136261
  for (let i = 0; i < text.length; i += 1) {
    hash ^= text.charCodeAt(i)
    hash = Math.imul(hash, 16777619)
  }
  return hash >>> 0
}

function createSeededRandom(seed) {
  let state = (seed >>> 0) || 1
  return () => {
    state = Math.imul(state, 1664525) + 1013904223
    return ((state >>> 0) / 4294967296)
  }
}

function shuffleLinksStable(items, seedSource) {
  const list = Array.isArray(items) ? [...items] : []
  if (list.length <= 1) return list
  const random = createSeededRandom(hashSeed(seedSource))
  for (let i = list.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1))
    ;[list[i], list[j]] = [list[j], list[i]]
  }
  return list
}

const relatedTopic = computed(() => {
  const raw = notionTitle.value || exercises.value[0]?.notion_nom || ''
  return stripTopicPrefix(raw)
})

const relatedLevel = computed(() => String(exercises.value[0]?.niveau_nom || '').trim())

const relatedLinksIntro = computed(() => {
  const topic = relatedTopic.value
  return topic
    ? `Pour progresser sur ${topic}, voici des cours, fiches et exercices proches.`
    : 'Voici des liens utiles vers des cours, fiches et exercices proches.'
})

const relatedLinks = computed(() => {
  const links = []
  const usedPaths = new Set()
  const currentPath = normalizePathname(route.path)

  const addLink = (label, to) => {
    const safeLabel = String(label || '').trim()
    const safeTo = String(to || '').trim()
    if (!safeLabel || !safeTo) return
    const normalizedPath = normalizePathname(stripQueryFromPath(safeTo))
    if (!normalizedPath || normalizedPath === currentPath || usedPaths.has(normalizedPath)) return
    usedPaths.add(normalizedPath)
    links.push({ label: safeLabel, to: safeTo })
  }

  const topic = relatedTopic.value
  const level = relatedLevel.value
  const topicTokens = tokenizeForRelatedMatch(topic)
  const levelTokens = tokenizeForRelatedMatch(level)

  pickAuthorityLinks({
    preferredTypes: ['summary'],
    topicTokens,
    levelTokens,
    excludedPaths: usedPaths,
    limit: 1
  }).forEach((link) => addLink(link.label, link.href))

  pickAuthorityLinks({
    preferredTypes: ['course'],
    topicTokens,
    levelTokens,
    excludedPaths: usedPaths,
    limit: 1
  }).forEach((link) => addLink(link.label, link.href))

  pickAuthorityLinks({
    preferredTypes: ['exercise'],
    topicTokens,
    levelTokens,
    excludedPaths: usedPaths,
    limit: 1
  }).forEach((link) => addLink(link.label, link.href))

  const authorityLinks = pickAuthorityLinks({
    preferredTypes: ['course', 'summary', 'exercise'],
    topicTokens,
    levelTokens,
    excludedPaths: usedPaths,
    limit: 7
  })
  authorityLinks.forEach((link) => addLink(link.label, link.href))

  if (links.length < 4) {
    const fallbackAuthorityLinks = pickAuthorityLinks({
      preferredTypes: ['summary', 'course', 'exercise'],
      topicTokens: [],
      levelTokens: [],
      excludedPaths: usedPaths,
      limit: 8
    })
    fallbackAuthorityLinks.forEach((link) => addLink(link.label, link.href))
  }

  if (links.length < 4) {
    addLink('Tous les cours gratuits', RELATED_LINK_BASE_PATHS.course)
    addLink('Toutes les fiches de synthèse', RELATED_LINK_BASE_PATHS.summary)
    addLink('Tous les exercices corrigés', RELATED_LINK_BASE_PATHS.exercise)
  }

  const seedSource = `${notionId.value || ''}|${route.path}|${topic}|${level}`
  return shuffleLinksStable(links, seedSource).slice(0, 8)
})

const orderedExercises = computed(() => {
  const unlocked = displayedExercises.value.filter((ex) => !ex._locked)
  const locked = displayedExercises.value.filter((ex) => ex._locked)
  return [...unlocked, ...locked]
})

const freeExercises = computed(() => orderedExercises.value.filter((ex) => !ex._locked))
const lockedExercises = computed(() => orderedExercises.value.filter((ex) => ex._locked))
const freeExercisesCount = computed(() => freeExercises.value.length)
const lockedExercisesCount = computed(() => lockedExercises.value.length)

const exercisesCountLabel = computed(() => {
  const freeCount = freeExercisesCount.value
  const lockedCount = lockedExercisesCount.value
  const parts = []

  if (freeCount) {
    parts.push(`${freeCount} exercice${freeCount > 1 ? 's' : ''} gratuit${freeCount > 1 ? 's' : ''}`)
  }

  if (lockedCount) {
    parts.push(`${lockedCount} exercice${lockedCount > 1 ? 's' : ''} premium`)
  }

  return parts.join(' • ')
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil((lockedExercises.value.length || 0) / itemsPerPage))
)

const paginatedLockedExercises = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return lockedExercises.value.slice(start, start + itemsPerPage)
})

const fetchExercises = async () => {
  if (!notionId.value) return
  loading.value = true
  error.value = null
  try {
    const data = await getFreeResources({
      type: 'exercise',
      notion: notionId.value,
      page_size: 500,
      include_images: 1
    })
    const list = Array.isArray(data?.results) ? data.results : data
    exercises.value = list
    currentPage.value = 1
    if (!notionTitle.value && list?.length && list[0]?.notion_nom) {
      notionTitle.value = list[0].notion_nom
    }
    if (list?.length) {
      syncCanonicalRoute(list[0])
    }
    await nextTick()
    await safeRenderMath()
    updateSeo()
  } catch (err) {
    console.error('Erreur chargement exercices gratuits', err)
    error.value = err?.message || "Impossible de charger les exercices gratuits pour ce chapitre."
  } finally {
    loading.value = false
  }
}

const safeRenderMath = async () => {
  try {
    await renderMath()
  } catch (_) {
    // ignore math errors
  }
}

const routeMatches = (params, canonical, hasGroup) => {
  if (!params || !canonical) return false
  if (String(params.pays || '') !== String(canonical.pays || '')) return false
  if (String(params.matiere || '') !== String(canonical.matiere || '')) return false
  if (String(params.slug || '') !== String(canonical.slug || '')) return false
  if (String(params.id || '') !== String(canonical.id || '')) return false
  if (hasGroup && String(params.niveauGroup || '') !== String(canonical.niveauGroup || '')) return false
  return true
}

const syncCanonicalRoute = (source) => {
  if (!source) return
  const canonicalParams = buildExerciseChapterRouteParams({
    paysNom: source?.pays_nom,
    matiereNom: source?.matiere_nom,
    niveauNom: source?.niveau_nom,
    niveauGroup: source?.niveau_nom,
    name: source?.notion_nom || source?.name || source?.titre,
    id: source?.notion || source?.id
  })
  if (!canonicalParams?.slug || !canonicalParams?.id) return
  const hasGroup = Boolean(canonicalParams.niveauGroup)
  const routeName = hasGroup ? 'FreeExerciseChapterSlugGrouped' : 'FreeExerciseChapterSlug'
  const routeParams = hasGroup
    ? canonicalParams
    : {
        pays: canonicalParams.pays,
        matiere: canonicalParams.matiere,
        slug: canonicalParams.slug,
        id: canonicalParams.id
      }
  const currentParams = route.params || {}
  if (route.name !== routeName || !routeMatches(currentParams, routeParams, hasGroup)) {
    router.replace({ name: routeName, params: routeParams, query: route.query, hash: route.hash }).catch(() => {})
  }
}

const updateSeo = () => {
  if (!notionTitle.value && exercises.value.length === 0) return
  const first = exercises.value[0] || {}
  const niveau = formatNiveauLabel(first.niveau_nom || '')
  const chapterTitle = notionTitle.value || first.notion_nom || 'Chapitre'
  const seoPayload = buildDynamicSeo({
    pageType: DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER,
    topic: chapterTitle,
    level: niveau,
    sourceText: pickChapterSeoSourceText(first)
  })
  const title = seoPayload.title
  const description = seoPayload.description
  const image = pickSeoImage(exercises.value) || undefined
  const canonicalResourcePath = buildCanonicalPath(first)
  const manualSeoOverride = getManualSeoOverrideByPath(canonicalResourcePath)
  const finalTitle = manualSeoOverride?.title || title
  const finalDescription = manualSeoOverride?.description || description
  const canonicalResourceUrl = toAbsoluteUrl(canonicalResourcePath)
  const isCanonicalRoute = isCanonicalRoutePath(route.path, canonicalResourcePath)
  const canonicalSeo = buildCanonicalSeoFields({
    routePath: route.path,
    canonicalPath: canonicalResourcePath,
    isCanonicalRoute,
    robotsWhenCanonical: getRobotsForRoute({ route })
  })
  const itemListElements = freeExercises.value
    .slice(0, 50)
    .map((exercise, index) => {
      const anchorId = getExerciseAnchorId(exercise, index)
      const url = anchorId ? `${canonicalResourceUrl}#${anchorId}` : canonicalResourceUrl
      return { '@type': 'ListItem', position: index + 1, name: exercise.titre, url }
    })
  const siteUrl = getSiteUrl()
  const organizationId = `${siteUrl}/#organization`
  const websiteId = `${siteUrl}/#website`
  const webPageId = `${canonicalResourceUrl}#webpage`
  const breadcrumbGraph = buildBreadcrumbJsonLd([
    { name: 'Accueil', item: '/' },
    { name: 'Exercices gratuits', item: '/ressources-gratuites/exercices' },
    { name: chapterTitle, item: canonicalResourceUrl }
  ])
  const chapterGraph = buildCreativeWorkJsonLd({
    id: `${canonicalResourceUrl}#creativework`,
    name: chapterTitle,
    description: finalDescription,
    url: canonicalResourceUrl,
    inLanguage: 'fr-FR',
    author: { '@id': organizationId },
    publisher: { '@id': organizationId },
    isPartOf: { '@id': websiteId },
    mainEntityOfPage: { '@id': webPageId },
    image: image || undefined,
    educationalLevel: niveau || undefined,
    learningResourceType: 'Exercise chapter',
    keywords: [first?.matiere_nom, niveau, chapterTitle].filter(Boolean),
    about: chapterTitle
  })
  const jsonLdGraph = [
    breadcrumbGraph,
    chapterGraph,
    itemListElements.length
      ? {
          '@type': 'ItemList',
          name: `Exercices gratuits : ${chapterTitle}`,
          numberOfItems: itemListElements.length,
          itemListOrder: 'https://schema.org/ItemListOrderAscending',
          itemListElement: itemListElements
        }
      : null
  ].filter(Boolean)

  setPageSeo({
    title: finalTitle,
    description: finalDescription,
    canonicalPath: canonicalSeo.canonicalPath,
    canonicalUrl: canonicalSeo.canonicalUrl ? toAbsoluteUrl(canonicalSeo.canonicalUrl) : undefined,
    robots: canonicalSeo.robots,
    ogType: seoPayload.ogType,
    image,
    jsonLdGraph
  })
}

const goBack = () => {
  router.push({ name: 'FreeExercises' })
}

watch(
  notionId,
  () => {
    fetchExercises()
  }
)

watch(
  () => route.query.title,
  (value) => {
    if (value && !props.notionTitleOverride) notionTitle.value = value
  }
)

watch(
  () => props.notionTitleOverride,
  (value) => {
    if (value) notionTitle.value = value
  }
)

watch(
  () => notionTitle.value,
  () => {
    if (exercises.value.length) updateSeo()
  }
)

watch(
  error,
  (value) => {
    const message = String(value || '').trim()
    if (!message) return
    setPageSeo({
      title: 'Chapitre introuvable',
      description: 'Ce chapitre est introuvable ou indisponible.',
      canonicalPath: route.path,
      robots: 'noindex,follow'
    })
  }
)

onMounted(() => {
  detectMobileAndZoomSupport()
  updateViewportWidth()
  setupViewportListener()
  fetchExercises()
})

onBeforeUnmount(() => {
  cleanupViewportListener()
})

watch(viewportWidth, () => {
  nextTick(() => measureContentHeightForFreeExercises())
})

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  nextTick(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    safeRenderMath()
    measureContentHeightForFreeExercises()
  })
}

const subscriptionCtaLabel = computed(() => (subscriptionStore.hasAccess ? 'Gérer mon abonnement' : "S'abonner"))

const onSubscriptionCtaClick = () => {
  if (!userStore.isAuthenticated) {
    openModal(MODAL_IDS.REGISTER)
    return
  }

  if (subscriptionStore.hasAccess) {
    router.push({ name: 'Subscription' }).catch(() => {})
    return
  }

  router.push({
    name: 'Billing',
    query: {
      redirect: route.fullPath,
      reason: 'free_exercise_chapter_cta'
    }
  }).catch(() => {})
}

const showSignupModal = () => {
  if (!userStore.isAuthenticated) {
    openModal(MODAL_IDS.REGISTER)
    return
  }

  if (subscriptionStore.hasAccess) {
    router.push({ name: 'Subscription' }).catch(() => {})
    return
  }

  router.push({
    name: 'Billing',
    query: {
      redirect: route.fullPath,
      reason: 'free_exercises_lock'
    }
  }).catch(() => {})
}

const buildInstruction = (exercise) => {
  if (!exercise?._locked) {
    return exercise.instruction
  }
  const raw = exercise.instruction || ''
  return `<span class="locked-blur">${raw}</span>`
}

function normalizeAnchorId(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function getExerciseAnchorId(exercise, index = 0) {
  const raw = exercise?.slug || exercise?.id || index
  const normalized = normalizeAnchorId(raw)
  if (!normalized) return `exercise-${index}`
  return `exercise-${normalized}`
}
</script>

<template>
  <MainLayout>
    <div class="free-exercise-chapter-page">
      <BackButton text="Retour aux exercices" :custom-action="goBack" position="top-left" />
      <Breadcrumbs :items="breadcrumbItems" class="breadcrumb-trail" />

      <header class="free-exercise-intro" aria-labelledby="free-exercise-title">
        <p v-if="chapterMetaLabel" class="free-exercise-meta">{{ chapterMetaLabel }}</p>
        <h1 id="free-exercise-title" class="free-exercise-title">{{ notionTitle || 'Exercices' }}</h1>
        <p v-if="exercisesCountLabel" class="free-exercise-count">{{ exercisesCountLabel }}</p>
      </header>

      <section class="free-resource-cta" aria-label="Accès professeur ou plateforme">
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
            data-nav-location="free_exercise_chapter_banner"
          >
            Cours particuliers
          </router-link>
          <button
            type="button"
            class="free-resource-cta__btn free-resource-cta__btn--secondary"
            data-cta-name="subscribe"
            data-cta-location="free_exercise_chapter_banner"
            @click="onSubscriptionCtaClick"
          >
            {{ subscriptionCtaLabel }}
          </button>
        </div>
      </section>

      <div v-if="loading" class="state-card">
        <div class="loading-spinner" aria-hidden="true"></div>
        <p class="loading-text">Chargement des exercices gratuits...</p>
      </div>
      <div v-else-if="error" class="state-card">
        <p>{{ error }}</p>
        <button @click="fetchExercises">Réessayer</button>
      </div>
      <div v-else-if="displayedExercises.length === 0" class="state-card">
        Aucun exercice gratuit n'est disponible pour ce chapitre pour le moment.
      </div>
      <div v-else class="content-wrapper" :style="zoomStyle" ref="contentRef">
        <div class="exercise-stack" v-if="freeExercises.length > 0">
          <div class="exercise-section-header">
            <h2 class="exercise-section-title">Exercices gratuits</h2>
          </div>
          <div
            v-for="(exercise, index) in freeExercises"
            :key="exercise.id || exercise.slug || index"
            class="exercise-card-wrapper"
            :id="getExerciseAnchorId(exercise, index)"
          >
            <ExerciceQCM
              :eid="exercise.id || exercise.slug || index"
              :titre="exercise.titre"
              :instruction="buildInstruction(exercise)"
              :solution="exercise.solution"
              :etapes="exercise.etapes"
              :difficulty="exercise.difficulty"
              :preview-images="exercise.previewImages"
              readonly
            />
          </div>
        </div>

        <div v-if="lockedExercises.length > 0" class="exercise-stack premium-exercise-stack">
          <div class="exercise-section-header">
            <h2 class="exercise-section-title premium-title">Exercices premium</h2>
            <p class="exercise-section-subtitle">
              Débloquez l’accès complet pour voir les exercices premium et progresser plus vite.
            </p>
          </div>
          <div
            v-for="(exercise, index) in paginatedLockedExercises"
            :key="exercise.id || exercise.slug || index"
            class="exercise-card-wrapper locked-tabs"
            :id="getExerciseAnchorId(exercise, index + freeExercises.length)"
          >
            <div class="locked-pill">Exercice premium</div>
            <ExerciceQCM
              :eid="exercise.id || exercise.slug || index"
              :titre="exercise.titre"
              :instruction="buildInstruction(exercise)"
              :solution="exercise.solution"
              :etapes="exercise.etapes"
              :difficulty="exercise.difficulty"
              :preview-images="exercise.previewImages"
              readonly
            />
            <div
              class="locked-cta"
              role="button"
              tabindex="0"
              @click="showSignupModal"
              @keydown.enter.prevent="showSignupModal"
            >
              Crée un compte pour tout voir
            </div>
          </div>
          <div v-if="totalPages > 1" class="pagination">
            <button
              class="pagination-btn"
              :disabled="currentPage === 1"
              @click="goToPage(currentPage - 1)"
            >
              &larr;
            </button>
            <span class="pagination-text">Page {{ currentPage }} / {{ totalPages }}</span>
            <button
              class="pagination-btn"
              :disabled="currentPage === totalPages"
              @click="goToPage(currentPage + 1)"
            >
              &rarr;
            </button>
          </div>
        </div>
      </div>

      <section class="related-resources" aria-labelledby="related-resources-title">
        <h2 id="related-resources-title" class="related-resources__title">Liens utiles pour continuer</h2>
        <p class="related-resources__intro">{{ relatedLinksIntro }}</p>
        <div class="related-resources__list">
          <router-link
            v-for="link in relatedLinks"
            :key="link.to"
            :to="link.to"
            class="related-resources__link"
          >
            {{ link.label }}
          </router-link>
        </div>
      </section>
    </div>
  </MainLayout>
</template>

<style scoped>
.free-exercise-chapter-page {
  min-height: 100vh;
  background: #fff;
  padding: 48px 24px 80px;
  width: 100%;
  max-width: none;
}

.free-exercise-intro {
  margin: 4px 0 18px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.breadcrumb-trail {
  margin: 6px 0 18px;
}

.free-exercise-meta {
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: #64748b;
}

.free-exercise-title {
  margin: 0;
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
}

.free-exercise-count {
  margin: 0;
  font-size: 14px;
  color: #475569;
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

@media (max-width: 768px) {
  .free-exercise-title {
    font-size: 22px;
  }
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

.content-wrapper {
  transform-origin: top left;
}

.state-card {
  margin-top: 30px;
  padding: 32px;
  border-radius: 18px;
  border: 1px dashed #cbd5f5;
  text-align: center;
  color: #475569;
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

.exercise-stack {
  display: flex;
  flex-direction: column;
  gap: 36px;
  width: 100%;
}

.exercise-section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.exercise-section-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.exercise-section-subtitle {
  margin: 0;
  font-size: 14px;
  color: #475569;
  max-width: 780px;
  line-height: 1.5;
}

.premium-exercise-stack {
  margin-top: 56px;
}

.premium-title {
  color: #111827;
}

.related-resources {
  margin-top: 32px;
  padding: 20px 22px;
  border-radius: 18px;
  border: 1px solid rgba(59, 130, 246, 0.18);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.06), rgba(99, 102, 241, 0.04));
}

.related-resources__title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.related-resources__intro {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #334155;
  line-height: 1.5;
}

.related-resources__list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 28px;
}

.related-resources__link {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 2px 0;
  color: #1d4ed8;
  font-weight: 700;
  font-size: 15px;
  text-decoration: none;
  line-height: 1.35;
  transition: color 0.2s ease;
}

.related-resources__link:hover {
  color: #1e40af;
  text-decoration: underline;
}

@media (max-width: 900px) {
  .related-resources__list {
    grid-template-columns: minmax(0, 1fr);
    gap: 8px;
  }
}

.exercise-card-wrapper {
  padding: 0;
  border: none;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.pagination-btn {
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #1e293b;
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-text {
  font-weight: 700;
  color: #0f172a;
}

.locked-pill {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #eef2ff;
  color: #1d4ed8;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid rgba(59, 130, 246, 0.4);
  z-index: 2;
}

.locked-tabs {
  position: relative;
}

.locked-cta {
  margin-top: 1rem;
  padding: 0.85rem 1rem;
  background: #eef2ff;
  border: 1px dashed #93c5fd;
  color: #1d4ed8;
  font-weight: 700;
  text-align: center;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.locked-cta:hover,
.locked-cta:focus {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.18);
  outline: none;
}

.separator-cta {
  margin: 32px 0 0 0;
  border-style: dashed;
  background: #eef2ff;
  color: #1d4ed8;
  display: block;
  width: 100%;
}

:deep(.locked-blur) {
  filter: blur(2px);
  display: inline-block;
  position: relative;
}

:deep(.locked-blur)::after {
  content: ' 🔒';
  color: #1d4ed8;
  font-weight: 700;
}

:deep(.locked-tabs .tabs-container .tab-btn:nth-child(2)),
:deep(.locked-tabs .tabs-container .tab-btn:nth-child(3)) {
  position: relative;
  overflow: hidden;
}

:deep(.locked-tabs .tabs-container .tab-btn:nth-child(2)::after),
:deep(.locked-tabs .tabs-container .tab-btn:nth-child(3)::after) {
  content: '🔒';
  margin-left: 6px;
  font-size: 12px;
}

:deep(.locked-tabs .tabs-container .tab-btn:nth-child(2)),
:deep(.locked-tabs .tabs-container .tab-btn:nth-child(3)) {
  opacity: 0.8;
  pointer-events: none;
}

:deep(.locked-tabs .steps-section),
:deep(.locked-tabs .answer-section) {
  position: relative;
  filter: blur(2px);
  pointer-events: none;
}

:deep(.locked-tabs .steps-section::after),
:deep(.locked-tabs .answer-section::after) {
  content: 'Section réservée aux abonnés';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(255,255,255,0.86), rgba(255,255,255,0.92));
  color: #1d4ed8;
  font-weight: 700;
  border: 1px dashed #cbd5f5;
  border-radius: 12px;
}

:deep(.locked-tabs .problem-section .problem-content) {
  position: relative;
}

:deep(.locked-tabs .problem-section .problem-content > :nth-of-type(n+2)) {
  filter: blur(5px);
  opacity: 0.35;
  pointer-events: none;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 10px;
  border-radius: 50%;
  border: 4px solid #e5ecff;
  border-top-color: #2563eb;
  animation: spin 0.9s linear infinite;
}

.loading-text {
  margin: 0;
  font-weight: 600;
  color: #1d3b8b;
  font-size: 15px;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .free-exercise-chapter-page {
    padding: 32px 16px 60px;
  }

  .exercise-card-wrapper {
    padding: 18px;
  }
}
</style>
