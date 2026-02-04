<template>
  <div class="billing-success">
    <h1>{{ headline }}</h1>
    <p class="status">{{ statusMessage }}</p>

    <div v-if="checking" class="spinner"></div>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <div class="buttons-row">
      <router-link class="btn btn-primary" :class="{ disabled: !isSuccess && checking }" to="/dashboard">
        {{ primaryLabel }}
      </router-link>
      
      <router-link v-if="!isSuccess" class="btn btn-secondary" to="/billing">
        Annuler / Changer d'offre
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionStore } from '@/stores/subscription'
import { finalizeCheckoutSession } from '@/api/subscriptions'

const route = useRoute()
const subscriptionStore = useSubscriptionStore()

const statusMessage = ref('Merci ! Votre abonnement est en cours d’activation.')
const errorMessage = ref('')
const checking = ref(false)
const hasAccess = ref(false)
const isGiftPayer = ref(false)
const beneficiaryLabel = ref('')

const sessionId = computed(() => route.query.session_id || '')
const isSuccess = computed(() => hasAccess.value || isGiftPayer.value)
const headline = computed(() => {
  if (isGiftPayer.value) return 'Paiement confirmé'
  return hasAccess.value ? 'Accès activé 🎉' : 'Validation du paiement en cours…'
})
const primaryLabel = computed(() => {
  if (isGiftPayer.value) return 'Retour au tableau de bord'
  return hasAccess.value ? 'Accéder au tableau de bord' : 'Retour au tableau de bord'
})

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms))

async function finalizeSessionIfNeeded() {
  if (!sessionId.value) return

  checking.value = true
  statusMessage.value = 'Nous confirmons votre paiement auprès de Stripe…'

  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const { data } = await finalizeCheckoutSession(sessionId.value)
      if (data?.status) {
        subscriptionStore.status = data.status
        subscriptionStore.loadedAt = Date.now()
      }
      if (data?.session) {
        isGiftPayer.value = Boolean(data.session.is_gift && data.session.is_payer)
        beneficiaryLabel.value = data.session.beneficiary_label || ''
      }
      if (data?.has_access) {
        statusMessage.value = 'Paiement confirmé, activation en cours…'
        break
      }
    } catch (error) {
      errorMessage.value = 'Impossible de confirmer la session Stripe. Nouvel essai…'
    }
    await wait(1500)
  }

  checking.value = false
}

onMounted(async () => {
  await finalizeSessionIfNeeded()
  if (isGiftPayer.value) {
    const name = beneficiaryLabel.value ? ` pour ${beneficiaryLabel.value}` : ''
    statusMessage.value = `Paiement confirmé${name}. L'accès de l'élève est en cours d'activation.`
    errorMessage.value = ''
    return
  }

  hasAccess.value = await subscriptionStore.refreshUntilAccess({ attempts: 8, interval: 1500 })

  if (hasAccess.value) {
    statusMessage.value = 'Ton accès complet est maintenant débloqué 🎉'
    errorMessage.value = ''
  } else {
    errorMessage.value = "Nous n'arrivons pas à confirmer l'activation automatiquement. Contacte le support si le problème persiste."
  }
})
</script>

<style scoped>
.billing-success {
  text-align: center;
  padding: 3rem 1rem;
  max-width: 540px;
  margin: 0 auto;
}
.status {
  margin-bottom: 1rem;
  color: #4b5563;
}
.spinner {
  width: 40px;
  height: 40px;
  margin: 1rem auto;
  border: 3px solid #e5e7eb;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
.error {
  color: #dc2626;
  margin-bottom: 1rem;
}
.buttons-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  margin-top: 16px;
}
.btn {
  display: inline-block;
  padding: 10px 16px;
  border-radius: 6px;
  text-decoration: none;
  transition: opacity 0.2s, background 0.2s;
  font-weight: 500;
}
.btn-primary {
  background: #10b981;
  color: white;
}
.btn-primary:hover {
  background: #059669;
}
.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}
.btn-secondary:hover {
  background: #e5e7eb;
}
.btn.disabled {
  pointer-events: none;
  opacity: 0.6;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
