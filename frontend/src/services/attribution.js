const TTCLID_STORAGE_KEY = 'optitab_ttclid'
const TTCLID_TIMESTAMP_KEY = 'optitab_ttclid_ts'
const TTCLID_TTL_MS = 90 * 24 * 60 * 60 * 1000

function isBrowser() {
  return typeof window !== 'undefined'
}

function readTtclidFromUrl() {
  if (!isBrowser()) return ''
  try {
    const currentUrl = new URL(window.location.href)
    return String(currentUrl.searchParams.get('ttclid') || '').trim()
  } catch (_) {
    return ''
  }
}

function readStorageValue(key) {
  if (!isBrowser()) return ''
  try {
    return String(window.localStorage?.getItem(key) || '').trim()
  } catch (_) {
    return ''
  }
}

function writeStorageValue(key, value) {
  if (!isBrowser()) return
  try {
    window.localStorage?.setItem(key, value)
  } catch (_) {}
}

function removeStorageValue(key) {
  if (!isBrowser()) return
  try {
    window.localStorage?.removeItem(key)
  } catch (_) {}
}

function persistTtclidIfPresent() {
  const ttclidFromUrl = readTtclidFromUrl()
  if (!ttclidFromUrl) return

  writeStorageValue(TTCLID_STORAGE_KEY, ttclidFromUrl)
  writeStorageValue(TTCLID_TIMESTAMP_KEY, String(Date.now()))
}

function purgeExpiredTtclid() {
  const timestampRaw = readStorageValue(TTCLID_TIMESTAMP_KEY)
  if (!timestampRaw) return

  const timestamp = Number(timestampRaw)
  if (!Number.isFinite(timestamp)) {
    removeStorageValue(TTCLID_STORAGE_KEY)
    removeStorageValue(TTCLID_TIMESTAMP_KEY)
    return
  }

  if (Date.now() - timestamp > TTCLID_TTL_MS) {
    removeStorageValue(TTCLID_STORAGE_KEY)
    removeStorageValue(TTCLID_TIMESTAMP_KEY)
  }
}

export function initAttributionTracking() {
  persistTtclidIfPresent()
  purgeExpiredTtclid()
}

export function getStoredTtclid() {
  persistTtclidIfPresent()
  purgeExpiredTtclid()
  return readStorageValue(TTCLID_STORAGE_KEY)
}

export function getCookieValue(name) {
  if (!isBrowser() || !name) return ''
  const escapedName = name.replace(/([.$?*|{}()\[\]\\/+^])/g, '\\$1')
  const match = document.cookie.match(new RegExp(`(?:^|; )${escapedName}=([^;]*)`))
  return match ? decodeURIComponent(match[1]) : ''
}

export function getTtpCookie() {
  return getCookieValue('_ttp') || getCookieValue('ttp')
}

export function getCurrentPageUrl() {
  if (!isBrowser()) return ''
  try {
    return String(window.location.href || '').trim()
  } catch (_) {
    return ''
  }
}

export function getDocumentReferrer() {
  if (!isBrowser()) return ''
  try {
    return String(document.referrer || '').trim()
  } catch (_) {
    return ''
  }
}
