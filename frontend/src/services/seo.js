const DEFAULT_SITE_NAME = 'OptiTAB'
const DEFAULT_TITLE = 'OptiTAB - Cours particuliers & ressources de maths'
const DEFAULT_DESCRIPTION =
  "OptiTAB : cours particuliers et ressources en maths, physique et informatique. Cours et exercices gratuits, fiches, quiz et suivi de progression."
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
  return 'https://www.optitab.net'
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

function canonicalizePath(pathLike) {
  if (!pathLike) return '/'
  try {
    const base = (typeof window !== 'undefined' && window.location?.origin) ? window.location.origin : 'https://www.optitab.net'
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

export function setPageSeo({
  title,
  description,
  robots,
  canonicalPath,
  canonicalUrl,
  ogType,
  image
} = {}) {
  if (typeof document === 'undefined') return

  const finalTitle = buildTitle(title)
  const finalDescription = String(description || DEFAULT_DESCRIPTION).trim() || DEFAULT_DESCRIPTION
  const finalRobots = String(robots || 'index,follow').trim()

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
}

const ROUTE_SEO = {
  Home: {
    title: DEFAULT_TITLE,
    description: DEFAULT_DESCRIPTION,
    canonicalPath: '/'
  },
  CoursParticuliers: {
    title: 'Cours particuliers de maths - OptiTAB',
    description:
      "Cours particuliers de maths, physique et informatique. Professeur experimente, methode personnalisee, progression mesuree.",
    canonicalPath: '/cours-particuliers'
  },
  FreeCourses: {
    title: 'Cours gratuits de maths - OptiTAB',
    description: 'Cours gratuits de maths, physique et informatique : chapitres clairs, exemples et exercices.',
    canonicalPath: '/ressources-gratuites/cours'
  },
  FreeCourseDetail: {
    title: 'Cours gratuit - OptiTAB',
    description: 'Cours gratuit a consulter en ligne : explications, exemples et exercices.',
    ogType: 'article'
  },
  FreeExercises: {
    title: 'Exercices gratuits de maths - OptiTAB',
    description: 'Exercices gratuits de maths, physique et informatique avec correction et explications.',
    canonicalPath: '/ressources-gratuites/exercices'
  },
  FreeExerciseDetail: {
    title: 'Exercice gratuit - OptiTAB',
    description: 'Exercice gratuit avec correction et explications.',
    ogType: 'article'
  },
  FreeSummaries: {
    title: 'Fiches gratuites (syntheses) - OptiTAB',
    description: 'Fiches de synthese gratuites pour reviser : definitions, formules, methodes et exemples.',
    canonicalPath: '/ressources-gratuites/syntheses'
  },
  FreeSummaryDetail: {
    title: 'Fiche gratuite - OptiTAB',
    description: 'Fiche de synthese gratuite pour reviser rapidement : formules, methodes et exemples.',
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
      robots: shouldNoIndex ? 'noindex,nofollow' : 'index,follow',
      ogType: routeSeo.ogType || 'website',
      image: routeSeo.image || DEFAULT_IMAGE_PATH
    })
  } catch (_) {
    // Never block navigation on SEO updates.
  }
}
