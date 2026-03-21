<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import PricingCards from '@/components/shared/PricingCards.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import { createCheckoutSession, createGuestCheckoutSession } from '@/api/subscriptions'
import { getNiveauxByPays } from '@/api/niveaux'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { setPageSeo, getRobotsForRoute } from '@/services/seo'
import * as analytics from '@/services/analytics'

const route = useRoute()
const userStore = useUserStore()
const { error: showErrorToast } = useToast()
const { openModal } = useModalManager()

const isStartRoute = computed(() => route.path === '/start')
const isBasesMethodeRoute = computed(() => route.path === '/bases-methode')
const isExercicesCorrigesRoute = computed(
  () =>
    route.name === 'ExercicesCorrigesLanding' ||
    route.path === '/exercices-corriges' ||
    route.path === '/exercices-corriges-pas-a-pas'
)

const CTA_LABEL = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Découvrir les exercices corrigés'
    : isStartRoute.value
      ? 'Découvrir la plateforme'
      : 'Choisir mon abonnement'
)
const OFFER_CTA_LABEL = 'Choisir mon abonnement'

const quickTrust = computed(() =>
  isStartRoute.value
    ? ['Commence gratuitement maintenant', 'Aucune carte bancaire requise', 'Inscription en 30 secondes']
    : isExercicesCorrigesRoute.value
      ? ['Sans engagement', 'Accès immédiat', 'Annulable à tout moment']
      : ['Sans engagement', 'Annulable à tout moment', 'Accès immédiat']
)

const heroKicker = computed(() =>
  isExercicesCorrigesRoute.value ? 'OptiTAB — Exercices corrigés' : 'OptiTAB — Plateforme maths'
)

const heroTitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'La plateforme pour comprendre les exercices pas à pas'
    : isBasesMethodeRoute.value
      ? 'Le parcours maths Bases & Méthode pour reprendre confiance'
      : 'La plateforme de maths pour mieux comprendre et progresser'
)

const heroSubtitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Des exercices corrigés étape par étape pour savoir comment faire seul ensuite'
    : isBasesMethodeRoute.value
      ? 'Cours, fiches de synthèse et exercices corrigés pas à pas pour combler les lacunes'
      : 'Cours, fiches de synthèse et exercices corrigés pas à pas'
)

const heroResult = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Comprends la méthode, avance plus sereinement et progresse exercice après exercice.'
    : isBasesMethodeRoute.value
      ? 'Déjà adopté par de nombreux élèves du lycée au supérieur.'
      : 'Travaille plus efficacement, comprends mieux, progresse à ton rythme.'
)

const levelsSectionTitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Choisis le parcours et avance pas à pas'
    : isBasesMethodeRoute.value
      ? 'Bases & Méthode pour repartir sur de bonnes bases'
      : 'Choisis le parcours qui te correspond'
)

const levelsSectionSubtitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Des exercices corrigés pas à pas, adaptés à chaque niveau pour comprendre la méthode et progresser.'
    : isBasesMethodeRoute.value
      ? 'Une méthode claire et progressive pour reprendre confiance, combler ses lacunes et avancer pas à pas.'
      : 'Trouve en quelques secondes le parcours adapté à ton niveau.'
)

const levelsSectionNote = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Chaque parcours inclut des corrigés détaillés pour ne plus rester bloqué.'
    : isBasesMethodeRoute.value
      ? ''
      : "Lycée : programmes alignés sur l'Éducation nationale (France)"
)

const finalCtaTitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Exercices corrigés pas à pas pour progresser durablement'
    : isBasesMethodeRoute.value
      ? 'Bases & Méthode : reprends les fondamentaux et progresse durablement'
      : 'La plateforme de maths pour mieux comprendre et progresser'
)

const finalCtaSubtitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Comprends la méthode, gagne en autonomie et avance étape par étape.'
    : isBasesMethodeRoute.value
      ? 'Déjà adopté par de nombreux élèves du lycée au supérieur.'
      : 'Cours clairs, fiches de synthèse, exercices corrigés pas à pas.'
)

