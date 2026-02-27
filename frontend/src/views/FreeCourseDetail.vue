<script setup>
import { ref, onMounted, nextTick, watch, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import BackButton from '@/components/common/BackButton.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import ExerciceQCM from '@/components/UI/ExerciceQCM.vue'
import { getFreeResource } from '@/api/free-content'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'
import { buildCourseRouteParams } from '@/utils/freeCourseSlug'
import { buildSummaryRouteParams } from '@/utils/freeSummarySlug'
import { buildExerciseChapterRouteParams, slugifyText } from '@/utils/freeExerciseSlug'
import { FREE_RESOURCES_AUTHORITY_CONTENT, isKnownBrokenPopularLink } from '@/config/freeResourcesAuthority'
import {
  setPageSeo,
  getRobotsForRoute,
  buildBreadcrumbJsonLd,
  buildCourseJsonLd,
  buildCreativeWorkJsonLd
} from '@/services/seo'
import {
  buildDynamicSeo,
  buildCanonicalSeoFields,
  pageTypeFromResourceType,
  topicFromSlug,
  normalizePathname,
  stripHtmlForSeo
} from '@/composables/useDynamicSeo'
import { useUserStore } from '@/stores/user'
import { useSubscriptionStore } from '@/stores/subscription'

const props = defineProps({
  resourceType: {
    type: String,
    default: 'course'
  },
  resolvedSlug: {
    type: String,
    default: ''
  }
})

const route = useRoute()
const router = useRouter()
const { openModal } = useModalManager()
const userStore = useUserStore()
const subscriptionStore = useSubscriptionStore()

const resource = ref(null)
const loading = ref(false)
const error = ref(null)
const tableOfContents = ref([])
const isTocExpanded = ref(false)
const contentRef = ref(null)
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1920)
const contentHeight = ref(0)
const renderedContent = computed(() => {
  if (!resource.value) return ''
  const raw = resource.value.contenu || resource.value.contenu_html || ''
  if (!raw) return ''
  return renderContentWithImages(raw, resource.value.images || [], { autoShiftHeadings: true })
})

const effectiveSlug = computed(() => {
  const override = String(props.resolvedSlug || '').trim()
  if (override) return override
  return String(route.params.slug || '').trim()
})
const isExerciseResource = computed(() => props.resourceType === 'exercise')
const exerciseInstruction = computed(() => {
  if (!resource.value) return ''
  return resource.value.question || resource.value.contenu || resource.value.accroche || ''
})
const exerciseSteps = computed(() => (resource.value?.etapes ? resource.value.etapes : ''))
const exerciseSolution = computed(() => {
  if (!resource.value) return ''
  return resource.value.solution || resource.value.reponse_correcte || ''
})
const exerciseDifficulty = computed(() => resource.value?.difficulty || 'medium')
const exerciseImages = computed(() => resource.value?.images || [])
const showBlurredTeaser = computed(() => !isExerciseResource.value && !subscriptionStore.hasAccess)

const blurredTeaserLines = computed(() => {
  const raw = stripHtml(renderedContent.value || resource.value?.contenu_html || resource.value?.contenu || '')
  const cleaned = raw.replace(/\s+/g, ' ').trim()
  if (!cleaned) {
    return [
      "Contenu complet réservé aux abonnés OptiTAB.",
      "Méthodes détaillées, démonstrations et exercices bonus.",
      "Exemples corrigés pas à pas et astuces de professeur.",
      "Accès illimité à toutes les ressources premium."
    ]
  }

  const words = cleaned.split(' ').slice(0, 60)
  const lines = []
  const chunkSize = 12
  for (let i = 0; i < words.length; i += chunkSize) {
    lines.push(words.slice(i, i + chunkSize).join(' '))
    if (lines.length >= 4) break
  }
  if (lines.length === 0) {
    return [
      "Contenu complet réservé aux abonnés OptiTAB.",
      "Méthodes détaillées, démonstrations et exercices bonus."
    ]
  }
  return lines
})

const courseRouteMatches = (params, canonical) => {
  if (!canonical || !params) return false
  return (
    String(params.pays || '') === String(canonical.pays || '') &&
    String(params.niveauGroup || '') === String(canonical.niveauGroup || '') &&
    String(params.matiere || '') === String(canonical.matiere || '') &&
    String(params.slug || '') === String(canonical.slug || '') &&
    String(params.id || '') === String(canonical.id || '')
  )
}

const safeRenderMath = async () => {
  try {
    await renderMath()
  } catch (_) {
    // Ignore MathJax failures (e.g., when the content is empty or MathJax is busy)
  }
}
const showScrollTopButton = ref(false)
const backButtonLabel = computed(() => {
  if (props.resourceType === 'exercise') {
    return 'Retour aux exercices gratuits'
  }
  if (props.resourceType === 'summary') {
    return 'Retour aux fiches'
  }
  return 'Retour aux chapitres'
})

