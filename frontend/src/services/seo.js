import { faq as homeFaq } from '@/config/homeFaq.js'

const DEFAULT_SITE_NAME = 'OptiTAB'
const DEFAULT_TITLE = 'OptiTAB | Cours particuliers en ligne & plateforme de maths'
const DEFAULT_DESCRIPTION =
  'OptiTAB : cours particuliers en ligne (maths, physique‑chimie, informatique) et plateforme de maths par abonnement. Cours, fiches de synthèse, exercices corrigés — du collège à l’université.'
const DEFAULT_IMAGE_PATH = '/Logo_bg.png'

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
  if (!value) return DEFAULT_TITLE
  if (/optitab/i.test(value)) return value
  return `${value} | ${DEFAULT_SITE_NAME}`
}

function toAbsoluteUrl(maybeUrlOrPath) {
  const raw = String(maybeUrlOrPath || '').trim()
  if (!raw) return ''
  if (/^https?:\/\//i.test(raw)) return raw
  return `${getSiteBaseUrl()}${raw.startsWith('/') ? '' : '/'}${raw}`
}

function buildFaqJsonLd(items) {
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
  const finalRobots = String(robots || 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1').trim()

  const path = canonicalizePath(canonicalPath || canonicalUrl || '/')
  const finalCanonical = String(canonicalUrl || `${getSiteBaseUrl()}${path}`).trim()

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
    title: 'Cours particuliers en ligne (maths, physique‑chimie, informatique)',
    description:
      'Soutien scolaire en ligne : cours particuliers et aide aux devoirs en maths, physique‑chimie et informatique — collège, lycée, prépa, université.',
    canonicalPath: '/cours-particuliers'
  },
  FreeCourses: {
    title: 'Cours de maths en ligne gratuits (Seconde, Première, Terminale)',
    description: 'Cours de maths gratuits : chapitres clairs, méthodes, exemples et exercices — collège et lycée (Seconde, Première, Terminale).',
    canonicalPath: '/ressources-gratuites/cours'
  },
  FreeCourseDetail: {
    title: 'Cours gratuit - OptiTAB',
    description: 'Cours gratuit à consulter en ligne : explications, exemples et exercices.',
    ogType: 'article'
  },
  FreeExercises: {
    title: 'Exercices corrigés de maths gratuits (Seconde, Première, Terminale)',
    description: 'Exercices corrigés de maths gratuits (Terminale, Première, Seconde) : dérivées, limites, suites, probabilités… avec correction et méthode.',
    canonicalPath: '/ressources-gratuites/exercices'
  },
  FreeExerciseDetail: {
    title: 'Exercice gratuit - OptiTAB',
    description: 'Exercice gratuit avec correction et explications.',
    ogType: 'article'
  },
  FreeSummaries: {
    title: 'Fiches de révision de maths gratuites (synthèses)',
    description: 'Fiches de synthèse gratuites de maths : définitions, formules et méthodes — collège, lycée, prépa.',
    canonicalPath: '/ressources-gratuites/syntheses'
  },
  FreeSummaryDetail: {
    title: 'Fiche gratuite - OptiTAB',
    description: 'Fiche de synthèse gratuite pour réviser rapidement : formules, méthodes et exemples.',
    ogType: 'article'
  },
  About: {
    title: 'A propos - OptiTAB',
    description: "Decouvrez OptiTAB : une plateforme de tutorat et de ressources pour progresser efficacement."
  },
  Contact: {
    title: 'Contact - OptiTAB',
    description: 'Contactez OptiTAB pour reserver un cours particulier ou poser vos questions.'
  },
  CGV: { title: 'CGV - OptiTAB' },
  CGU: { title: 'CGU - OptiTAB' },
  Confidentialite: { title: 'Confidentialite - OptiTAB' },
  Legal: { title: 'Mentions legales - OptiTAB' },
  Cookies: { title: 'Cookies - OptiTAB' },
  Conditions: { title: 'Conditions - OptiTAB' }
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
    const shouldNoIndex = Boolean(routeSeo.noindex) || requiresAuth || NOINDEX_ROUTE_NAMES.has(name)

    setPageSeo({
      title: routeSeo.title || DEFAULT_TITLE,
      description: routeSeo.description || DEFAULT_DESCRIPTION,
      canonicalPath: routeSeo.canonicalPath || route?.path || '/',
      robots: shouldNoIndex ? 'noindex,nofollow' : 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1',
      ogType: routeSeo.ogType || 'website',
      image: routeSeo.image || DEFAULT_IMAGE_PATH,
      jsonLdGraph: routeSeo.jsonLdGraph
    })
  } catch (_) {
    // Never block navigation on SEO updates.
  }
}
