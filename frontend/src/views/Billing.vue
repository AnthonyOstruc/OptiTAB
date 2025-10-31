<template>
  <div class="billing">
    <h1>Abonnement</h1>
    <p>Choisissez un plan pour démarrer.</p>

    <div v-if="loading" class="loading">Chargement des plans...</div>
    <div v-else>
      <div v-if="plans.length === 0">Aucun plan disponible pour le moment.</div>
      <div class="plans">
        <div v-for="p in plans" :key="p.id" class="plan">
          <h3>{{ p.name }} — {{ humanPeriod(p.billing_period) }}</h3>
          <p class="price">{{ p.price.toFixed(2) }} €</p>
          <ul class="features">
            <li v-for="(f, idx) in p.features" :key="idx">{{ f }}</li>
          </ul>
          <button class="btn-primary" :disabled="submitting" @click="subscribe(p.stripe_price_id)">
            {{ submitting ? 'Redirection...' : 'S’abonner' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getPlans, createCheckoutSession } from '@/api/subscriptions'

const plans = ref([])
const loading = ref(true)
const submitting = ref(false)

const humanPeriod = (p) => (p === 'monthly' ? 'Mensuel' : p === 'yearly' ? 'Annuel' : p)

onMounted(async () => {
  try {
    const { data } = await getPlans()
    plans.value = data?.plans || []
  } finally {
    loading.value = false
  }
})

async function subscribe(priceId) {
  try {
    submitting.value = true
    const { data } = await createCheckoutSession(priceId)
    if (data?.checkout_url) {
      window.location.assign(data.checkout_url)
    }
  } catch (e) {
    alert('Impossible de démarrer le paiement. Veuillez réessayer.')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.plans { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.plan { border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; background: #fff; }
.price { font-size: 1.25rem; font-weight: 600; margin: 8px 0; }
.btn-primary { background: #3b82f6; color: #fff; border: none; padding: 10px 12px; border-radius: 6px; cursor: pointer; }
.btn-primary:disabled { opacity: 0.7; cursor: default; }
</style>

