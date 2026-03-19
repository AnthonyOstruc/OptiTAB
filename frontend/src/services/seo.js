import { faq as homeFaq } from '@/config/homeFaq.js'
import { FREE_RESOURCES_FAQ_BY_ROUTE } from '@/config/freeResourcesAuthority'
import { getManualSeoOverrideByPath } from '@/config/manualSeoOverrides'

const DEFAULT_SITE_NAME = 'OptiTAB'
const DEFAULT_TITLE = 'Plateforme de maths & cours particuliers en ligne'
const DEFAULT_DESCRIPTION =
  'Plateforme de maths & cours particuliers : 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale (Bac), Prepa (MPSI, MP2I, PCSI). Cours, fiches, exercices corriges.'
const DEFAULT_KEYWORDS = [
  'cours de maths',
  'cours de maths gratuits',
  'exercices corriges maths',
  'fiches de revision maths',
  'brevet maths',
  'bac maths',
  'prepa maths'
].join(', ')
const DEFAULT_IMAGE_PATH = '/Logo_bg.png'
const DEFAULT_ROBOTS_INDEX =
  'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1'
const DEFAULT_ROBOTS_NOINDEX = 'noindex,follow'
const CANONICAL_SITE_ORIGIN = 'https://www.optitab.net'
const CANONICAL_SITE_HOSTS = new Set(['optitab.net', 'www.optitab.net'])

const TRACKING_QUERY_KEYS = new Set([
  'gclid',
  'dclid',
  'gbraid',
  'wbraid',
  'fbclid',
  'msclkid',
  'igshid',
  '_gl',
  '_ga'
])

function normalizeSiteUrl(raw) {
  const value = String(raw || '').trim()
  if (!value) return ''
  try {
    const url = new URL(value)
    const hostname = String(url.hostname || '').toLowerCase()
    if (CANONICAL_SITE_HOSTS.has(hostname)) {
      return CANONICAL_SITE_ORIGIN
    }
    return String(url.origin || '').replace(/\/+$/, '')
  } catch (_) {
    return value.replace(/\/+$/, '')
  }
}

function getSiteBaseUrl() {
  const fromEnv = normalizeSiteUrl(import.meta?.env?.VITE_SITE_URL)
  if (fromEnv) return fromEnv
  return CANONICAL_SITE_ORIGIN
}

function removeTrailingSlash(value) {
  if (!value) return value
  if (value.length <= 1) return value
  return value.replace(/\/+$/, '')
}

function isTrackingQueryKey(key) {
  const k = String(key || '').trim().toLowerCase()
  if (!k) return false
  if (k.startsWith('utm_')) return true
  return TRACKING_QUERY_KEYS.has(k)
}

function analyzeQuery(query) {
  if (!query || typeof query !== 'object') {
    return { hasAny: false, hasTracking: false, hasNonTracking: false }
  }

  const keys = Object.keys(query).filter(Boolean)
  const hasAny = keys.length > 0
  if (!hasAny) {
    return { hasAny: false, hasTracking: false, hasNonTracking: false }
  }

  let hasTracking = false
  let hasNonTracking = false
  for (const key of keys) {
    if (isTrackingQueryKey(key)) {
      hasTracking = true
    } else {
      hasNonTracking = true
    }
    if (hasTracking && hasNonTracking) break
  }

  return { hasAny, hasTracking, hasNonTracking }
}

export function getRobotsForRoute({ route, noindex = false } = {}) {
  if (noindex) return DEFAULT_ROBOTS_NOINDEX
  const { hasNonTracking } = analyzeQuery(route?.query)
  if (hasNonTracking) return DEFAULT_ROBOTS_NOINDEX
  return DEFAULT_ROBOTS_INDEX
}

function ensureMeta(attr, key, content) {
  if (typeof document === 'undefined') return
  if (!key) return
  const safeKey = String(key).replaceAll('"', '\\"')
  const selector = `meta[${attr}="${safeKey}"]`
  let el = document.querySelector(selector)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, String(key))
    document.head.appendChild(el)
  }
  if (typeof content === 'string') {
    el.setAttribute('content', content)
  }
}

