<template>
  <DashboardLayout>
    <div class="billing">
      <header class="head">
        <h1>Choisissez votre offre</h1>
        <p class="sub">Accédez à tous les contenus d'OptiTAB</p>
      </header>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Chargement des offres…</p>
      </div>
      <div v-else>
        <div v-if="cards.length === 0" class="empty">Aucune offre disponible pour le moment.</div>

        <section class="grid">
          <article v-for="c in cards" :key="c.key" class="card" :class="{ recommended: c.recommended }">
            <div v-if="c.recommended" class="badge">Recommandé</div>
            
            <div class="card-header">
              <h3 class="plan-title">{{ c.title }}</h3>
              <p class="plan-subtitle">{{ c.subtitle }}</p>
            </div>
            
            <div class="price-section">
              <div class="price">
                <span class="amount">{{ c.price.toFixed(2) }}€</span>
                <span v-if="c.per" class="period">{{ c.per }}</span>
              </div>
            </div>
            
            <ul class="features">
              <li v-for="(f, i) in c.features" :key="i">
                <svg class="check-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span>{{ f }}</span>
              </li>
            </ul>
            
            <button class="cta-btn" :disabled="submitting || !c.priceId" @click="subscribe(c.priceId)">
              {{ submitting ? 'Redirection…' : c.cta }}
            </button>
          </article>
        </section>

        <p class="legal">Annulation possible à tout moment • Paiement sécurisé par Stripe</p>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { getPlans, createCheckoutSession } from '@/api/subscriptions'
import { DEFAULT_PLANS } from '@/config/subscriptions'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'

const plans = ref([])
const loading = ref(true)
const submitting = ref(false)

const humanPeriod = (p) => {
  if (p === 'daily') return 'jour'
  if (p === 'weekly') return 'semaine'
  if (p === 'monthly') return 'mois'
  if (p === 'yearly') return 'an'
  return p
}
const planMode = (p) => (p?.mode || p?.plan_mode || '').toLowerCase()
const isOneTime = (p) => planMode(p) === 'one_time' || (p?.access_days && Number(p.access_days) > 0)
const isSubscription = (p) => planMode(p) === 'subscription' && !(p?.access_days && Number(p.access_days) > 0)

const cards = computed(() => {
  const subs = plans.value.filter(isSubscription)
  const passes = plans.value.filter(isOneTime)

  const monthly = subs.find(p => p.billing_period === 'monthly')
  const weekly = subs.find(p => p.billing_period === 'weekly')
  const yearly = subs.find(p => p.billing_period === 'yearly')
  const passMonth = passes.find(p => (p.access_days || 0) >= 28)
  const passDay = passes.find(p => Number(p.access_days) === 1 || p.billing_period === 'daily')

  const baseFeatures = ['Accès à tous les cours', 'Exercices illimités', 'Suivi des progrès']

  const out = []
  if (monthly) out.push({
    key: `m-${monthly.id}`,
    title: 'Mensuel',
    subtitle: 'Sans engagement',
    price: Number(monthly.price || 0),
    per: '/ mois',
    features: monthly.features?.length ? monthly.features : baseFeatures,
    priceId: monthly.stripe_price_id,
    cta: 'S’abonner',
    recommended: true,
  })
  if (weekly) out.push({
    key: `w-${weekly.id}`,
    title: 'Hebdomadaire',
    subtitle: 'Flexibilité semaine par semaine',
    price: Number(weekly.price || 0),
    per: '/ semaine',
    features: weekly.features?.length ? weekly.features : [
      'Accès à tous les contenus',
      'Renouvellement toutes les semaines',
    ],
    priceId: weekly.stripe_price_id,
    cta: 'S’abonner',
    recommended: false,
  })
  if (yearly) out.push({
    key: `y-${yearly.id}`,
    title: 'Annuel',
    subtitle: 'Économique sur 12 mois',
    price: Number(yearly.price || 0),
    per: '/ an',
    features: yearly.features?.length ? yearly.features : baseFeatures,
    priceId: yearly.stripe_price_id,
    cta: 'S’abonner',
    recommended: false,
  })
  if (passMonth) out.push({
    key: `pm-${passMonth.id}`,
    title: 'Pass 1 mois',
    subtitle: 'Paiement unique',
    price: Number(passMonth.price || 0),
    per: '',
    features: passMonth.features?.length ? passMonth.features : ['Accès 30 jours', 'Idéal pour réviser'],
    priceId: passMonth.stripe_price_id,
    cta: 'Acheter le pass',
    recommended: false,
  })
  if (passDay) out.push({
    key: `pd-${passDay.id}`,
    title: 'Pass 24h',
    subtitle: 'Accès rapide',
    price: Number(passDay.price || 0),
    per: '/ jour',
    features: passDay.features?.length ? passDay.features : ['Accès 24 heures', 'Parfait pour un contrôle'],
    priceId: passDay.stripe_price_id,
    cta: 'Acheter le pass',
    recommended: false,
  })
  return out
})

