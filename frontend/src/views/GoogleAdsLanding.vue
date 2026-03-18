<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import PricingCards from '@/components/shared/PricingCards.vue'
import { createCheckoutSession } from '@/api/subscriptions'
import { getNiveauxByPays } from '@/api/niveaux'
import { useUserStore } from '@/stores/user'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useCheckoutIntentStore } from '@/stores/checkoutIntent'
import { useToast } from '@/composables/useToast'
import { setPageSeo, buildFaqJsonLd, getRobotsForRoute } from '@/services/seo'

const route = useRoute()
const userStore = useUserStore()
const checkoutIntentStore = useCheckoutIntentStore()
const { openModal } = useModalManager()
const { info: showInfoToast, error: showErrorToast } = useToast()

const submitting = ref(false)
const niveaux = ref([])
const niveauxLoading = ref(false)
const niveauxError = ref('')
const selectedNiveauId = ref(
  userStore.niveau_pays?.id ? Number(userStore.niveau_pays.id) : null
)
const showLevelModal = ref(false)
const pendingPriceId = ref('')
const pendingPlanName = ref('')

const faqItems = [
  {
    question: 'C\'est pour quel niveau ?',
    answer: 'OptiTAB suit le programme officiel français. Il couvre les Bases & Méthode (pour tout le monde), la Seconde, la Première et la Terminale. Chaque abonnement donne accès au contenu complet d\'un niveau.'
  },
  {
    question: 'Comment ça marche concrètement ?',
    answer: 'Après ton abonnement, tu accèdes immédiatement à tous les cours, fiches de synthèse et exercices corrigés pas à pas de ton niveau. Tu avances à ton rythme.'
  },
  {
    question: 'C\'est sans engagement ?',
    answer: 'Oui. Tu peux annuler ton abonnement à tout moment depuis ton espace personnel, sans frais.'
  },
  {
    question: 'Quand est-ce que je paie ?',
    answer: 'Le paiement se fait au moment de l\'abonnement. Tu es ensuite prélevé automatiquement à chaque période (mensuel ou annuel selon ton choix).'
  },
  {
    question: 'Comment résilier ?',
    answer: 'Tu peux résilier en un clic depuis ton espace abonné. Ton accès reste actif jusqu\'à la fin de la période déjà payée.'
  },
  {
    question: 'Est-ce adapté si j\'ai des lacunes ?',
    answer: 'Oui. Les cours sont structurés pas à pas et les exercices sont guidés étape par étape. La méthode est pensée pour progresser même en partant de zéro.'
  }
]

// ── SEO ──
const title = 'Plateforme de maths en ligne — Programme français, cours et exercices corrigés | OptiTAB'
const description = 'Abonne-toi à OptiTAB : +120 cours, +120 fiches et +1 000 exercices corrigés pas à pas. Programme officiel français du collège au lycée. Sans engagement.'
const faqGraph = buildFaqJsonLd(faqItems)
const jsonLdGraph = [
  {
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Accueil', item: 'https://www.optitab.net/' },
      { '@type': 'ListItem', position: 2, name: 'Plateforme maths', item: 'https://www.optitab.net/plateforme-maths' }
    ]
  },
  ...(faqGraph ? [faqGraph] : [])
]

setPageSeo({
  title,
  description,
  canonicalPath: '/plateforme-maths',
  robots: getRobotsForRoute({ route }),
  ogType: 'website',
  jsonLdGraph
})

// ── UTM persistence ──
onMounted(() => {
  const params = new URLSearchParams(window.location.search)
  const gclid = params.get('gclid')
  if (gclid) {
    try { sessionStorage.setItem('gclid', gclid) } catch (_) {}
  }
})

