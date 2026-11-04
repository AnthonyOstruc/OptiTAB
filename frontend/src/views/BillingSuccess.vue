<template>
  <PaiementCadre>
    <!-- Accès activé (ou cadeau activé) -->
    <template v-if="isSuccess">
      <span class="pc-icone" aria-hidden="true"><CheckIcon /></span>
      <h1>{{ headline }}</h1>
      <p class="pc-texte">{{ texteSucces }}</p>
      <ul v-if="!isGiftPayer" class="bs-recap">
        <li><BookOpenIcon aria-hidden="true" />Tous les chapitres de ta classe sont débloqués</li>
        <li><EnvelopeIcon aria-hidden="true" />Ta facture t’est envoyée par e-mail</li>
        <li><CreditCardIcon aria-hidden="true" />Tu gères ton abonnement depuis « Mon abonnement »</li>
      </ul>
      <p v-if="accountCreated" class="bs-info">
        Un e-mail t’a été envoyé pour choisir ton mot de passe.
      </p>
      <router-link class="pc-btn" :to="isGiftPayer ? '/subscription' : '/chapitres'">
        {{ primaryLabel }}
        <ArrowRightIcon aria-hidden="true" />
      </router-link>
      <router-link class="pc-lien" to="/dashboard">Aller à l’accueil</router-link>
    </template>

    <!-- Paiement non confirmé -->
    <template v-else-if="isFailure">
      <span class="pc-icone pc-icone--alerte" aria-hidden="true"><ExclamationTriangleIcon /></span>
      <h1>Paiement non confirmé</h1>
      <p class="pc-texte">
        Nous n’avons pas encore reçu la confirmation de ton paiement. Si ton compte a été débité,
        écris-nous : nous réglons ça rapidement.
      </p>
      <router-link class="pc-btn" to="/billing">Réessayer</router-link>
      <router-link class="pc-lien" to="/dashboard">Aller à l’accueil</router-link>
    </template>

    <!-- Activation en cours -->
    <template v-else>
      <span class="bs-attente" aria-hidden="true"></span>
      <h1>Activation de ton accès</h1>
      <p class="pc-texte">{{ statusMessage }}</p>
      <ol class="bs-etapes" aria-label="Étapes">
        <li v-for="(nom, i) in ETAPES" :key="nom" :class="{ 'is-fait': i + 1 < etapeVisible || etapeVisible === 3, 'is-encours': i + 1 === etapeVisible && etapeVisible < 3 }">
          <span class="bs-etapes__point" aria-hidden="true"><CheckIcon /></span>
          {{ nom }}
        </li>
      </ol>
      <p class="bs-patience">Cela prend quelques secondes, ne ferme pas cette page.</p>
    </template>
  </PaiementCadre>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUserStore } from '@/stores/user'
import { finalizeCheckoutSession, finalizeGuestCheckoutSession } from '@/api/subscriptions'
import * as analytics from '@/services/analytics'
import PaiementCadre from '@/components/payments/PaiementCadre.vue'
import { ArrowRightIcon, BookOpenIcon, CheckIcon, CreditCardIcon, EnvelopeIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const ETAPES = ['Paiement reçu', 'Vérification', 'Accès activé']
// De retour du paiement, il est forcément reçu : on affiche au moins l'étape 2.
const etapeVisible = computed(() => Math.max(2, step.value))

const route = useRoute()
const subscriptionStore = useSubscriptionStore()
const userStore = useUserStore()

const statusMessage = ref('Connexion au service de paiement…')
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
const headline = computed(() => {
  if (accountCreated.value) return 'Bienvenue sur OptiTAB !'
  if (isGiftPayer.value) return 'Ton cadeau est activé'
  return 'Ton accès est activé'
})
const primaryLabel = computed(() => (isGiftPayer.value ? 'Voir mon abonnement' : 'Commencer mes chapitres'))
const texteSucces = computed(() => {
  if (isGiftPayer.value) {
    return beneficiaryLabel.value
      ? `${beneficiaryLabel.value} a maintenant accès à tout OptiTAB. Tu retrouves cet abonnement dans « Mon abonnement ».`
      : 'Le bénéficiaire a maintenant accès à tout OptiTAB. Tu retrouves cet abonnement dans « Mon abonnement ».'
  }
  if (accountCreated.value) return 'Ton compte est créé et ton accès est activé. Merci de ta confiance !'
  return 'Merci de ta confiance ! Tout le programme de ta classe t’attend.'
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
  const tiktokEventId = String(payment.tiktok_event_id || '').trim()
  if (transactionId && readTrackedPurchase(transactionId)) {
    purchaseTracked.value = true
    return
  }

  const statusPlan = data?.status?.plan || {}
  analytics.purchase({
    value,
    currency: payment.currency || 'EUR',
    transactionId,
    eventId: tiktokEventId,
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
    updateProgress(3, 100, 'Accès activé !')
    hasAccess.value = true
    return
  }

  updateProgress(1, 20, 'Vérification du paiement…')

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
        updateProgress(2, pct, 'Paiement confirmé, activation de ton accès…')

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
            updateProgress(3, 100, `Cadeau activé${name} !`)
          } else {
            const msg = accountCreated.value
              ? 'Compte créé et accès activé !'
              : 'Accès activé !'
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
  statusMessage.value = "Le paiement n'a pas été confirmé."
}

onMounted(() => {
  finalizeSessionIfNeeded()
})
</script>

<style scoped>
/* Cadre, titres, boutons : components/payments/PaiementCadre.vue */
.bs-recap {
  display: grid;
  gap: 10px;
  width: 100%;
  margin: 0 0 24px;
  padding: 18px 20px;
  border-radius: 16px;
  background: #f5f7fb;
  list-style: none;
  text-align: left;
}

.bs-recap li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  color: #172033;
}

.bs-recap svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: #1b3c8e;
}

.bs-info {
  margin: -8px 0 20px;
  padding: 10px 14px;
  border-radius: 12px;
  background: #eef1f8;
  font-size: 14px;
  color: #1b3c8e;
}

/* Activation en cours */
.bs-attente {
  width: 64px;
  height: 64px;
  margin-bottom: 22px;
  border: 5px solid #e3e7ef;
  border-top-color: #1b3c8e;
  border-radius: 50%;
  animation: bs-tourne 0.9s linear infinite;
}

@keyframes bs-tourne {
  to { transform: rotate(360deg); }
}

.bs-etapes {
  display: grid;
  gap: 10px;
  width: 100%;
  max-width: 280px;
  margin: 0 0 22px;
  padding: 0;
  list-style: none;
  text-align: left;
}

.bs-etapes li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 600;
  color: #98a2b3;
}

.bs-etapes__point {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border: 2px solid #e3e7ef;
  border-radius: 50%;
  color: transparent;
}

.bs-etapes__point svg {
  width: 14px;
  height: 14px;
  stroke-width: 3;
}

.bs-etapes li.is-encours {
  color: #172033;
}

.bs-etapes li.is-encours .bs-etapes__point {
  border-color: #1b3c8e;
  box-shadow: 0 0 0 4px rgba(27, 60, 142, 0.12);
}

.bs-etapes li.is-fait {
  color: #3b8544;
}

.bs-etapes li.is-fait .bs-etapes__point {
  border-color: #3b8544;
  background: #3b8544;
  color: #fff;
}

.bs-patience {
  margin: 0;
  font-size: 13.5px;
  color: #667085;
}

@media (prefers-reduced-motion: reduce) {
  .bs-attente {
    animation-duration: 2.5s;
  }
}
</style>
