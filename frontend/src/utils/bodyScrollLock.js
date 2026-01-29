const locks = new Map()

let originalBodyState = null
let activeMode = null

function canUseDom() {
  return typeof document !== 'undefined' && typeof window !== 'undefined' && document.body
}

function captureOriginalBodyState() {
  if (!canUseDom() || originalBodyState) return

  originalBodyState = {
    overflow: document.body.style.overflow,
    position: document.body.style.position,
    top: document.body.style.top,
    width: document.body.style.width,
    scrollY: window.scrollY || window.pageYOffset || 0
  }
}

function restoreOriginalBodyState() {
  if (!canUseDom() || !originalBodyState) return

  document.body.style.overflow = originalBodyState.overflow
  document.body.style.position = originalBodyState.position
  document.body.style.top = originalBodyState.top
  document.body.style.width = originalBodyState.width

  window.scrollTo(0, originalBodyState.scrollY)

  originalBodyState = null
  activeMode = null
}

function computeActiveMode() {
  for (const lock of locks.values()) {
    if (lock.mode === 'fixed') return 'fixed'
  }
  return 'overflow'
}

function applyBodyState() {
  if (!canUseDom()) return

  if (locks.size === 0) {
    restoreOriginalBodyState()
    return
  }

  captureOriginalBodyState()

  const nextMode = computeActiveMode()

  if (activeMode === 'fixed' && nextMode !== 'fixed' && originalBodyState) {
    window.scrollTo(0, originalBodyState.scrollY)
  }

  if (nextMode === 'fixed') {
    const y = originalBodyState?.scrollY || 0
    document.body.style.overflow = 'hidden'
    document.body.style.position = 'fixed'
    document.body.style.width = '100%'
    document.body.style.top = `-${y}px`
  } else {
    document.body.style.overflow = 'hidden'
    document.body.style.position = originalBodyState?.position || ''
    document.body.style.top = originalBodyState?.top || ''
    document.body.style.width = originalBodyState?.width || ''
  }

  activeMode = nextMode
}

export function lockBodyScroll(key = 'default', { mode = 'overflow' } = {}) {
  if (!canUseDom()) return
  const safeKey = String(key || 'default')
  locks.set(safeKey, { mode: mode === 'fixed' ? 'fixed' : 'overflow' })
  applyBodyState()
}

export function unlockBodyScroll(key = 'default') {
  if (!canUseDom()) return
  const safeKey = String(key || 'default')
  locks.delete(safeKey)
  applyBodyState()
}

export function isBodyScrollLocked() {
  return locks.size > 0
}