const heroStats = ['+150 chapitres', '+150 résumés', '+150 cours', '+1000 exercices']
const levels = computed(() =>
  isBasesMethodeRoute.value
    ? [
        {
          title: 'Bases & Méthode',
          description: 'Pour combler ses lacunes, retrouver une méthode et progresser durablement.',
          badge: 'Le plus choisi pour reprendre les bases',
          chips: ['Progressif', 'Pas à pas', 'Accès immédiat'],
          isHighlight: true
        }
      ]
    : isExercicesCorrigesRoute.value
      ? [
          {
            title: 'Seconde',
            description: 'Exercices corrigés pas à pas'
          },
          {
            title: 'Première',
            description: 'Exercices corrigés pas à pas'
          },
          {
            title: 'Terminale',
            description: 'Exercices corrigés pas à pas'
          },
          {
            title: 'Bases & Méthode',
            description: 'Exercices guidés pour reprendre les bases',
            badge: 'Priorité exercices corrigés',
            isHighlight: true
          }
        ]
    : [
        {
          title: 'Seconde',
          description: 'Programme officiel'
        },
        {
          title: 'Première',
          description: 'Programme officiel'
        },
        {
          title: 'Terminale',
          description: 'Programme officiel'
        },
        {
          title: 'Bases & Méthode',
          description: 'Pour reprendre les bases et combler ses lacunes',
          badge: 'Idéal pour consolider les bases',
          isHighlight: true
        }
      ]
)
const proofSectionTitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Ce que tu obtiens avec les exercices corrigés'
    : 'Ce que tu obtiens concrètement'
)
const proofSectionSubtitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Un aperçu clair de la méthode pas à pas, sur desktop comme sur mobile.'
    : 'Découvre concrètement l’expérience OptiTAB sur ordinateur et sur mobile.'
)
const proofHook = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Tu comprends chaque étape, puis tu sais refaire seul.'
    : 'Tu vois la méthode, tu gagnes du temps dès la première séance.'
)
const proofCards = computed(() =>
  isExercicesCorrigesRoute.value
    ? [
        {
          title: 'Méthode détaillée',
          text: "Vois chaque étape pour comprendre comment résoudre l'exercice."
        },
        {
          title: 'Corrigés pas à pas',
          text: 'Avance ligne par ligne avec une logique claire.'
        },
        {
          title: 'Compréhension durable',
          text: 'Apprends la méthode pour réussir seul ensuite.'
        }
      ]
    : [
        {
          title: 'Cours clairs',
          text: 'Des cours structurés pour comprendre vite et retenir durablement.'
        },
        {
          title: 'Fiches de synthèse',
          text: 'Les points essentiels à réviser sans perdre de temps.'
        },
        {
          title: 'Exercices corrigés pas à pas',
          text: 'Une méthode détaillée pour savoir comment faire seul ensuite.'
        }
      ]
)
const faqItems = computed(() =>
  isExercicesCorrigesRoute.value
    ? [
        {
          question: "À qui s’adressent les exercices corrigés pas à pas ?",
          answer: 'Aux élèves du lycée au supérieur qui veulent comprendre la méthode et progresser avec un cadre clair.'
        },
        {
          question: 'Est-ce adapté si je bloque souvent en maths ?',
          answer: 'Oui. Le format pas à pas est conçu pour débloquer chaque exercice sans sauter les étapes clés.'
        },
        {
          question: 'Est-ce que je vois vraiment toutes les étapes ?',
          answer: 'Oui. Les corrigés détaillent le raisonnement étape par étape pour comprendre la logique complète.'
        },
        {
          question: 'Est-ce utile pour apprendre à faire seul ensuite ?',
          answer: 'Oui. L’objectif est de te transmettre une méthode réutilisable pour résoudre ensuite en autonomie.'
        },
        {
          question: 'Puis-je arrêter à tout moment ?',
          answer: "Oui. L'abonnement est sans engagement et annulable à tout moment."
        }
      ]
    : [
        {
          question: "À qui s'adresse OptiTAB ?",
          answer: 'Aux élèves de Seconde, Première, Terminale et Bases & Méthode.'
        },
        {
          question: "À qui s'adresse Bases & Méthode ?",
          answer: "Bases & Méthode s’adresse aux élèves qui veulent combler leurs lacunes, reprendre les fondamentaux et progresser durablement en maths. Ce parcours est particulièrement adapté aux élèves du collège au lycée, ainsi qu’aux étudiants en BTS et en classes préparatoires qui ont besoin de consolider leurs bases avec une méthode claire, progressive et efficace. Il est déjà utilisé et recommandé par de nombreux élèves, notamment en Bac, en BTS et en prépa."
        },
        {
          question: 'Est-ce sans engagement ?',
          answer: "Oui. L'abonnement est sans engagement."
        },
        {
          question: 'Puis-je annuler à tout moment ?',
          answer: "Oui. L'annulation se fait quand vous voulez."
        },
        {
          question: "Que contient l'abonnement ?",
          answer: 'Cours clairs, fiches de synthèse et exercices corrigés pas à pas.'
        },
        {
          question: "Comment contacter quelqu'un si j'ai une question ?",
          answer: 'Par WhatsApp ou par email. Réponse rapide.'
        }
      ]
)

