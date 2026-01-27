let lastPagePath = null
let lastAppUserId = null
let ctaTrackingInitialized = false
let lastTouchCta = { ts: 0, el: null }

const ALLOWED_CTA_NAMES = new Set(['whatsapp', 'signup', 'login', 'subscribe', 'pricing'])
const CTA_TRACKING_WINDOW_FLAG = '__optitab_cta_tracking_initialized__'
const CTA_TRACKING_WINDOW_HANDLER = '__optitab_cta_tracking_handler__'

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

function withAppUserId(params) {
  if (!lastAppUserId) return params
  return { ...params, app_user_id: lastAppUserId }
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

  pushToDataLayer(withDebug(withAppUserId({
    event: 'page_view',
    page_path: pagePath,
    page_location: safePageLocation(),
    page_title: typeof document !== 'undefined' ? document.title : '',
  })))
}

export function login(method = 'email_password') {
  pushToDataLayer(withDebug(withAppUserId({
    event: 'login',
    method: String(method || 'email_password'),
  })))
}

export function logout() {
  pushToDataLayer(withDebug(withAppUserId({ event: 'logout' })))
}

export function setUserId(userId) {
  const id = String(userId ?? '').trim()
  if (!id) return

  // Guardrail to avoid accidental PII (e.g. passing an email)
  if (id.includes('@')) {
    if (import.meta?.env?.DEV) {
      console.warn('[analytics] Refusing to set app_user_id that looks like an email.')
    }
    return
  }

  if (id === lastAppUserId) return
  lastAppUserId = id

  // NOTE: keep this as an app-scoped identifier (non-PII). If you want GA4 user_id,
  // map `app_user_id` to GA4's `user_id` at the GA4 config level (via GTM).
  pushToDataLayer(withDebug({ event: 'set_user_id', app_user_id: id }))
}

function normalizeCtaValue(value) {
  return String(value ?? '').trim().toLowerCase()
}

function closestCtaElement(target) {
  if (!target) return null

  // Text node -> use parent element
  if (target.nodeType === 3) {
    return target.parentElement?.closest?.('[data-cta-name]') || null
  }

  return target.closest?.('[data-cta-name]') || null
}

export function initCtaTracking() {
  if (typeof document === 'undefined') return

  const w = typeof window !== 'undefined' ? window : null

  if (ctaTrackingInitialized) return
  ctaTrackingInitialized = true

  try {
    // If a previous handler exists (e.g. HMR), remove it defensively.
    const previous = w?.[CTA_TRACKING_WINDOW_HANDLER]
    if (typeof previous === 'function') {
      document.removeEventListener('click', previous, true)
      document.removeEventListener('pointerup', previous, true)
      document.removeEventListener('touchend', previous, true)
    }
  } catch (_) {}

  const handler = (event) => {
    try {
      // On touch devices, `touchend.preventDefault()` can suppress the subsequent `click`.
      // Track touch via pointer/touch events, and ignore the follow-up click to avoid duplicates.
      const eventType = event?.type || ''
      const isTouchPointerUp = eventType === 'pointerup' && event?.pointerType === 'touch'
      const isTouchEnd = eventType === 'touchend'

      if (eventType === 'pointerup' && !isTouchPointerUp) return

      const ctaEl = closestCtaElement(event?.target)
      if (!ctaEl) return

      const ctaName = normalizeCtaValue(ctaEl.getAttribute('data-cta-name'))
      if (!ALLOWED_CTA_NAMES.has(ctaName)) return

      const ctaLocation = normalizeCtaValue(ctaEl.getAttribute('data-cta-location')) || 'unknown'

      if (eventType === 'click') {
        const now = Date.now()
        if (lastTouchCta.el && (now - lastTouchCta.ts) < 800 && lastTouchCta.el === ctaEl) {
          return
        }
      } else if (isTouchPointerUp || isTouchEnd) {
        lastTouchCta = { ts: Date.now(), el: ctaEl }
      }

      pushToDataLayer(withDebug({
        event: 'cta_click',
        cta_name: ctaName,
        cta_location: ctaLocation,
        ...(lastAppUserId ? { app_user_id: lastAppUserId } : {})
      }))
    } catch (_) {}
  }

  try {
    if (w) {
      w[CTA_TRACKING_WINDOW_FLAG] = true
      w[CTA_TRACKING_WINDOW_HANDLER] = handler
    }
  } catch (_) {}

  document.addEventListener(
    'click',
    handler,
    { capture: true }
  )

  // Touch reliability (mobile bottom nav uses touchend.preventDefault()).
  if (w && 'PointerEvent' in w) {
    document.addEventListener('pointerup', handler, { capture: true, passive: true })
  } else {
    document.addEventListener('touchend', handler, { capture: true, passive: true })
  }
}
