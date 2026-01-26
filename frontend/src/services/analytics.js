let lastPagePath = null
let lastUserId = null

function getDataLayer() {
  if (typeof window === 'undefined') return null

  const existing = window.dataLayer
  if (!existing) {
    window.dataLayer = []
    return window.dataLayer
  }

  if (Array.isArray(existing)) return existing
  if (typeof existing.push === 'function') return existing
  return null
}

function pushToDataLayer(payload) {
  const dataLayer = getDataLayer()
  if (!dataLayer) return
  try {
    dataLayer.push(payload)
  } catch (_) {}
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

function withDebug(params) {
  if (!isDebugModeEnabled()) return params
  return { ...params, debug_mode: true }
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
  const pagePath = sanitizePath(path)
  if (!pagePath) return

  // Avoid duplicates (hash-only navigations, repeated pushes, etc.)
  if (pagePath === lastPagePath) return
  lastPagePath = pagePath

  pushToDataLayer(withDebug({
    event: 'page_view',
    page_path: pagePath,
    page_location: safePageLocation(),
    page_title: typeof document !== 'undefined' ? document.title : '',
    ...(lastUserId ? { user_id: lastUserId } : {})
  }))
}

export function login(method = 'email_password') {
  pushToDataLayer(withDebug({
    event: 'login',
    method: String(method || 'email_password'),
    ...(lastUserId ? { user_id: lastUserId } : {})
  }))
}

export function logout() {
  pushToDataLayer(withDebug({
    event: 'logout',
    ...(lastUserId ? { user_id: lastUserId } : {})
  }))
}

export function setUserId(userId) {
  const id = String(userId ?? '').trim()
  if (!id) return

  // Guardrail to avoid accidental PII (e.g. passing an email)
  if (id.includes('@')) {
    if (import.meta?.env?.DEV) {
      console.warn('[analytics] Refusing to set user_id that looks like an email.')
    }
    return
  }

  if (id === lastUserId) return
  lastUserId = id

  pushToDataLayer(withDebug({ event: 'set_user_id', user_id: id }))
}
