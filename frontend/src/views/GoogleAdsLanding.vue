<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/layout/Header.vue'
import PricingCards from '@/components/shared/PricingCards.vue'
import { createCheckoutSession, createGuestCheckoutSession } from '@/api/subscriptions'
import { getNiveauxByPays } from '@/api/niveaux'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import { setPageSeo, buildFaqJsonLd, getRobotsForRoute } from '@/services/seo'

const route = useRoute()
const userStore = useUserStore()
const { error: showErrorToast } = useToast()

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
const openFaqIndex = ref(null)

const faqItems = [
  {
    question: 'Comment ça marche ?',
    answer: 'Tu choisis ton abonnement, tu sélectionnes ton niveau (Seconde, Première ou Terminale) et tu accèdes immédiatement à tous les cours, fiches et exercices corrigés. Tu avances à ton rythme, quand tu veux.'
  },
  {
    question: 'Quand est-ce que je paie ?',
    answer: 'Le paiement se fait au moment de l\'abonnement. Tu es ensuite prélevé automatiquement chaque mois (ou chaque année si tu choisis l\'offre annuelle).'
  },
  {
    question: 'Comment résilier ?',
    answer: 'En un clic depuis ton espace abonné, à tout moment. Ton accès reste actif jusqu\'à la fin de la période déjà payée. Pas de frais, pas de délai.'
  },
  {
    question: 'À qui s\'adresse la plateforme ?',
    answer: 'À tous les élèves de Seconde, Première et Terminale qui veulent progresser en maths. Le contenu suit le programme officiel de l\'Éducation nationale française.'
  },
  {
    question: 'Qu\'est-ce que le parcours Bases & Méthode ?',
    answer: 'C\'est un parcours complémentaire accessible à tous les abonnés — lycéens, élèves de prépa ou toute personne souhaitant reprendre les fondamentaux. Utilisable librement, sans obligation.'
  }
]

function toggleFaq(idx) {
  openFaqIndex.value = openFaqIndex.value === idx ? null : idx
}

// ── SEO ──
const title = 'Abonnement maths en ligne dès 3,99 € — Cours, fiches et exercices corrigés | OptiTAB'
const description = 'Cours clairs, fiches de synthèse et exercices corrigés pas à pas pour la Seconde, Première et Terminale. Parcours Bases & Méthode inclus. Accès immédiat. Sans engagement. Dès 3,99 €/mois.'
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

// ── Scroll animations ──
let scrollObserver = null

onMounted(() => {
  // UTM persistence
  const params = new URLSearchParams(window.location.search)
  const gclid = params.get('gclid')
  if (gclid) {
    try { sessionStorage.setItem('gclid', gclid) } catch (_) {}
  }

  // Scroll reveal
  scrollObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('revealed')
      })
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  )
  document.querySelectorAll('.reveal-on-scroll').forEach(el => scrollObserver.observe(el))
})

onUnmounted(() => {
  scrollObserver?.disconnect()
})