// ── Scroll CTA ──
function scrollToPricing() {
  const el = document.getElementById('gads-pricing')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// ── Checkout flow (same logic as home PricingPlans) ──
async function loadLevels(force = false) {
  if (niveauxLoading.value) return
  if (!force && niveaux.value.length) return
  try {
    niveauxLoading.value = true
    niveauxError.value = ''
    const data = await getNiveauxByPays()
    const rawList = Array.isArray(data?.results)
      ? data.results
      : Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : [])
    niveaux.value = rawList.filter(n => n && (n.est_actif === undefined || n.est_actif))
    if (!selectedNiveauId.value && niveaux.value.length) {
      const preferredId = userStore.niveau_pays?.id
      const match = preferredId ? niveaux.value.find(n => Number(n.id) === Number(preferredId)) : null
      selectedNiveauId.value = match ? match.id : niveaux.value[0].id
    }
  } catch (error) {
    niveauxError.value = 'Impossible de récupérer les niveaux.'
  } finally {
    niveauxLoading.value = false
  }
}

async function handleSubscribe(card) {
  const priceId = card?.priceId
  if (!priceId) {
    showErrorToast('Ce plan doit encore être configuré (Price ID manquant).')
    return
  }
  pendingPriceId.value = priceId
  pendingPlanName.value = card?.title || 'OptiTAB'
  await loadLevels()
  if (!niveaux.value.length) {
    showErrorToast('Impossible de proposer les niveaux pour le moment.')
    pendingPriceId.value = ''
    pendingPlanName.value = ''
    return
  }
  if (!selectedNiveauId.value) selectedNiveauId.value = niveaux.value[0].id
  showLevelModal.value = true
}

function closeLevelModal() {
  if (submitting.value) return
  showLevelModal.value = false
  pendingPriceId.value = ''
  pendingPlanName.value = ''
}

async function confirmSubscription() {
  if (!pendingPriceId.value) { closeLevelModal(); return }
  if (!selectedNiveauId.value) {
    showErrorToast('Choisis un niveau pour continuer.')
    return
  }
  if (!userStore.isAuthenticated) {
    checkoutIntentStore.setIntent({
      priceId: pendingPriceId.value,
      niveauId: selectedNiveauId.value,
      planName: pendingPlanName.value,
      source: 'gads-landing'
    })
    showInfoToast('Crée ton compte gratuit pour finaliser le paiement.', 6000)
    closeLevelModal()
    openModal(MODAL_IDS.REGISTER)
    return
  }
  try {
    submitting.value = true
    const { data } = await createCheckoutSession(pendingPriceId.value, {
      niveau_pays_id: selectedNiveauId.value
    })
    const redirectUrl = data?.checkout_url || data?.url
    if (redirectUrl) {
      window.location.href = redirectUrl
    } else {
      showErrorToast("Impossible d'ouvrir la page de paiement.")
    }
  } catch (err) {
    showErrorToast("Erreur lors de la création du paiement.")
  } finally {
    submitting.value = false
    closeLevelModal()
  }
}
</script>

