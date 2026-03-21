let lastPagePath = null
let lastAppUserId = null
let ctaTrackingInitialized = false
let lastTouchTracked = { ts: 0, el: null }

// Business CTAs only
const ALLOWED_CTA_NAMES = new Set(['whatsapp', 'signup', 'login', 'subscribe', 'pricing', 'contact'])
// Navigation only (menu + logo)
const ALLOWED_NAV_NAMES = new Set([
  'home',
  'calculator',
  'about',
  'tutoring',
  'free_resources',
  'contact',
  // Content navigation (tabs / footer)
  'course',
  'summary',
  'exercise',
  'quiz',
  'pricing',
  'cgv',
  'cgu',
  'privacy',
  'legal',
  'cookies',
])
const CTA_TRACKING_WINDOW_FLAG = '__optitab_cta_tracking_initialized__'
const CTA_TRACKING_WINDOW_HANDLER = '__optitab_cta_tracking_handler__'
const REGISTRATION_COMPLETED_EVENT = 'optitab_registration_completed'
const PURCHASE_COMPLETED_EVENT = 'optitab_purchase_completed'
const BEGIN_CHECKOUT_EVENT = 'begin_checkout'

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

function normalizeRegistrationMethod(method) {
  const normalized = String(method ?? '').trim().toLowerCase().replace(/\s+/g, '_')
  return normalized || 'email_password'
}

function normalizeAppUserIdForTracking(userId) {
  const id = String(userId ?? '').trim()
  if (!id || id.includes('@')) return ''
  return id
}

function normalizeCurrency(currency) {
  const value = String(currency ?? '').trim().toUpperCase()
  return value || 'EUR'
}

function normalizePurchaseValue(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric) || numeric <= 0) return null
  return Math.round(numeric * 100) / 100
}

export function completeRegistration(method = 'email_password', { appUserId = null, eventId = null } = {}) {
  const payload = {
    event: REGISTRATION_COMPLETED_EVENT,
    registration_method: normalizeRegistrationMethod(method),
  }

  const normalizedProvidedId = normalizeAppUserIdForTracking(appUserId)
  if (normalizedProvidedId) {
    payload.app_user_id = normalizedProvidedId
  } else if (lastAppUserId) {
    payload.app_user_id = lastAppUserId
  }

  const normalizedEventId = String(eventId ?? '').trim()
  if (normalizedEventId) payload.event_id = normalizedEventId

  pushToDataLayer(withDebug(payload))
}

export function purchase({
  value,
  currency = 'EUR',
  transactionId = null,
  eventId = null,
  planName = null,
  planMode = null,
} = {}) {
  const normalizedValue = normalizePurchaseValue(value)
  if (normalizedValue === null) return

  const payload = {
    event: PURCHASE_COMPLETED_EVENT,
    value: normalizedValue,
    currency: normalizeCurrency(currency),
  }

  const txId = String(transactionId ?? '').trim()
  if (txId) payload.transaction_id = txId

  const normalizedEventId = String(eventId ?? '').trim()
  if (normalizedEventId) payload.event_id = normalizedEventId

  const normalizedPlanName = String(planName ?? '').trim()
  if (normalizedPlanName) payload.plan_name = normalizedPlanName

  const normalizedPlanMode = String(planMode ?? '').trim().toLowerCase()
  if (normalizedPlanMode) payload.plan_mode = normalizedPlanMode

  pushToDataLayer(withDebug(withAppUserId(payload)))
}

export function beginCheckout({
  value,
  currency = 'EUR',
  planName = null,
  planMode = null,
  transactionId = null,
  eventId = null,
} = {}) {
  const payload = {
    event: BEGIN_CHECKOUT_EVENT,
    currency: normalizeCurrency(currency),
  }

  const normalizedValue = normalizePurchaseValue(value)
  if (normalizedValue !== null) payload.value = normalizedValue

  const normalizedPlanName = String(planName ?? '').trim()
  if (normalizedPlanName) payload.plan_name = normalizedPlanName

  const normalizedPlanMode = String(planMode ?? '').trim().toLowerCase()
  if (normalizedPlanMode) payload.plan_mode = normalizedPlanMode

  const txId = String(transactionId ?? '').trim()
  if (txId) payload.transaction_id = txId

  const normalizedEventId = String(eventId ?? '').trim() || txId
  if (normalizedEventId) payload.event_id = normalizedEventId

  pushToDataLayer(withDebug(withAppUserId(payload)))
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

function normalizeTrackValue(value) {
  return String(value ?? '').trim().toLowerCase()
}

function closestElement(target, selector) {
  if (!target) return null

  // Text node -> use parent element
  if (target.nodeType === 3) {
    return target.parentElement?.closest?.(selector) || null
  }

  return target.closest?.(selector) || null
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

      const navEl = closestElement(event?.target, '[data-track="nav"]')
      if (navEl) {
        const navName = normalizeTrackValue(navEl.getAttribute('data-nav-name'))
        const navLocation = normalizeTrackValue(navEl.getAttribute('data-nav-location'))
        if (!navName || !navLocation) return
        if (!ALLOWED_NAV_NAMES.has(navName)) return

        if (eventType === 'click') {
          const now = Date.now()
          if (lastTouchTracked.el && (now - lastTouchTracked.ts) < 800 && lastTouchTracked.el === navEl) {
            return
          }
        } else if (isTouchPointerUp || isTouchEnd) {
          lastTouchTracked = { ts: Date.now(), el: navEl }
        }

        pushToDataLayer(withDebug(withAppUserId({
          event: 'nav_click',
          nav_name: navName,
          nav_location: navLocation,
        })))
        return
      }

      const ctaEl = closestElement(event?.target, '[data-cta-name]')
      if (!ctaEl) return

      const ctaName = normalizeTrackValue(ctaEl.getAttribute('data-cta-name'))
      const ctaLocation = normalizeTrackValue(ctaEl.getAttribute('data-cta-location'))
      if (!ctaName || !ctaLocation) return
      if (!ALLOWED_CTA_NAMES.has(ctaName)) return

      if (eventType === 'click') {
        const now = Date.now()
        if (lastTouchTracked.el && (now - lastTouchTracked.ts) < 800 && lastTouchTracked.el === ctaEl) {
          return
        }
      } else if (isTouchPointerUp || isTouchEnd) {
        lastTouchTracked = { ts: Date.now(), el: ctaEl }
      }

      pushToDataLayer(withDebug(withAppUserId({
        event: 'cta_click',
        cta_name: ctaName,
        cta_location: ctaLocation,
      })))
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