// ── Scroll CTA ──
function scrollToPricing() {
  const el = document.getElementById('gads-pricing')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function scrollToDemo() {
  const el = document.getElementById('gads-demo')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

// ── Checkout flow ──
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
  try {
    submitting.value = true
    let redirectUrl
    if (!userStore.isAuthenticated) {
      const { data } = await createGuestCheckoutSession(pendingPriceId.value, {
        niveau_pays_id: selectedNiveauId.value
      })
      redirectUrl = data?.checkout_url || data?.url
    } else {
      const { data } = await createCheckoutSession(pendingPriceId.value, {
        niveau_pays_id: selectedNiveauId.value
      })
      redirectUrl = data?.checkout_url || data?.url
    }
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
  <div class="lp">
    <Header />

    <!-- ══════════ HERO ══════════ -->
    <section class="hero">
      <div class="hero__deco">
        <div class="hero__circle hero__circle--1"></div>
        <div class="hero__circle hero__circle--2"></div>
        <div class="hero__circle hero__circle--3"></div>
      </div>
      <div class="hero__body">
        <h1 class="hero__title">
          Progresse en maths<br><span class="hero__grad">dès 3,99 €/mois</span>
        </h1>
        <p class="hero__sub">
          Cours structurés, fiches de synthèse et exercices corrigés pas à pas<br class="hide-mobile">
          pour la Seconde, Première et Terminale.
        </p>
        <div class="hero__chips">
          <span class="chip"><span class="chip__icon">✓</span> Accès immédiat</span>
          <span class="chip"><span class="chip__icon">✓</span> Sans engagement</span>
          <span class="chip"><span class="chip__icon">✓</span> Résiliation en 1 clic</span>
        </div>
        <div class="hero__ctas">
          <button class="btn btn--main" data-cta-name="subscribe" data-cta-location="gads_hero" @click="scrollToPricing">
            <span class="btn__label">Je m'abonne maintenant</span>
            <span class="btn__hint">Accès immédiat après paiement</span>
          </button>
          <button class="btn btn--ghost" @click="scrollToDemo">
            Voir la plateforme en action
          </button>
        </div>
        <p class="hero__trust">Paiement sécurisé Stripe · Contenu aligné Éducation nationale</p>
      </div>
    </section>

    <!-- ══════════ DÉMO ══════════ -->
    <section class="demo reveal-on-scroll" id="gads-demo">
      <div class="wrap">
        <div class="demo__badge"><span class="demo__sparkle">✨</span> Découvrez OptiTAB en action</div>
        <h2 class="section-title">La plateforme qui <span class="grad">transforme</span> l'apprentissage</h2>
        <p class="section-sub">Exercices guidés avec corrections détaillées, fiches prêtes à l'emploi et progression structurée.</p>
        <div class="demo__grid">
          <div class="demo__card reveal-on-scroll">
            <div class="demo__tag"><span>💻</span> Version Desktop</div>
            <div class="demo__frame">
              <img src="/video/optitab-demo-exercices.gif" alt="Démonstration des exercices corrigés pas à pas sur OptiTAB" loading="lazy" />
            </div>
            <p class="demo__caption">Interface complète pour travailler confortablement</p>
          </div>
          <div class="demo__card demo__card--mobile reveal-on-scroll">
            <div class="demo__tag"><span>📱</span> Version Mobile</div>
            <div class="demo__frame demo__frame--mobile">
              <img src="/video/optitab-demo-mobile.gif" alt="Interface mobile OptiTAB" loading="lazy" />
            </div>
            <p class="demo__caption">Étudiez partout, à tout moment</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════ FEATURES ══════════ -->
    <section class="features reveal-on-scroll">
      <div class="wrap">
        <h2 class="section-title">Tout ce qu'il faut pour <span class="grad">vraiment progresser</span></h2>
        <p class="section-sub">Une méthode pensée pour les lycéens, pas un catalogue de vidéos.</p>
        <div class="features__grid">
          <div class="feat-card reveal-on-scroll">
            <div class="feat-card__ico feat-card__ico--blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            </div>
            <div class="feat-card__body">
              <h3>Cours structurés par chapitre</h3>
              <p>Chaque notion est expliquée clairement, dans l'ordre du programme officiel de l'Éducation nationale.</p>
            </div>
          </div>
          <div class="feat-card reveal-on-scroll">
            <div class="feat-card__ico feat-card__ico--indigo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
            </div>
            <div class="feat-card__body">
              <h3>Exercices corrigés pas à pas</h3>
              <p>Pas juste la réponse — chaque étape est détaillée pour que tu comprennes la méthode.</p>
            </div>
          </div>
          <div class="feat-card reveal-on-scroll">
            <div class="feat-card__ico feat-card__ico--violet">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div class="feat-card__body">
              <h3>Fiches de synthèse</h3>
              <p>Des fiches prêtes à l'emploi pour chaque chapitre — idéales avant un contrôle ou le bac.</p>
            </div>
          </div>
          <div class="feat-card reveal-on-scroll">
            <div class="feat-card__ico feat-card__ico--emerald">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <div class="feat-card__body">
              <h3>Progression guidée</h3>
              <p>Un parcours structuré chapitre par chapitre pour avancer dans le bon ordre, sans se perdre.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════ NIVEAUX ══════════ -->
    <section class="levels reveal-on-scroll">
      <div class="wrap">
        <p class="eyebrow">Adapté à chaque niveau</p>
        <h2 class="section-title">Pour tous les <span class="grad">lycéens</span></h2>
        <p class="section-sub">Des contenus complets de la Seconde à la Terminale, alignés sur le programme officiel.</p>
        <div class="levels__grid">
          <div class="lv-card reveal-on-scroll">
            <div class="lv-card__ico lv-card__ico--blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="9" y1="11" x2="15" y2="11"/></svg>
            </div>
            <h3>Seconde</h3>
            <p>Consolide tes bases et prends les bons réflexes dès le lycée.</p>
          </div>
          <div class="lv-card reveal-on-scroll">
            <div class="lv-card__ico lv-card__ico--indigo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </div>
            <h3>Première</h3>
            <p>Approfondis chaque notion et prépare sereinement les épreuves.</p>
          </div>
          <div class="lv-card reveal-on-scroll">
            <div class="lv-card__ico lv-card__ico--violet">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 1.657 2.686 3 6 3s6-1.343 6-3v-5"/></svg>
            </div>
            <h3>Terminale</h3>
            <p>Maîtrise le programme et vise l'excellence au bac.</p>
          </div>
        </div>

        <!-- Bases & Méthode — bloc séparé -->
        <div class="bases-block reveal-on-scroll">
          <div class="bases-block__ico">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
          </div>
          <div class="bases-block__body">
            <div class="bases-block__header">
              <h3>Bases &amp; Méthode</h3>
              <span class="bases-block__tag">Inclus pour tous</span>
            </div>
            <p>Un parcours complémentaire accessible à tous les abonnés — lycéens en difficulté, élèves de prépa ou toute personne souhaitant reprendre les fondamentaux. Utilisable librement, sans obligation.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════ PRICING ══════════ -->
    <section class="pricing reveal-on-scroll" id="gads-pricing">
      <div class="wrap">
        <p class="eyebrow">Abonnement simple et transparent</p>
        <h2 class="section-title">Dès <span class="grad">3,99 €/mois</span></h2>
        <p class="section-sub">Sans engagement · Accès immédiat · Résiliation en un clic</p>
        <PricingCards
          :submitting="submitting"
          cta-location="gads_pricing"
          @select="handleSubscribe"
        />
      </div>
    </section>

    <!-- ══════════ FAQ ══════════ -->
    <section class="faq reveal-on-scroll">
      <div class="wrap wrap--narrow">
        <h2 class="section-title">Questions <span class="grad">fréquentes</span></h2>
        <div class="faq__list">
          <div
            v-for="(item, idx) in faqItems"
            :key="idx"
            class="faq__item"
            :class="{ 'faq__item--open': openFaqIndex === idx }"
          >
            <button class="faq__q" @click="toggleFaq(idx)" type="button">
              <span>{{ item.question }}</span>
              <svg class="faq__arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div class="faq__a-wrap">
              <p class="faq__a">{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════ FINAL CTA ══════════ -->
    <section class="final-cta">
      <div class="wrap">
        <h2 class="final-cta__title">Prêt à progresser en maths ?</h2>
        <p class="final-cta__sub">Rejoins des centaines d'élèves qui progressent avec OptiTAB. Accès immédiat dès 3,99 €/mois.</p>
        <button class="btn btn--white" data-cta-name="subscribe" data-cta-location="gads_final" @click="scrollToPricing">
          Je m'abonne maintenant
        </button>
      </div>
    </section>

    <!-- ══════════ FOOTER ══════════ -->
    <footer class="lp-footer">
      <div class="lp-footer__inner">
        <span>© {{ new Date().getFullYear() }} OptiTAB</span>
        <span class="lp-footer__sep">·</span>
        <router-link to="/legal">Mentions légales</router-link>
        <span class="lp-footer__sep">·</span>
        <router-link to="/confidentialite">Confidentialité</router-link>
        <span class="lp-footer__sep">·</span>
        <router-link to="/cgu">CGU</router-link>
        <span class="lp-footer__sep">·</span>
        <router-link to="/cgv">CGV</router-link>
      </div>
    </footer>

    <!-- ══════════ MODAL NIVEAU ══════════ -->
    <Teleport to="body">
      <div v-if="showLevelModal" class="modal-overlay" @click="closeLevelModal">
        <div class="modal" @click.stop>
          <button class="modal__close" type="button" :disabled="submitting" @click="closeLevelModal">&times;</button>
          <div class="modal__header">
            <h3>Choisis ton niveau</h3>
            <p>L'abonnement <strong>{{ pendingPlanName || 'OptiTAB' }}</strong> débloquera un seul niveau.</p>
          </div>
          <div class="modal__body">
            <div v-if="niveauxLoading" class="modal__loading">Chargement…</div>
            <div v-else-if="niveauxError" class="modal__error">
              <p>{{ niveauxError }}</p>
              <button @click="loadLevels(true)">Réessayer</button>
            </div>
            <div v-else>
              <label for="lp-level-select">Niveau à débloquer</label>
              <select id="lp-level-select" v-model.number="selectedNiveauId">
                <option v-for="n in niveaux" :key="n.id" :value="n.id">
                  {{ n.nom }}{{ n.pays?.nom ? ` — ${n.pays.nom}` : '' }}
                </option>
              </select>
            </div>
            <p v-if="!userStore.isAuthenticated" class="modal__hint">
              Pas encore de compte ? Choisis ton niveau puis crée ton compte pour finaliser le paiement.
            </p>
          </div>
          <div class="modal__actions">
            <button class="modal__btn modal__btn--ghost" :disabled="submitting" @click="closeLevelModal">Annuler</button>
            <button class="modal__btn modal__btn--main" :disabled="submitting || !selectedNiveauId" @click="confirmSubscription">
              {{ submitting ? 'Redirection…' : 'Continuer vers le paiement' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped lang="scss">
/* ═══════════════════════════════════════════
   Design tokens
   ═══════════════════════════════════════════ */
$blue: #2a38b7;
$blue-light: #667eea;
$blue-soft: #3b82f6;
$dark: #0f172a;
$text: #334155;
$text-muted: #64748b;
$white: #ffffff;
$bg: #f8fafc;
$bg-alt: #f1f5f9;
$radius: 20px;
$radius-sm: 14px;

/* ═══════════════════════════════════════════
   Globals
   ═══════════════════════════════════════════ */
.lp {
  min-height: 100vh;
  background: $white;
  font-family: 'Poppins', 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: $text;
  line-height: 1.6;
  padding-top: 64px;
  overflow-x: hidden;
}

.wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 clamp(16px, 4vw, 40px);
}
.wrap--narrow { max-width: 720px; }

.section-title {
  font-size: clamp(1.6rem, 3.5vw, 2.6rem);
  font-weight: 900;
  color: $dark;
  text-align: center;
  margin: 0 0 14px;
  line-height: 1.15;
  letter-spacing: -0.025em;
}

.section-sub {
  font-size: clamp(0.95rem, 1.6vw, 1.15rem);
  color: $text-muted;
  text-align: center;
  margin: 0 auto 40px;
  max-width: 640px;
  line-height: 1.65;
}

.grad {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}

.eyebrow {
  text-align: center;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $blue;
  margin: 0 0 10px;
}

.hide-mobile {
  @media (max-width: 640px) { display: none; }
}

/* ═══════════════════════════════════════════
   Scroll reveal
   ═══════════════════════════════════════════ */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 0.7s ease-out, transform 0.7s ease-out;
  &.revealed {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ═══════════════════════════════════════════
   Buttons
   ═══════════════════════════════════════════ */
.btn {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: $radius-sm;
  font-weight: 700;
  font-size: 1.02rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.25s, background 0.25s;
  font-family: inherit;
  min-height: 56px;
  padding: 14px 32px;
}

.btn--main {
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: $white;
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.24);
  min-width: 260px;
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(29, 78, 216, 0.33);
  }
}

.btn__label { font-weight: 700; line-height: 1.3; }
.btn__hint {
  font-size: 0.72rem;
  font-weight: 600;
  opacity: 0.85;
  margin-top: 2px;
}

.btn--ghost {
  background: rgba(255,255,255,0.88);
  color: $dark;
  border: 1px solid #c5d1e2;
  box-shadow: 0 2px 8px rgba(15,23,42,0.08);
  min-width: 240px;
  &:hover {
    background: $white;
    border-color: #9fb2cf;
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(15,23,42,0.12);
  }
}

.btn--white {
  background: $white;
  color: $blue;
  font-size: 1.1rem;
  padding: 16px 44px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.16);
  }
}

/* ═══════════════════════════════════════════
   HERO
   ═══════════════════════════════════════════ */
.hero {
  position: relative;
  text-align: center;
  padding: 80px 24px 64px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f1f5f9 60%, #e2e8f0 100%);
  overflow: hidden;
}

.hero__deco {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.hero__circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(42,56,183,0.04) 0%, transparent 70%);
  animation: floatC 20s ease-in-out infinite;
  &--1 { width: 400px; height: 400px; top: -150px; left: -100px; }
  &--2 { width: 350px; height: 350px; bottom: -100px; right: -80px; animation-delay: 7s; }
  &--3 { width: 300px; height: 300px; top: 40%; right: 5%; animation-delay: 14s; }
}

@keyframes floatC {
  0%, 100% { transform: translate(0,0) scale(1); opacity: .5; }
  50% { transform: translate(30px,-30px) scale(1.1); opacity: .7; }
}

.hero__body {
  position: relative;
  z-index: 1;
  max-width: 760px;
  margin: 0 auto;
  animation: fadeUp .8s ease-out;
}

.hero__title {
  font-size: clamp(1.7rem, 4vw, 2.8rem);
  font-weight: 900;
  color: $dark;
  line-height: 1.12;
  margin: 0 0 18px;
  letter-spacing: -0.02em;
}

.hero__grad {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}

.hero__sub {
  font-size: clamp(0.95rem, 1.5vw, 1.12rem);
  color: $text;
  font-weight: 500;
  line-height: 1.62;
  margin: 0 auto 20px;
  max-width: 640px;
}

.hero__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin: 0 0 28px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(34,197,94,0.1);
  border: 1px solid rgba(34,197,94,0.25);
  color: #166534;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 999px;
}
.chip__icon { color: #22c55e; font-weight: 700; }

.hero__ctas {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 0 0 16px;
}

.hero__trust {
  font-size: 0.82rem;
  color: $text-muted;
  margin: 0;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ═══════════════════════════════════════════
   DEMO
   ═══════════════════════════════════════════ */
.demo {
  padding: 88px 0;
  background: $white;
}

.demo__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(236,72,153,0.08));
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 50px;
  padding: 10px 24px;
  margin: 0 auto 24px;
  font-size: 0.92rem;
  font-weight: 600;
  color: #6366f1;
  text-align: center;
}