const categoryInfo = computed(() => {
  if (props.resourceType === 'exercise') {
    return { label: 'Exercices gratuits', path: '/ressources-gratuites/exercices' }
  }
  if (props.resourceType === 'summary') {
    return { label: 'Fiches de synthese gratuites', path: '/ressources-gratuites/syntheses' }
  }
  return { label: 'Cours gratuits', path: '/ressources-gratuites/cours' }
})

const introText = computed(() => {
  if (!resource.value) return ''
  if (props.resourceType === 'course') return ''
  const raw = resource.value.accroche || resource.value.excerpt || resource.value.resume || ''
  const cleaned = stripHtml(raw)
  if (!cleaned) return ''
  return cleaned.length > 180 ? `${cleaned.slice(0, 177).trimEnd()}...` : cleaned
})

const exerciseChapterPath = computed(() => {
  if (props.resourceType !== 'exercise') return ''
  const source = resource.value
  if (!source) return ''

  const params = buildExerciseChapterRouteParams({
    paysNom: source?.pays_nom,
    matiereNom: source?.matiere_nom || source?.matiere,
    niveauNom: source?.niveau_nom,
    niveauGroup: source?.niveau_nom,
    name: source?.notion_nom,
    id: source?.notion
  })
  if (!params?.slug || !params?.id) return ''

  if (params.niveauGroup) {
    return `/ressources-gratuites/exercices/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`
  }
  return `/ressources-gratuites/exercices/${params.pays}/${params.matiere}/${params.slug}-${params.id}`
})

const breadcrumbItems = computed(() => {
  const crumbs = [
    { label: 'Accueil', to: '/' },
    { label: categoryInfo.value.label, to: categoryInfo.value.path }
  ]

  if (props.resourceType === 'exercise' && resource.value?.notion_nom && exerciseChapterPath.value) {
    crumbs.push({ label: resource.value.notion_nom, to: exerciseChapterPath.value })
  }

  crumbs.push({ label: resource.value?.titre || 'Ressource gratuite' })
  return crumbs
})

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
    if (picked.length >= (limit || 4)) break
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
  const raw = resource.value?.notion_nom || resource.value?.chapitre_nom || resource.value?.titre || ''
  return stripTopicPrefix(raw)
})

const relatedLevel = computed(() => {
  return String(resource.value?.niveau_nom || resource.value?.tag_secondaire || '').trim()
})

const relatedLinksIntro = computed(() => {
  const topic = relatedTopic.value
  if (props.resourceType === 'exercise') {
    return topic
      ? `Continuez avec des cours et des fiches autour de ${topic}.`
      : 'Continuez avec des cours et des fiches sur les notions proches.'
  }
  if (props.resourceType === 'summary') {
    return topic
      ? `Pour bien retenir ${topic}, combinez cours et exercices corrigés.`
      : 'Pour progresser, combinez les fiches avec des cours et des exercices corrigés.'
  }
  return topic
    ? `Pour maîtriser ${topic}, passez ensuite aux exercices corrigés et aux fiches de synthèse.`
    : 'Complétez ce cours avec des exercices corrigés et des fiches de synthèse.'
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

  if (props.resourceType === 'exercise' && exerciseChapterPath.value && resource.value?.notion_nom) {
    addLink(`Chapitre d'exercices: ${resource.value.notion_nom}`, exerciseChapterPath.value)
  }

  pickAuthorityLinks({
    preferredTypes: ['course'],
    topicTokens,
    levelTokens,
    excludedPaths: usedPaths,
    limit: 1
  }).forEach((link) => addLink(link.label, link.href))

  pickAuthorityLinks({
    preferredTypes: ['summary'],
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
    limit: 6
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
    addLink('Tous les exercices corrigés', RELATED_LINK_BASE_PATHS.exercise)
    addLink('Toutes les fiches de synthèse', RELATED_LINK_BASE_PATHS.summary)
  }

  const seedSource = `${props.resourceType}|${resource.value?.id || ''}|${route.path}|${topic}|${level}`
  return shuffleLinksStable(links, seedSource).slice(0, 8)
})

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
      reason: 'free_resource_detail_cta'
    }
  }).catch(() => {})
}

function computeAutoZoom(width) {
  let base
  if (width >= 1400) base = 1
  else if (width >= 1200) base = 0.95
  else if (width >= 1024) base = 0.9
  else if (width >= 900) base = 0.85
  else if (width >= 768) base = 0.8
  else if (width >= 640) base = 0.78
  else if (width >= 520) base = 0.76
  else if (width >= 420) base = 0.74
  else base = 0.72

  if (width < 1024) {
    const extra = width < 768 ? 0.1 : 0.07
    return Math.max(0.6, base - extra)
  }
  return base
}