const orderedPlans = computed(() => {
  // Afficher dans l’ordre souhaité: mensuel 4.99 (badge), annuel 50, pass 1 mois 6.99, pass 1 jour 0.99
  const byKey = (p) => {
    if (isSubscription(p) && p.billing_period === 'monthly') return 0
    if (isSubscription(p) && p.billing_period === 'weekly') return 1
    if (isSubscription(p) && p.billing_period === 'yearly') return 2
    if (isOneTime(p) && (p.access_days || 0) >= 28) return 3
    if (isOneTime(p) && p.access_days === 1) return 4
    return 9
  }
  const withBadges = (plans.value || []).map(p => ({ ...p }))
  // Ajouter un badge “Recommandé” sur le mensuel 4.99
  const monthly = withBadges.find(p => isSubscription(p) && p.billing_period === 'monthly')
  if (monthly) monthly._badge = 'Recommandé'
  return withBadges.sort((a,b) => byKey(a) - byKey(b))
})

onMounted(async () => {
  try {
    const { data } = await getPlans()
    const remote = (data?.plans || [])
    plans.value = remote.length ? remote : DEFAULT_PLANS
  } catch (e) {
    // Fallback to default plans if backend not ready
    plans.value = DEFAULT_PLANS
  } finally {
    loading.value = false
  }
})

async function subscribe(priceId) {
  try {
    submitting.value = true
    if (!priceId) {
      alert('Ce plan doit encore être configuré (Price ID manquant).')
      return
    }
    const { data } = await createCheckoutSession(priceId)
    if (data?.checkout_url) {
      window.location.assign(data.checkout_url)
    }
  } catch (e) {
    const msg = e?.response?.data?.error || 'Impossible de démarrer le paiement. Vérifiez que les plans existent côté admin et que le Price ID est correct.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped lang="scss">
.billing {
  padding: 3rem 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.head {
  text-align: center;
  margin-bottom: 3rem;
}

.head h1 {
  margin: 0 0 0.75rem 0;
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.025em;
}

.head .sub {
  color: #6b7280;
  font-size: 1.125rem;
  margin: 0;
}

/* Loading State */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #6b7280;
  font-size: 1rem;
}

.empty {
  text-align: center;
  color: #9ca3af;
  padding: 3rem 0;
  font-size: 1.125rem;
}

/* Grid Layout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin: 0 auto;
  max-width: 1000px;
}

/* Card Styling */
.card {
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #d1d5db;
}

.card.recommended {
  border-color: #007bff;
  border-width: 2px;
  box-shadow: 0 4px 6px -1px rgba(0, 123, 255, 0.1), 0 2px 4px -1px rgba(0, 123, 255, 0.06);
}

.card.recommended:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 123, 255, 0.15), 0 10px 10px -5px rgba(0, 123, 255, 0.1);
  border-color: #0056b3;
}

/* Badge */
.badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 6px 16px;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 123, 255, 0.3);
}

/* Card Header */
.card-header {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-top: 0.5rem;
}

.plan-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.plan-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 0.95rem;
}

/* Price Section */
.price-section {
  text-align: center;
  padding: 1.5rem 0;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
}

.price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
}

.amount {
  font-size: 3rem;
  font-weight: 800;
  color: #111827;
  line-height: 1;
}

.period {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 500;
}

/* Features List */
.features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
  flex: 1;
}

.features li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.625rem 0;
  color: #374151;
  font-size: 0.95rem;
  line-height: 1.5;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
  margin-top: 2px;
}

/* CTA Button */
.cta-btn {
  width: 100%;
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 1rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 123, 255, 0.2);
  margin-top: auto;
}

.cta-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 123, 255, 0.3);
}

.cta-btn:active:not(:disabled) {
  transform: translateY(0);
}

.cta-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Legal Text */
.legal {
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

/* Responsive */
@media (max-width: 768px) {
  .billing {
    padding: 2rem 1rem;
  }
  
  .head h1 {
    font-size: 1.875rem;
  }
  
  .head .sub {
    font-size: 1rem;
  }
  
  .grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .card {
    padding: 1.5rem;
  }
  
  .amount {
    font-size: 2.5rem;
  }
}
</style>
