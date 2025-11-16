<template>
  <DashboardLayout>
    <div class="billing-page">
      <!-- Header -->
      <div class="page-header">
        <div class="header-badge">
          <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          <span>Abonnement</span>
        </div>
        <h1>Choisissez votre formule</h1>
        <p>Accès illimité aux cours, exercices et outils pour progresser en maths</p>
      </div>

      <!-- Level Selector -->
      <div class="level-selector-card">
        <div class="level-card-header">
          <div>
            <p class="level-eyebrow">Niveau d'accès</p>
            <h2>Choisissez votre niveau</h2>
            <p class="level-subtitle">{{ levelHelper }}</p>
          </div>
        </div>
        <div class="level-select-group">
          <label for="billing-level-select">Niveau disponible</label>
          <div class="level-select-wrapper">
            <select
              id="billing-level-select"
              v-model.number="selectedNiveauId"
              :disabled="niveauxLoading || !niveaux.length"
            >
              <option v-if="niveauxLoading" value="">Chargement...</option>
              <option
                v-for="niveau in niveaux"
                :key="niveau.id"
                :value="niveau.id"
              >
                {{ niveau.nom }}
                <span v-if="niveau.pays?.nom"> — {{ niveau.pays.nom }}</span>
              </option>
            </select>
            <p class="level-hint">
              Choisissez le niveau que vous souhaitez débloquer avec cet abonnement.
            </p>
          </div>
        </div>
        <p v-if="levelReady" class="level-selection-pill">
          Accès prévu : {{ levelDisplay }}
        </p>
        <p v-else-if="levelAlertMessage" class="level-warning">
          {{ levelAlertMessage }}
        </p>
        <div v-if="unlockedLevels.length" class="level-access-chips">
          <span class="access-label">Niveaux déjà débloqués :</span>
          <div class="chips">
            <span v-for="level in unlockedLevels" :key="level.id" class="chip">
              {{ level.nom }}
              <span v-if="level.pays?.nom" class="chip-sub">{{ level.pays.nom }}</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Pricing Cards -->
      <div class="pricing-container">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Chargement des offres…</p>
        </div>

        <div v-else-if="cards.length === 0" class="empty-state">
          <p>Aucune offre disponible pour le moment.</p>
        </div>

        <div v-else class="pricing-grid">
          <div
            v-for="card in cards"
            :key="card.key"
            class="pricing-card"
            :class="{ 
              'is-popular': card.recommended,
              'is-current': isCurrentPlan(card)
            }"
          >
            <!-- Badge -->
            <div class="card-badge-area">
              <span v-if="card.recommended" class="badge badge-popular">
                Le plus populaire
              </span>
              <span v-if="card.savings" class="badge badge-savings">
                Économise {{ card.savings }}%
              </span>
            </div>

            <!-- Header -->
            <div class="card-header">
              <h3 class="card-title">{{ card.title }}</h3>
              <p class="card-subtitle">{{ card.subtitle }}</p>
            </div>

            <!-- Price -->
            <div class="card-price">
              <div class="price-amount">{{ card.price.toFixed(2) }}€</div>
              <div v-if="card.per" class="price-period">{{ card.per }}</div>
            </div>

            <!-- Features -->
            <ul class="card-features">
              <li v-for="(feature, idx) in card.features" :key="idx">
                <svg class="feature-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                {{ feature }}
              </li>
            </ul>

            <!-- Reviews -->
            <div class="card-reviews">
              <GoogleReviewsCompact />
            </div>

            <!-- CTA Button -->
            <button
              class="card-button"
              :disabled="submitting || !card.priceId || levelAlreadyUnlocked || isCurrentPlan(card)"
              @click="handlePlanClick(card)"
            >
              {{ buttonLabel(card) }}
            </button>

            <!-- Security Note -->
            <p class="card-note">🔒 Paiement sécurisé • Annulable à tout moment</p>
          </div>
        </div>
      </div>

      <!-- Contact Section -->
      <div class="contact-section">
        <div class="contact-content">
          <div class="contact-header">
            <h3>Besoin d'aide ?</h3>
            <p>Notre équipe est disponible pour répondre à vos questions</p>
          </div>
          <div class="contact-actions">
            <a
              class="contact-btn whatsapp"
              href="https://wa.me/33764040251"
              target="_blank"
              rel="noopener"
            >
              <svg class="btn-icon whatsapp-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
              <span>WhatsApp</span>
            </a>
            <a
              class="contact-btn email"
              href="mailto:contact@optitab.net"
            >
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
              <span>Email</span>
            </a>
          </div>
        </div>
        <div class="contact-badge">
          <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>Réponse sous 24h</span>
        </div>
      </div>

      <!-- Trust Section -->
      <div class="trust-section">
        <div class="trust-content">
          <span class="trust-text">Utilisé par des étudiants</span>
          <div class="trust-divider"></div>
          <div class="trust-badges">
            <span class="trust-badge">Collège</span>
            <span class="trust-badge">Lycée</span>
            <span class="trust-badge">MPSI</span>
            <span class="trust-badge">BUT</span>
          </div>
        </div>
      </div>

      <!-- Benefits Section -->
      <div class="benefits-section">
        <h2>Pourquoi choisir OptiTAB ?</h2>
        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="benefit-icon">📚</div>
            <h3>Cours complets</h3>
            <p>Cours clairs et progressifs sur les notions essentielles du programme</p>
          </div>
          <div class="benefit-card">
            <div class="benefit-icon">✍️</div>
            <h3>Exercices corrigés</h3>
            <p>Des centaines d'exercices avec corrections détaillées pour progresser rapidement</p>
          </div>
          <div class="benefit-card">
            <div class="benefit-icon">📊</div>
            <h3>Suivi personnalisé</h3>
            <p>Analysez votre progression et identifiez vos points à améliorer</p>
          </div>
          <div class="benefit-card">
            <div class="benefit-icon">🎯</div>
            <h3>Accès illimité</h3>
            <p>Tout le contenu accessible 24/7 sur ordinateur, tablette et mobile</p>
          </div>
        </div>
      </div>

      <!-- FAQ -->
      <div class="faq-section">
        <FaqSection :faq="billingFaq" />
      </div>

      

      <Footer />
    </div>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { getPlans, createCheckoutSession } from '@/api/subscriptions'