<template>
  <div class="gads-page">
    <!-- ═══════ SECTION 1 — HERO ═══════ -->
    <section class="gads-hero">
      <div class="gads-hero__inner">
        <span class="gads-hero__badge">🇫🇷 Programme officiel français</span>
        <h1 class="gads-hero__title">
          Réussis en maths avec<br />
          <span class="gads-hero__highlight">+120 cours, +120 fiches, +1 000 exercices</span>
        </h1>
        <p class="gads-hero__subtitle">
          Cours structurés, fiches de synthèse et exercices corrigés pas à pas.<br />
          Lycée · Bases & Méthode. Accès immédiat.
        </p>
        <button
          class="gads-cta gads-cta--primary"
          data-cta-name="subscribe"
          data-cta-location="gads_hero"
          @click="scrollToPricing"
        >
          S'abonner maintenant
        </button>
        <p class="gads-hero__reassurance">Sans engagement · Annulable à tout moment · Paiement sécurisé</p>
      </div>
    </section>

    <!-- ═══════ SECTION 2 — 3 BÉNÉFICES ═══════ -->
    <section class="gads-benefits">
      <div class="gads-section__inner">
        <h2 class="gads-section__title">Tout est prêt pour que tu progresses</h2>
        <div class="gads-benefits__grid">
          <div class="gads-benefit-card">
            <div class="gads-benefit-card__icon">📖</div>
            <h3 class="gads-benefit-card__title">Cours clairs</h3>
            <p class="gads-benefit-card__desc">
              Des notions expliquées étape par étape, organisées par chapitre et par niveau.
            </p>
          </div>
          <div class="gads-benefit-card">
            <div class="gads-benefit-card__icon">📝</div>
            <h3 class="gads-benefit-card__title">Fiches de synthèse</h3>
            <p class="gads-benefit-card__desc">
              Les formules et méthodes essentielles résumées pour réviser rapidement.
            </p>
          </div>
          <div class="gads-benefit-card">
            <div class="gads-benefit-card__icon">✏️</div>
            <h3 class="gads-benefit-card__title">Exercices corrigés pas à pas</h3>
            <p class="gads-benefit-card__desc">
              Un entraînement guidé pour comprendre la méthode, pas juste la réponse.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════ SECTION 3 — POUR QUI ═══════ -->
    <section class="gads-audience">
      <div class="gads-section__inner">
        <h2 class="gads-section__title">Pour qui ?</h2>

        <p class="gads-section__subtitle">
          Le programme suit le <strong>programme officiel de l'Éducation nationale française</strong>.
        </p>

        <!-- Bloc Bases & Méthode -->
        <div class="gads-audience__universal">
          <div class="gads-audience__universal-card">
            <span class="gads-audience__universal-icon">🧱</span>
            <div>
              <h3 class="gads-audience__universal-title">Bases & Méthode</h3>
              <p class="gads-audience__universal-desc">
                Reprendre les fondamentaux depuis zéro et apprendre à raisonner.<br />
                <strong>Adapté à tout le monde, quel que soit le niveau de départ.</strong>
              </p>
            </div>
          </div>
        </div>

        <!-- Niveaux -->
        <p class="gads-audience__level-intro">
          Ou choisis ton niveau pour accéder à tout le programme :
        </p>
        <div class="gads-audience__tags">
          <span class="gads-tag">Seconde</span>
          <span class="gads-tag">Première</span>
          <span class="gads-tag">Terminale</span>
        </div>
      </div>
    </section>

    <!-- ═══════ SECTION 3b — CHIFFRES ═══════ -->
    <section class="gads-stats">
      <div class="gads-section__inner">
        <div class="gads-stats__grid">
          <div class="gads-stats__item">
            <span class="gads-stats__number">120+</span>
            <span class="gads-stats__label">chapitres de cours</span>
          </div>
          <div class="gads-stats__item">
            <span class="gads-stats__number">120+</span>
            <span class="gads-stats__label">fiches de synthèse</span>
          </div>
          <div class="gads-stats__item">
            <span class="gads-stats__number">1 000+</span>
            <span class="gads-stats__label">exercices corrigés</span>
          </div>
        </div>
        <p class="gads-stats__caption">Tout le programme français est couvert. Il n'y a plus qu'à s'y mettre.</p>
      </div>
    </section>

    <!-- ═══════ SECTION 4 — CONTENU DE L'ABONNEMENT ═══════ -->
    <section class="gads-includes">
      <div class="gads-section__inner">
        <h2 class="gads-section__title">Ce que tu obtiens avec l'abonnement</h2>
        <ul class="gads-includes__list">
          <li class="gads-includes__item"><span class="gads-check">✓</span> Accès complet à la plateforme</li>
          <li class="gads-includes__item"><span class="gads-check">✓</span> Programme officiel français (Lycée)</li>
          <li class="gads-includes__item"><span class="gads-check">✓</span> 120+ cours structurés par chapitre</li>
          <li class="gads-includes__item"><span class="gads-check">✓</span> 120+ fiches de synthèse</li>
          <li class="gads-includes__item"><span class="gads-check">✓</span> 1 000+ exercices corrigés pas à pas</li>
          <li class="gads-includes__item"><span class="gads-check">✓</span> Module Bases & Méthode inclus</li>
          <li class="gads-includes__item"><span class="gads-check">✓</span> Progression structurée et guidée</li>
        </ul>
      </div>
    </section>

    <!-- ═══════ SECTION 5 — PRIX / OFFRE ═══════ -->
    <section class="gads-pricing" id="gads-pricing">
      <div class="gads-section__inner">
        <h2 class="gads-section__title">Choisis ton abonnement</h2>
        <p class="gads-section__subtitle">Sans engagement · Accès immédiat · Annulable à tout moment</p>
        <PricingCards
          :submitting="submitting"
          cta-location="gads_pricing"
          @select="handleSubscribe"
        />
      </div>
    </section>

    <!-- ═══════ SECTION 6 — PREUVE VISUELLE ═══════ -->
    <section class="gads-preview">
      <div class="gads-section__inner">
        <h2 class="gads-section__title">Aperçu de la plateforme</h2>
        <p class="gads-section__subtitle">
          Un espace clair pour réviser, s'entraîner et suivre ta progression.
        </p>
        <div class="gads-preview__wrapper">
          <img
            src="/video/optitab-demo-exercices.gif"
            alt="Démonstration des exercices corrigés pas à pas sur OptiTAB"
            class="gads-preview__img"
            loading="lazy"
            width="800"
            height="500"
          />
        </div>
      </div>
    </section>

    <!-- ═══════ SECTION 7 — FAQ ═══════ -->
    <section class="gads-faq">
      <div class="gads-section__inner">
        <h2 class="gads-section__title">Questions fréquentes</h2>
        <div class="gads-faq__list">
          <details
            v-for="(item, idx) in faqItems"
            :key="idx"
            class="gads-faq__item"
          >
            <summary class="gads-faq__question">{{ item.question }}</summary>
            <p class="gads-faq__answer">{{ item.answer }}</p>
          </details>
        </div>
      </div>
    </section>

    <!-- ═══════ SECTION 8 — DERNIER CTA ═══════ -->
    <section class="gads-final-cta">
      <div class="gads-section__inner">
        <h2 class="gads-final-cta__title">Prêt à réussir en maths ?</h2>
        <p class="gads-final-cta__subtitle">+120 cours · +120 fiches · +1 000 exercices corrigés. Tout le programme français, accès immédiat.</p>
        <button
          class="gads-cta gads-cta--primary gads-cta--large"
          data-cta-name="subscribe"
          data-cta-location="gads_final"
          @click="scrollToPricing"
        >
          S'abonner maintenant
        </button>
      </div>
    </section>

    <!-- ═══════ FOOTER MINIMAL ═══════ -->
    <footer class="gads-footer">
      <div class="gads-footer__inner">
        <span class="gads-footer__copy">© {{ new Date().getFullYear() }} OptiTAB</span>
        <span class="gads-footer__sep">·</span>
        <router-link to="/legal" class="gads-footer__link">Mentions légales</router-link>
        <span class="gads-footer__sep">·</span>
        <router-link to="/confidentialite" class="gads-footer__link">Confidentialité</router-link>
        <span class="gads-footer__sep">·</span>
        <router-link to="/cgu" class="gads-footer__link">CGU</router-link>
        <span class="gads-footer__sep">·</span>
        <router-link to="/cgv" class="gads-footer__link">CGV</router-link>
      </div>
    </footer>

    <!-- ═══════ MODAL NIVEAU ═══════ -->
    <div v-if="showLevelModal" class="gads-modal-overlay" @click="closeLevelModal">
      <div class="gads-modal" @click.stop>
        <button class="gads-modal__close" type="button" :disabled="submitting" @click="closeLevelModal">
          &times;
        </button>
        <div class="gads-modal__header">
          <h3>Choisis ton niveau</h3>
          <p>L'abonnement <strong>{{ pendingPlanName || 'OptiTAB' }}</strong> débloquera un seul niveau.</p>
        </div>
        <div class="gads-modal__body">
          <div v-if="niveauxLoading" class="gads-modal__loading">Chargement…</div>
          <div v-else-if="niveauxError" class="gads-modal__error">
            <p>{{ niveauxError }}</p>
            <button @click="loadLevels(true)">Réessayer</button>
          </div>
          <div v-else>
            <label for="gads-level-select">Niveau à débloquer</label>
            <select id="gads-level-select" v-model.number="selectedNiveauId">
              <option v-for="n in niveaux" :key="n.id" :value="n.id">
                {{ n.nom }}{{ n.pays?.nom ? ` — ${n.pays.nom}` : '' }}
              </option>
            </select>
          </div>
          <p v-if="!userStore.isAuthenticated" class="gads-modal__hint">
            Pas encore de compte ? Choisis ton niveau puis crée ton compte pour finaliser le paiement.
          </p>
        </div>
        <div class="gads-modal__actions">
          <button class="gads-modal__btn gads-modal__btn--secondary" :disabled="submitting" @click="closeLevelModal">
            Annuler
          </button>
          <button class="gads-modal__btn gads-modal__btn--primary" :disabled="submitting || !selectedNiveauId" @click="confirmSubscription">
            {{ submitting ? 'Redirection…' : 'Continuer vers le paiement' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
/* ──────────────────────────────────────────────
   Variables
   ────────────────────────────────────────────── */
$primary: #2a38b7;
$primary-light: #667eea;
$text-dark: #0f172a;
$text: #475569;
$text-light: #64748b;
$white: #ffffff;
$bg-light: #f8fafc;
$bg-alt: #f1f5f9;
$radius: 16px;
$radius-sm: 10px;
$shadow: 0 4px 24px rgba(42, 56, 183, 0.08);

/* ──────────────────────────────────────────────
   Page
   ────────────────────────────────────────────── */
.gads-page {
  min-height: 100vh;
  background: $white;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: $text;
  line-height: 1.6;
}

/* ──────────────────────────────────────────────
   Section generic
   ────────────────────────────────────────────── */
.gads-section__inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 24px;
}

.gads-section__title {
  font-size: 1.75rem;
  font-weight: 800;
  color: $text-dark;
  text-align: center;
  margin-bottom: 12px;
  line-height: 1.25;
}

.gads-section__subtitle {
  font-size: 1.05rem;
  color: $text;
  text-align: center;
  margin-bottom: 2rem;
  line-height: 1.5;
}

/* ──────────────────────────────────────────────
   CTA button global
   ────────────────────────────────────────────── */
.gads-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.gads-cta--primary {
  background: linear-gradient(135deg, $primary, $primary-light);
  color: $white;
  padding: 16px 40px;
  font-size: 1.1rem;
  box-shadow: 0 4px 16px rgba(42, 56, 183, 0.25);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(42, 56, 183, 0.35);
  }
}