const zoomLevel = computed(() => computeAutoZoom(viewportWidth.value))

const zoomStyle = computed(() => {
  let z = zoomLevel.value || 1
  if (viewportWidth.value <= 768) {
    z = Math.max(0.6, z - 0.08)
  }
  const widthPercent = (100 / z).toFixed(3)

  const style = {
    transform: `scale(${z})`,
    transformOrigin: 'top left',
    width: `${widthPercent}%`,
    height: 'auto',
    minHeight: 'auto'
  }

  if (contentHeight.value > 0 && Number.isFinite(z) && z < 1) {
    const marginBottom = -Math.round(contentHeight.value * (1 - z))
    style.marginBottom = `${marginBottom}px`
  }

  return style
})

const fetchResource = async () => {
  loading.value = true
  error.value = null
  try {
    const slugToFetch = effectiveSlug.value
    if (!slugToFetch) {
      error.value = "Impossible de charger cette ressource gratuite."
      return
    }
    resource.value = await getFreeResource(slugToFetch)
  } catch (err) {
    console.error('Erreur chargement de la ressource gratuite', err)
    error.value = err?.message || "Impossible de charger cette ressource gratuite."
  } finally {
    loading.value = false
  }
}

const buildTableOfContents = () => {
  tableOfContents.value = []
  const root = contentRef.value
  if (!root) return
  const selectors = root.querySelectorAll('h1, h2, h3')
  const toc = []
  selectors.forEach((heading, index) => {
    const level = Number(heading.tagName.replace('H', ''))
    const text = heading.textContent?.trim()
    if (!text) return
    const id = heading.id || `free-course-heading-${index}`
    heading.id = id
    toc.push({ id, text, level })
  })
  tableOfContents.value = toc
}

const measureContentHeight = () => {
  if (!contentRef.value) {
    contentHeight.value = 0
    return
  }
  contentHeight.value = contentRef.value.scrollHeight || contentRef.value.offsetHeight || 0
}

const updateViewportWidth = () => {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
  nextTick(() => measureContentHeight())
}

const handleScroll = () => {
  const threshold = 300
  showScrollTopButton.value = (window.scrollY || document.documentElement.scrollTop || 0) > threshold
}