function ensureLink(rel, href) {
  if (typeof document === 'undefined') return
  const safeRel = String(rel).replaceAll('"', '\\"')
  const selector = `link[rel="${safeRel}"]`
  let el = document.querySelector(selector)
  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', rel)
    document.head.appendChild(el)
  }
  if (typeof href === 'string') {
    el.setAttribute('href', href)
  }
}

function ensureJsonLd(id, jsonObject) {
  if (typeof document === 'undefined') return
  const scriptId = String(id || 'seo-jsonld')
  const existing = document.getElementById(scriptId)

  if (!jsonObject) {
    if (existing && existing.parentNode) {
      existing.parentNode.removeChild(existing)
    }
    return
  }

  let el = existing
  if (!el) {
    el = document.createElement('script')
    el.type = 'application/ld+json'
    el.id = scriptId
    document.head.appendChild(el)
  }

  try {
    el.textContent = JSON.stringify(jsonObject)
  } catch (_) {
    el.textContent = ''
  }
}


function normalizeCanonicalUrl(rawUrl) {
  const raw = String(rawUrl || '').trim()
  if (!raw) return ''
  try {
    const siteBase = getSiteBaseUrl()
    const url = new URL(raw, siteBase)
    url.search = ''
    url.hash = ''
    let pathname = url.pathname || '/'
    if (pathname.length > 1) {
      pathname = pathname.replace(/\/+$/, '')
    }
    const safePath = pathname.startsWith('/') ? pathname : `/${pathname}`
    return `${siteBase}${safePath}`
  } catch (_) {
    return ''
  }
}

function canonicalizePath(pathLike) {
  if (!pathLike) return '/'
  try {
    const base = getSiteBaseUrl()
    const url = new URL(String(pathLike), base)
    let pathname = url.pathname || '/'
    if (pathname.length > 1) {
      pathname = pathname.replace(/\/+$/, '')
    }
    return pathname
  } catch (_) {
    const raw = String(pathLike)
    if (!raw.startsWith('/')) return `/${raw}`
    return raw
  }
}

function buildTitle(title) {
  const value = String(title || '').trim()
  if (!value) return `${DEFAULT_SITE_NAME} - ${DEFAULT_TITLE}`
  if (/optitab/i.test(value)) return value
  return `${DEFAULT_SITE_NAME} - ${value}`
}

function toAbsoluteUrl(maybeUrlOrPath) {
  const raw = String(maybeUrlOrPath || '').trim()
  if (!raw) return ''
  if (/^https?:\/\//i.test(raw)) {
    try {
      const url = new URL(raw)
      const hostname = String(url.hostname || '').toLowerCase()
      if (CANONICAL_SITE_HOSTS.has(hostname)) {
        return `${CANONICAL_SITE_ORIGIN}${url.pathname}${url.search}${url.hash}`
      }
      return raw
    } catch (_) {
      return raw
    }
  }
  return `${getSiteBaseUrl()}${raw.startsWith('/') ? '' : '/'}${raw}`
}

export function buildFaqJsonLd(items) {
  if (!Array.isArray(items) || items.length === 0) return null
  const entities = items
    .map((item) => {
      const question = String(item?.question || '').trim()
      const answer = String(item?.answer || '').trim()
      if (!question || !answer) return null
      return {
        '@type': 'Question',
        name: question,
        acceptedAnswer: {
          '@type': 'Answer',
          text: answer
        }
      }
    })
    .filter(Boolean)
    .slice(0, 10)

  if (entities.length === 0) return null
  return {
    '@type': 'FAQPage',
    mainEntity: entities
  }
}

function toEntityReference(entity) {
  if (!entity) return undefined
  if (typeof entity === 'string') {
    const id = String(entity).trim()
    return id ? { '@id': id } : undefined
  }
  if (typeof entity === 'object') return entity
  return undefined
}

function normalizeImageArray(image) {
  if (Array.isArray(image)) {
    const urls = image
      .map((item) => toAbsoluteUrl(item))
      .filter(Boolean)
    return urls.length ? urls : undefined
  }
  const single = toAbsoluteUrl(image)
  return single ? [single] : undefined
}

function normalizeKeywords(keywords) {
  if (Array.isArray(keywords)) {
    const values = keywords
      .map((value) => String(value || '').trim())
      .filter(Boolean)
    return values.length ? values.join(', ') : undefined
  }
  const value = String(keywords || '').trim()
  return value || undefined
}