.gads-cta--large {
  padding: 18px 48px;
  font-size: 1.2rem;
}

/* ──────────────────────────────────────────────
   SECTION 1 — Hero
   ────────────────────────────────────────────── */
.gads-hero {
  padding: 80px 24px 60px;
  text-align: center;
  background: linear-gradient(180deg, $bg-light 0%, $white 100%);
}

.gads-hero__inner {
  max-width: 720px;
  margin: 0 auto;
}

.gads-hero__badge {
  display: inline-block;
  background: $white;
  color: $primary;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 6px 18px;
  border-radius: 50px;
  border: 1.5px solid #e0e7ff;
  margin-bottom: 20px;
  letter-spacing: 0.02em;
}

.gads-hero__title {
  font-size: 2.5rem;
  font-weight: 900;
  color: $text-dark;
  line-height: 1.2;
  margin-bottom: 20px;
  letter-spacing: -0.02em;
}

.gads-hero__highlight {
  background: linear-gradient(135deg, $primary, $primary-light);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.gads-hero__subtitle {
  font-size: 1.15rem;
  color: $text;
  line-height: 1.6;
  margin-bottom: 32px;
}

.gads-hero__reassurance {
  margin-top: 14px;
  font-size: 0.9rem;
  color: $text-light;
}

/* ──────────────────────────────────────────────
   SECTION 2 — Bénéfices
   ────────────────────────────────────────────── */
.gads-benefits {
  padding: 64px 24px;
  background: $white;
}

.gads-benefits__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 8px;
}

