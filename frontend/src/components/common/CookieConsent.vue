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
        <div class="cookie-banner__text">
          <strong>Votre vie privée compte.</strong>
          <p>
            OptiTAB utilise des cookies essentiels pour le fonctionnement du site et des cookies de
            statistiques et marketing/publicité pour mesurer l'audience et personnaliser nos campagnes.
            Vous pouvez accepter, refuser ou personnaliser votre choix.
            <router-link to="/cookies" class="cookie-link">En savoir plus</router-link>.
          </p>
        </div>
        <div class="cookie-banner__actions">
          <button type="button" class="om-btn om-btn--primary cookie-btn" @click="acceptAll">Tout accepter</button>
          <button type="button" class="om-btn om-btn--ghost cookie-btn" @click="denyAll">Tout refuser</button>
          <button type="button" class="om-btn om-btn--ghost cookie-btn" @click="openPanel">Personnaliser</button>
        </div>
      </section>
    </transition>

    <Modal
      :is-open="isPanelOpen"
      title="Préférences de cookies"
      subtitle="Choisissez les catégories que vous autorisez. Vous pouvez changer d’avis à tout moment."
      :icon="ShieldCheckIcon"
      size="small"
      @close="closePanel"
    >
      <div class="cookie-categories">
        <div class="cookie-category">
          <div>
            <p class="cookie-category__title">Essentiels</p>
            <p>Indispensables au fonctionnement du site (authentification, sécurité, navigation).</p>
          </div>
          <span class="cookie-tag">Toujours actifs</span>
        </div>
        <label class="cookie-category">
          <div>
            <p class="cookie-category__title">Statistiques</p>
            <p>Nous aident à mesurer l’audience et à améliorer l’expérience (Google Analytics, Microsoft Clarity).</p>
          </div>
          <span class="cookie-switch">
            <input v-model="analyticsEnabled" type="checkbox" aria-label="Autoriser les cookies de statistiques" />
            <span class="cookie-switch__track" aria-hidden="true"></span>
          </span>
        </label>
        <label class="cookie-category">
          <div>
            <p class="cookie-category__title">Marketing / Publicité</p>
            <p>Active les traceurs publicitaires pour la mesure et l’optimisation de campagnes (Meta Pixel).</p>
          </div>
          <span class="cookie-switch">
            <input v-model="marketingEnabled" type="checkbox" aria-label="Autoriser les cookies marketing et publicitaires" />
            <span class="cookie-switch__track" aria-hidden="true"></span>
          </span>
        </label>
      </div>

      <template #footer>
        <div class="cookie-panel-actions">
          <button type="button" class="om-btn om-btn--primary cookie-panel-actions__main" @click="savePreferences">Enregistrer mes choix</button>
          <button type="button" class="om-btn om-btn--ghost" @click="denyAll">Tout refuser</button>
          <button type="button" class="om-btn om-btn--ghost" @click="acceptAll">Tout accepter</button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ShieldCheckIcon } from '@heroicons/vue/24/outline'
import Modal from '@/components/common/Modal.vue'

const STORAGE_KEY = 'optitab_cookie_consent_v1'
const CONSENT_EVENT = 'open-cookie-preferences'
const CONSENT_MONTHS = 6
const CONSENT_UPDATED_DATALAYER_EVENT = 'optitab_consent_updated'
const MARKETING_GRANTED_DATALAYER_EVENT = 'optitab_marketing_consent_granted'

const isBannerVisible = ref(false)
const isPanelOpen = ref(false)
const analyticsEnabled = ref(false)
const marketingEnabled = ref(false)
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

const pushConsentUpdateEvents = (analyticsGranted, marketingGranted, emitMarketingGrantEvent) => {
  if (typeof window === 'undefined') return
  const existing = window.dataLayer
  if (!Array.isArray(existing)) {
    window.dataLayer = []
  }

  const analyticsStorage = analyticsGranted ? 'granted' : 'denied'
  const marketingStorage = marketingGranted ? 'granted' : 'denied'

  window.dataLayer.push({
    event: CONSENT_UPDATED_DATALAYER_EVENT,
    analytics_consent: analyticsStorage,
    marketing_consent: marketingStorage
  })

  if (emitMarketingGrantEvent && marketingGranted) {
    window.dataLayer.push({
      event: MARKETING_GRANTED_DATALAYER_EVENT,
      marketing_consent: marketingStorage
    })
  }
}

const updateConsent = (analyticsGranted, marketingGranted, { emitMarketingGrantEvent = false } = {}) => {
  const gtag = ensureGtag()
  if (!gtag) return

  const marketingStorage = marketingGranted ? 'granted' : 'denied'
  const analyticsStorage = analyticsGranted ? 'granted' : 'denied'
  gtag('consent', 'update', {
    analytics_storage: analyticsStorage,
    ad_storage: marketingStorage,
    ad_user_data: marketingStorage,
    ad_personalization: marketingStorage
  })

  pushConsentUpdateEvents(analyticsGranted, marketingGranted, emitMarketingGrantEvent)
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
  const marketing = stored.marketing === 'granted' ? 'granted' : 'denied'
  return { analytics, marketing, expiresAt: stored.expiresAt }
}