export function buildBreadcrumbJsonLd(items) {
  if (!Array.isArray(items) || items.length === 0) return null
  const list = items
    .map((item, index) => {
      const name = String(item?.name || item?.label || '').trim()
      const url = String(item?.item || item?.url || item?.to || '').trim()
      if (!name || !url) return null
      return {
        '@type': 'ListItem',
        position: index + 1,
        name,
        item: toAbsoluteUrl(url)
      }
    })
    .filter(Boolean)
  if (!list.length) return null
  return {
    '@type': 'BreadcrumbList',
    itemListElement: list
  }
}

export function buildArticleJsonLd({
  id,
  url,
  headline,
  description,
  inLanguage = 'fr-FR',
  isPartOf,
  mainEntityOfPage,
  author,
  publisher,
  image,
  datePublished,
  dateModified,
  keywords
} = {}) {
  const finalHeadline = String(headline || '').trim()
  const finalUrl = toAbsoluteUrl(url)
  if (!finalHeadline || !finalUrl) return null

  return {
    '@type': 'Article',
    '@id': String(id || `${finalUrl}#article`).trim(),
    headline: finalHeadline,
    description: String(description || '').trim() || undefined,
    inLanguage: String(inLanguage || '').trim() || undefined,
    url: finalUrl,
    isPartOf: toEntityReference(isPartOf),
    mainEntityOfPage: toEntityReference(mainEntityOfPage),
    author: toEntityReference(author),
    publisher: toEntityReference(publisher),
    image: normalizeImageArray(image),
    datePublished: String(datePublished || '').trim() || undefined,
    dateModified: String(dateModified || '').trim() || undefined,
    keywords: normalizeKeywords(keywords)
  }
}

export function buildCourseJsonLd({
  id,
  url,
  name,
  description,
  inLanguage = 'fr-FR',
  provider,
  isPartOf,
  mainEntityOfPage,
  image,
  dateModified,
  educationalLevel,
  keywords,
  about
} = {}) {
  const finalName = String(name || '').trim()
  const finalUrl = toAbsoluteUrl(url)
  if (!finalName || !finalUrl) return null

  return {
    '@type': 'Course',
    '@id': String(id || `${finalUrl}#course`).trim(),
    name: finalName,
    description: String(description || '').trim() || undefined,
    url: finalUrl,
    inLanguage: String(inLanguage || '').trim() || undefined,
    provider: toEntityReference(provider),
    isPartOf: toEntityReference(isPartOf),
    mainEntityOfPage: toEntityReference(mainEntityOfPage),
    image: normalizeImageArray(image),
    dateModified: String(dateModified || '').trim() || undefined,
    educationalLevel: String(educationalLevel || '').trim() || undefined,
    keywords: normalizeKeywords(keywords),
    about: String(about || '').trim() || undefined
  }
}

export function buildCreativeWorkJsonLd({
  id,
  url,
  name,
  description,
  inLanguage = 'fr-FR',
  author,
  publisher,
  isPartOf,
  mainEntityOfPage,
  image,
  dateModified,
  learningResourceType,
  educationalLevel,
  keywords,
  about
} = {}) {
  const finalName = String(name || '').trim()
  const finalUrl = toAbsoluteUrl(url)
  if (!finalName || !finalUrl) return null

  return {
    '@type': 'CreativeWork',
    '@id': String(id || `${finalUrl}#creativework`).trim(),
    name: finalName,
    description: String(description || '').trim() || undefined,
    url: finalUrl,
    inLanguage: String(inLanguage || '').trim() || undefined,
    author: toEntityReference(author),
    publisher: toEntityReference(publisher),
    isPartOf: toEntityReference(isPartOf),
    mainEntityOfPage: toEntityReference(mainEntityOfPage),
    image: normalizeImageArray(image),
    dateModified: String(dateModified || '').trim() || undefined,
    learningResourceType: String(learningResourceType || '').trim() || undefined,
    educationalLevel: String(educationalLevel || '').trim() || undefined,
    keywords: normalizeKeywords(keywords),
    about: String(about || '').trim() || undefined
  }
}

