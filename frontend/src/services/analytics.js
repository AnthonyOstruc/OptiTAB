const DEFAULT_MEASUREMENT_ID = 'G-1LJEYKL7EL'

const measurementId = (import.meta?.env?.VITE_GA_MEASUREMENT_ID || DEFAULT_MEASUREMENT_ID || '').trim()

let lastPagePath = null
let lastUserId = null
let didInit = false

function getGtag() {
  if (typeof window === 'undefined') return null
  return typeof window.gtag === 'function' ? window.gtag : null
}

function isDebugModeEnabled() {
  try {
    if (import.meta?.env?.DEV) return true
  } catch (_) {}

  if (typeof window === 'undefined') return false

  try {
    const url = new URL(window.location.href)
    const debugParam = url.searchParams.get('ga_debug')
    if (debugParam === '1') {
      try {
        window.localStorage?.setItem('ga_debug', '1')
      } catch (_) {}
      return true
    }
    if (debugParam === '0') {
      try {
        window.localStorage?.removeItem('ga_debug')
      } catch (_) {}
      return false
    }
  } catch (_) {}

  try {
    return window.localStorage?.getItem('ga_debug') === '1'
  } catch (_) {
    return false
  }
}

function baseConfig() {
  const config = { send_page_view: false }
  if (isDebugModeEnabled()) {
    config.debug_mode = true
  }
  return config
}

function withDebug(params) {
  if (!isDebugModeEnabled()) return params
  return { ...params, debug_mode: true }
}

function ensureInitialized() {
  if (didInit) return
  didInit = true

  const gtag = getGtag()
  if (!gtag || !measurementId) return

  // Ensure SPA config + optional debug mode (safe: never sends automatic page_view)
  gtag('config', measurementId, baseConfig())
}

function sanitizePath(path) {
  if (typeof path !== 'string') return ''
  const trimmed = path.trim()
  if (!trimmed) return ''

  // Route inputs like "/password-reset?token=..." or "/route#anchor"
  const noHash = trimmed.split('#')[0]
  const noQuery = noHash.split('?')[0]

  // If a full URL is passed, keep only pathname
  if (/^https?:\/\//i.test(noQuery)) {
    try {
      return new URL(noQuery).pathname || '/'
    } catch (_) {
      return '/'
    }
  }

  return noQuery.startsWith('/') ? noQuery : `/${noQuery}`
}

function safePageLocation() {
  if (typeof window === 'undefined') return ''
  try {
    return `${window.location.origin}${window.location.pathname}`
  } catch (_) {
    return ''
  }
}

export function pageView(path) {
  ensureInitialized()
  const gtag = getGtag()
  if (!gtag || !measurementId) return

  const pagePath = sanitizePath(path)
  if (!pagePath) return

  // Avoid duplicates (hash-only navigations, repeated pushes, etc.)
  if (pagePath === lastPagePath) return
  lastPagePath = pagePath

  gtag('event', 'page_view', withDebug({
    page_path: pagePath,
    page_location: safePageLocation(),
    page_title: typeof document !== 'undefined' ? document.title : ''
  }))
}

export function login(method = 'email_password') {
  ensureInitialized()
  const gtag = getGtag()
  if (!gtag) return
  gtag('event', 'login', withDebug({ method: String(method || 'email_password') }))
}

export function logout() {
  ensureInitialized()
  const gtag = getGtag()
  if (!gtag) return
  gtag('event', 'logout', withDebug({}))
}

export function setUserId(userId) {
  ensureInitialized()
  const gtag = getGtag()
  if (!gtag || !measurementId) return

  const id = String(userId ?? '').trim()
  if (!id) return

  // Guardrail to avoid accidental PII (e.g. passing an email)
  if (id.includes('@')) {
    if (import.meta?.env?.DEV) {
      console.warn('[analytics] Refusing to set GA user_id that looks like an email.')
    }
    return
  }

  if (id === lastUserId) return
  lastUserId = id

  gtag('config', measurementId, { ...baseConfig(), user_id: id })
}