.gads-benefit-card {
  background: $bg-light;
  border-radius: $radius;
  padding: 28px 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.gads-benefit-card__icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.gads-benefit-card__title {
  font-size: 1.1rem;
  font-weight: 700;
  color: $text-dark;
  margin-bottom: 8px;
}

.gads-benefit-card__desc {
  font-size: 0.95rem;
  color: $text;
  line-height: 1.55;
}

/* ──────────────────────────────────────────────
   SECTION 3 — Pour qui
   ────────────────────────────────────────────── */
.gads-audience {
  padding: 56px 24px 32px;
  background: $bg-alt;
}

.gads-audience__universal {
  max-width: 540px;
  margin: 0 auto 28px;
}

.gads-audience__universal-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: $white;
  border: 2px solid #e0e7ff;
  border-radius: $radius;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(42, 56, 183, 0.06);
}

.gads-audience__universal-icon {
  font-size: 2rem;
  flex-shrink: 0;
  line-height: 1;
}

.gads-audience__universal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: $primary;
  margin-bottom: 6px;
}

.gads-audience__universal-desc {
  font-size: 0.95rem;
  color: $text;
  line-height: 1.55;

  strong {
    color: $text-dark;
  }
}

.gads-audience__level-intro {
  font-size: 1rem;
  color: $text;
  text-align: center;
  margin-bottom: 16px;
}

