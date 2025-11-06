<template>
  <section class="pricing-plans-section" id="tarifs">
    <!-- Header -->
    <div class="pricing-header">
      <h2 class="pricing-title">
        Choisissez votre <span class="pricing-highlight">Abonnement</span>
      </h2>
      <p class="pricing-desc">Des formules adaptées à tous les besoins, sans engagement</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Chargement des offres…</p>
    </div>

    <!-- Pricing Cards -->
    <div v-else>
      <div v-if="cards.length === 0" class="empty">Aucune offre disponible</div>

      <div v-else class="pricing-grid">
        <article v-for="c in cards" :key="c.key" class="pricing-card" :class="{ recommended: c.recommended }">
          <!-- Badge Populaire -->
          <div v-if="c.recommended" class="badge">
            ⭐ Le plus populaire
          </div>
          
          <!-- Économies -->
          <div v-if="c.recommended && c.savings" class="savings-badge">
            Économise {{ c.savings }}%
          </div>
          
          <!-- En-tête -->
          <div class="card-header">
            <h3 class="plan-title">{{ c.title }}</h3>
            <p class="plan-subtitle">{{ c.subtitle }}</p>
          </div>
          
          <!-- Prix -->
          <div class="price-section">
            <div class="price">
              <span class="amount">{{ c.price.toFixed(2) }}€</span>
              <span v-if="c.per" class="period">{{ c.per }}</span>
            </div>
          </div>
          
          <!-- Fonctionnalités -->
          <ul class="features">
            <li v-for="(f, i) in c.features" :key="i">
              <svg class="check-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span>{{ f }}</span>
            </li>
          </ul>
          
          <!-- Avis Google -->
          <div class="card-reviews">
            <GoogleReviewsCompact />
          </div>
          
          <!-- Bouton d'action -->
          <button class="cta-btn" :disabled="submitting || !c.priceId" @click="handleSubscribe(c.priceId)">
            {{ submitting ? 'Redirection…' : c.cta }}
          </button>
          
          <p class="security-note">🔒 Paiement sécurisé • Annulable à tout moment</p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { getPlans, createCheckoutSession } from '@/api/subscriptions'
import { DEFAULT_PLANS } from '@/config/subscriptions'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'

const plans = ref([])
const loading = ref(true)
const submitting = ref(false)

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

  // Calculer l'économie pour le mensuel vs hebdomadaire
  const weeklyPrice = weekly ? Number(weekly.price || 0) : 0
  const monthlyPrice = monthly ? Number(monthly.price || 0) : 0
  const weeklyMonthlyEquivalent = weeklyPrice * 4 // 4 semaines = 1 mois
  const savings = weeklyPrice > 0 && monthlyPrice > 0 
    ? Math.round(((weeklyMonthlyEquivalent - monthlyPrice) / weeklyMonthlyEquivalent) * 100)
    : null

  const out = []
  if (monthly) out.push({
    key: `m-${monthly.id}`,
    title: 'Mensuel',
    subtitle: 'Sans engagement',
    price: Number(monthly.price || 0),
    per: '/ mois',
    features: monthly.features?.length ? monthly.features : baseFeatures,
    priceId: monthly.stripe_price_id,
    cta: "S'abonner",
    recommended: true,
    savings: savings,
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
    cta: "S'abonner",
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
    cta: "S'abonner",
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

async function handleSubscribe(priceId) {
  try {
    submitting.value = true
    if (!priceId) {
      alert('Ce plan doit encore être configuré (Price ID manquant).')
      return
    }
    const { data } = await createCheckoutSession(priceId)
    if (data?.url) {
      window.location.href = data.url
    } else {
      alert('Une erreur est survenue.')
    }
  } catch (err) {
    console.error(err)
    alert('Une erreur est survenue.')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.pricing-plans-section {
  padding: 80px 0;
  background: #f8f9fa;
}

.pricing-header {
  max-width: 800px;
  margin: 0 auto 60px;
  text-align: center;
  padding: 0 2vw;
}

.pricing-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 16px;
  line-height: 1.2;
}

.pricing-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.pricing-desc {
  font-size: 1.15rem;
  color: #475569;
  line-height: 1.6;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  
  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(42, 56, 183, 0.1);
    border-top-color: #2a38b7;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 20px;
  }
  
  p {
    color: #64748b;
    font-size: 1rem;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
  font-size: 1.1rem;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2vw;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

.pricing-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 32px 28px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  }
  
  &.recommended {
    border: 2px solid #2a38b7;
    box-shadow: 0 8px 32px rgba(42, 56, 183, 0.2);
    
    &:hover {
      box-shadow: 0 16px 48px rgba(42, 56, 183, 0.25);
    }
  }
}

.badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: white;
  padding: 6px 20px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(42, 56, 183, 0.3);
}

.savings-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
}

.card-header {
  text-align: center;
  margin-bottom: 24px;
  margin-top: 8px;
}

.plan-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
}

.plan-subtitle {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

.price-section {
  text-align: center;
  margin-bottom: 28px;
}

.price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 6px;
}

.amount {
  font-size: 2.5rem;
  font-weight: 900;
  color: #2a38b7;
}

.period {
  font-size: 1rem;
  color: #64748b;
  font-weight: 600;
}

.features {
  list-style: none;
  padding: 0;
  margin: 0 0 28px 0;
  flex: 1;
  
  li {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.5;
  }
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
  margin-top: 2px;
}

.card-reviews {
  margin-bottom: 20px;
}

.cta-btn {
  width: 100%;
  padding: 16px 32px;
  font-size: 1.05rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(42, 56, 183, 0.2);
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(42, 56, 183, 0.3);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.security-note {
  text-align: center;
  font-size: 0.85rem;
  color: #64748b;
  margin: 16px 0 0 0;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .pricing-plans-section {
    padding: 60px 0;
  }
  
  .pricing-header {
    margin-bottom: 48px;
  }
  
  .pricing-title {
    font-size: 2rem;
  }
  
  .pricing-desc {
    font-size: 1rem;
  }
  
  .pricing-card {
    padding: 28px 24px;
  }
  
  .amount {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .pricing-title {
    font-size: 1.75rem;
  }
  
  .badge {
    font-size: 0.75rem;
    padding: 5px 16px;
  }
}
</style>