const submitting = ref(false)
const niveaux = ref([])
const niveauxLoading = ref(false)
const niveauxError = ref('')
const selectedNiveauId = ref(userStore.niveau_pays?.id ? Number(userStore.niveau_pays.id) : null)
const showLevelModal = ref(false)
const pendingPriceId = ref('')
const pendingPlanName = ref('')
const heroOfferTitle = computed(() =>
  isExercicesCorrigesRoute.value
    ? 'Abonnement dès 4.99€'
    : isStartRoute.value
    ? 'Déjà adoptée par de nombreux élèves\ndu lycée au supérieur'
    : isBasesMethodeRoute.value
      ? 'Le parcours Bases & Méthode\ndéjà adopté par de nombreux élèves'
      : 'Abonnements dès 4,99 €'
)
const heroOfferSub = computed(() =>
  isBasesMethodeRoute.value
    ? 'Parcours recommandé en Bac, BTS et prépa'
    : 'Accès immédiat à la plateforme'
)
const showHeroOfferCard = computed(() => !isStartRoute.value && !isBasesMethodeRoute.value)

watch(
  () => userStore.niveau_pays?.id,
  (newId) => {
    if (newId) selectedNiveauId.value = Number(newId)
  }
)

watch(showLevelModal, (isOpen) => {
  if (typeof document === 'undefined') return
  document.body.style.overflow = isOpen ? 'hidden' : ''
})

const selectedNiveau = computed(() => {
  return niveaux.value.find((niveau) => Number(niveau.id) === Number(selectedNiveauId.value)) || null
})

const selectedNiveauLabel = computed(() => {
  if (!selectedNiveau.value) return ''
  const pays = selectedNiveau.value.pays?.nom
  return pays ? `${selectedNiveau.value.nom} - ${pays}` : selectedNiveau.value.nom
})

