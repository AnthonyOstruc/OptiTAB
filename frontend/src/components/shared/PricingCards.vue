<template>
  <div class="pricing-cards-container">
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Chargement des offres...</p>
    </div>

    <template v-else>
      <div v-if="!subscriptionOnly" class="pricing-tabs">
        <button
          class="pricing-tab"
          :class="{ active: activeTab === 'recurring' }"
          @click="activeTab = 'recurring'"
        >
          <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 1l4 4-4 4" />
            <path d="M3 11V9a4 4 0 014-4h14" />
            <path d="M7 23l-4-4 4-4" />
            <path d="M21 13v2a4 4 0 01-4 4H3" />
          </svg>
          Abonnements
        </button>
        <button
          class="pricing-tab"
          :class="{ active: activeTab === 'pass' }"
          @click="activeTab = 'pass'"
        >
          <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
          Pass (paiement unique)
        </button>
      </div>

      <div v-if="displayedCards.length === 0" class="empty-state">
        <p>Aucune offre disponible pour le moment.</p>
      </div>

      <div v-else class="pricing-grid">
        <article
          v-for="card in displayedCards"
          :key="card.key"
          class="pricing-card"
          :class="{
            'is-popular': card.recommended,
            'is-current': isCurrentPlan(card)
          }"
        >
          <div class="card-badge-area">
            <span v-if="card.recommended" class="badge badge-popular">
              Le plus populaire
            </span>
            <span v-if="card.savings" class="badge badge-savings">
              Économise {{ card.savings }}%
            </span>
          </div>

          <div class="card-header">
            <h3 class="card-title">{{ card.title }}</h3>
            <p class="card-subtitle">{{ card.subtitle }}</p>
          </div>

          <div class="card-price">
            <div class="price-amount">{{ card.price.toFixed(2) }}€</div>
            <div v-if="card.per" class="price-period">{{ card.per }}</div>
          </div>

          <ul class="card-features">
            <li v-for="(feature, idx) in card.features" :key="idx">
              <svg class="feature-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ feature }}
            </li>
          </ul>

          <div class="card-reviews">
            <GoogleReviewsCompact />
          </div>

          <button
            class="card-button"
            data-cta-name="subscribe"
            :data-cta-location="ctaLocation"
            :disabled="submitting || !card.priceId || isCardDisabled(card)"
            @click="$emit('select', card)"
          >
            {{ getButtonLabel(card) }}
          </button>

          <p class="card-note">Paiement sécurisé - Annulable à tout moment</p>
        </article>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getPlans } from '@/api/subscriptions'
import { DEFAULT_PLANS } from '@/config/subscriptions'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'