.demo__sparkle { animation: sparkle 2s ease-in-out infinite; }

@keyframes sparkle {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(180deg); }
}

.demo__grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 36px;
  margin-top: 40px;
  align-items: start;
  @media (max-width: 900px) { grid-template-columns: 1fr; }
}

.demo__card {
  border-radius: $radius;
  padding: 24px;
  transition: transform .3s ease, box-shadow .3s ease;
  &:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(42,56,183,0.1); }
}

.demo__tag {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 8px 16px;
  margin-bottom: 16px;
  font-weight: 700;
  font-size: 0.88rem;
  color: #0369a1;
}

.demo__frame {
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 14px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  img { width: 100%; height: auto; display: block; }
}

.demo__frame--mobile {
  max-width: 300px;
  margin: 0 auto 14px;
}

.demo__caption {
  font-size: 0.88rem;
  color: $text-muted;
  text-align: center;
  font-weight: 500;
}

/* ═══════════════════════════════════════════
   FEATURES
   ═══════════════════════════════════════════ */
.features {
  padding: 88px 0 72px;
  background: linear-gradient(160deg, #f8faff 0%, #eef2ff 50%, #f5f3ff 100%);
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
  @media (max-width: 700px) {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

.feat-card {
  background: $white;
  border-radius: 28px;
  box-shadow: 0 4px 28px rgba(42,56,183,0.1);
  padding: 36px 32px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
  transition: box-shadow .25s, transform .25s;
  &:hover {
    box-shadow: 0 10px 40px rgba(42,56,183,0.16);
    transform: translateY(-5px);
  }
  @media (max-width: 700px) {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 28px 22px;
  }
}

.feat-card__ico {
  width: 64px;
  height: 64px;
  min-width: 64px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  svg { width: 30px; height: 30px; }
  &--blue    { background: #dbeafe; color: #2563eb; }
  &--indigo  { background: #e0e7ff; color: #4f46e5; }
  &--violet  { background: #ede9fe; color: #7c3aed; }
  &--emerald { background: #d1fae5; color: #059669; }
}

.feat-card__body {
  h3 {
    font-size: 1.15rem;
    font-weight: 800;
    color: $dark;
    margin: 0 0 8px;
    letter-spacing: -0.01em;
  }
  p {
    font-size: 0.95rem;
    color: $text;
    line-height: 1.65;
    margin: 0;
  }
}

/* ═══════════════════════════════════════════
   LEVELS
   ═══════════════════════════════════════════ */
.levels {
  padding: 88px 0 72px;
  background: $white;
}

.levels__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 8px;
  @media (max-width: 768px) { grid-template-columns: 1fr; }
}

.lv-card {
  background: $bg;
  border-radius: $radius;
  padding: 36px 24px 28px;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: transform .25s, box-shadow .25s, border-color .25s;
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(42,56,183,0.1);
    border-color: rgba(99,102,241,0.3);
  }
  h3 {
    font-size: 1.15rem;
    font-weight: 800;
    color: $dark;
    margin: 0 0 8px;
  }
  p {
    font-size: 0.88rem;
    color: $text-muted;
    line-height: 1.55;
    margin: 0;
  }
}

.lv-card__ico {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 18px;
  svg { width: 28px; height: 28px; }
  &--blue   { background: #dbeafe; color: #2563eb; }
  &--indigo { background: #e0e7ff; color: #4f46e5; }
  &--violet { background: #ede9fe; color: #7c3aed; }
}

/* Bases & Méthode */
.bases-block {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  max-width: 720px;
  margin: 36px auto 0;
  background: $bg;
  border: 1px solid #e2e8f0;
  border-radius: $radius;
  padding: 28px 32px;
  transition: transform .25s, box-shadow .25s;
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(42,56,183,0.08);
  }
  @media (max-width: 600px) {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 24px 20px;
  }
}

.bases-block__ico {
  width: 56px;
  height: 56px;
  min-width: 56px;
  border-radius: 16px;
  background: #fef3c7;
  color: #d97706;
  display: flex;
  align-items: center;
  justify-content: center;
  svg { width: 26px; height: 26px; }
}

.bases-block__body { flex: 1; }
.bases-block__header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  flex-wrap: wrap;
  h3 { font-size: 1.1rem; font-weight: 800; color: $dark; margin: 0; }
  @media (max-width: 600px) { justify-content: center; }
}

.bases-block__tag {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #d97706;
  background: #fef3c7;
  padding: 3px 10px;
  border-radius: 20px;
}

.bases-block__body p {
  font-size: 0.9rem;
  color: $text;
  line-height: 1.6;
  margin: 0;
}

/* ═══════════════════════════════════════════
   PRICING
   ═══════════════════════════════════════════ */
.pricing {
  padding: 88px 0 72px;
  background: linear-gradient(160deg, #f8faff 0%, #eef2ff 50%, #f5f3ff 100%);
  scroll-margin-top: 60px;
}

/* ═══════════════════════════════════════════
   FAQ
   ═══════════════════════════════════════════ */
.faq {
  padding: 80px 0 72px;
  background: $white;
}

.faq__list {
  margin-top: 8px;
}

.faq__item {
  border-bottom: 1px solid #e2e8f0;
}

.faq__q {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 20px 0;
  font-family: inherit;
  font-size: 1.05rem;
  font-weight: 600;
  color: $dark;
  text-align: left;
  gap: 16px;
  transition: color .2s;
  &:hover { color: $blue; }
}

.faq__arrow {
  width: 20px;
  height: 20px;
  min-width: 20px;
  color: $text-muted;
  transition: transform .3s ease;
  .faq__item--open & { transform: rotate(180deg); }
}

.faq__a-wrap {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows .35s ease;
  .faq__item--open & { grid-template-rows: 1fr; }
}

.faq__a {
  overflow: hidden;
  font-size: 0.95rem;
  color: $text;
  line-height: 1.65;
  margin: 0;
  padding: 0 0 20px;
}

/* ═══════════════════════════════════════════
   FINAL CTA
   ═══════════════════════════════════════════ */
.final-cta {
  padding: 80px 24px;
  background: linear-gradient(135deg, $blue 0%, $blue-light 100%);
  text-align: center;
}

.final-cta__title {
  font-size: clamp(1.5rem, 3vw, 2.2rem);
  font-weight: 900;
  color: $white;
  margin: 0 0 14px;
}

.final-cta__sub {
  font-size: clamp(0.95rem, 1.5vw, 1.12rem);
  color: rgba(255,255,255,0.9);
  margin: 0 auto 32px;
  max-width: 560px;
  line-height: 1.6;
}

/* ═══════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════ */
.lp-footer {
  padding: 24px;
  background: $dark;
  text-align: center;
}

.lp-footer__inner {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.85rem;
  color: rgba(255,255,255,0.55);
  a {
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    &:hover { color: $white; }
  }
}

.lp-footer__sep { color: rgba(255,255,255,0.25); }

/* ═══════════════════════════════════════════
   MODAL
   ═══════════════════════════════════════════ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 24px;
  backdrop-filter: blur(4px);
}

.modal {
  background: $white;
  border-radius: $radius;
  max-width: 440px;
  width: 100%;
  padding: 32px;
  position: relative;
  box-shadow: 0 24px 64px rgba(0,0,0,0.18);
}

.modal__close {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  font-size: 1.6rem;
  color: $text-muted;
  cursor: pointer;
}

.modal__header h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: $dark;
  margin: 0 0 8px;
}

.modal__header p {
  font-size: 0.95rem;
  color: $text;
  margin: 0 0 20px;
}

.modal__body label {
  display: block;
  font-weight: 600;
  font-size: 0.9rem;
  color: $dark;
  margin-bottom: 8px;
}

.modal__body select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  color: $dark;
  background: $white;
  margin-bottom: 12px;
}

.modal__hint {
  font-size: 0.85rem;
  color: $text-muted;
  margin-top: 8px;
}

.modal__loading, .modal__error {
  text-align: center;
  padding: 16px 0;
  color: $text;
}

.modal__actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.modal__btn {
  flex: 1;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-family: inherit;
  transition: all .2s;
}

.modal__btn--ghost {
  background: $bg;
  color: $text;
  &:hover { background: $bg-alt; }
}

.modal__btn--main {
  background: linear-gradient(135deg, $blue, $blue-light);
  color: $white;
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(42,56,183,0.3);
  }
  &:disabled {
    opacity: .6;
    cursor: not-allowed;
    transform: none;
  }
}

/* ═══════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════ */
@media (max-width: 768px) {
  .hero { padding: 64px 20px 48px; }
  .hero__ctas { flex-direction: column; align-items: center; }
  .btn--main, .btn--ghost { width: 100%; max-width: 360px; }
  .demo, .features, .levels, .pricing, .faq { padding-top: 64px; padding-bottom: 56px; }
}

@media (max-width: 480px) {
  .hero { padding: 48px 16px 40px; }
  .chip { font-size: 0.78rem; padding: 5px 11px; }
  .feat-card { padding: 24px 18px; border-radius: 22px; }
  .lv-card { padding: 28px 20px 24px; }
}
</style>