import { DEFAULT_PLANS } from '@/config/subscriptions'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import Footer from '@/components/layout/Footer.vue'
// FAQ spécifique à la page Billing (plus court et focalisé)
import { useSubscriptionStore } from '@/stores/subscription'
import { getNiveauxByPays } from '@/api/niveaux'
import { useUserStore } from '@/stores/user'

const plans = ref([])
const loading = ref(true)
const submitting = ref(false)
const subscriptionStore = useSubscriptionStore()
const userStore = useUserStore()

const niveaux = ref([])
const niveauxLoading = ref(false)
const niveauxError = ref('')
const selectedNiveauId = ref(
  userStore.niveau_pays?.id ? Number(userStore.niveau_pays.id) : null
)

watch(
  () => userStore.niveau_pays?.id,
  (newId) => {
    if (newId) {
      selectedNiveauId.value = Number(newId)
    }
  }
)

const offersSectionId = 'billing-offers'
const faqSectionId = 'billing-faq'

const selectedNiveau = computed(() =>
  niveaux.value.find(n => n.id === selectedNiveauId.value) || null
)
const levelReady = computed(() => Boolean(selectedNiveauId.value))
const levelDisplay = computed(() => {
  if (!selectedNiveau.value) return 'Sélectionner un niveau'
  const paysName = selectedNiveau.value.pays?.nom
  return paysName ? `${selectedNiveau.value.nom} · ${paysName}` : selectedNiveau.value.nom
})
const levelHelper = computed(() => 'Ce niveau déterminera les contenus disponibles dans votre espace.')

const levelAlertMessage = computed(() => {
  if (niveauxError.value) {
    return niveauxError.value
  }
  if (!levelReady.value && !niveauxLoading.value) {
    return 'Sélectionnez un niveau avant de finaliser votre abonnement.'
  }
  return ''
})