const persistConsent = (analyticsGranted, marketingGranted) => {
  const now = new Date()
  const expiresAt = new Date(now)
  expiresAt.setMonth(expiresAt.getMonth() + CONSENT_MONTHS)

  const payload = {
    analytics: analyticsGranted ? 'granted' : 'denied',
    marketing: marketingGranted ? 'granted' : 'denied',
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
    marketingEnabled.value = stored.marketing === 'granted'
    hasChoice.value = true
    isBannerVisible.value = false
    updateConsent(analyticsEnabled.value, marketingEnabled.value)
    return
  }

  analyticsEnabled.value = false
  marketingEnabled.value = false
  hasChoice.value = false
  isBannerVisible.value = true
  updateConsent(false, false)
}

const saveConsent = ({ analyticsGranted, marketingGranted }) => {
  analyticsEnabled.value = analyticsGranted
  marketingEnabled.value = marketingGranted
  hasChoice.value = true
  persistConsent(analyticsGranted, marketingGranted)
  updateConsent(analyticsGranted, marketingGranted, { emitMarketingGrantEvent: true })
  isBannerVisible.value = false
  isPanelOpen.value = false
}

const acceptAll = () => saveConsent({ analyticsGranted: true, marketingGranted: true })
const denyAll = () => saveConsent({ analyticsGranted: false, marketingGranted: false })

const openPanel = () => {
  if (!hasChoice.value) {
    analyticsEnabled.value = true
    marketingEnabled.value = true
  }
  isPanelOpen.value = true
  isBannerVisible.value = false
}

const closePanel = () => {
  isPanelOpen.value = false
  if (!hasChoice.value) {
    isBannerVisible.value = true
  }
}

const savePreferences = () => {
  saveConsent({
    analyticsGranted: analyticsEnabled.value,
    marketingGranted: marketingEnabled.value
  })
}

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
/* Boutons (.om-btn) et fenêtre : components/common/Modal.vue */
.cookie-consent-root {
  position: relative;
  z-index: 10000;
}

.cookie-banner {
  position: fixed;
  right: 16px;
  bottom: 16px;
  left: 16px;
  z-index: 10000;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px 24px;
  max-width: 980px;
  margin: 0 auto;
  padding: 18px 20px;
  border: 1px solid #e4e8f0;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 2px 6px rgba(16, 32, 79, 0.08), 0 24px 60px rgba(16, 32, 79, 0.18);
  color: #121a33;
  font-family: 'Montserrat', 'Segoe UI', system-ui, sans-serif;
  font-size: 14px;
}

.cookie-banner__text {
  flex: 1 1 420px;
}

.cookie-banner__text p {
  margin: 4px 0 0;
  color: #2c3550;
  line-height: 1.5;
}

.cookie-link {
  color: #1b3c8e;
  font-weight: 600;
}

.cookie-banner__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.cookie-btn {
  min-height: 42px;
  padding: 0 18px;
  font-size: 14px;
}

.cookie-categories {
  display: grid;
  gap: 10px;
}

.cookie-panel-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  width: 100%;
}

.cookie-panel-actions__main {
  grid-column: 1 / -1;
}

.cookie-category {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border: 1px solid var(--om-line);
  border-radius: 14px;
  cursor: pointer;
}

div.cookie-category {
  cursor: default;
}

.cookie-category p {
  margin: 2px 0 0;
  color: var(--om-muted);
  font-size: 13.5px;
  line-height: 1.45;
}

.cookie-category .cookie-category__title {
  margin: 0;
  color: var(--om-ink);
  font-size: 15px;
  font-weight: 700;
}

.cookie-tag {
  flex-shrink: 0;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--om-green-50);
  color: var(--om-green-700);
  font-size: 12.5px;
  font-weight: 700;
  white-space: nowrap;
}

.cookie-switch {
  position: relative;
  flex-shrink: 0;
  width: 46px;
  height: 26px;
}

.cookie-switch input {
  position: absolute;
  inset: 0;
  z-index: 1;
  margin: 0;
  opacity: 0;
  cursor: pointer;
}

.cookie-switch__track {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  background: var(--om-line-strong);
  transition: background 0.2s;
}

.cookie-switch__track::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(16, 32, 79, 0.25);
  transition: transform 0.2s;
}

.cookie-switch input:checked + .cookie-switch__track {
  background: var(--om-navy);
}

.cookie-switch input:checked + .cookie-switch__track::after {
  transform: translateX(20px);
}

.cookie-switch input:focus-visible + .cookie-switch__track {
  outline: 2px solid var(--om-navy);
  outline-offset: 2px;
}

.cookie-fade-enter-active,
.cookie-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.cookie-fade-enter-from,
.cookie-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@media (max-width: 640px) {
  .cookie-banner {
    right: 10px;
    bottom: 10px;
    left: 10px;
    padding: 16px;
  }

  .cookie-banner__actions .cookie-btn {
    flex: 1 1 auto;
  }
}
</style>