export function buildEducationalOccupationalProgramJsonLd({
  id,
  url,
  name,
  description,
  inLanguage = 'fr-FR',
  provider,
  isPartOf,
  mainEntityOfPage,
  educationalLevel,
  occupationalCategory,
  timeToComplete,
  image,
  keywords
} = {}) {
  const finalName = String(name || '').trim()
  const finalUrl = toAbsoluteUrl(url)
  if (!finalName || !finalUrl) return null

  return {
    '@type': 'EducationalOccupationalProgram',
    '@id': String(id || `${finalUrl}#program`).trim(),
    name: finalName,
    description: String(description || '').trim() || undefined,
    url: finalUrl,
    inLanguage: String(inLanguage || '').trim() || undefined,
    provider: toEntityReference(provider),
    isPartOf: toEntityReference(isPartOf),
    mainEntityOfPage: toEntityReference(mainEntityOfPage),
    educationalLevel: String(educationalLevel || '').trim() || undefined,
    occupationalCategory: String(occupationalCategory || '').trim() || undefined,
    timeToComplete: String(timeToComplete || '').trim() || undefined,
    image: normalizeImageArray(image),
    keywords: normalizeKeywords(keywords)
  }
}

export function setPageSeo({
  title,
  description,
  keywords,
  robots,
  canonicalPath,
  canonicalUrl,
  ogType,
  image,
  jsonLdGraph
} = {}) {
  if (typeof document === 'undefined') return

  const finalTitle = buildTitle(title)
  const finalDescription = String(description || DEFAULT_DESCRIPTION).trim() || DEFAULT_DESCRIPTION
  const finalKeywords = normalizeKeywords(keywords) || DEFAULT_KEYWORDS
  const finalRobots = String(robots || DEFAULT_ROBOTS_INDEX).trim()

  const normalizedCanonicalUrl = normalizeCanonicalUrl(canonicalUrl)

  const path = canonicalizePath(canonicalPath || normalizedCanonicalUrl || '/')
  const finalCanonical = removeTrailingSlash(String(normalizedCanonicalUrl || `${getSiteBaseUrl()}${path}`).trim()) || `${getSiteBaseUrl()}${path}`

  const finalImage = toAbsoluteUrl(image || DEFAULT_IMAGE_PATH)
  const finalOgType = String(ogType || 'website').trim() || 'website'

  document.title = finalTitle
  ensureMeta('name', 'description', finalDescription)
  ensureMeta('name', 'keywords', finalKeywords)
  ensureMeta('name', 'robots', finalRobots)

  ensureLink('canonical', finalCanonical)

  ensureMeta('property', 'og:site_name', DEFAULT_SITE_NAME)
  ensureMeta('property', 'og:locale', 'fr_FR')
  ensureMeta('property', 'og:type', finalOgType)
  ensureMeta('property', 'og:title', finalTitle)
  ensureMeta('property', 'og:description', finalDescription)
  ensureMeta('property', 'og:url', finalCanonical)
  if (finalImage) {
    ensureMeta('property', 'og:image', finalImage)
  }

  ensureMeta('name', 'twitter:card', 'summary_large_image')
  ensureMeta('name', 'twitter:title', finalTitle)
  ensureMeta('name', 'twitter:description', finalDescription)
  if (finalImage) {
    ensureMeta('name', 'twitter:image', finalImage)
  }

  try {
    const siteUrl = getSiteBaseUrl()
    const organizationId = `${siteUrl}/#organization`
    const websiteId = `${siteUrl}/#website`
    const webPageId = `${finalCanonical}#webpage`

    const extraGraph = Array.isArray(jsonLdGraph) ? jsonLdGraph.filter(Boolean) : []

    ensureJsonLd('seo-jsonld', {
      '@context': 'https://schema.org',
      '@graph': [
        {
          '@type': 'Organization',
          '@id': organizationId,
          name: DEFAULT_SITE_NAME,
          url: siteUrl,
          email: 'contact@optitab.net',
          telephone: '+33764040251',
          contactPoint: [
            {
              '@type': 'ContactPoint',
              contactType: 'customer support',
              telephone: '+33764040251',
              email: 'contact@optitab.net',
              areaServed: 'FR',
              availableLanguage: ['fr']
            }
          ],
          logo: {
            '@type': 'ImageObject',
            url: toAbsoluteUrl(DEFAULT_IMAGE_PATH)
          }
        },
        {
          '@type': 'WebSite',
          '@id': websiteId,
          url: siteUrl,
          name: DEFAULT_SITE_NAME,
          publisher: { '@id': organizationId },
          inLanguage: 'fr-FR'
        },
        {
          '@type': 'WebPage',
          '@id': webPageId,
          url: finalCanonical,
          name: finalTitle,
          description: finalDescription,
          isPartOf: { '@id': websiteId },
          inLanguage: 'fr-FR'
        },
        ...extraGraph
      ]
    })
  } catch (_) {
    // Never block rendering on JSON-LD.
  }
}