.gads-audience__tags {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.gads-tag {
  display: inline-flex;
  align-items: center;
  padding: 10px 28px;
  font-size: 1rem;
  font-weight: 600;
  color: $primary;
  background: $white;
  border: 2px solid $primary;
  border-radius: 50px;
}

/* ──────────────────────────────────────────────
   SECTION 3b — Chiffres
   ────────────────────────────────────────────── */
.gads-stats {
  padding: 48px 24px;
  background: $white;
}

.gads-stats__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 700px;
  margin: 0 auto;
}

.gads-stats__item {
  text-align: center;
}

.gads-stats__number {
  display: block;
  font-size: 2.5rem;
  font-weight: 900;
  color: $primary;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.gads-stats__label {
  display: block;
  font-size: 0.95rem;
  color: $text;
  margin-top: 6px;
}

.gads-stats__caption {
  text-align: center;
  font-size: 1rem;
  color: $text-light;
  margin-top: 24px;
  font-style: italic;
}

/* ──────────────────────────────────────────────
   SECTION 4 — Contenu abonnement
   ────────────────────────────────────────────── */
.gads-includes {
  padding: 64px 24px;
  background: $bg-alt;
}

.gads-includes__list {
  list-style: none;
  padding: 0;
  max-width: 480px;
  margin: 0 auto;
}

.gads-includes__item {
  font-size: 1.05rem;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
  color: $text-dark;

  &:last-child {
    border-bottom: none;
  }
}

.gads-check {
  color: #22c55e;
  font-weight: 700;
  margin-right: 10px;
}

/* ──────────────────────────────────────────────
   SECTION 5 — Pricing
   ────────────────────────────────────────────── */
.gads-pricing {
  padding: 72px 24px;
  background: $bg-alt;
}

/* ──────────────────────────────────────────────
   SECTION 6 — Preview
   ────────────────────────────────────────────── */
.gads-preview {
  padding: 64px 24px;
  background: $white;
}

.gads-preview__wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.gads-preview__img {
  max-width: 100%;
  height: auto;
  border-radius: $radius;
  border: 1px solid #e2e8f0;
  box-shadow: $shadow;
}

/* ──────────────────────────────────────────────
   SECTION 7 — FAQ
   ────────────────────────────────────────────── */
.gads-faq {
  padding: 64px 24px;
  background: $bg-alt;
}

.gads-faq__list {
  max-width: 640px;
  margin: 0 auto;
}

.gads-faq__item {
  border-bottom: 1px solid #e2e8f0;
  padding: 16px 0;

  &[open] .gads-faq__question::after {
    transform: rotate(180deg);
  }
}

.gads-faq__question {
  font-size: 1.05rem;
  font-weight: 600;
  color: $text-dark;
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;

  &::after {
    content: '▾';
    font-size: 1.1rem;
    color: $text-light;
    transition: transform 0.2s ease;
    flex-shrink: 0;
    margin-left: 12px;
  }

  &::-webkit-details-marker {
    display: none;
  }
}

.gads-faq__answer {
  margin-top: 10px;
  font-size: 0.95rem;
  color: $text;
  line-height: 1.6;
}

/* ──────────────────────────────────────────────
   SECTION 8 — Final CTA
   ────────────────────────────────────────────── */
.gads-final-cta {
  padding: 72px 24px;
  background: linear-gradient(135deg, $primary 0%, $primary-light 100%);
  text-align: center;
}

.gads-final-cta__title {
  font-size: 2rem;
  font-weight: 800;
  color: $white;
  margin-bottom: 12px;
}

.gads-final-cta__subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 28px;
}