// Questions fréquentes adaptées à la facturation/abonnement
const billingFaq = [
  {
    question: "Qu'est-ce que j'obtiens avec OptiTAB ?",
    answer: "Cours et fiches clairs, exercices guidés pas à pas, outils de calcul, et un suivi simple de ta progression."
  },
  {
    question: "Comment choisir mon plan ?",
    answer: "Pass 24h (coup de boost) • Hebdo (avant un contrôle) • Mensuel (le plus rentable si tu révises > 2 semaines)."
  },
  {
    question: "Puis-je annuler à tout moment ?",
    answer: "Oui, depuis Mon compte → Abonnement. Tu gardes l'accès jusqu'à la fin de la période payée."
  },
  {
    question: "Puis-je changer de formule (hebdo ⇄ mensuel) ?",
    answer: "Oui, le changement prend effet à la prochaine échéance."
  },
  {
    question: "Le paiement est-il sécurisé ?",
    answer: "Oui, via Stripe. Aucune donnée de carte n'est stockée chez nous."
  },
  {
    question: "Factures disponibles ?",
    answer: "Oui, une facture est envoyée par email après chaque règlement."
  },
  {
    question: "OptiTAB fonctionne sur mobile ?",
    answer: "Oui, le site est responsive (ordinateur, tablette, smartphone)."
  }
]

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

  const baseFeatures = ['Accès complet à OptiTAB', 'Sans engagement', 'Annulable à tout moment']

  const weeklyPrice = weekly ? Number(weekly.price || 0) : 0
  const monthlyPrice = monthly ? Number(monthly.price || 0) : 0
  const weeklyMonthlyEquivalent = weeklyPrice * 4
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
    savings
  })
  if (weekly) out.push({
    key: `w-${weekly.id}`,
    title: 'Hebdomadaire',
    subtitle: 'Flexibilité semaine par semaine',
    price: Number(weekly.price || 0),
    per: '/ semaine',
    features: weekly.features?.length ? weekly.features : [
      'Accès complet à OptiTAB',
      'Idéal pour réviser un contrôle',
      'Sans engagement'
    ],
    priceId: weekly.stripe_price_id,
    cta: "S'abonner",
    recommended: false
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
    recommended: false
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
    recommended: false
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
    recommended: false
  })
  return out
})

const hasActiveSubscription = computed(() =>
  Boolean(subscriptionStore.status?.subscriptions?.some(sub => sub?.is_active))
)
const unlockedLevels = computed(() => subscriptionStore.unlockedLevels || [])
const levelAlreadyUnlocked = computed(() =>
  Boolean(
    selectedNiveauId.value &&
    unlockedLevels.value.some(level => Number(level.id) === Number(selectedNiveauId.value))
  )
)
const activePlanPriceId = computed(() => subscriptionStore.status?.plan_stripe_price_id || '')
const activePlanLabel = computed(() => {
  const name = subscriptionStore.status?.plan_name || ''
  const period = subscriptionStore.status?.plan_billing_period || ''
  if (name && period) return `${name} (${humanPeriod(period)})`
  if (name) return name
  if (period) return `Offre ${humanPeriod(period)}`
  return 'ton offre actuelle'
})

const isCurrentPrice = (priceId) => {
  if (!priceId || !activePlanPriceId.value) return false
  if (priceId !== activePlanPriceId.value) return false
  return levelAlreadyUnlocked.value
}

const isCurrentPlan = (card) => isCurrentPrice(card?.priceId)

const buttonLabel = (card) => {
  if (levelAlreadyUnlocked.value) return 'Niveau débloqué'
  if (isCurrentPlan(card)) return 'Déjà abonné'
  if (!levelReady.value) return 'Choisir un niveau'
  return submitting.value ? 'Redirection…' : card.cta
}

const handlePlanClick = (card) => {
  if (!card?.priceId) return
  if (levelAlreadyUnlocked.value || isCurrentPlan(card) || submitting.value) return
  subscribe(card.priceId)
}

onMounted(async () => {
  try {
    await subscriptionStore.fetchStatus({ force: true }).catch(() => {})
    const { data } = await getPlans()
    const remote = (data?.plans || [])
    plans.value = remote.length ? remote : DEFAULT_PLANS
    await loadNiveauxOptions()
  } catch (e) {
    plans.value = DEFAULT_PLANS
  } finally {
    loading.value = false
  }
})

async function loadNiveauxOptions() {
  try {
    niveauxLoading.value = true
    niveauxError.value = ''
    const data = await getNiveauxByPays()
    const rawList = Array.isArray(data?.results) ? data.results : data || []
    const activeList = rawList.filter(n => n && (n.est_actif === undefined || n.est_actif))
    niveaux.value = activeList

    const selectedStillActive = activeList.some(n => n.id === selectedNiveauId.value)
    if (!selectedStillActive) {
      selectedNiveauId.value = null
    }

    if (!selectedNiveauId.value && activeList.length) {
      const preferredId = userStore.niveau_pays?.id
      const match = preferredId ? activeList.find(n => n.id === Number(preferredId)) : null
      selectedNiveauId.value = match ? match.id : activeList[0].id
    }
  } catch (error) {
    console.error('Erreur chargement niveaux:', error)
    niveauxError.value = 'Impossible de charger la liste des niveaux.'
  } finally {
    niveauxLoading.value = false
  }
}

