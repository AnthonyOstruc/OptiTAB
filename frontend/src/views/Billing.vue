<template>
  <DashboardLayout>
    <div class="billing">
      <!-- Hero Section -->
      <header class="head">
        <div class="hero-badge">🎓 Réussis tes examens</div>
        <h1>Accède à tous les contenus</h1>
        <p class="sub">Cours complets, exercices corrigés et outils pour progresser en maths</p>
      </header>

      <!-- Value Props -->
      <div class="value-props">
        <div class="value-card">
          <div class="value-icon">📚</div>
          <h3>Contenus vérifiés</h3>
          <p>Créés par des profs expérimentés</p>
        </div>
        <div class="value-card">
          <div class="value-icon">⚡</div>
          <h3>Accès immédiat</h3>
          <p>Commence en 2 minutes</p>
        </div>
        <div class="value-card">
          <div class="value-icon">🎯</div>
          <h3>Sans engagement</h3>
          <p>Annule quand tu veux</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Chargement des offres…</p>
      </div>

      <!-- Pricing Plans -->
      <div v-else>
        <div v-if="cards.length === 0" class="empty">Aucune offre disponible</div>

        <section class="grid">
          <article v-for="c in cards" :key="c.key" class="card" :class="{ recommended: c.recommended }">
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
            <button class="cta-btn" :disabled="submitting || !c.priceId" @click="subscribe(c.priceId)">
              {{ submitting ? 'Redirection…' : c.cta }}
            </button>
            
            <p class="security-note">🔒 Paiement sécurisé • Annulable à tout moment</p>
          </article>
        </section>
        
        <!-- Section Aide -->
        <div class="help-section">
          <h3 class="help-title">Une question ?</h3>
          <p class="help-description">Notre équipe est là pour t'aider</p>
          <div class="help-actions">
            <a href="https://wa.me/33764040251" target="_blank" rel="noopener noreferrer" class="help-btn help-btn-primary">
              <img src="/icons/whatsapp.svg" alt="WhatsApp" class="help-icon" />
              <span>WhatsApp</span>
            </a>
            <a href="mailto:contact@optitab.net" target="_blank" rel="noopener noreferrer" class="help-btn help-btn-secondary">
              <img src="/icons/envelope.svg" alt="Email" class="help-icon" />
              <span>Email</span>
            </a>
          </div>
          <div class="help-badge">
            <span class="badge-icon">⏱️</span>
            <span>7 j/7</span>
            <span class="badge-separator">•</span>
            <span>Réponse sous 24 h</span>
          </div>
        </div>

        <!-- FAQ -->
        <div class="faq-section">
          <FaqSection :faq="faq" />
        </div>
      </div>
    </div>

    <!-- Footer -->
    <Footer />
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { getPlans, createCheckoutSession } from '@/api/subscriptions'
import { DEFAULT_PLANS } from '@/config/subscriptions'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import Footer from '@/components/layout/Footer.vue'
import { faq } from '@/config/homeContent.js'

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
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Header */
.head {
  text-align: center;
  margin-bottom: 3rem;
}

.hero-badge {
  display: inline-block;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.head h1 {
  margin: 0 0 1rem 0;
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1.2;
}

.head .sub {
  color: #64748b;
  font-size: 1.125rem;
  margin: 0;
  line-height: 1.6;
}

/* Value Props */
.value-props {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
}

.value-card {
  text-align: center;
  padding: 1.5rem 1rem;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.value-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.value-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  line-height: 1;
}

.value-card h3 {
  margin: 0 0 0.375rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.value-card p {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
}

/* Loading */
.loading {
  text-align: center;
  padding: 3rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #64748b;
  font-size: 1rem;
}

.empty {
  text-align: center;
  color: #94a3b8;
  padding: 3rem 0;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

/* Card */
.card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.card.recommended {
  border-color: #3b82f6;
  border-width: 3px;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.15);
}

.badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: #78350f;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 6px 16px;
  border-radius: 20px;
  white-space: nowrap;
}

.savings-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 8px;
}

.card-header {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-top: 0.5rem;
}

.plan-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.plan-subtitle {
  margin: 0;
  color: #64748b;
  font-size: 0.875rem;
}

.price-section {
  text-align: center;
  padding: 1.5rem 0;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #f1f5f9;
}

.price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.5rem;
}

.amount {
  font-size: 3rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
}

.period {
  font-size: 1rem;
  color: #64748b;
  font-weight: 500;
}

.features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
  flex: 1;
}

.features li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0;
  color: #475569;
  font-size: 0.95rem;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
}