const ROUTE_SEO = {
  Home: {
    title: DEFAULT_TITLE,
    description: DEFAULT_DESCRIPTION,
    canonicalPath: '/',
    jsonLdGraph: (() => {
      const faqGraph = buildFaqJsonLd(homeFaq)
      return faqGraph ? [faqGraph] : undefined
    })()
  },
  CoursParticuliers: {
    title: 'Cours particuliers de maths en ligne du college a la prepa | OptiTAB',
    description:
      'Cours particuliers de maths en ligne de la 6e a la prepa : explications claires, suivi regulier, exercices cibles et accompagnement pas a pas.',
    canonicalPath: '/cours-particuliers'
  },
  FreeCourses: {
    title: 'Cours de maths gratuits du college a la prepa | OptiTAB',
    description:
      'Comprends chaque notion avec des cours de maths clairs, methodes et exemples concrets pour college, lycee, bac et prepa.',
    canonicalPath: '/ressources-gratuites/cours',
    faq: FREE_RESOURCES_FAQ_BY_ROUTE.FreeCourses
  },
  FreeCourseDetail: {
    title: 'Cours gratuit de maths',
    description: 'Cours de maths gratuit : explications, exemples et exercices corriges.',
    ogType: 'article'
  },
  FreeCourseSlug: {
    title: 'Cours gratuit de maths',
    description: 'Cours de maths gratuit : explications, exemples et exercices corriges.',
    ogType: 'article'
  },
  FreeCourseSlugGrouped: {
    title: 'Cours gratuit de maths',
    description: 'Cours de maths gratuit : explications, exemples et exercices corriges.',
    ogType: 'article'
  },
  FreeExercises: {
    title: 'Exercices corriges de maths du college a la prepa | OptiTAB',
    description:
      'Entraine-toi avec des exercices de maths corriges pas a pas pour progresser en methode, du college a la prepa.',
    canonicalPath: '/ressources-gratuites/exercices',
    faq: FREE_RESOURCES_FAQ_BY_ROUTE.FreeExercises
  },
  FreeExerciseDetail: {
    title: 'Exercice de maths corrige',
    description: 'Exercice de maths gratuit avec correction, methode et explications.',
    ogType: 'article'
  },
  FreeSummaries: {
    title: 'Fiches de revision de maths du college a la prepa | OptiTAB',
    description:
      'Revise vite avec des fiches de maths claires: formules, methodes et points essentiels pour college, lycee, bac et prepa.',
    canonicalPath: '/ressources-gratuites/syntheses',
    faq: FREE_RESOURCES_FAQ_BY_ROUTE.FreeSummaries
  },
  FreeSummaryDetail: {
    title: 'Fiche de revision de maths',
    description: 'Fiche de synthese gratuite : formules, methodes et exemples pour reviser vite.',
    ogType: 'article'
  },
  FreeSummarySlug: {
    title: 'Fiche de revision de maths',
    description: 'Fiche de synthese gratuite : formules, methodes et exemples pour reviser vite.',
    ogType: 'article'
  },
  FreeSummarySlugGrouped: {
    title: 'Fiche de revision de maths',
    description: 'Fiche de synthese gratuite : formules, methodes et exemples pour reviser vite.',
    ogType: 'article'
  },
  About: {
    title: 'La methode : cours particuliers & plateforme maths',
    description:
      'OptiTAB combine plateforme de maths et cours particuliers : 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale (Bac), Prepa (MPSI, MP2I, PCSI).',
    canonicalPath: '/about'
  },
  Contact: {
    title: 'Contact : WhatsApp & email',
    description: 'Contactez OptiTAB (WhatsApp ou email) pour un cours particulier ou une question. Reponse rapide 7j/7.',
    canonicalPath: '/contact'
  },
  TarifsPage: {
    title: 'Tarifs abonnement maths en ligne sans engagement | OptiTAB',
    description: 'Decouvre les tarifs OptiTAB pour acceder aux cours de maths, exercices corriges et fiches de synthese, avec annulation a tout moment.',
    canonicalPath: '/tarifs'
  },
  GoogleAdsLanding: {
    title: 'Plateforme de maths en ligne — Cours, fiches et exercices corriges | OptiTAB',
    description: 'Abonne-toi a OptiTAB : cours de maths structures, fiches de synthese et exercices corriges pas a pas du lycee. Sans engagement, acces immediat.',
    canonicalPath: '/plateforme-maths'
  },
  ExercicesCorrigesLanding: {
    title: 'Exercices corriges pas a pas : comprendre chaque etape | OptiTAB',
    description: 'Des exercices corriges etape par etape pour comprendre la methode, debloquer les exercices et progresser plus vite.',
    canonicalPath: '/exercices-corriges'
  },
  FreeResourcesHome: {
    title: 'Ressources gratuites de maths: cours, exercices corriges et fiches | OptiTAB',
    description: 'Accede a des cours de maths gratuits, des exercices corriges pas a pas et des fiches de revision pour college, lycee et prepa.',
    keywords: [
      'ressources gratuites maths',
      'cours de maths gratuits',
      'exercices corriges maths',
      'fiches de revision maths',
      'reviser brevet maths',
      'reviser bac maths'
    ],
    canonicalPath: '/ressources-gratuites',
    faq: FREE_RESOURCES_FAQ_BY_ROUTE.FreeResourcesHome,
    jsonLdGraph: [
      {
        '@type': 'ItemList',
        '@id': `${toAbsoluteUrl('/ressources-gratuites')}#resource-types`,
        name: 'Formats de ressources gratuites de maths',
        itemListOrder: 'https://schema.org/ItemListOrderAscending',
        numberOfItems: 3,
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Cours de maths gratuits',
            item: toAbsoluteUrl('/ressources-gratuites/cours')
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Exercices corriges de maths',
            item: toAbsoluteUrl('/ressources-gratuites/exercices')
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: 'Fiches de revision de maths',
            item: toAbsoluteUrl('/ressources-gratuites/syntheses')
          }
        ]
      }
    ]
  },
  CGV: { title: 'CGV', canonicalPath: '/cgv', noindex: true },
  CGU: { title: 'CGU', canonicalPath: '/cgu', noindex: true },
  Confidentialite: { title: 'Confidentialite', canonicalPath: '/confidentialite', noindex: true },
  Legal: { title: 'Mentions legales', canonicalPath: '/legal', noindex: true },
  Cookies: { title: 'Cookies', canonicalPath: '/cookies', noindex: true },
  Conditions: { title: 'Conditions', canonicalPath: '/conditions', noindex: true }
}