async function subscribe(priceId) {
  try {
    if (!levelReady.value) {
      alert('Merci de sélectionner un niveau avant de continuer.')
      return
    }
    if (levelAlreadyUnlocked.value) {
      alert('Ce niveau est déjà débloqué. Sélectionnez un autre niveau pour souscrire.')
      return
    }
    const payload = selectedNiveauId.value
      ? { niveau_pays_id: selectedNiveauId.value }
      : {}

    if (isCurrentPrice(priceId)) {
      alert('Vous disposez déjà de cet abonnement actif. Utilisez « Gérer mon abonnement » pour le modifier.')
      return
    }
    if (!priceId) {
      alert('Ce plan doit encore être configuré (Price ID manquant).')
      return
    }
    submitting.value = true
    const { data } = await createCheckoutSession(priceId, payload)
    if (data?.checkout_url) {
      window.location.assign(data.checkout_url)
    }
  } catch (e) {
    const msg = e?.response?.data?.error || 'Impossible de démarrer le paiement. Vérifiez la configuration Stripe.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped lang="scss">
/* Base Layout */
.billing-page {
  min-height: 100vh;
  padding: 2.25rem 1rem; /* dézoom global */
  font-size: 0.96rem; /* lisibilité globale plus compacte */
}

/* Page Header */
.page-header {
  max-width: 800px;
  margin: 0 auto 3rem; /* moins d'espace */
  text-align: center;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  color: #1e40af;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.badge-icon {
  width: 16px;
  height: 16px;
  color: #3b82f6;
}

.page-header h1 {
  font-size: 2.2rem; /* plus compact */
  font-weight: 700;
  color: #111827;
  margin: 0 0 1rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.page-header p {
  font-size: 1rem; /* plus compact */
  color: #6b7280;
  margin: 0;
  line-height: 1.6;
}

.level-selector-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1.75rem 2rem;
  margin: 0 auto 2rem;
  max-width: 960px;
  box-shadow: 0 15px 45px rgba(15, 23, 42, 0.08);
}

.level-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.level-eyebrow {
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: #4c1d95;
  margin: 0 0 0.3rem;
}

.level-card-header h2 {
  margin: 0;
  font-size: 1.45rem;
  color: #0f172a;
}

.level-subtitle {
  margin: 0.2rem 0 0;
  color: #475569;
  font-size: 0.95rem;
}

.level-lock-chip {
  background: #fee2e2;
  color: #b91c1c;
  font-weight: 600;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  font-size: 0.85rem;
}

.level-select-group {
  margin-top: 1.5rem;
}

.level-select-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: #0f172a;
}

.level-select-wrapper select {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 0.85rem 1rem;
  font-size: 1rem;
  background: #f8fafc;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.level-select-wrapper select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.level-hint {
  margin: 0.4rem 0 0;
  font-size: 0.9rem;
  color: #64748b;
}

.level-selection-pill {
  margin-top: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 1rem;
  background: #eef2ff;
  color: #3730a3;
  border-radius: 999px;
  font-weight: 600;
}

.level-warning {
  margin-top: 1rem;
  color: #b91c1c;
  font-weight: 600;
}

.level-access-chips {
  margin-top: 1.25rem;
}

.level-access-chips .access-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #312e81;
  margin-bottom: 0.4rem;
}

.level-access-chips .chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.level-access-chips .chip {
  background: #f3f4ff;
  color: #312e81;
  border: 1px solid #c7d2fe;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.level-access-chips .chip-sub {
  display: inline-block;
  margin-left: 0.35rem;
  font-weight: 400;
  color: #6366f1;
}

/* Pricing Container */
.pricing-container {
  max-width: 1200px;
  margin: 0 auto 3rem; /* moins d'espace */
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem; /* réduit */
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

/* Pricing Grid */
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.75rem; /* léger dézoom global */
  align-items: start;
}