const normalizeText = (value = '') =>
  String(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()

const findBasesMethodeLevel = (list = []) =>
  list.find((niveau) => {
    const label = normalizeText(niveau?.nom)
    return label.includes('base') && label.includes('methode')
  }) || null

function scrollToOffer() {
  if (typeof document === 'undefined') return
  const node = document.getElementById('offre')
  if (!node) return
  node.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function openRegisterModal() {
  openModal(MODAL_IDS.REGISTER)
}

function handlePrimaryCta() {
  if (isStartRoute.value) {
    openRegisterModal()
    return
  }
  scrollToOffer()
}

async function handlePlanSelect(card) {
  await handleSubscribe(card)
}

async function loadLevels(force = false) {
  if (niveauxLoading.value) return
  if (!force && niveaux.value.length) return

  try {
    niveauxLoading.value = true
    niveauxError.value = ''
    const data = await getNiveauxByPays()
    const raw = Array.isArray(data?.results)
      ? data.results
      : Array.isArray(data)
        ? data
        : Array.isArray(data?.data)
          ? data.data
          : []

    niveaux.value = raw.filter((niveau) => niveau && (niveau.est_actif === undefined || niveau.est_actif))

    if (isBasesMethodeRoute.value) {
      const basesMethodeLevel = findBasesMethodeLevel(niveaux.value)
      if (basesMethodeLevel) {
        selectedNiveauId.value = Number(basesMethodeLevel.id)
      }
    }

    if (!selectedNiveauId.value && niveaux.value.length) {
      const preferred = userStore.niveau_pays?.id
      const match = preferred ? niveaux.value.find((niveau) => Number(niveau.id) === Number(preferred)) : null
      selectedNiveauId.value = match ? match.id : niveaux.value[0].id
    }
  } catch (error) {
    console.error('Erreur chargement niveaux:', error)
    niveauxError.value = 'Impossible de charger les niveaux.'
  } finally {
    niveauxLoading.value = false
  }
}

async function handleSubscribe(card) {
  const priceId = card?.priceId
  if (!priceId) {
      showErrorToast('Plan non configuré (Price ID manquant).')
    return
  }

  pendingPriceId.value = priceId
  pendingPlanName.value = card?.title || 'OptiTAB'

  await loadLevels()

  if (!niveaux.value.length) {
    showErrorToast('Niveaux indisponibles pour le moment.')
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
  if (!pendingPriceId.value) {
    closeLevelModal()
    return
  }

  if (!selectedNiveauId.value) {
      showErrorToast('Choisis un niveau pour continuer.')
    return
  }

  try {
    submitting.value = true
    const checkoutFn = userStore.isAuthenticated ? createCheckoutSession : createGuestCheckoutSession
    const { data } = await checkoutFn(pendingPriceId.value, {
      niveau_pays_id: selectedNiveauId.value
    })

    const redirectUrl = data?.checkout_url || data?.url
    if (!redirectUrl) {
      showErrorToast('Paiement indisponible. Réessaie plus tard.')
      return
    }

    analytics.beginCheckout({
      value: data?.amount,
      currency: data?.currency || 'EUR',
      planName: data?.plan_name || pendingPlanName.value,
      planMode: data?.plan_mode,
      transactionId: data?.transaction_id || data?.tiktok_event_id || '',
      eventId: data?.tiktok_event_id || data?.transaction_id || '',
    })

    window.location.assign(redirectUrl)
  } catch (error) {
    console.error(error)
    showErrorToast('Erreur lors du paiement.')
  } finally {
    submitting.value = false
    showLevelModal.value = false
    pendingPriceId.value = ''
    pendingPlanName.value = ''
  }
}

function handleEscape(event) {
  if (event.key === 'Escape') closeLevelModal()
}

function storeGclid() {
  if (typeof window === 'undefined') return
  try {
    const params = new URLSearchParams(window.location.search)
    const gclid = params.get('gclid')
    if (gclid) window.localStorage?.setItem('optitab_gclid', gclid)
  } catch (_) {}
}

onMounted(() => {
  setPageSeo({
    title: isExercicesCorrigesRoute.value
      ? 'Exercices corrigés pas à pas : comprendre chaque étape | OptiTAB'
      : isBasesMethodeRoute.value
        ? 'Bases & Méthode : le parcours pour combler ses lacunes | OptiTAB'
        : 'La plateforme de maths pour mieux comprendre et progresser | OptiTAB',
    description: isExercicesCorrigesRoute.value
      ? 'Des exercices corrigés étape par étape pour comprendre la méthode, ne plus rester bloqué et progresser plus vite.'
      : isBasesMethodeRoute.value
        ? 'Le parcours Bases & Méthode pour reprendre les fondamentaux : cours clairs, fiches de synthèse et exercices corrigés pas à pas.'
        : 'Cours clairs, fiches de synthèse et exercices corrigés pas à pas. Sans engagement, annulable à tout moment, accès immédiat.',
    canonicalPath: isExercicesCorrigesRoute.value
      ? '/exercices-corriges'
      : isBasesMethodeRoute.value
        ? '/bases-methode'
        : (isStartRoute.value ? '/start' : '/plateforme-maths'),
    robots: getRobotsForRoute({ route }),
    ogType: 'website'
  })

  storeGclid()
  if (typeof window !== 'undefined') window.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  if (typeof window !== 'undefined') window.removeEventListener('keydown', handleEscape)
  if (typeof document !== 'undefined') document.body.style.overflow = ''
})
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <div class="landing-ads">
      <div class="landing-shell">
        <section class="block hero-block">
          <div class="hero-copy">
            <p class="hero-kicker">{{ heroKicker }}</p>
            <h1>{{ heroTitle }}</h1>
            <p class="hero-subtitle">{{ heroSubtitle }}</p>
            <p class="hero-result">{{ heroResult }}</p>

            <button
              type="button"
              class="cta-primary"
              data-cta-name="pricing"
              data-cta-location="hero"
              @click="handlePrimaryCta"
            >
              {{ CTA_LABEL }}
            </button>

            <div class="trust-row">
              <span v-for="item in quickTrust" :key="item" class="trust-chip">{{ item }}</span>
            </div>
          </div>

          <div :class="['hero-side', { 'hero-side--stats-only': !showHeroOfferCard }]">
            <div v-if="showHeroOfferCard" class="hero-offer-card">
              <p :class="['hero-offer-title', { 'hero-offer-title--start': isStartRoute, 'hero-offer-title--bases': isBasesMethodeRoute, 'hero-offer-title--exercise': isExercicesCorrigesRoute }]">{{ heroOfferTitle }}</p>
              <p class="hero-offer-sub">{{ heroOfferSub }}</p>
              <GoogleReviewsCompact />
            </div>
            <div
              :class="['hero-stats', 'hero-stats--side', { 'hero-stats--solo': !showHeroOfferCard }]"
              aria-label="Statistiques OptiTAB"
            >
              <article v-for="item in heroStats" :key="item" class="hero-stat">
                <span class="hero-stat-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.8" />
                    <path d="M8.5 12.2L10.8 14.5L15.7 9.6" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
                <span class="hero-stat-text">{{ item }}</span>
              </article>
            </div>
          </div>
        </section>

        <section class="block proof-block">
          <div class="section-head">
            <h2>{{ proofSectionTitle }}</h2>
            <p>{{ proofSectionSubtitle }}</p>
          </div>

          <div class="proof-media">
            <article class="proof-media-card">
              <p class="proof-media-label">Version desktop</p>
              <img src="/video/optitab-demo-exercices.gif" alt="Aperçu desktop de la plateforme OptiTAB" />
            </article>
            <article class="proof-media-card proof-media-card--mobile">
              <p class="proof-media-label">Version mobile</p>
              <img src="/video/optitab-demo-mobile.gif" alt="Aperçu mobile de la plateforme OptiTAB" />
            </article>
          </div>

          <div class="proof-grid">
            <article v-for="item in proofCards" :key="item.title" class="proof-card">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
          <p class="proof-hook">{{ proofHook }}</p>
        </section>

        <section :class="['block', 'levels-block', { 'levels-block--bases': isBasesMethodeRoute }]">
          <div class="section-head">
            <h2>{{ levelsSectionTitle }}</h2>
            <p>{{ levelsSectionSubtitle }}</p>
            <p v-if="levelsSectionNote" class="levels-professional-note">
              {{ levelsSectionNote }}
            </p>
          </div>

          <div :class="['levels-grid', { 'levels-grid--single': levels.length === 1 }]">
            <article
              v-for="level in levels"
              :key="level.title"
              :class="[
                'level-card',
                {
                  'level-card--highlight': level.isHighlight,
                  'level-card--compact': isBasesMethodeRoute && levels.length === 1
                }
              ]"
              role="button"
              tabindex="0"
              :aria-label="`Choisir ${level.title}`"
              @click="scrollToOffer"
              @keydown.enter.prevent="scrollToOffer"
              @keydown.space.prevent="scrollToOffer"
            >
              <h3 class="level-title">{{ level.title }}</h3>
              <p v-if="level.badge" class="level-badge">{{ level.badge }}</p>
              <p class="level-desc">{{ level.description }}</p>
              <div v-if="level.chips?.length" class="level-mini-badges">
                <span v-for="chip in level.chips" :key="`${level.title}-${chip}`" class="level-mini-badge">
                  {{ chip }}
                </span>
              </div>
            </article>
          </div>
        </section>

        <section id="offre" class="block offer-block">
          <div class="section-head">
            <h2>Choisis la formule qui te convient</h2>
            <p>Deux formules simples pour accéder à OptiTAB selon ton rythme.</p>
          </div>

          <PricingCards
            :submitting="submitting"
            cta-location="landing_offer"
            :primary-cta-label="OFFER_CTA_LABEL"
            :subscription-only="false"
            @select="handlePlanSelect"
          />
        </section>

        <section class="block faq-block">
          <FaqSection
            :faq="faqItems"
            description="On lève les freins avant abonnement."
          />

          <div class="contact-card">
            <h3>Une question avant de t'abonner ?</h3>
            <p>Contact rapide par WhatsApp ou par email.</p>
            <div class="contact-actions">
              <a
                href="https://wa.me/33764040251?text=Bonjour%2C%20j%27ai%20une%20question%20sur%20l%27abonnement%20OptiTAB."
                target="_blank"
                rel="noopener noreferrer"
                class="contact-link contact-link--whatsapp"
                data-cta-name="whatsapp"
                data-cta-location="landing_contact"
              >
                WhatsApp
              </a>
              <a href="mailto:contact@optitab.net" class="contact-link">
                contact@optitab.net
              </a>
            </div>
          </div>
        </section>

        <section class="block final-cta-block">
          <h2>{{ finalCtaTitle }}</h2>
          <p>{{ finalCtaSubtitle }}</p>
          <div class="trust-row trust-row--center">
            <span v-for="item in quickTrust" :key="`final-${item}`" class="trust-chip">{{ item }}</span>
          </div>
          <button
            type="button"
            class="cta-primary"
            data-cta-name="pricing"
            data-cta-location="final"
            @click="handlePrimaryCta"
          >
            {{ CTA_LABEL }}
          </button>
        </section>
      </div>
    </div>

    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur l'abonnement OptiTAB."
      tooltip="Besoin d'aide ? WhatsApp"
    />

    <Teleport to="body">
      <div v-if="showLevelModal" class="level-modal-overlay" @click="closeLevelModal">
        <div class="level-modal" @click.stop>
          <button type="button" class="modal-close" :disabled="submitting" @click="closeLevelModal">&times;</button>

          <div class="modal-header">
            <p class="modal-kicker">Avant paiement</p>
            <h3>Choisis ton niveau</h3>
            <p>{{ pendingPlanName || 'OptiTAB' }}</p>
          </div>

          <div class="modal-body">
            <div v-if="niveauxLoading" class="modal-loading">
              <div class="spinner"></div>
              <p>Chargement...</p>
            </div>

            <div v-else-if="niveauxError" class="modal-error">
              <p>{{ niveauxError }}</p>
              <button type="button" class="retry-btn" @click="loadLevels(true)">Réessayer</button>
            </div>

            <div v-else class="modal-select">
              <label for="level-select">Niveau</label>
              <select id="level-select" v-model.number="selectedNiveauId">
                <option v-for="niveau in niveaux" :key="niveau.id" :value="niveau.id">
                  {{ niveau.pays?.nom ? `${niveau.nom} - ${niveau.pays.nom}` : niveau.nom }}
                </option>
              </select>
              <p v-if="selectedNiveauLabel" class="modal-selected">Accès : {{ selectedNiveauLabel }}</p>
            </div>

            <p v-if="!userStore.isAuthenticated" class="modal-hint">
              Le compte est créé automatiquement après paiement.
            </p>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-light" :disabled="submitting" @click="closeLevelModal">Annuler</button>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="submitting || !selectedNiveauId"
              @click="confirmSubscription"
            >
              {{ submitting ? 'Redirection...' : 'Continuer' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </MainLayout>
</template>

<style scoped lang="scss">
.landing-ads {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 45%, #f6f8ff 100%);
  min-height: 100%;
}

.landing-shell {
  max-width: 1120px;
  margin: 0 auto;
  padding: 26px 16px 88px;
  display: grid;
  gap: 0;
}

.block {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 34px 0;
  box-shadow: none;
}

.block + .block {
  border-top: 1px solid rgba(30, 58, 138, 0.12);
}

.hero-block {
  display: grid;
  grid-template-columns: minmax(0, 1.34fr) minmax(0, 0.66fr);
  gap: 22px;
  align-items: start;
}

.hero-copy {
  max-width: 820px;
}

.hero-kicker {
  margin: 0;
  color: #2a38b7;
  font-size: 0.82rem;
  letter-spacing: 0.02em;
  font-weight: 800;
}

.hero-stats {
  margin: 12px 0 14px;
  max-width: 470px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 10px;
}

.hero-stats--side {
  margin: 0;
  max-width: none;
}

.hero-stats--solo {
  width: 100%;
  gap: 8px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.hero-stat {
  min-height: 40px;
  border-radius: 11px;
  border: 1px solid #d7e3ff;
  background: linear-gradient(145deg, #f8fbff 0%, #f1f5ff 100%);
  padding: 0 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hero-stat-icon {
  width: 16px;
  height: 16px;
  color: #2a38b7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.hero-stat-icon svg {
  width: 100%;
  height: 100%;
}

.hero-stat-text {
  color: #1e293b;
  font-size: 0.88rem;
  font-weight: 700;
  line-height: 1.2;
}

.hero-stats--solo .hero-stat {
  min-height: 54px;
  border-radius: 13px;
  padding: 0 10px;
  gap: 8px;
  justify-content: flex-start;
}

.hero-stats--solo .hero-stat-icon {
  width: 16px;
  height: 16px;
}

.hero-stats--solo .hero-stat-text {
  font-size: 0.9rem;
  font-weight: 730;
  line-height: 1.2;
  white-space: nowrap;
}

.hero-copy h1 {
  margin: 10px 0 0;
  max-width: 30ch;
  font-size: clamp(1.52rem, 2.7vw, 2.2rem);
  line-height: 1.08;
  text-wrap: balance;
  color: #0f172a;
}

.hero-subtitle {
  margin: 14px 0 0;
  color: #1e293b;
  font-size: 1.04rem;
  font-weight: 600;
  line-height: 1.35;
}

.hero-result {
  margin: 14px 0 0;
  color: #475569;
  font-size: 0.96rem;
  line-height: 1.45;
}

.hero-side {
  display: grid;
  align-content: start;
  gap: 9px;
  max-width: 500px;
  justify-self: end;
}

.hero-side--stats-only {
  width: 100%;
  max-width: 560px;
  justify-self: center;
  align-self: center;
}

.hero-offer-card {
  width: 100%;
  background: linear-gradient(145deg, #f7faff 0%, #f1f5ff 100%);
  border: 1px solid #d7e2ff;
  border-radius: 18px;
  padding: 16px;
  display: grid;
  gap: 9px;
}

.hero-offer-title {
  margin: 0;
  color: #1e3a8a;
  font-size: 1.06rem;
  font-weight: 780;
  line-height: 1.2;
  white-space: pre-line;
}

.hero-offer-title--start {
  font-size: 1.02rem;
  line-height: 1.12;
}

.hero-offer-title--bases {
  font-size: 1rem;
  line-height: 1.16;
}

.hero-offer-title--exercise {
  font-size: 1.02rem;
  line-height: 1.18;
}

.hero-offer-sub {
  margin: 0;
  color: #475569;
  font-size: 0.9rem;
}

.cta-primary {
  margin-top: 20px;
  min-height: 50px;
  border: 1px solid #1f4ed2;
  border-radius: 14px;
  padding: 0 20px;
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cta-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
}

.trust-row {
  margin-top: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.trust-row--center {
  justify-content: center;
}

.trust-chip {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: 0 10px;
  border-radius: 999px;
  background: #eef4ff;
  border: 1px solid #cfe0ff;
  color: #1e3a8a;
  font-size: 0.82rem;
  font-weight: 700;
}

.section-head {
  margin-bottom: 16px;
}

.section-head h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.45rem, 2.6vw, 2rem);
}

.section-head p {
  margin: 8px 0 0;
  color: #475569;
  font-size: 0.96rem;
}

.levels-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.levels-grid--single {
  grid-template-columns: minmax(280px, 520px);
}

.level-card {
  min-height: 118px;
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: linear-gradient(140deg, #ffffff 0%, #f5f8ff 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  padding: 16px 14px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease, background 0.22s ease;
}

.level-card:hover {
  transform: translateY(-2px);
  border-color: #a8c1ff;
  box-shadow: 0 10px 24px rgba(30, 58, 138, 0.1);
}

.level-card:focus-visible {
  outline: none;
  border-color: #6d8dff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.level-title {
  margin: 0;
  font-weight: 800;
  color: #0f172a;
  font-size: 1.12rem;
  letter-spacing: -0.01em;
}

.level-badge {
  margin: 0;
  color: #2a38b7;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.level-desc {
  margin: 0;
  color: #475569;
  font-size: 0.84rem;
  line-height: 1.4;
  font-weight: 650;
}

.level-card--highlight {
  border-color: #9fb6ff;
  background: linear-gradient(140deg, #f7faff 0%, #edf3ff 100%);
}

.level-card--highlight:hover {
  border-color: #7596ff;
  box-shadow: 0 12px 26px rgba(42, 56, 183, 0.14);
}

.level-card--compact {
  min-height: 0;
  justify-content: flex-start;
  align-items: flex-start;
  text-align: left;
  gap: 6px;
  padding: 16px 18px;
}

.level-card--compact .level-title {
  font-size: 1.16rem;
}

.level-card--compact .level-badge {
  font-size: 0.76rem;
  font-weight: 800;
}

.level-card--compact .level-desc {
  font-size: 0.9rem;
  line-height: 1.42;
}

.level-mini-badges {
  margin-top: 2px;
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.level-mini-badge {
  min-height: 24px;
  padding: 0 9px;
  border-radius: 999px;
  border: 1px solid #c9d8ff;
  background: #f4f8ff;
  color: #1e3a8a;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
}

.levels-professional-note {
  margin: 9px 0 0;
  color: #334155;
  font-size: 0.9rem;
  font-weight: 600;
}

.proof-media {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 14px;
  margin-bottom: 14px;
}

.proof-media-card {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.proof-media-label {
  margin: 0 0 10px;
  color: #1e3a8a;
  font-size: 0.9rem;
  font-weight: 800;
  text-align: center;
}

.proof-media-card img {
  width: 100%;
  border-radius: 14px;
  display: block;
}

.proof-media-card--mobile img {
  max-width: 300px;
  margin: 0 auto;
}

.proof-media-card--mobile .proof-media-label {
  max-width: 300px;
  margin: 0 auto 10px;
  text-align: center;
}

.proof-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.proof-card {
  border-radius: 14px;
  border: 1px solid #dbe6ff;
  background: #ffffff;
  padding: 14px;
}

.proof-card h3 {
  margin: 0 0 6px;
  font-size: 1rem;
  color: #0f172a;
}

.proof-card p {
  margin: 0;
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.45;
}

.proof-hook {
  margin: 14px 0 0;
  color: #1e3a8a;
  font-size: 0.95rem;
  font-weight: 700;
  text-align: center;
}

.offer-block {
  background: transparent;
  border-color: transparent;
}

.offer-block :deep(.pricing-card) {
  border-color: #dbe6ff;
}

.faq-block :deep(.faq-section) {
  margin-bottom: 0;
}

.contact-card {
  margin-top: 14px;
  border-radius: 16px;
  border: 1px solid #cfe0ff;
  background: linear-gradient(145deg, #f8fbff 0%, #eef3ff 100%);
  padding: 16px;
}

.contact-card h3 {
  margin: 0;
  color: #0f172a;
  font-size: 1.02rem;
}

.contact-card p {
  margin: 6px 0 0;
  color: #475569;
  font-size: 0.92rem;
}

.contact-actions {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.contact-link {
  min-height: 40px;
  border-radius: 10px;
  border: 1px solid #c8d6fa;
  background: #ffffff;
  color: #1f2937;
  text-decoration: none;
  font-weight: 700;
  padding: 0 14px;
  display: inline-flex;
  align-items: center;
}

.contact-link--whatsapp {
  background: #25d366;
  border-color: #25d366;
  color: #ffffff;
}

.final-cta-block {
  text-align: center;
  background: linear-gradient(145deg, #ffffff 0%, #eef2ff 100%);
}

.final-cta-block h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.45rem, 2.6vw, 2rem);
}

.final-cta-block p {
  margin: 8px 0 0;
  color: #475569;
}

.level-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(15, 23, 42, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px;
}

.level-modal {
  width: min(520px, 100%);
  background: #ffffff;
  border-radius: 16px;
  padding: 22px;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 34px;
  height: 34px;
  border-radius: 999px;
  border: none;
  background: #f1f5f9;
  font-size: 1.3rem;
  cursor: pointer;
}

.modal-header {
  text-align: center;
}

.modal-kicker {
  margin: 0;
  font-size: 0.75rem;
  color: #4338ca;
  font-weight: 800;
  text-transform: uppercase;
}

.modal-header h3 {
  margin: 8px 0 4px;
}

.modal-header p {
  margin: 0;
  color: #475569;
}

.modal-body {
  margin-top: 16px;
}

.modal-select label {
  display: block;
  margin-bottom: 6px;
  font-weight: 700;
}

.modal-select select {
  width: 100%;
  min-height: 48px;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 0 10px;
}

.modal-selected {
  margin: 8px 0 0;
  color: #1e3a8a;
  font-size: 0.9rem;
  font-weight: 700;
}

.modal-hint {
  margin: 10px 0 0;
  font-size: 0.85rem;
  color: #475569;
}

.modal-loading {
  text-align: center;
}

.spinner {
  width: 28px;
  height: 28px;
  margin: 0 auto 8px;
  border: 3px solid #dbeafe;
  border-top-color: #1d4ed8;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.retry-btn {
  min-height: 40px;
  border: none;
  border-radius: 10px;
  background: #eef2ff;
  color: #3730a3;
  font-weight: 700;
  padding: 0 12px;
  cursor: pointer;
}

.modal-error {
  text-align: center;
  color: #b91c1c;
}

.modal-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.btn {
  min-height: 46px;
  border-radius: 12px;
  border: 1px solid transparent;
  padding: 0 14px;
  font-weight: 800;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
}

.btn-light {
  background: #f1f5f9;
  color: #0f172a;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 960px) {
  .hero-block {
    grid-template-columns: 1fr;
  }

  .hero-side {
    width: 100%;
    max-width: 100%;
    justify-self: center;
  }

  .hero-offer-card {
    display: none;
  }

  .hero-stats--side {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
  }

  .levels-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .levels-grid--single {
    grid-template-columns: 1fr;
  }

  .proof-media,
  .proof-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .landing-shell {
    padding: 18px 12px 82px;
  }

  .block {
    padding: 24px 0;
    border-radius: 0;
  }

  .hero-stats {
    gap: 8px;
  }

  .hero-stat {
    min-height: 36px;
    padding: 0 8px;
  }

  .hero-stat-text {
    font-size: 0.8rem;
  }

  .hero-side--stats-only {
    max-width: 100%;
  }

  .hero-stats--solo {
    gap: 10px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hero-stats--solo .hero-stat {
    min-height: 46px;
    padding: 0 10px;
    gap: 7px;
    justify-content: flex-start;
  }

  .hero-stats--solo .hero-stat-text {
    font-size: 0.82rem;
    white-space: nowrap;
  }

  .cta-primary {
    width: 100%;
  }

  .modal-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