.card-reviews {
  padding: 1rem 0;
  margin: 0.5rem 0 1rem 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
}

.cta-btn {
  width: 100%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.security-note {
  text-align: center;
  margin: 1rem 0 0 0;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
  font-size: 0.8rem;
  color: #94a3b8;
}

/* Help Section */
.help-section {
  text-align: center;
  padding: 3rem 2.5rem;
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  margin-top: 4rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.help-title {
  margin: 0 0 1rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.02em;
}

.help-description {
  margin: 0 0 2rem 0;
  color: #64748b;
  font-size: 1.05rem;
  line-height: 1.6;
}

.help-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.75rem;
}

.help-btn {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.75rem;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 1rem;
  min-width: 160px;
  justify-content: center;
}

.help-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.help-btn-primary {
  background: linear-gradient(135deg, #25D366, #22c55e);
  color: #111827;
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
  
  .help-icon {
    filter: brightness(0) saturate(100%) invert(7%) sepia(1%) saturate(0%) hue-rotate(0deg) brightness(98%) contrast(100%);
  }
  
  &:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(37, 211, 102, 0.4);
  }
}

.help-btn-secondary {
  background: white;
  color: #475569;
  border: 2px solid #cbd5e1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  
  .help-icon {
    filter: brightness(0) saturate(100%) invert(36%) sepia(11%) saturate(557%) hue-rotate(177deg) brightness(94%) contrast(90%);
  }
  
  &:hover {
    border-color: #3b82f6;
    color: #1e293b;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.15);
    
    .help-icon {
      filter: brightness(0) saturate(100%) invert(46%) sepia(98%) saturate(2618%) hue-rotate(205deg) brightness(100%) contrast(91%);
    }
  }
}

.help-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  border-radius: 24px;
  font-size: 0.875rem;
  color: #475569;
  font-weight: 600;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.badge-icon {
  font-size: 0.875rem;
  line-height: 1;
}

.badge-separator {
  color: #94a3b8;
  font-weight: 400;
}

/* FAQ Section */
.faq-section {
  margin-top: 4rem;
  padding-top: 3rem;
  border-top: 2px solid #f1f5f9;
}

/* Footer */
:deep(.footer) {
  width: 100%;
  margin-top: 3rem;
}

/* Responsive */
@media (max-width: 768px) {
  .billing {
    padding: 1.5rem 0.75rem;
  }
  
  .head h1 {
    font-size: 1.875rem;
  }
  
  .head .sub {
    font-size: 1rem;
  }

  .value-props {
    grid-template-columns: 1fr;
    gap: 0.875rem;
  }

  .value-card {
    padding: 1.25rem 1rem;
  }

  .value-icon {
    font-size: 2rem;
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
  
  .help-section {
    padding: 2.5rem 1.5rem;
  }

  .help-title {
    font-size: 1.625rem;
  }

  .help-description {
    font-size: 0.95rem;
    margin-bottom: 1.75rem;
  }
  
  .help-actions {
    flex-direction: column;
    gap: 0.875rem;
  }
  
  .help-btn {
    width: 100%;
    justify-content: center;
    padding: 0.875rem 1.5rem;
  }

  .help-badge {
    font-size: 0.8125rem;
    padding: 0.5rem 1rem;
  }

  .faq-section {
    margin-top: 3rem;
    padding-top: 2rem;
  }

  :deep(.footer) {
    margin-top: 2.5rem;
  }
}

@media (max-width: 480px) {
  .billing {
    padding: 1rem 0.5rem;
  }
  
  .head h1 {
    font-size: 1.5rem;
  }
  
  .head .sub {
    font-size: 0.9rem;
  }

  .value-card {
    padding: 1rem;
  }

  .value-icon {
    font-size: 1.75rem;
  }

  .value-card h3 {
    font-size: 0.9rem;
  }

  .value-card p {
    font-size: 0.8rem;
  }
  
  .amount {
    font-size: 2rem;
  }

  .help-section {
    padding: 2rem 1.25rem;
  }

  .help-title {
    font-size: 1.375rem;
  }

  .help-description {
    font-size: 0.875rem;
  }

  .help-btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.9375rem;
  }

  .help-icon {
    width: 18px;
    height: 18px;
  }

  .help-badge {
    font-size: 0.75rem;
    padding: 0.4rem 0.875rem;
  }

  .faq-section {
    margin-top: 2.5rem;
    padding-top: 1.5rem;
  }

  :deep(.footer) {
    margin-top: 2rem;
  }
}
</style>