const props = defineProps({
  showCurrentPlan: {
    type: Boolean,
    default: false
  },
  currentPriceId: {
    type: String,
    default: ''
  },
  levelAlreadyUnlocked: {
    type: Boolean,
    default: false
  },
  submitting: {
    type: Boolean,
    default: false
  },
  ctaLocation: {
    type: String,
    default: 'pricing'
  },
  disabledLabel: {
    type: String,
    default: 'Choisir un niveau'
  },
  alreadySubscribedLabel: {
    type: String,
    default: 'Déjà souscrit'
  },
  primaryCtaLabel: {
    type: String,
    default: ''
  },
  subscriptionOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select', 'loaded'])

const plans = ref(DEFAULT_PLANS)
const loading = ref(true)
const activeTab = ref('recurring')

const normalizePeriod = (period) => {
  if (!period) return ''
  const p = period.toLowerCase()
  if (p === 'mensuel' || p === 'monthly') return 'monthly'
  if (p === 'hebdomadaire' || p === 'weekly') return 'weekly'
  if (p === 'annuel' || p === 'yearly') return 'yearly'
  if (p === 'daily' || p === 'journalier') return 'daily'
  return p
}

const planMode = (p) => (p?.mode || p?.plan_mode || '').toLowerCase()
const isOneTime = (p) => planMode(p) === 'one_time' || (p?.access_days && Number(p.access_days) > 0)
const isSubscription = (p) => planMode(p) === 'subscription' && !(p?.access_days && Number(p.access_days) > 0)

const cards = computed(() => {
  const subs = plans.value.filter(isSubscription)
  const passes = plans.value.filter(isOneTime)

  const monthly = subs.find((p) => normalizePeriod(p.billing_period) === 'monthly')
  const weekly = subs.find((p) => normalizePeriod(p.billing_period) === 'weekly')
  const yearly = subs.find((p) => normalizePeriod(p.billing_period) === 'yearly')
  const passYear = passes.find((p) => normalizePeriod(p.billing_period) === 'yearly')
  const passMonth = passes.find((p) => (p.access_days || 0) >= 28 && (p.access_days || 0) < 365 && normalizePeriod(p.billing_period) !== 'yearly')
  const passDay = passes.find((p) => Number(p.access_days) === 1 || normalizePeriod(p.billing_period) === 'daily')

  const baseFeatures = ['Accès complet à OptiTAB', 'Sans engagement', 'Annulable à tout moment']

  const weeklyPrice = weekly ? Number(weekly.price || 0) : 0
  const monthlyPrice = monthly ? Number(monthly.price || 0) : 0
  const weeklyMonthlyEquivalent = weeklyPrice * 4
  const savings = weeklyPrice > 0 && monthlyPrice > 0
    ? Math.round(((weeklyMonthlyEquivalent - monthlyPrice) / weeklyMonthlyEquivalent) * 100)
    : null

  const recurringCards = []
  const passCards = []

  if (monthly) recurringCards.push({
    key: `m-${monthly.id}`,
    title: 'Mensuel',
    subtitle: 'Sans engagement',
    price: Number(monthly.price || 0),
    per: '/ mois',
    features: monthly.features?.length ? monthly.features : baseFeatures,
    priceId: monthly.stripe_price_id,
    cta: "S'abonner",
    recommended: true,
    savings,
    type: 'recurring'
  })

  if (weekly) recurringCards.push({
    key: `w-${weekly.id}`,
    title: 'Hebdomadaire',
    subtitle: 'Flexibilité semaine par semaine',
    price: Number(weekly.price || 0),
    per: '/ semaine',
    features: weekly.features?.length ? weekly.features : [
      'Accès complet à OptiTAB',
      'Idéal pour réviser un contrôle',
      'Sans engagement',
      'Annulable à tout moment'
    ],
    priceId: weekly.stripe_price_id,
    cta: "S'abonner",
    recommended: false,
    type: 'recurring'
  })

  if (yearly) recurringCards.push({
    key: `y-${yearly.id}`,
    title: 'Annuel',
    subtitle: 'Économique sur 12 mois',
    price: Number(yearly.price || 0),
    per: '/ an',
    features: yearly.features?.length ? yearly.features : baseFeatures,
    priceId: yearly.stripe_price_id,
    cta: "S'abonner",
    recommended: false,
    type: 'recurring'
  })

  if (passYear) passCards.push({
    key: `py-${passYear.id}`,
    title: passYear.name || 'Pass Annuel',
    subtitle: 'Paiement unique pour 1 an',
    price: Number(passYear.price || 0),
    per: '',
    features: passYear.features?.length ? passYear.features : ['Accès 12 mois', 'Paiement unique, sans renouvellement'],
    priceId: passYear.stripe_price_id,
    cta: 'Acheter le pass',
    recommended: true,
    type: 'pass'
  })

  if (passMonth) passCards.push({
    key: `pm-${passMonth.id}`,
    title: 'Pass 1 mois',
    subtitle: 'Paiement unique',
    price: Number(passMonth.price || 0),
    per: '',
    features: passMonth.features?.length ? passMonth.features : ['Accès 30 jours', 'Idéal pour réviser'],
    priceId: passMonth.stripe_price_id,
    cta: 'Acheter le pass',
    recommended: false,
    type: 'pass'
  })

  if (passDay) passCards.push({
    key: `pd-${passDay.id}`,
    title: 'Pass 24h',
    subtitle: 'Accès rapide',
    price: Number(passDay.price || 0),
    per: '/ jour',
    features: passDay.features?.length ? passDay.features : ['Accès 24 heures', 'Parfait pour un contrôle'],
    priceId: passDay.stripe_price_id,
    cta: 'Acheter le pass',
    recommended: false,
    type: 'pass'
  })

  return { recurring: recurringCards, pass: passCards, all: [...recurringCards, ...passCards] }
})

const displayedCards = computed(() => {
  if (activeTab.value === 'recurring') return cards.value.recurring
  if (activeTab.value === 'pass') return cards.value.pass
  return cards.value.all
})

const isCurrentPlan = (card) => {
  if (!props.showCurrentPlan || !props.currentPriceId) return false
  return card.priceId === props.currentPriceId && props.levelAlreadyUnlocked
}

const isCardDisabled = (card) => {
  if (props.showCurrentPlan && props.levelAlreadyUnlocked) return true
  if (props.showCurrentPlan && isCurrentPlan(card)) return true
  return false
}

const getButtonLabel = (card) => {
  if (props.showCurrentPlan && props.levelAlreadyUnlocked) return props.alreadySubscribedLabel
  if (props.showCurrentPlan && isCurrentPlan(card)) return 'Déjà abonné'
  if (props.submitting) return 'Redirection...'
  if (props.primaryCtaLabel && props.primaryCtaLabel.trim()) return props.primaryCtaLabel.trim()
  return card.cta
}

onMounted(async () => {
  try {
    const { data } = await getPlans()
    const remote = data?.plans || []
    if (remote.length) {
      plans.value = remote
    }
    emit('loaded', plans.value)
  } catch (e) {
    console.error('Erreur chargement plans:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped lang="scss">
.pricing-cards-container {
  width: 100%;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e5e5;
  border-top-color: #2563eb;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pricing-tabs {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  background: #f1f5f9;
  border-radius: 12px;
  padding: 0.375rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.pricing-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
}

.pricing-tab:hover {
  color: #334155;
  background: rgba(255, 255, 255, 0.5);
}

.pricing-tab.active {
  background: white;
  color: #1e40af;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.tab-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.75rem;
  align-items: start;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 768px) {
  .pricing-grid {
    grid-template-columns: 1fr;
  }
}

.pricing-card {
  background: white;
  border: 2px solid #e5e5e5;
  border-radius: 16px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  height: 100%;
}

.pricing-card:hover {
  border-color: #2563eb;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
  transform: translateY(-4px);
}

.pricing-card.is-popular {
  border-color: #2563eb;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
  position: relative;
}

.pricing-card.is-current {
  border-color: #10b981;
}

.card-badge-area {
  min-height: 32px;
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.025em;
}

.badge-popular {
  background: #fbbf24;
  color: #78350f;
}

.badge-savings {
  background: #10b981;
  color: white;
}

.card-header {
  text-align: center;
  margin-bottom: 1.25rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.375rem;
}

.card-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.card-price {
  text-align: center;
  margin-bottom: 1.5rem;
}

.price-amount {
  font-size: 2.75rem;
  font-weight: 800;
  color: #111827;
  line-height: 1;
}

.price-period {
  color: #6b7280;
  font-size: 1rem;
  margin-top: 0.25rem;
}

.card-features {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
  flex-grow: 1;
}

.card-features li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.5rem 0;
  color: #374151;
  font-size: 0.925rem;
}

.feature-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.card-reviews {
  margin-bottom: 1.25rem;
}

.card-button {
  width: 100%;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.card-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.card-button:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.card-note {
  text-align: center;
  margin-top: 0.875rem;
  color: #9ca3af;
  font-size: 0.8rem;
}
</style>