const scrollToTop = () => {
  if (typeof window === 'undefined') return
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const goBack = () => {
  let routeName = 'FreeCourses'
  if (props.resourceType === 'exercise') {
    routeName = 'FreeExercises'
  } else if (props.resourceType === 'summary') {
    routeName = 'FreeSummaries'
  }
  router.push({ name: routeName })
}

const openSignup = () => {
  openModal(MODAL_IDS.REGISTER)
}

function stripHtml(input) {
  return String(input || '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()
}

function pickSeoSourceText(value, resourceType) {
  const type = String(resourceType || '').trim().toLowerCase()
  const raw = type === 'exercise'
    ? (value?.question || value?.excerpt || value?.accroche || value?.contenu || value?.contenu_html || '')
    : (type === 'summary'
        ? (value?.accroche || value?.excerpt || value?.contenu || value?.contenu_html || '')
        : (value?.excerpt || value?.accroche || value?.contenu || value?.contenu_html || ''))
  return stripHtmlForSeo(raw)
}

function pickSeoImage(value) {
  const cover = value?.cover_image
  if (cover) return cover
  const img = Array.isArray(value?.images) ? value.images[0]?.image : ''
  return img || ''
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

function toIsoDate(value) {
  if (!value) return ''
  try {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return ''
    return date.toISOString()
  } catch (_) {
    return ''
  }
}

function normalizeSeoText(value) {
  return String(value || '').replace(/\s+/g, ' ').trim()
}

function buildResourceImageObjects(value, canonicalResourceUrl) {
  if (!canonicalResourceUrl || !Array.isArray(value?.images)) return []

  return value.images
    .map((img, index) => {
      const contentUrl = toAbsoluteUrl(img?.image)
      if (!contentUrl) return null

      const caption = normalizeSeoText(
        img?.legende || img?.caption || img?.alt_text_resolved || img?.alt_text || ''
      )
      const title = normalizeSeoText(
        img?.title_text_resolved || img?.title_text || caption || `Illustration ${index + 1}`
      )
      const width = Number.parseInt(img?.width, 10)
      const height = Number.parseInt(img?.height, 10)

      return {
        '@type': 'ImageObject',
        '@id': `${canonicalResourceUrl}#image-${img?.id || index + 1}`,
        contentUrl,
        url: contentUrl,
        name: title || undefined,
        caption: caption || undefined,
        width: Number.isFinite(width) && width > 0 ? width : undefined,
        height: Number.isFinite(height) && height > 0 ? height : undefined,
        representativeOfPage: index === 0 ? true : undefined
      }
    })
    .filter(Boolean)
}

function buildCanonicalPath(value) {
  if (!value) return route.path
  if (props.resourceType === 'course') {
    const params = buildCourseRouteParams({
      paysNom: value?.pays_nom,
      matiereNom: value?.matiere_nom,
      niveauNom: value?.niveau_nom,
      titre: value?.titre,
      id: value?.id
    })
    if (params?.slug && params?.id) {
      if (params.niveauGroup) {
        return `/ressources-gratuites/cours/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`
      }
      return `/ressources-gratuites/cours/${params.pays}/${params.matiere}/${params.slug}-${params.id}`
    }
  }

  if (props.resourceType === 'summary') {
    const params = buildSummaryRouteParams({
      paysNom: value?.pays_nom,
      matiereNom: value?.matiere_nom,
      niveauNom: value?.niveau_nom,
      titre: value?.titre,
      id: value?.id
    })
    if (params?.slug && params?.id) {
      if (params.niveauGroup) {
        return `/ressources-gratuites/syntheses/${params.pays}/${params.niveauGroup}/${params.matiere}/${params.slug}-${params.id}`
      }
      return `/ressources-gratuites/syntheses/${params.pays}/${params.matiere}/${params.slug}-${params.id}`
    }
  }

  if (props.resourceType === 'exercise') {
    const slug = value?.slug ? String(value.slug).trim() : ''
    if (slug) return `/ressources-gratuites/exercices/${slug}`
  }

  return route.path
}

function isCanonicalRoutePath(currentPath, canonicalPath) {
  return normalizePathname(currentPath) === normalizePathname(canonicalPath)
}

function getRouteParamValue(key) {
  const raw = route?.params?.[key]
  if (Array.isArray(raw)) {
    return String(raw[0] || '').trim()
  }
  return String(raw || '').trim()
}

function buildBestKnownCanonicalPathFromRoute() {
  const currentPath = normalizePathname(route.path)
  if (props.resourceType === 'exercise') {
    const slug = getRouteParamValue('slug')
    return slug ? `/ressources-gratuites/exercices/${slug}` : currentPath
  }

  const pays = getRouteParamValue('pays')
  const niveauGroup = getRouteParamValue('niveauGroup')
  const matiere = getRouteParamValue('matiere')
  const slug = getRouteParamValue('slug')
  const id = getRouteParamValue('id')
  if (!pays || !matiere || !slug || !id) return currentPath

  if (props.resourceType === 'summary') {
    if (niveauGroup) {
      return `/ressources-gratuites/syntheses/${pays}/${niveauGroup}/${matiere}/${slug}-${id}`
    }
    return `/ressources-gratuites/syntheses/${pays}/${matiere}/${slug}-${id}`
  }

  if (niveauGroup) {
    return `/ressources-gratuites/cours/${pays}/${niveauGroup}/${matiere}/${slug}-${id}`
  }
  return `/ressources-gratuites/cours/${pays}/${matiere}/${slug}-${id}`
}

function applySafeSeoBeforeResourceLoaded() {
  const canonicalTargetPath = buildBestKnownCanonicalPathFromRoute()
  const currentPath = normalizePathname(route.path)
  const seoPayload = buildDynamicSeo({
    pageType: pageTypeFromResourceType(props.resourceType),
    topic: topicFromSlug(getRouteParamValue('slug')),
    level: getRouteParamValue('niveauGroup'),
    sourceText: getRouteParamValue('slug')
  })

  setPageSeo({
    title: seoPayload.title,
    description: seoPayload.description,
    canonicalPath: currentPath,
    canonicalUrl: canonicalTargetPath !== currentPath ? canonicalTargetPath : undefined,
    robots: 'noindex,follow',
    ogType: seoPayload.ogType
  })
}

watch(
  [resource, () => route.fullPath, () => props.resourceType],
  ([value]) => {
    if (value) return
    applySafeSeoBeforeResourceLoaded()
  },
  { immediate: true }
)

watch(
  [resource, () => route.fullPath],
  ([value]) => {
    if (!value) return
    if (props.resourceType === 'course') {
      const canonicalParams = buildCourseRouteParams({
        paysNom: value?.pays_nom,
        matiereNom: value?.matiere_nom,
        niveauNom: value?.niveau_nom,
        titre: value?.titre,
        id: value?.id
      })
      if (canonicalParams && !courseRouteMatches(route.params, canonicalParams)) {
        const routeName = canonicalParams.niveauGroup ? 'FreeCourseSlugGrouped' : 'FreeCourseSlug'
        const routeParams = canonicalParams.niveauGroup
          ? canonicalParams
          : {
              pays: canonicalParams.pays,
              matiere: canonicalParams.matiere,
              slug: canonicalParams.slug,
              id: canonicalParams.id
            }
        router.replace({
          name: routeName,
          params: routeParams,
          query: route.query,
          hash: route.hash
        }).catch(() => {})
      }
    }
    if (props.resourceType === 'summary') {
      const canonicalParams = buildSummaryRouteParams({
        paysNom: value?.pays_nom,
        matiereNom: value?.matiere_nom,
        niveauNom: value?.niveau_nom,
        titre: value?.titre,
        id: value?.id
      })
      if (canonicalParams && !courseRouteMatches(route.params, canonicalParams)) {
        const routeName = canonicalParams.niveauGroup ? 'FreeSummarySlugGrouped' : 'FreeSummarySlug'
        const routeParams = canonicalParams.niveauGroup
          ? canonicalParams
          : {
              pays: canonicalParams.pays,
              matiere: canonicalParams.matiere,
              slug: canonicalParams.slug,
              id: canonicalParams.id
            }
        router.replace({
          name: routeName,
          params: routeParams,
          query: route.query,
          hash: route.hash
        }).catch(() => {})
      }
    }
    const canonicalSlug = value?.slug ? String(value.slug) : ''
    const currentSlug = route?.params?.slug ? String(route.params.slug) : ''
    if (props.resourceType === 'exercise' && canonicalSlug && currentSlug && canonicalSlug !== currentSlug) {
      router.replace({
        name: route.name,
        params: { ...route.params, slug: canonicalSlug },
        query: route.query,
        hash: route.hash
      }).catch(() => {})
    }
    const matiere = value?.matiere_nom ? String(value.matiere_nom).trim() : ''
    const niveau = value?.niveau_nom ? String(value.niveau_nom).trim() : (value?.tag_secondaire ? String(value.tag_secondaire).trim() : '')
    const baseTitle = value?.titre ? String(value.titre).trim() : ''
    const notionOrChapterTitle = value?.notion_nom
      ? String(value.notion_nom).trim()
      : (value?.chapitre_nom ? String(value.chapitre_nom).trim() : '')
    const sourceText = pickSeoSourceText(value, props.resourceType)
    const seoPayload = buildDynamicSeo({
      pageType: pageTypeFromResourceType(props.resourceType),
      topic: notionOrChapterTitle || baseTitle || topicFromSlug(route?.params?.slug),
      level: niveau,
      sourceText
    })
    const title = seoPayload.title
    const description = seoPayload.description
    const image = pickSeoImage(value) || undefined
    const imageAbs = image ? toAbsoluteUrl(image) : ''
    const canonicalResourcePath = buildCanonicalPath(value)
    const canonicalResourceUrl = toAbsoluteUrl(canonicalResourcePath)
    const isCanonicalRoute = isCanonicalRoutePath(route.path, canonicalResourcePath)
    const canonicalSeo = buildCanonicalSeoFields({
      routePath: route.path,
      canonicalPath: canonicalResourcePath,
      isCanonicalRoute,
      robotsWhenCanonical: getRobotsForRoute({ route })
    })
    const siteUrl = getSiteUrl()
    const organizationId = `${siteUrl}/#organization`
    const websiteId = `${siteUrl}/#website`
    const webPageId = `${canonicalResourceUrl}#webpage`
    const categoryPath = props.resourceType === 'exercise'
      ? '/ressources-gratuites/exercices'
      : (props.resourceType === 'summary' ? '/ressources-gratuites/syntheses' : '/ressources-gratuites/cours')
    const categoryLabel = props.resourceType === 'exercise'
      ? 'Exercices corrigés gratuits'
      : (props.resourceType === 'summary' ? 'Fiches de synthèse gratuites' : 'Cours gratuits')
    const dateModified = toIsoDate(value?.date_modification || value?.updated_at || value?.date_update || value?.date_mise_a_jour)

    const resourceName = baseTitle || seoPayload.topic || 'Ressource gratuite'
    const keywords = [matiere, niveau].filter(Boolean)
    const resourceImageObjects = (
      props.resourceType === 'course' ||
      props.resourceType === 'exercise' ||
      props.resourceType === 'summary'
    )
      ? buildResourceImageObjects(value, canonicalResourceUrl)
      : []
    const resourceImageUrls = resourceImageObjects.map((img) => img.contentUrl).filter(Boolean)
    const breadcrumbGraph = buildBreadcrumbJsonLd([
      { name: 'Accueil', item: '/' },
      { name: categoryLabel, item: categoryPath },
      { name: resourceName, item: canonicalResourceUrl }
    ])

    const primaryGraph = props.resourceType === 'course'
      ? buildCourseJsonLd({
          id: `${canonicalResourceUrl}#course`,
          name: resourceName,
          description,
          url: canonicalResourceUrl,
          inLanguage: 'fr-FR',
          provider: { '@id': organizationId },
          isPartOf: { '@id': websiteId },
          mainEntityOfPage: { '@id': webPageId },
          image: resourceImageUrls.length ? resourceImageUrls : (imageAbs || undefined),
          dateModified: dateModified || undefined,
          educationalLevel: niveau || undefined,
          keywords,
          about: notionOrChapterTitle || undefined
        })
      : buildCreativeWorkJsonLd({
          id: `${canonicalResourceUrl}#creativework`,
          name: resourceName,
          description,
          url: canonicalResourceUrl,
          inLanguage: 'fr-FR',
          author: { '@id': organizationId },
          publisher: { '@id': organizationId },
          isPartOf: { '@id': websiteId },
          mainEntityOfPage: { '@id': webPageId },
          image: resourceImageUrls.length ? resourceImageUrls : (imageAbs || undefined),
          dateModified: dateModified || undefined,
          educationalLevel: niveau || undefined,
          learningResourceType: props.resourceType === 'summary' ? 'Revision summary' : 'Exercise',
          keywords,
          about: notionOrChapterTitle || undefined
        })

    const jsonLdGraph = [breadcrumbGraph, primaryGraph, ...resourceImageObjects].filter(Boolean)

    setPageSeo({
      title,
      description,
      canonicalPath: canonicalSeo.canonicalPath,
      canonicalUrl: canonicalSeo.canonicalUrl ? toAbsoluteUrl(canonicalSeo.canonicalUrl) : undefined,
      robots: canonicalSeo.robots,
      ogType: seoPayload.ogType,
      image,
      jsonLdGraph
    })
  },
  { immediate: true }
)

watch(
  error,
  (value) => {
    const message = String(value || '').trim()
    if (!message) return
    const currentPath = normalizePathname(route.path)
    const fallbackCanonicalUrl = props.resourceType === 'exercise'
      ? toAbsoluteUrl('/ressources-gratuites/exercices')
      : undefined
    setPageSeo({
      title: 'Ressource introuvable | OptiTAB',
      description: 'Cette ressource gratuite est introuvable ou indisponible.',
      canonicalPath: currentPath,
      canonicalUrl: fallbackCanonicalUrl,
      robots: 'noindex,follow'
    })
  }
)

watch(
  () => effectiveSlug.value,
  () => {
    resource.value = null
    fetchResource()
  }
)

watch(
  renderedContent,
  async (html) => {
    if (!html) {
      tableOfContents.value = []
      return
    }
    await nextTick()
    buildTableOfContents()
    await safeRenderMath()
    measureContentHeight()
  },
  { immediate: true }
)

watch(zoomLevel, () => {
  nextTick(() => measureContentHeight())
})

onMounted(() => {
  fetchResource()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', updateViewportWidth, { passive: true })
    window.addEventListener('scroll', handleScroll, { passive: true })
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportWidth)
    window.removeEventListener('scroll', handleScroll)
  }
})
</script>

<template>
  <MainLayout>
    <section class="cours-section">
      <BackButton 
        :text="backButtonLabel" 
        :custom-action="goBack"
        position="top-left"
      />
      <Breadcrumbs :items="breadcrumbItems" class="breadcrumb-trail" />

      <div class="cours-body">
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner" aria-hidden="true"></div>
          <p class="loading-text">Chargement de la ressource...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchResource">Réessayer</button>
        </div>

        <div v-else-if="resource" class="cours-container">
           <header class="cours-header">
             <div class="cours-title-row">
               <h1 class="cours-title">{{ resource.titre }}</h1>
             </div>
             <p v-if="introText" class="cours-intro">{{ introText }}</p>
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
                 data-nav-location="free_resource_detail_banner"
               >
                 Cours particuliers
               </router-link>
               <button
                 type="button"
                 class="free-resource-cta__btn free-resource-cta__btn--secondary"
                 data-cta-name="subscribe"
                 data-cta-location="free_resource_detail_banner"
                 @click="onSubscriptionCtaClick"
               >
                 {{ subscriptionCtaLabel }}
               </button>
             </div>
           </section>

           <div v-if="isExerciseResource" class="exercise-detail-body">
             <ExerciceQCM
               :eid="resource.id"
              :titre="resource.titre"
              :instruction="exerciseInstruction"
              :etapes="exerciseSteps"
              :solution="exerciseSolution"
              :difficulty="exerciseDifficulty"
              :preview-images="exerciseImages"
              :readonly="true"
            />
          </div>

          <nav v-if="tableOfContents.length && !isExerciseResource" class="toc-container">
            <div class="toc-header" @click="isTocExpanded = !isTocExpanded">
              <div class="toc-header-content">
                <svg class="toc-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="8" y1="6" x2="21" y2="6"/>
                  <line x1="8" y1="12" x2="21" y2="12"/>
                  <line x1="8" y1="18" x2="21" y2="18"/>
                  <line x1="3" y1="6" x2="3.01" y2="6"/>
                  <line x1="3" y1="12" x2="3.01" y2="12"/>
                  <line x1="3" y1="18" x2="3.01" y2="18"/>
                </svg>
                <h3 class="toc-title">Sommaire</h3>
              </div>
              <svg class="toc-toggle-icon" :class="{ expanded: isTocExpanded }" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9" />
              </svg>
          </div>
          <transition name="toc-expand">
              <div v-show="isTocExpanded" class="toc-body">
                <ul class="toc-list">
                  <li 
                    v-for="(item, index) in tableOfContents" 
                    :key="item.id || index"
                    :class="['toc-item', `toc-level-${item.level}`]"
                  >
                    <a class="toc-link" href="#" @click.prevent="scrollToSection(item.id)">
                      {{ item.text }}
                    </a>
                  </li>
                </ul>
              </div>
            </transition>
          </nav>

          <div v-if="!isExerciseResource" class="cours-content-outer" :style="zoomStyle">
            <div class="cours-content" ref="contentRef" v-html="renderedContent" />
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

           <div v-if="showBlurredTeaser" class="blurred-teaser">
             <div class="blurred-teaser__header">
               <h3>Contenu complet</h3>
               <p>Accès réservé aux abonnés OptiTAB.</p>
             </div>
             <div class="blurred-teaser__content" aria-hidden="true">
               <p v-for="(line, index) in blurredTeaserLines" :key="index">{{ line }}</p>
             </div>
             <button class="blurred-teaser__cta" type="button" @click="onSubscriptionCtaClick">
               Débloquer l’accès complet
             </button>
           </div>

           <transition name="scroll-top-fade">
             <button
               v-show="showScrollTopButton && !isExerciseResource"
              class="scroll-top-btn"
              @click="scrollToTop"
              aria-label="Retour en haut"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="18 15 12 9 6 15" />
              </svg>
            </button>
          </transition>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<style scoped>
.cours-section {
  padding: 48px 2vw 60px;
  background: #fff;
  min-height: 100vh;
  position: relative;
}

.breadcrumb-trail {
  margin: 6px 0 16px;
}

.cours-body {
  width: 100%;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 4px solid #e5ecff;
  border-top-color: #2563eb;
  animation: spin 0.9s linear infinite;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 36px 0;
}

.loading-text {
  margin: 0;
  font-weight: 600;
  color: #1d3b8b;
  font-size: 15px;
}

@media (max-width: 768px) {
  .cours-section {
    padding-top: 32px;
  }

  .cours-header {
    margin-bottom: 0;
  }
}

.cours-header {
  text-align: center;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.cours-intro {
  margin: 0;
  max-width: 860px;
  color: #475569;
  font-weight: 600;
  font-size: 14px;
  line-height: 1.6;
}

.cours-title-row {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.cours-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.cours-badge,
.cours-type-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid transparent;
}

.cours-badge {
  background: #e0f2fe;
  color: #0f172a;
  border-color: rgba(37, 99, 235, 0.4);
}

.cours-type-pill {
  background: #f1f5f9;
  color: #1d3557;
  border-color: rgba(148, 163, 184, 0.5);
}

.cours-context {
  margin: 0;
  color: #475569;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.exercise-detail-body {
  margin: 20px 0 0;
  width: 100%;
  padding: 0 0 24px;
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
  margin: 18px 0 22px 0;
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

.exercise-intro {
  font-size: 16px;
  color: #1f2937;
  margin: 0 0 16px;
}

.exercise-section {
  margin-bottom: 24px;
  padding: 18px;
  border-radius: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.exercise-section h3 {
  margin: 0 0 12px;
  font-size: 18px;
  color: #0f172a;
}

.exercise-card {
  background: #fff;
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
  padding: 20px 22px;
  margin: 18px 0 16px;
}

.exercise-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 12px;
}

.exercise-card-title {
  margin: 0;
  font-size: clamp(20px, 2vw, 26px);
  font-weight: 700;
  color: #0f172a;
}

.exercise-card-subtitle {
  margin: 4px 0 0;
  color: #475569;
  font-size: 15px;
}

.exercise-card-star {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  background: #fefefe;
  width: 42px;
  height: 42px;
  font-size: 18px;
  cursor: pointer;
}

.exercise-card-tabs {
  display: flex;
  justify-content: flex-start;
  gap: 8px;
  margin-top: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.exercise-card-panel {
  margin-top: 10px;
  padding: 0;
}

.exercise-section-card {
  background: #f9fafb;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  padding: 16px 18px;
  min-height: 190px;
  font-size: 16px;
  line-height: 1.4;
}

.exercise-section-card :deep(*) {
  margin: 0;
  line-height: inherit;
}

.exercise-section-card :deep(p + p),
.exercise-section-card :deep(p + ul),
.exercise-section-card :deep(p + ol),
.exercise-section-card :deep(ul + p),
.exercise-section-card :deep(ol + p),
.exercise-section-card :deep(li + li) {
  margin-top: 4px;
}

.exercise-section-card :deep(ul),
.exercise-section-card :deep(ol) {
  padding-left: 18px;
}

.exercise-section-card :deep(li) {
  padding: 0;
}

.exercise-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 18px;
  padding-bottom: 4px;
  border-bottom: 1px solid #dbeafe;
}

.exercise-tab {
  border: none;
  background: transparent;
  padding: 8px 20px;
  font-weight: 600;
  color: #64748b;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.exercise-tab.active {
  color: #0f172a;
  background: #e0f2fe;
  box-shadow: inset 0 -3px 0 0 #2563eb;
}

.cours-title {
  font-size: clamp(24px, 3vw, 30px);
  color: #193e8e;
  margin: 0 0 8px;
  font-weight: 800;
}

.detail-meta {
  color: #475569;
  font-weight: 600;
  margin: 8px 0 0;
}

.inline-back {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid rgba(25, 62, 142, 0.3);
  background: #f5f8ff;
  color: #193e8e;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.inline-back:hover {
  border-color: #193e8e;
}

.toc-container {
  margin: 12px 0 18px;
  width: 100%;
  border-radius: 24px;
  background: #f5f8ff;
  border: 1px solid rgba(25, 62, 142, 0.12);
  overflow: hidden;
  transform-origin: top left;
}

@media (max-width: 1024px) {
  .toc-container {
    transform: scale(0.96);
  }
}

@media (max-width: 768px) {
  .toc-container {
    transform: scale(0.85);
    margin: 0 auto;
  }

  .toc-header {
    font-size: 0.95rem;
    padding: 6px 14px;
  }

  .toc-body {
    padding: 8px 14px 12px;
  }

  .toc-item {
    font-size: 0.9rem;
  }

  .toc-level-3 .toc-link {
    padding-left: 18px;
    font-size: 0.85rem;
  }
}

.toc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px;
  cursor: pointer;
  color: #1d3b8b;
  font-weight: 600;
  font-size: 16px;
}

.toc-header-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toc-body {
  border-top: 1px solid rgba(25, 62, 142, 0.12);
  padding: 10px 22px 16px;
}

.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toc-item {
  font-size: 16px;
  color: #0f172a;
}

.toc-link {
  text-decoration: none;
  color: #193e8e;
  font-weight: 600;
}

.toc-level-3 .toc-link {
  font-weight: 400;
  color: #1d4ed8;
  padding-left: 24px;
}

.cours-content-outer {
  width: 100%;
  transform-origin: top left;
  transition: transform 0.2s ease;
  overflow-x: hidden;
  margin-top: -8px;
}

.cours-content {
  width: 100%;
  padding: 0 0 40px;
  line-height: 1.75;
  color: #1f2937;
  font-size: 17px;
}

.related-resources {
  margin: 24px 0 28px;
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

.blurred-teaser {
  margin: 24px 0 32px;
  padding: 18px 20px;
  border-radius: 20px;
  border: 1px solid rgba(37, 99, 235, 0.18);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(99, 102, 241, 0.05));
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.blurred-teaser__header h3 {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
}

.blurred-teaser__header p {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.blurred-teaser__content {
  padding: 14px 16px;
  border-radius: 14px;
  background: #ffffff;
  border: 1px dashed rgba(148, 163, 184, 0.5);
  filter: blur(6px);
  user-select: none;
  pointer-events: none;
}

.blurred-teaser__content p {
  margin: 0 0 6px;
  font-size: 14px;
  color: #1f2937;
  line-height: 1.5;
}

.blurred-teaser__content p:last-child {
  margin-bottom: 0;
}

.blurred-teaser__cta {
  align-self: flex-start;
  border: none;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 700;
  font-size: 13px;
  color: #fff;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.25);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.2s ease;
}

.blurred-teaser__cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 28px rgba(37, 99, 235, 0.3);
}

.blurred-teaser__cta:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}

.cours-content :deep(h1),
.cours-content :deep(h2),
.cours-content :deep(h3) {
  color: #0f172a;
  margin-top: 32px;
  border-bottom: 2px solid #3b82f6;
  padding-bottom: 8px;
}

.scroll-top-btn {
  position: fixed;
  bottom: 28px;
  left: 24px;
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: #1d3b8b;
  color: #fff;
  box-shadow: 0 15px 30px rgba(29, 59, 139, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1200;
}

.scroll-top-fade-enter-active,
.scroll-top-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.scroll-top-fade-enter-from,
.scroll-top-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
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
