<template>
  <div class="billing-success">
    <h1>{{ hasAccess ? 'Accès activé 🎉' : 'Validation du paiement en cours…' }}</h1>
    <p class="status">{{ statusMessage }}</p>

    <div v-if="checking" class="spinner"></div>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <router-link class="btn" :class="{ disabled: !hasAccess }" to="/dashboard">
      {{ hasAccess ? 'Accéder au tableau de bord' : 'Retour au tableau de bord' }}
    </router-link>
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

const sessionId = computed(() => route.query.session_id || '')

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
.btn {
  display: inline-block;
  margin-top: 16px;
  background: #10b981;
  color: white;
  padding: 10px 16px;
  border-radius: 6px;
  text-decoration: none;
  transition: opacity 0.2s;
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