/* Pricing Card */
.pricing-card {
  background: white;
  border: 2px solid #e5e5e5;
  border-radius: 16px;
  padding: 1.75rem; /* léger dézoom */
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

/* Badge Area */
.card-badge-area {
  min-height: 32px;
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
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

/* Card Header */
.card-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
}

.card-subtitle {
  font-size: 0.84rem; /* plus fin */
  color: #666;
  margin: 0;
}

/* Card Price */
.card-price {
  text-align: center;
  margin-bottom: 1.75rem; /* resserré */
  padding-bottom: 1.75rem;
  border-bottom: 1px solid #f0f0f0;
}

.price-amount {
  font-size: 2.75rem; /* dézoom global */
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.price-period {
  font-size: 1rem;
  color: #999;
  font-weight: 500;
}

/* Card Features */
.card-features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem;
  flex: 1;
}

.card-features li {
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  padding: 0.55rem 0;
  font-size: 0.9rem; /* plus compact */
  color: #333;
  line-height: 1.5;
}

.feature-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

/* Card Reviews */
.card-reviews {
  margin-bottom: 1.5rem;
}

/* Card Button */
.card-button {
  width: 100%;
  padding: 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 1rem;
}

.card-button:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.card-button:disabled {
  background: #e5e5e5;
  color: #999;
  cursor: not-allowed;
  transform: none;
}

/* Card Note */
.card-note {
  font-size: 0.75rem;
  color: #999;
  text-align: center;
  margin: 0;
  line-height: 1.4;
}

/* Contact Section */
.contact-section {
  max-width: 900px;
  margin: 0 auto 3rem; /* moins d'espace */
  padding: 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.contact-content {
  padding: 2rem 2.25rem; /* dézoom */
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.contact-header h3 {
  font-size: 1.375rem; /* plus compact */
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem;
  line-height: 1.3;
}

.contact-header p {
  font-size: 0.95rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.contact-actions {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

.contact-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center; /* centre icône + texte */
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  text-align: center;
}

.contact-btn.whatsapp {
  background: #25d366;
  border-color: #25d366;
  color: white;
}

.contact-btn.whatsapp:hover {
  background: #20ba5a;
  border-color: #20ba5a;
  transform: translateY(-1px);
}

.contact-btn.email:hover {
  border-color: #9ca3af;
  background: #f9fafb;
}

.btn-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.contact-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: #f3f4f6;
  border-top: 1px solid #e5e7eb;
  font-size: 0.875rem;
  color: #4b5563;
  font-weight: 500;
}

.badge-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

/* Trust Section */
.trust-section {
  max-width: 1100px;
  margin: 0 auto 3.5rem; /* moins d'espace */
  padding: 0 1rem;
}

.trust-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem; /* resserré */
  flex-wrap: wrap;
  padding: 1.5rem;
  background: #fafbfc;
  border-radius: 10px;
  border: 1px solid #f0f1f3;
}

.trust-text {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
  letter-spacing: 0.005em;
}

.trust-divider {
  width: 1px;
  height: 24px;
  background: #e2e8f0;
}

.trust-badges {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.trust-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.45rem 1.1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.84rem;
  color: #1f2937;
  font-weight: 600;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.trust-badge:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* Benefits Section */
.benefits-section {
  max-width: 1200px;
  margin: 0 auto 3rem; /* moins d'espace */
  padding: 0 1rem;
}

.benefits-section h2 {
  text-align: center;
  font-size: 1.75rem; /* dézoom */
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 2.25rem;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* cartes un peu plus compactes */
  gap: 1.5rem;
}

.benefit-card {
  text-align: center;
  padding: 1.5rem 1.25rem; /* réduit */
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.benefit-card:hover {
  border-color: #2563eb;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.1);
  transform: translateY(-4px);
}

.benefit-icon {
  font-size: 2.5rem; /* dézoom */
  margin-bottom: 0.875rem;
  display: block;
}

.benefit-card h3 {
  font-size: 1.125rem; /* dézoom */
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.6rem;
}

.benefit-card p {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* FAQ Section */
.faq-section {
  max-width: 1200px;
  margin: 0 auto 3rem;
  padding: 0 1rem;
}

/* Footer - Full width */
.billing-page :deep(.footer) {
  width: 100%;
  margin: 0;
  border-radius: 0;
}

/* Manage Section */
.manage-section {
  max-width: 900px;
  margin: 0 auto 4rem;
  padding: 0 1rem;
}

.manage-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding: 2rem 2.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.manage-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem;
  line-height: 1.3;
}

.manage-content p {
  font-size: 0.9375rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.manage-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: #111827;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9375rem;
  text-decoration: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.manage-link:hover {
  background: #1f2937;
  transform: translateX(2px);
}

.manage-link svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 968px) {
  .billing-page {
    padding: 2.5rem 1.25rem;
  }

  .billing-page :deep(.footer) {
    width: 100%;
    margin: 0;
    border-radius: 0;
  }

  .page-header {
    margin-bottom: 3rem;
  }

  .header-badge {
    font-size: 0.8125rem;
    padding: 0.4375rem 0.875rem;
    margin-bottom: 1.25rem;
  }

  .badge-icon {
    width: 14px;
    height: 14px;
  }

  .page-header h1 {
    font-size: 2rem;
    line-height: 1.3;
  }

  .page-header p {
    font-size: 1.0625rem;
  }
 
  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 520px;
    margin: 0 auto;
    gap: 1.25rem;
  }

  .pricing-card {
    padding: 1.75rem 1.5rem;
  }
 
  .contact-content {
    flex-direction: column;
    align-items: flex-start;
    padding: 2rem 1.75rem;
    gap: 1.75rem;
  }
 
  .contact-actions {
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
  }
 
  .contact-btn {
    flex: 1 1 150px;
  }

  .trust-section {
    margin-bottom: 3rem;
  }

  .trust-content {
    gap: 1.25rem;
    padding: 1.5rem 1.25rem;
  }

  .trust-text {
    font-size: 0.8125rem;
  }

  .trust-divider {
    display: none;
  }

  .trust-badges {
    justify-content: center;
    gap: 0.625rem;
  }

  .trust-badge {
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
  }
 
  .benefits-grid {
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1.25rem;
  }

  .benefit-card {
    padding: 1.5rem;
  }
 
  .benefits-section h2 {
    font-size: 1.75rem;
  }

  .manage-card {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.75rem 2rem;
  }

  .manage-link {
    width: 100%;
    justify-content: center;
  }
}
 
@media (max-width: 480px) {
  .page-header {
    margin-bottom: 1.625rem;
  }

  .header-badge {
    font-size: 0.75rem;
    padding: 0.375rem 0.8125rem;
    margin-bottom: 1rem;
  }

  .badge-icon {
    width: 13px;
    height: 13px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .page-header p {
    font-size: 0.875rem;
  }

  .level-selector-card {
    padding: 1.375rem 1.625rem;
    margin-bottom: 1.625rem;
  }

  .level-eyebrow {
    font-size: 0.6875rem;
  }

  .level-card-header h2 {
    font-size: 1.3125rem;
  }

  .level-subtitle {
    font-size: 0.875rem;
  }

  .level-select-wrapper select {
    padding: 0.8125rem 0.9375rem;
    font-size: 0.9375rem;
  }

  .level-hint {
    font-size: 0.8125rem;
  }

  .level-selection-pill {
    font-size: 0.8125rem;
  }

  .level-access-chips .chip {
    font-size: 0.8125rem;
  }

  .trust-section {
    margin-bottom: 2.25rem;
    padding: 0 0.625rem;
  }

  .trust-content {
    padding: 1.125rem 1rem;
    gap: 0.875rem;
  }

  .trust-text {
    font-size: 0.78125rem;
  }

  .trust-badges {
    gap: 0.5rem;
  }

  .trust-badge {
    padding: 0.4rem 0.8125rem;
    font-size: 0.71875rem;
  }

}

@media (max-width: 640px) {
  .billing-page {
    padding: 1.25rem 0.875rem;
  }

  .billing-page :deep(.footer) {
    width: 100%;
    margin: 0;
    border-radius: 0;
  }


  .faq-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: calc(100% + 1.75rem);
    margin-left: -0.875rem;
    margin-right: -0.875rem;
    padding-left: 0;
    padding-right: 0;
  }

  .billing-page :deep(.faq-section) {
    width: 100%;
    max-width: 100%;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .billing-page :deep(.faq-list),
  .billing-page :deep(.faq-item) {
    width: 100%;
  }

  .page-header {
    margin-bottom: 1.5rem;
    padding: 0;
  }

  .header-badge {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
    margin-bottom: 1rem;
    gap: 0.375rem;
  }

  .badge-icon {
    width: 13px;
    height: 13px;
  }

  .page-header h1 {
    font-size: 1.5rem;
    line-height: 1.25;
    margin-bottom: 0.625rem;
  }

  .page-header p {
    font-size: 0.875rem;
    line-height: 1.5;
  }

  .level-selector-card {
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 14px;
  }

  .level-eyebrow {
    font-size: 0.6875rem;
    margin-bottom: 0.25rem;
  }

  .level-card-header h2 {
    font-size: 1.25rem;
  }

  .level-subtitle {
    font-size: 0.875rem;
    margin-top: 0.15rem;
  }

  .level-select-group {
    margin-top: 1.25rem;
  }

  .level-select-group label {
    font-size: 0.875rem;
    margin-bottom: 0.375rem;
  }

  .level-select-wrapper select {
    padding: 0.75rem 0.875rem;
    font-size: 0.9375rem;
    border-radius: 9px;
  }

  .level-hint {
    font-size: 0.8125rem;
    margin-top: 0.375rem;
  }

  .level-selection-pill {
    margin-top: 0.875rem;
    padding: 0.4rem 0.875rem;
    font-size: 0.8125rem;
  }

  .level-warning {
    margin-top: 0.875rem;
    font-size: 0.8125rem;
  }

  .level-access-chips {
    margin-top: 1.125rem;
  }

  .level-access-chips .access-label {
    font-size: 0.8125rem;
    margin-bottom: 0.375rem;
  }

  .level-access-chips .chip {
    padding: 0.3125rem 0.6875rem;
    font-size: 0.8rem;
  }

  .pricing-container {
    margin-bottom: 2.5 rem;
  }

  .pricing-section {
    padding: 0;
    background: transparent;
    border: none;
    box-shadow: none;
  }

  .pricing-header {
    padding: 0;
    margin-bottom: 1.5rem;
  }

  .pricing-header h2 {
    font-size: 1.375rem;
    margin-bottom: 0.5rem;
  }

  .pricing-header p {
    font-size: 0.875rem;
  }

  .pricing-grid {
    gap: 1rem;
  }

  .pricing-card {
    padding: 1.25rem 1.125rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  .pricing-card.recommended {
    border-width: 2px;
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.15);
  }

  .pricing-badge-row {
    min-height: 1.875rem;
    margin-bottom: 0.75rem;
  }

  .pricing-badge {
    padding: 0.4375rem 0.875rem;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .pricing-badge.popular {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  }

  .pricing-badge.savings {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  }

  .card-header {
    margin-bottom: 0.875rem;
  }

  .card-title {
    font-size: 1.25rem;
    margin-bottom: 0.375rem;
    font-weight: 700;
  }

  .card-subtitle {
    font-size: 0.8125rem;
    min-height: 1.25rem;
  }

  .card-price {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
  }

  .price-amount {
    font-size: 2.25rem;
    font-weight: 700;
  }

  .price-period {
    font-size: 0.875rem;
    font-weight: 600;
  }

  .card-features {
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .card-features li {
    font-size: 0.8125rem;
    line-height: 1.4;
    padding: 0.4375rem 0;
  }

  .feature-icon {
    width: 13px;
    height: 13px;
  }

  .card-reviews {
    margin-bottom: 1rem;
  }

  .card-button {
    padding: 0.875rem 1rem;
    font-size: 0.9375rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  }

  .card-button:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
  }

  .card-note {
    font-size: 0.6875rem;
    margin-top: 0.625rem;
    opacity: 0.85;
  }

  .contact-section {
    margin-bottom: 2.5rem;
  }

  .contact-content {
    padding: 1.5rem 1.25rem;
    gap: 1.25rem;
  }
 
  .contact-header h3 {
    font-size: 1.25rem;
    line-height: 1.3;
  }

  .contact-header p {
    font-size: 0.875rem;
    line-height: 1.4;
  }

  .contact-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.625rem;
    width: 100%;
  }

  .contact-btn {
    width: 100%;
    padding: 0.8125rem 1rem;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .contact-btn.whatsapp {
    box-shadow: 0 4px 12px rgba(37, 211, 102, 0.25);
  }

  .btn-icon {
    width: 16px;
    height: 16px;
  }

  .contact-badge {
    padding: 0.625rem 1rem;
    font-size: 0.75rem;
  }

  .badge-icon {
    width: 14px;
    height: 14px;
  }

  .trust-section {
    margin-bottom: 2rem;
    padding: 0 0.5rem;
  }

  .trust-content {
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem 0.875rem;
    text-align: center;
    border-radius: 8px;
  }

  .trust-text {
    font-size: 0.75rem;
    line-height: 1.4;
  }

  .trust-badges {
    gap: 0.4375rem;
    justify-content: center;
  }

  .trust-badge {
    padding: 0.375rem 0.75rem;
    font-size: 0.6875rem;
    border-radius: 6px;
  }

  .benefits-section {
    margin-bottom: 2.5rem;
  }

  .benefits-section h2 {
    font-size: 1.375rem;
    margin-bottom: 1.5rem;
    line-height: 1.3;
  }

  .benefits-grid {
    gap: 1rem;
    grid-template-columns: 1fr;
  }

  .benefit-card {
    padding: 1.25rem;
  }

  .benefit-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
  }

  .benefit-card h3 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
    line-height: 1.3;
  }

  .benefit-card p {
    font-size: 0.8125rem;
    line-height: 1.5;
  }

  .faq-section {
    margin-bottom: 2rem;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .faq-section :deep(.faq-section) {
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    max-width: 100%;
  }

  .manage-section {
    margin-bottom: 2rem;
  }

  .manage-card {
    padding: 1.25rem;
    gap: 1.25rem;
  }

  .manage-content h3 {
    font-size: 1.125rem;
  }

  .manage-content p {
    font-size: 0.8125rem;
    line-height: 1.4;
  }

  .manage-link {
    padding: 0.8125rem 1.25rem;
    font-size: 0.875rem;
  }

  .manage-link svg {
    width: 16px;
    height: 16px;
  }
}

@media (max-width: 380px) {
  .billing-page {
    padding: 1rem 0.75rem;
  }

  .billing-page :deep(.footer) {
    width: 100%;
    margin: 0;
    border-radius: 0;
  }


  .faq-section {
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-left: 0.125rem;
    padding-right: 0.125rem;
  }

  .billing-page :deep(.faq-section) {
    margin-left: auto;
    margin-right: auto;
    padding-left: 0.125rem;
    padding-right: 0.125rem;
    width: 100%;
    max-width: 100%;
  }

  .page-header {
    margin-bottom: 1.25rem;
  }

  .header-badge {
    font-size: 0.6875rem;
    padding: 0.3125rem 0.6875rem;
    margin-bottom: 0.875rem;
  }

  .badge-icon {
    width: 12px;
    height: 12px;
  }

  .page-header h1 {
    font-size: 1.375rem;
    margin-bottom: 0.5rem;
  }

  .page-header p {
    font-size: 0.8125rem;
  }

  .level-selector-card {
    padding: 1.125rem 1.25rem;
    margin-bottom: 1.25rem;
    border-radius: 12px;
  }

  .level-eyebrow {
    font-size: 0.65rem;
  }

  .level-card-header h2 {
    font-size: 1.125rem;
  }

  .level-subtitle {
    font-size: 0.8125rem;
  }

  .level-select-group {
    margin-top: 1.125rem;
  }

  .level-select-group label {
    font-size: 0.8125rem;
  }

  .level-select-wrapper select {
    padding: 0.6875rem 0.8125rem;
    font-size: 0.875rem;
    border-radius: 8px;
  }

  .level-hint {
    font-size: 0.75rem;
  }

  .level-selection-pill {
    padding: 0.375rem 0.8125rem;
    font-size: 0.75rem;
  }

  .level-warning {
    font-size: 0.75rem;
  }

  .level-access-chips .access-label {
    font-size: 0.75rem;
  }

  .level-access-chips .chip {
    padding: 0.3125rem 0.625rem;
    font-size: 0.75rem;
  }

  .pricing-card {
    padding: 1.125rem 1rem;
  }

  .card-title {
    font-size: 1.1875rem;
  }

  .price-amount {
    font-size: 2.125rem;
  }

  .card-features li {
    font-size: 0.8125rem;
  }

  .contact-content {
    padding: 1.25rem 1rem;
  }

  .trust-section {
    margin-bottom: 1.75rem;
    padding: 0 0.375rem;
  }

  .trust-content {
    padding: 0.875rem 0.75rem;
    gap: 0.625rem;
    border-radius: 7px;
  }

  .trust-text {
    font-size: 0.6875rem;
  }

  .trust-badges {
    gap: 0.375rem;
  }

  .trust-badge {
    padding: 0.3125rem 0.6875rem;
    font-size: 0.625rem;
    border-radius: 5px;
  }

  .benefit-card {
    padding: 1.125rem 1rem;
  }

  .manage-card {
    padding: 1.125rem 1rem;
  }

  .manage-content h3 {
    font-size: 1.0625rem;
  }

  .manage-content p {
    font-size: 0.8125rem;
  }

  .manage-link {
    padding: 0.8125rem 1.125rem;
    font-size: 0.8125rem;
  }
}
</style>
