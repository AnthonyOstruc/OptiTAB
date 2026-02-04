<template>
  <div class="cookie-consent-root">
    <transition name="cookie-fade">
      <section
        v-if="isBannerVisible"
        class="cookie-banner"
        role="dialog"
        aria-live="polite"
        aria-label="Gestion des cookies"
      >
        <div class="cookie-banner__content">
          <div class="cookie-banner__text">
            <strong>Votre vie privee compte.</strong>
            <p>
              OptiTAB utilise des cookies essentiels pour le fonctionnement du site et des cookies de
              statistiques pour mesurer l'audience. Vous pouvez accepter, refuser ou personnaliser votre
              choix.
              <router-link to="/cookies" class="cookie-link">En savoir plus</router-link>.
            </p>
          </div>
          <div class="cookie-banner__actions">
            <button type="button" class="cookie-button" @click="acceptAll">Tout accepter</button>
            <button type="button" class="cookie-button" @click="denyAll">Tout refuser</button>
            <button type="button" class="cookie-button" @click="openPanel">Personnaliser</button>
          </div>
        </div>
      </section>
    </transition>

    <transition name="cookie-fade">
      <div v-if="isPanelOpen" class="cookie-panel-backdrop" @click.self="closePanel">
        <section class="cookie-panel" role="dialog" aria-modal="true" aria-label="Preferences de cookies">
          <header class="cookie-panel__header">
            <div>
              <h3>Preferences de cookies</h3>
              <p>Choisissez les categories que vous autorisez.</p>
            </div>
            <button type="button" class="cookie-panel__close" @click="closePanel" aria-label="Fermer">
              x
            </button>
          </header>

          <div class="cookie-panel__body">
            <div class="cookie-category">
              <div>
                <h4>Essentiels</h4>
                <p>Indispensables au fonctionnement du site (authentification, securite, navigation).</p>
              </div>
              <span class="cookie-tag">Toujours actifs</span>
            </div>

            <div class="cookie-category cookie-category--toggle">
              <div>
                <h4>Statistiques</h4>
                <p>
                  Nous aide a mesurer l'audience et ameliorer l'experience (Google Analytics, Microsoft
                  Clarity).
                </p>
              </div>
              <label class="cookie-toggle" aria-label="Autoriser les cookies de statistiques">
                <input type="checkbox" v-model="analyticsEnabled" />
                <span class="cookie-toggle__track">
                  <span class="cookie-toggle__thumb"></span>
                </span>
              </label>
            </div>
          </div>

          <div class="cookie-panel__actions">
            <button type="button" class="cookie-button cookie-button--panel" @click="acceptAll">
              Tout accepter
            </button>
            <button type="button" class="cookie-button cookie-button--panel" @click="denyAll">
              Tout refuser
            </button>
            <button type="button" class="cookie-button cookie-button--primary" @click="savePreferences">
              Enregistrer
            </button>
          </div>
        </section>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const STORAGE_KEY = 'optitab_cookie_consent_v1'
const CONSENT_EVENT = 'open-cookie-preferences'
const CONSENT_MONTHS = 6

const isBannerVisible = ref(false)
const isPanelOpen = ref(false)
const analyticsEnabled = ref(false)
const hasChoice = ref(false)

const ensureGtag = () => {
  if (typeof window === 'undefined') return null

  const existing = window.dataLayer
  if (!Array.isArray(existing)) {
    window.dataLayer = []
  }

  if (typeof window.gtag !== 'function') {
    window.gtag = function () {
      window.dataLayer.push(arguments)
    }
  }

  return window.gtag
}

const updateConsent = (analyticsGranted) => {
  const gtag = ensureGtag()
  if (!gtag) return

  gtag('consent', 'update', {
    analytics_storage: analyticsGranted ? 'granted' : 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  })
}

const safeJsonParse = (value) => {
  if (!value) return null
  try {
    return JSON.parse(value)
  } catch (_) {
    return null
  }
}

const getCookie = (name) => {
  if (typeof document === 'undefined') return null
  const prefix = `${name}=`
  const parts = document.cookie ? document.cookie.split('; ') : []
  for (const part of parts) {
    if (part.startsWith(prefix)) {
      return decodeURIComponent(part.slice(prefix.length))
    }
  }
  return null
}

const setCookie = (name, value, expiresAt) => {
  if (typeof document === 'undefined') return
  const expires = new Date(expiresAt).toUTCString()
  const secure = typeof window !== 'undefined' && window.location?.protocol === 'https:' ? '; Secure' : ''
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax${secure}`
}

const clearCookie = (name) => {
  if (typeof document === 'undefined') return
  const secure = typeof window !== 'undefined' && window.location?.protocol === 'https:' ? '; Secure' : ''
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax${secure}`
}

const readStoredConsent = () => {
  if (typeof window === 'undefined') return null

  const now = Date.now()
  let stored = null

  try {
    stored = safeJsonParse(window.localStorage?.getItem(STORAGE_KEY))
  } catch (_) {
    stored = null
  }

  if (!stored) {
    stored = safeJsonParse(getCookie(STORAGE_KEY))
  }

  if (!stored || !stored.expiresAt) return null

  if (stored.expiresAt <= now) {
    try {
      window.localStorage?.removeItem(STORAGE_KEY)
    } catch (_) {}
    clearCookie(STORAGE_KEY)
    return null
  }

  const analytics = stored.analytics === 'granted' ? 'granted' : 'denied'
  return { analytics, expiresAt: stored.expiresAt }
}