.gads-final-cta .gads-cta--primary {
  background: $white;
  color: $primary;

  &:hover {
    background: #f8fafc;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  }
}

/* ──────────────────────────────────────────────
   Footer
   ────────────────────────────────────────────── */
.gads-footer {
  padding: 24px;
  background: $text-dark;
  text-align: center;
}

.gads-footer__inner {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
}

.gads-footer__link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;

  &:hover {
    color: $white;
  }
}

.gads-footer__sep {
  color: rgba(255, 255, 255, 0.3);
}

/* ──────────────────────────────────────────────
   Modal niveau
   ────────────────────────────────────────────── */
.gads-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 24px;
}

.gads-modal {
  background: $white;
  border-radius: $radius;
  max-width: 440px;
  width: 100%;
  padding: 32px;
  position: relative;
}

.gads-modal__close {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  font-size: 1.6rem;
  color: $text-light;
  cursor: pointer;
}

.gads-modal__header h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: $text-dark;
  margin-bottom: 8px;
}

.gads-modal__header p {
  font-size: 0.95rem;
  color: $text;
  margin-bottom: 20px;
}

.gads-modal__body label {
  display: block;
  font-weight: 600;
  font-size: 0.9rem;
  color: $text-dark;
  margin-bottom: 8px;
}

.gads-modal__body select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  color: $text-dark;
  background: $white;
  margin-bottom: 12px;
}

.gads-modal__hint {
  font-size: 0.85rem;
  color: $text-light;
  margin-top: 8px;
}

.gads-modal__loading,
.gads-modal__error {
  text-align: center;
  padding: 16px 0;
  color: $text;
}

.gads-modal__actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.gads-modal__btn {
  flex: 1;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.gads-modal__btn--secondary {
  background: $bg-light;
  color: $text;

  &:hover {
    background: $bg-alt;
  }
}

.gads-modal__btn--primary {
  background: linear-gradient(135deg, $primary, $primary-light);
  color: $white;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(42, 56, 183, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
}

/* ──────────────────────────────────────────────
   Mobile responsive
   ────────────────────────────────────────────── */
@media (max-width: 768px) {
  .gads-hero {
    padding: 56px 20px 44px;
  }

  .gads-hero__title {
    font-size: 1.75rem;
  }

  .gads-hero__subtitle {
    font-size: 1rem;
  }

  .gads-section__title {
    font-size: 1.4rem;
  }

  .gads-benefits__grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .gads-cta--primary {
    padding: 14px 32px;
    font-size: 1rem;
    width: 100%;
  }

  .gads-cta--large {
    padding: 16px 36px;
    font-size: 1.05rem;
  }

  .gads-audience__tags {
    gap: 10px;
  }

  .gads-tag {
    padding: 8px 20px;
    font-size: 0.9rem;
  }

  .gads-stats__grid {
    gap: 16px;
  }

  .gads-stats__number {
    font-size: 2rem;
  }

  .gads-final-cta__title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .gads-hero__title {
    font-size: 1.5rem;
  }

  .gads-benefits, .gads-includes, .gads-preview, .gads-faq {
    padding: 48px 16px;
  }

  .gads-pricing {
    padding: 56px 16px;
  }

  .gads-stats {
    padding: 36px 16px;
  }

  .gads-stats__number {
    font-size: 1.75rem;
  }

  .gads-audience__universal-card {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
}
</style>
