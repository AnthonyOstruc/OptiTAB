import { faq as homeFaq } from '@/config/homeFaq.js'

const DEFAULT_SITE_NAME = 'OptiTAB'
const DEFAULT_TITLE = 'Plateforme de maths & cours particuliers en ligne'
const DEFAULT_DESCRIPTION =
  'Plateforme de maths & cours particuliers : 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale (Bac), Prepa (MPSI, MP2I, PCSI). Cours, fiches, exercices corriges.'
const DEFAULT_IMAGE_PATH = '/Logo_bg.png'
const DEFAULT_ROBOTS_INDEX =
  'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1'
const DEFAULT_ROBOTS_NOINDEX = 'noindex,follow'

function normalizeSiteUrl(raw) {
  const value = String(raw || '').trim()
  if (!value) return ''
  return value.replace(/\/+$/, '')
}

function getSiteBaseUrl() {
  const fromEnv = normalizeSiteUrl(import.meta?.env?.VITE_SITE_URL)
  if (fromEnv) return fromEnv
  if (typeof window !== 'undefined' && window.location?.origin) return window.location.origin
  return 'https://optitab.net'
}

function removeTrailingSlash(value) {
  if (!value) return value
  if (value.length <= 1) return value
  return value.replace(/\/+$/, '')
}

function hasQueryParams(query) {
  if (!query || typeof query !== 'object') return false
  return Object.keys(query).length > 0
}

export function getRobotsForRoute({ route, noindex = false } = {}) {
  const hasQuery = hasQueryParams(route?.query)
  if (noindex || hasQuery) return DEFAULT_ROBOTS_NOINDEX
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
    const base = getSiteBaseUrl()
    const url = new URL(raw, base)
    url.search = ''
    url.hash = ''
    url.pathname = url.pathname || '/'
    if (url.pathname.length > 1) {
      url.pathname = url.pathname.replace(/\/+$/, '')
    }
    return `${url.origin}${url.pathname}`
  } catch (_) {
    return ''
  }
}