const NOINDEX_ROUTE_NAMES = new Set([
  'PasswordReset',
  'NotFound',
  'Calculator',
  'TestFiltrageStrict'
])

export function applyRouteSeo(route) {
  try {
    const name = route?.name ? String(route.name) : ''
    const routeSeo = ROUTE_SEO[name] || {}
    const routePath = canonicalizePath(route?.path || '/')
    const routeCanonicalPath = routeSeo.canonicalPath || routePath
    const manualSeoByCanonical = getManualSeoOverrideByPath(routeCanonicalPath)
    const manualSeoByPath = getManualSeoOverrideByPath(routePath)
    const manualSeo = manualSeoByCanonical || manualSeoByPath || null
    const resolvedSeo = manualSeo ? { ...routeSeo, ...manualSeo } : routeSeo
    const inferredCanonicalPath = resolvedSeo.canonicalPath || routeCanonicalPath

    const requiresAuth = Boolean(route?.meta?.requiresAuth || route?.meta?.requiresAdmin || route?.meta?.requiresSubscription)
    const isConfiguredNoIndex = Boolean(resolvedSeo.noindex)
    const isSystemNoIndex = requiresAuth || NOINDEX_ROUTE_NAMES.has(name)
    const slugParam = String(route?.params?.slug || '')
    // Suppression de la logique qui interdit l'indexation des exercices corrigés
    const shouldNoIndex = isConfiguredNoIndex || isSystemNoIndex
    const robots = getRobotsForRoute({ route, noindex: shouldNoIndex })

    const routeMetaBreadcrumbs = Array.isArray(route?.meta?.breadcrumbs) ? route.meta.breadcrumbs : []
    const breadcrumbs = Array.isArray(resolvedSeo.breadcrumbs) && resolvedSeo.breadcrumbs.length
      ? [...resolvedSeo.breadcrumbs]
      : [...routeMetaBreadcrumbs]
    if (breadcrumbs.length === 0 && !['Home', 'NotFound'].includes(name)) {
      if (inferredCanonicalPath) {
        breadcrumbs.push({ name: 'Accueil', item: '/' })
        if (inferredCanonicalPath !== '/') {
          const label = String(resolvedSeo.breadcrumbLabel || resolvedSeo.title || '')
            .replace(/^OptiTAB\s*-\s*/i, '')
            .trim()
          if (label) {
            breadcrumbs.push({ name: label, item: inferredCanonicalPath })
          }
        }
      }
    }

    const routeMetaFaq = Array.isArray(route?.meta?.faq) ? route.meta.faq : []
    const faqItems = Array.isArray(resolvedSeo.faq) && resolvedSeo.faq.length ? resolvedSeo.faq : routeMetaFaq
    const breadcrumbGraph = buildBreadcrumbJsonLd(breadcrumbs)
    const faqGraph = buildFaqJsonLd(faqItems)
    const extraGraph = Array.isArray(resolvedSeo.jsonLdGraph) ? resolvedSeo.jsonLdGraph : []
    const finalCanonical = toAbsoluteUrl(inferredCanonicalPath || '/')
    const websiteId = `${getSiteBaseUrl()}/#website`
    const webPageId = `${finalCanonical}#webpage`
    const organizationId = `${getSiteBaseUrl()}/#organization`

    const articleMeta = route?.meta?.article && typeof route.meta.article === 'object'
      ? route.meta.article
      : {}
    const hasArticleGraphAlready = extraGraph.some((graph) => String(graph?.['@type'] || '').toLowerCase() === 'article')
    const looksLikeEditorialPath = /^\/(?:blog|articles)(?:\/|$)/i.test(routePath)
    const shouldAttachArticle = !hasArticleGraphAlready && !shouldNoIndex && (looksLikeEditorialPath || Boolean(resolvedSeo.article || route?.meta?.article))
    const articleGraph = shouldAttachArticle
      ? buildArticleJsonLd({
          id: articleMeta.id || `${finalCanonical}#article`,
          url: finalCanonical,
          headline: articleMeta.headline || resolvedSeo.title || DEFAULT_TITLE,
          description: articleMeta.description || resolvedSeo.description || DEFAULT_DESCRIPTION,
          datePublished: articleMeta.datePublished,
          dateModified: articleMeta.dateModified,
          image: articleMeta.image || resolvedSeo.image || DEFAULT_IMAGE_PATH,
          author: articleMeta.author || { '@id': organizationId },
          publisher: articleMeta.publisher || { '@id': organizationId },
          isPartOf: { '@id': websiteId },
          mainEntityOfPage: { '@id': webPageId }
        })
      : null

    const jsonLdGraph = [breadcrumbGraph, faqGraph, articleGraph, ...extraGraph].filter(Boolean)

    setPageSeo({
      title: resolvedSeo.title || DEFAULT_TITLE,
      description: resolvedSeo.description || DEFAULT_DESCRIPTION,
      keywords: resolvedSeo.keywords,
      canonicalPath: inferredCanonicalPath,
      robots,
      ogType: resolvedSeo.ogType || 'website',
      image: resolvedSeo.image || DEFAULT_IMAGE_PATH,
      jsonLdGraph
    })
  } catch (_) {
    // Never block navigation on SEO updates.
  }
}

