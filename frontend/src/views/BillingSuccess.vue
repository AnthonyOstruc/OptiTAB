<template>
  <div class="billing-success">
    <!-- Success State -->
    <template v-if="isSuccess">
      <div class="success-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10" />
          <path d="M8 12l3 3 5-6" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
      <h1 class="headline success">{{ headline }}</h1>
      <p class="status success-text">{{ statusMessage }}</p>
      <p v-if="accountCreated" class="status account-created-hint">
        Un email vous a été envoyé pour définir votre mot de passe et accéder à votre compte.
      </p>
      <router-link class="btn btn-primary" to="/dashboard">
        {{ primaryLabel }}
      </router-link>
    </template>

    <!-- Failure State -->
    <template v-else-if="isFailure">
      <div class="error-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10" />
          <path d="M8 8l8 8M16 8l-8 8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
      <h1 class="headline error">Paiement non confirmé</h1>
      <p class="status">{{ statusMessage }}</p>
      <div class="buttons-row">
        <router-link class="btn btn-primary" to="/billing">
          Réessayer le paiement
        </router-link>
      </div>
    </template>

    <!-- Loading State -->
    <template v-else>
      <div class="loading-container">
        <div class="progress-ring">
          <svg viewBox="0 0 100 100">
            <circle class="progress-bg" cx="50" cy="50" r="42" />
            <circle class="progress-bar" cx="50" cy="50" r="42" :style="progressStyle" />
          </svg>
          <div class="progress-text">{{ progressPercent }}%</div>
        </div>
        <h1 class="headline">Activation en cours</h1>
        <p class="status">{{ statusMessage }}</p>
        <div class="steps-indicator">
          <div class="step" :class="{ done: step >= 1, active: step === 1 }">
            <span class="step-icon">&#10003;</span>
            <span class="step-label">Paiement recu</span>
          </div>
          <div class="step-line" :class="{ done: step >= 2 }"></div>
          <div class="step" :class="{ done: step >= 2, active: step === 2 }">
            <span class="step-icon">&#10003;</span>
            <span class="step-label">Verification</span>
          </div>
          <div class="step-line" :class="{ done: step >= 3 }"></div>
          <div class="step" :class="{ done: step >= 3, active: step === 3 }">
            <span class="step-icon">&#10003;</span>
            <span class="step-label">Activation</span>
          </div>
        </div>
      </div>
      <div class="buttons-row">
        <router-link class="btn btn-secondary" to="/dashboard">
          Retour au tableau de bord
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUserStore } from '@/stores/user'
import { finalizeCheckoutSession, finalizeGuestCheckoutSession } from '@/api/subscriptions'
import * as analytics from '@/services/analytics'

const route = useRoute()
const subscriptionStore = useSubscriptionStore()
const userStore = useUserStore()

const statusMessage = ref('Connexion avec Stripe...')
const hasAccess = ref(false)
const isGiftPayer = ref(false)
const beneficiaryLabel = ref('')
const accountCreated = ref(false)
const step = ref(1)
const progress = ref(10)
const purchaseTracked = ref(false)
const paymentFailed = ref(false)

const sessionId = computed(() => route.query.session_id || '')
const isSuccess = computed(() => hasAccess.value || isGiftPayer.value)
const isFailure = computed(() => paymentFailed.value && !isSuccess.value)
const progressPercent = computed(() => Math.min(100, progress.value))
const progressStyle = computed(() => {
  const circumference = 2 * Math.PI * 42
  const offset = circumference - (progressPercent.value / 100) * circumference
  return { strokeDasharray: `${circumference}`, strokeDashoffset: `${offset}` }
})

const headline = computed(() => {
  if (accountCreated.value) return 'Compte cree et acces active !'
  if (isGiftPayer.value) return 'Cadeau active !'
  return hasAccess.value ? 'Acces active !' : 'Activation en cours'
})
const primaryLabel = computed(() => {
  if (isGiftPayer.value) return 'Retour au tableau de bord'
  return 'Acceder au tableau de bord'
})

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms))
const PURCHASE_TRACKED_PREFIX = 'optitab_purchase_tracked_'

function updateProgress(targetStep, targetProgress, message) {
  step.value = targetStep
  progress.value = targetProgress
  statusMessage.value = message
}

function readTrackedPurchase(transactionId) {
  if (!transactionId || typeof window === 'undefined') return false
  try {
    return window.localStorage?.getItem(`${PURCHASE_TRACKED_PREFIX}${transactionId}`) === '1'
  } catch (_) {
    return false
  }
}

function markTrackedPurchase(transactionId) {
  if (!transactionId || typeof window === 'undefined') return
  try {
    window.localStorage?.setItem(`${PURCHASE_TRACKED_PREFIX}${transactionId}`, '1')
  } catch (_) {}
}

function trackPurchaseIfPaid(data) {
  if (purchaseTracked.value) return

  const payment = data?.payment
  if (!payment?.is_paid) return

  const value = Number(payment.value)
  if (!Number.isFinite(value) || value <= 0) return

  const transactionId = String(payment.transaction_id || sessionId.value || '').trim()
  if (transactionId && readTrackedPurchase(transactionId)) {
    purchaseTracked.value = true
    return
  }

  const statusPlan = data?.status?.plan || {}
  analytics.purchase({
    value,
    currency: payment.currency || 'EUR',
    transactionId,
    planName: statusPlan?.name || statusPlan?.label || '',
    planMode: statusPlan?.mode || '',
  })

  if (transactionId) {
    markTrackedPurchase(transactionId)
  }
  purchaseTracked.value = true
}