function canonicalizePath(pathLike) {
  if (!pathLike) return '/'
  try {
    const base = (typeof window !== 'undefined' && window.location?.origin) ? window.location.origin : 'https://optitab.net'
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
  if (/^https?:\/\//i.test(raw)) return raw
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


function buildBreadcrumbJsonLd(items) {
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

export function setPageSeo({
  title,
  description,
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
  const finalRobots = String(robots || DEFAULT_ROBOTS_INDEX).trim()

  const normalizedCanonicalUrl = normalizeCanonicalUrl(canonicalUrl)

  const path = canonicalizePath(canonicalPath || normalizedCanonicalUrl || '/')
  const finalCanonical = removeTrailingSlash(String(normalizedCanonicalUrl || `${getSiteBaseUrl()}${path}`).trim()) || `${getSiteBaseUrl()}${path}`

  const finalImage = toAbsoluteUrl(image || DEFAULT_IMAGE_PATH)
  const finalOgType = String(ogType || 'website').trim() || 'website'

  document.title = finalTitle
  ensureMeta('name', 'description', finalDescription)
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
    title: 'Cours particuliers de maths en ligne (6e-Prepa)',
    description:
      'Cours particuliers de maths en ligne : 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale (Bac), Prepa (MPSI, MP2I, PCSI). Professeurs experts, suivi.',
    canonicalPath: '/cours-particuliers'
  },
  FreeCourses: {
    title: 'Cours de maths gratuits (6e-Prepa, Brevet, Bac)',
    description:
      'Cours de maths gratuits : 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale, Prepa (MPSI, MP2I, PCSI). Methodes, exemples, exercices.',
    canonicalPath: '/ressources-gratuites/cours'
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
    title: 'Exercices de maths corriges (6e-Prepa)',
    description:
      'Exercices de maths corriges : 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale (Bac), Prepa (MPSI, MP2I, PCSI). Methode + correction.',
    canonicalPath: '/ressources-gratuites/exercices'
  },
  FreeExerciseDetail: {
    title: 'Exercice de maths corrigé',
    description: 'Exercice de maths gratuit avec correction, methode et explications.',
    ogType: 'article'
  },
  FreeSummaries: {
    title: 'Fiches de revision de maths (6e-Prepa)',
    description:
      'Fiches de revision de maths : formules, methodes, exemples - 6e, 5e, 4e, 3e (Brevet), 2nde, 1re, Terminale (Bac), Prepa (MPSI, MP2I, PCSI).',
    canonicalPath: '/ressources-gratuites/syntheses'
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
    title: 'Tarifs OptiTAB : abonnement maths en ligne',
    description: 'Tarifs OptiTAB : abonnement mensuel sans engagement pour acceder aux cours, exercices corriges et fiches de synthese. Paiement securise, annulation a tout moment.',
    canonicalPath: '/tarifs'
  },
  FreeResourcesHome: {
    title: 'Ressources gratuites de maths',
    description: 'Cours gratuits, exercices corriges et fiches de synthese pour reviser efficacement du college a la prepa. Acces libre sur OptiTAB.',
    canonicalPath: '/ressources-gratuites',
    faq: homeFaq
  },
  CGV: { title: 'CGV', canonicalPath: '/cgv', noindex: true },
  CGU: { title: 'CGU', canonicalPath: '/cgu', noindex: true },
  Confidentialite: { title: 'Confidentialité', canonicalPath: '/confidentialite', noindex: true },
  Legal: { title: 'Mentions légales', canonicalPath: '/legal', noindex: true },
  Cookies: { title: 'Cookies', canonicalPath: '/cookies', noindex: true },
  Conditions: { title: 'Conditions', canonicalPath: '/conditions', noindex: true }
}

const NOINDEX_ROUTE_NAMES = new Set([
  'PasswordReset',
  'NotFound'
])

export function applyRouteSeo(route) {
  try {
    const name = route?.name ? String(route.name) : ''
    const routeSeo = ROUTE_SEO[name] || {}

    const requiresAuth = Boolean(route?.meta?.requiresAuth || route?.meta?.requiresAdmin || route?.meta?.requiresSubscription)
    const isConfiguredNoIndex = Boolean(routeSeo.noindex)
    const isSystemNoIndex = requiresAuth || NOINDEX_ROUTE_NAMES.has(name)
    const shouldNoIndex = isConfiguredNoIndex || isSystemNoIndex
    const robots = getRobotsForRoute({ route, noindex: shouldNoIndex })

    const breadcrumbs = Array.isArray(routeSeo.breadcrumbs) ? [...routeSeo.breadcrumbs] : []
    if (breadcrumbs.length === 0 && !['Home', 'NotFound'].includes(name)) {
      if (routeSeo.canonicalPath) {
        breadcrumbs.push({ name: 'Accueil', item: '/' })
        if (routeSeo.canonicalPath !== '/') {
          const label = String(routeSeo.breadcrumbLabel || routeSeo.title || '')
            .replace(/^OptiTAB\s*-\s*/i, '')
            .trim()
          if (label) {
            breadcrumbs.push({ name: label, item: routeSeo.canonicalPath })
          }
        }
      }
    }

    const breadcrumbGraph = buildBreadcrumbJsonLd(breadcrumbs)
    const faqGraph = buildFaqJsonLd(routeSeo.faq)
    const extraGraph = Array.isArray(routeSeo.jsonLdGraph) ? routeSeo.jsonLdGraph : []
    const jsonLdGraph = [breadcrumbGraph, faqGraph, ...extraGraph].filter(Boolean)

    setPageSeo({
      title: routeSeo.title || DEFAULT_TITLE,
      description: routeSeo.description || DEFAULT_DESCRIPTION,
      canonicalPath: routeSeo.canonicalPath || route?.path || '/',
      robots,
      ogType: routeSeo.ogType || 'website',
      image: routeSeo.image || DEFAULT_IMAGE_PATH,
      jsonLdGraph
    })
  } catch (_) {
    // Never block navigation on SEO updates.
  }
}

