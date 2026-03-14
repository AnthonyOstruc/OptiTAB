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
import { finalizeCheckoutSession } from '@/api/subscriptions'
import * as analytics from '@/services/analytics'

const route = useRoute()
const subscriptionStore = useSubscriptionStore()

const statusMessage = ref('Connexion avec Stripe...')
const hasAccess = ref(false)
const isGiftPayer = ref(false)
const beneficiaryLabel = ref('')
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

async function finalizeSessionIfNeeded() {
  if (!sessionId.value) {
    updateProgress(1, 100, 'Redirection vers le tableau de bord...')
    hasAccess.value = true
    return
  }

  updateProgress(1, 20, 'Verification du paiement...')

  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      const { data } = await finalizeCheckoutSession(sessionId.value)
      trackPurchaseIfPaid(data)
      
      updateProgress(2, 50, 'Paiement confirme, activation...')
      
      if (data?.status) {
        subscriptionStore.status = data.status
        subscriptionStore.loadedAt = Date.now()
      }
      if (data?.session) {
        isGiftPayer.value = Boolean(data.session.is_gift && data.session.is_payer)
        beneficiaryLabel.value = data.session.beneficiary_label || ''
      }
      if (data?.has_access || isGiftPayer.value) {
        updateProgress(3, 80, 'Finalisation...')
        return
      }
    } catch {
      // Silently retry - no error display
      progress.value = Math.min(40, 15 + attempt * 5)
    }
    await wait(1200)
  }
  
  updateProgress(2, 50, 'Synchronisation en cours...')
}

onMounted(async () => {
  await finalizeSessionIfNeeded()
  
  if (isGiftPayer.value) {
    const name = beneficiaryLabel.value ? ` pour ${beneficiaryLabel.value}` : ''
    updateProgress(3, 100, `Cadeau active${name} !`)
    await wait(500)
    hasAccess.value = true
    return
  }

  updateProgress(3, 70, 'Activation de ton acces...')
  
  const totalAttempts = 10
  for (let i = 0; i < totalAttempts; i++) {
    await subscriptionStore.fetchStatus()
    const accessGranted = subscriptionStore.status?.has_access
    progress.value = 70 + Math.floor((i / totalAttempts) * 25)
    
    if (accessGranted) {
      updateProgress(3, 100, 'Acces active avec succes !')
      await wait(400)
      hasAccess.value = true
      return
    }
    await wait(1200)
  }
  
  // Pas de succès forcé: aucun accès tant que le paiement n'est pas confirmé.
  paymentFailed.value = true
  progress.value = 100
  statusMessage.value = 'Le paiement n’a pas été confirmé. Aucun accès supplémentaire n’a été débloqué.'
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

/* Success State */
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
.success-icon svg {
  width: 100%;
  height: 100%;
}
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