function loginFromGuestResponse(data) {
  const auth = data?.auth
  if (!auth?.access || !auth?.refresh) return false
  localStorage.setItem('access_token', auth.access)
  localStorage.setItem('refresh_token', auth.refresh)
  userStore.setUser({
    id: auth.user_id,
    email: auth.email,
    first_name: auth.first_name,
    last_name: auth.last_name,
  })
  return true
}


async function finalizeSessionIfNeeded() {
  if (!sessionId.value) {
    updateProgress(1, 100, 'Redirection vers le tableau de bord...')
    hasAccess.value = true
    return
  }

  updateProgress(1, 20, 'Verification du paiement...')

  const isGuest = !userStore.isAuthenticated
  const maxAttempts = 12

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      let data
      // Premieres tentatives : appeler finalize (guest ou auth)
      if (attempt < 3) {
        const finalizeFn = isGuest ? finalizeGuestCheckoutSession : finalizeCheckoutSession
        const res = await finalizeFn(sessionId.value)
        data = res.data
      } else if (userStore.isAuthenticated) {
        // Tentatives suivantes : polling simple du statut
        await subscriptionStore.fetchStatus()
        data = { status: subscriptionStore.status, has_access: subscriptionStore.status?.has_access }
      }

      if (data) {
        trackPurchaseIfPaid(data)

        // Progression fluide en une seule montee
        const pct = Math.min(90, 20 + Math.floor((attempt / maxAttempts) * 70))
        updateProgress(2, pct, 'Paiement confirme, activation...')

        // Si guest checkout, auto-login avec les tokens retournes
        if (isGuest && data?.auth) {
          loginFromGuestResponse(data)
          accountCreated.value = Boolean(data.account_created)
          try { await userStore.fetchUser() } catch (_) {}
        }

        if (data?.status) {
          subscriptionStore.status = data.status
          subscriptionStore.loadedAt = Date.now()
        }
        if (data?.session) {
          isGiftPayer.value = Boolean(data.session.is_gift && data.session.is_payer)
          beneficiaryLabel.value = data.session.beneficiary_label || ''
        }

        if (data?.has_access || isGiftPayer.value) {
          if (isGiftPayer.value) {
            const name = beneficiaryLabel.value ? ` pour ${beneficiaryLabel.value}` : ''
            updateProgress(3, 100, `Cadeau active${name} !`)
          } else {
            const msg = accountCreated.value
              ? 'Compte cree et acces active !'
              : 'Acces active avec succes !'
            updateProgress(3, 100, msg)
          }
          await wait(400)
          hasAccess.value = true
          return
        }
      }
    } catch {
      // Silently retry
    }
    await wait(1200)
  }

  // Aucun acces confirme apres toutes les tentatives
  paymentFailed.value = true
  progress.value = 100
  statusMessage.value = "Le paiement n'a pas ete confirme. Veuillez contacter le support."
}

onMounted(() => {
  finalizeSessionIfNeeded()
})
</script>

<style scoped>
.billing-success {
  text-align: center;
  padding: 3rem 1.5rem;
  max-width: 480px;
  margin: 0 auto;
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* Success / Error icons */
.success-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 1.5rem;
  color: #10b981;
  animation: scaleIn 0.4s ease-out;
}
.error-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 1.5rem;
  color: #ef4444;
  animation: scaleIn 0.4s ease-out;
}
.success-icon svg,
.error-icon svg {
  width: 100%;
  height: 100%;
}

.headline {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}
.headline.success {
  color: #059669;
}
.headline.error {
  color: #b91c1c;
}
.status {
  font-size: 1.1rem;
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.5;
}
.success-text {
  color: #374151;
}
.account-created-hint {
  color: #059669;
  font-size: 0.95rem;
  margin-top: -0.5rem;
  margin-bottom: 1.5rem;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
.progress-ring {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 1rem;
}
.progress-ring svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.progress-bg {
  fill: none;
  stroke: #e5e7eb;
  stroke-width: 8;
}
.progress-bar {
  fill: none;
  stroke: #10b981;
  stroke-width: 8;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.4s ease;
}
.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
}

/* Steps Indicator */
.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-top: 1.5rem;
  margin-bottom: 2rem;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.step-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e5e7eb;
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
}
.step.done .step-icon {
  background: #10b981;
  color: white;
}
.step.active .step-icon {
  background: #10b981;
  color: white;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
  animation: pulse 1.5s infinite;
}
.step-label {
  font-size: 0.75rem;
  color: #9ca3af;
  white-space: nowrap;
  transition: color 0.3s ease;
}
.step.done .step-label,
.step.active .step-label {
  color: #374151;
}
.step-line {
  width: 40px;
  height: 3px;
  background: #e5e7eb;
  margin: 0 0.5rem;
  margin-bottom: 1.5rem;
  border-radius: 2px;
  transition: background 0.3s ease;
}
.step-line.done {
  background: #10b981;
}

/* Buttons */
.buttons-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  margin-top: 1rem;
  width: 100%;
}
.btn {
  display: inline-block;
  padding: 14px 28px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
  font-weight: 600;
  font-size: 1rem;
}
.btn-primary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}
.btn-secondary {
  background: #f9fafb;
  color: #6b7280;
  border: 1px solid #e5e7eb;
  padding: 10px 20px;
  font-size: 0.875rem;
}
.btn-secondary:hover {
  background: #f3f4f6;
  color: #374151;
}

/* Animations */
@keyframes scaleIn {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2); }
  50% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0.1); }
}
</style>