const persistConsent = (analyticsGranted) => {
  const now = new Date()
  const expiresAt = new Date(now)
  expiresAt.setMonth(expiresAt.getMonth() + CONSENT_MONTHS)

  const payload = {
    analytics: analyticsGranted ? 'granted' : 'denied',
    updatedAt: now.toISOString(),
    expiresAt: expiresAt.getTime()
  }

  const serialized = JSON.stringify(payload)

  try {
    window.localStorage?.setItem(STORAGE_KEY, serialized)
  } catch (_) {}

  setCookie(STORAGE_KEY, serialized, payload.expiresAt)
}

const applyStoredConsent = () => {
  const stored = readStoredConsent()
  if (stored) {
    analyticsEnabled.value = stored.analytics === 'granted'
    hasChoice.value = true
    isBannerVisible.value = false
    updateConsent(analyticsEnabled.value)
    return
  }

  analyticsEnabled.value = false
  hasChoice.value = false
  isBannerVisible.value = true
  updateConsent(false)
}

const saveConsent = (analyticsGranted) => {
  analyticsEnabled.value = analyticsGranted
  hasChoice.value = true
  persistConsent(analyticsGranted)
  updateConsent(analyticsGranted)
  isBannerVisible.value = false
  isPanelOpen.value = false
}

const acceptAll = () => saveConsent(true)
const denyAll = () => saveConsent(false)

const openPanel = () => {
  isPanelOpen.value = true
  isBannerVisible.value = false
}

const closePanel = () => {
  isPanelOpen.value = false
  if (!hasChoice.value) {
    isBannerVisible.value = true
  }
}

const savePreferences = () => saveConsent(analyticsEnabled.value)

const handleOpenEvent = () => {
  openPanel()
}

onMounted(() => {
  applyStoredConsent()

  if (typeof window !== 'undefined') {
    window.addEventListener(CONSENT_EVENT, handleOpenEvent)
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener(CONSENT_EVENT, handleOpenEvent)
  }
})
</script>

<style scoped>
.cookie-consent-root {
  position: relative;
  z-index: 10000;
}

.cookie-banner {
  position: fixed;
  left: 24px;
  right: 24px;
  bottom: calc(24px + env(safe-area-inset-bottom));
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(17, 24, 39, 0.18);
  padding: 20px 24px;
  border: 1px solid #e5e7eb;
  pointer-events: auto;
}

.cookie-banner__content {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
}

.cookie-banner__text {
  flex: 1 1 320px;
  color: #1f2937;
}

.cookie-banner__text strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.35rem;
}

.cookie-banner__text p {
  margin: 0;
  font-size: 0.92rem;
  color: #4b5563;
}

.cookie-link {
  color: #4e63c2;
  font-weight: 600;
  text-decoration: underline;
  margin-left: 0.35rem;
}

.cookie-banner__actions {
  display: flex;
  gap: 0.75rem;
  flex: 1 1 280px;
  justify-content: flex-end;
}

.cookie-button {
  flex: 1 1 auto;
  border: 1px solid #4e63c2;
  background: #ffffff;
  color: #4e63c2;
  padding: 0.6rem 0.9rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}

.cookie-button:hover {
  background: #eef1ff;
  box-shadow: 0 8px 20px rgba(78, 99, 194, 0.2);
  transform: translateY(-1px);
}

.cookie-button--primary {
  background: #4e63c2;
  color: #ffffff;
}

.cookie-button--primary:hover {
  background: #4053b6;
}

.cookie-button--panel {
  background: #ffffff;
}

.cookie-panel-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  pointer-events: auto;
}

.cookie-panel {
  background: #ffffff;
  border-radius: 18px;
  max-width: 640px;
  width: 100%;
  padding: 24px;
  box-shadow: 0 30px 80px rgba(15, 23, 42, 0.3);
}

.cookie-panel__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.cookie-panel__header h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.2rem;
  color: #111827;
}

.cookie-panel__header p {
  margin: 0;
  color: #6b7280;
  font-size: 0.95rem;
}

.cookie-panel__close {
  border: none;
  background: #f3f4f6;
  width: 36px;
  height: 36px;
  border-radius: 999px;
  font-size: 1.2rem;
  cursor: pointer;
  color: #111827;
}

.cookie-panel__body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cookie-category {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #f9fafb;
}

.cookie-category h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: #111827;
}

.cookie-category p {
  margin: 0;
  font-size: 0.9rem;
  color: #6b7280;
}

.cookie-tag {
  background: #e5e7eb;
  color: #374151;
  font-size: 0.75rem;
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  font-weight: 600;
  white-space: nowrap;
}

.cookie-category--toggle {
  background: #fdfdfd;
}

.cookie-toggle {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.cookie-toggle input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  width: 1px;
  height: 1px;
}

.cookie-toggle__track {
  width: 48px;
  height: 28px;
  background: #e5e7eb;
  border-radius: 999px;
  padding: 3px;
  display: inline-flex;
  align-items: center;
  transition: background 0.2s ease;
}

.cookie-toggle__thumb {
  width: 22px;
  height: 22px;
  background: #ffffff;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(15, 23, 42, 0.2);
  transform: translateX(0);
  transition: transform 0.2s ease;
}

.cookie-toggle input:checked + .cookie-toggle__track {
  background: #4e63c2;
}

.cookie-toggle input:checked + .cookie-toggle__track .cookie-toggle__thumb {
  transform: translateX(20px);
}

.cookie-panel__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 20px;
  justify-content: flex-end;
}

.cookie-fade-enter-active,
.cookie-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.cookie-fade-enter-from,
.cookie-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 768px) {
  .cookie-banner {
    left: 16px;
    right: 16px;
    bottom: calc(16px + env(safe-area-inset-bottom));
  }

  .cookie-banner__actions {
    flex-direction: column;
    align-items: stretch;
  }

  .cookie-panel {
    padding: 18px;
  }

  .cookie-panel__actions {
    flex-direction: column;
  }

  .cookie-button {
    width: 100%;
  }
}
</style>
