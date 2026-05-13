<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import { submitDiagnosticLead } from '@/api/newsletter'
import { setPageSeo, getRobotsForRoute } from '@/services/seo'

const route = useRoute()
const router = useRouter()

const SESSION_KEY = 'optitab_diagnostic_lead'

const LEVEL_OPTIONS = [
  { value: '', label: '— Choisis ton niveau —', disabled: true },
  { value: 'college', label: 'Collège' },
  { value: 'seconde', label: 'Seconde' },
  { value: 'premiere', label: 'Première' },
  { value: 'terminale', label: 'Terminale' },
  { value: 'prepa', label: 'Prépa' },
  { value: 'bts', label: 'BTS' },
  { value: 'parent', label: 'Parent (je remplis pour mon enfant)' }
]

const DIFFICULTY_OPTIONS = [
  { value: '', label: '— Sur quoi tu bloques le plus ? —', disabled: true },
  { value: 'cours_vs_exercices', label: 'Je comprends le cours mais pas les exercices' },
  { value: 'organisation', label: 'Je n\'arrive pas à m\'organiser ou réviser efficacement' },
  { value: 'methode', label: 'Je n\'ai pas de méthode claire' },
  { value: 'bac', label: 'Je prépare le Bac et j\'ai besoin de structure' },
  { value: 'motivation', label: 'Je manque de motivation / je me décourage' }
]

const leadMagnetItems = [
  {
    title: 'Ton diagnostic clair',
    text: 'On identifie où tu bloques : cours, méthode, exercices ou gestion du temps.'
  },
  {
    title: 'Ton plan 7 jours',
    text: 'Une feuille de route concrète pour les 7 prochains jours, adaptée à ton niveau.'
  },
  {
    title: 'Les erreurs à éviter',
    text: 'Les erreurs typiques qui font perdre des points en contrôle et au Bac.'
  },
  {
    title: 'Une méthode de travail',
    text: 'Comment réviser efficacement, sans rester bloqué·e devant la feuille.'
  },
  {
    title: 'Des exercices corrigés type',
    text: 'Des exemples corrigés pas à pas pour voir la méthode en action.'
  },
  {
    title: 'Conseils selon ton niveau',
    text: 'Des recommandations différentes pour la Seconde, la Première et la Terminale.'
  }
]

const painPoints = [
  'Je comprends le cours, mais dès que j\'attaque un exercice, je bloque.',
  'Je révise, je révise… et mes notes ne montent pas.',
  'Je ne sais jamais par quoi commencer ni quoi travailler en priorité.',
  'Les corrections vont trop vite, je ne suis pas la logique.',
  'Les cours particuliers coûtent trop cher pour ce que ça apporte.'
]

const solutionCards = [
  {
    title: 'Des cours courts et clairs',
    text: 'Chaque notion est expliquée simplement, pour comprendre vite et retenir longtemps.'
  },
  {
    title: 'Des fiches de synthèse',
    text: 'L\'essentiel à retenir, prêt à imprimer avant un contrôle ou le Bac.'
  },
  {
    title: 'Des exercices corrigés pas à pas',
    text: 'On t\'explique chaque étape — tu sais ensuite refaire seul·e.'
  },
  {
    title: 'Une progression structurée',
    text: 'Un parcours pour chaque niveau, du collège à la Terminale, programme officiel.'
  }
]

const trustItems = [
  { title: 'Programme officiel', text: 'Contenus alignés sur les programmes Éducation nationale, collège et lycée.' },
  { title: 'Pas à pas', text: 'Exercices corrigés étape par étape, sans sauter la logique.' },
  { title: 'Fiches claires', text: 'Des fiches de synthèse pour réviser sans perdre de temps.' },
  { title: 'Progression structurée', text: 'Une plateforme pensée pour progresser semaine après semaine.' },
  { title: 'Accessible', text: 'Une alternative concrète et abordable aux cours particuliers.' }
]

const comparisonRows = [
  { criterion: 'Structure', youtube: 'Non, contenu dispersé', tutor: 'Oui, dépend du prof', optitab: 'Oui, parcours par niveau' },
  { criterion: 'Exercices corrigés pas à pas', youtube: 'Rare', tutor: 'Oui, mais limité au prof', optitab: 'Oui, sur toute la plateforme' },
  { criterion: 'Coût mensuel', youtube: 'Gratuit', tutor: '30-50 €/h', optitab: 'Dès 4,99 €/mois' },
  { criterion: 'Accessible 24/7', youtube: 'Oui', tutor: 'Non', optitab: 'Oui' },
  { criterion: 'Méthode adaptée Bac', youtube: 'Aléatoire', tutor: 'Variable', optitab: 'Oui' }
]

const faqItems = [
  {
    question: 'Le diagnostic est-il vraiment gratuit ?',
    answer: 'Oui, 100 % gratuit. Aucune carte bancaire, aucun engagement. Tu reçois le diagnostic par email dès que tu valides le formulaire.'
  },
  {
    question: 'Que vais-je recevoir exactement ?',
    answer: 'Un diagnostic personnalisé selon ton niveau et ta principale difficulté, un plan 7 jours, les erreurs typiques à éviter, et un aperçu d\'exercices corrigés pas à pas.'
  },
  {
    question: 'Est-ce adapté à mon niveau ?',
    answer: 'Oui. Le diagnostic et les conseils sont adaptés au collège, à la Seconde, la Première, la Terminale, la prépa et le BTS.'
  },
  {
    question: 'Est-ce utile pour préparer le Bac ?',
    answer: 'Oui, c\'est même un des cas d\'usage principaux. La méthode OptiTAB couvre les chapitres et types d\'exercices typiques du Bac.'
  },
  {
    question: 'Vais-je recevoir trop d\'emails ?',
    answer: 'Non. Tu reçois une séquence courte d\'environ 5 emails utiles répartis sur 2 semaines, puis un email occasionnel avec des conseils ou ressources.'
  },
  {
    question: 'Puis-je me désinscrire facilement ?',
    answer: 'Oui, en un clic, depuis n\'importe quel email. Pas de justification à fournir.'
  },
  {
    question: 'Combien coûte OptiTAB ensuite ?',
    answer: 'OptiTAB est un abonnement sans engagement à partir de 4,99 €/mois. Tu peux annuler à tout moment depuis ton compte. Tu n\'es jamais obligé·e de t\'abonner pour profiter du diagnostic.'
  }
]

function createInitialForm() {
  return {
    firstName: '',
    email: '',
    level: '',
    difficulty: '',
    consent: false,
    website: ''
  }
}

const formHero = reactive(createInitialForm())
const formMain = reactive(createInitialForm())
const formFinal = reactive(createInitialForm())

const submittingHero = ref(false)
const submittingMain = ref(false)
const submittingFinal = ref(false)

const errorHero = ref('')
const errorMain = ref('')
const errorFinal = ref('')

const successHero = ref(false)
const successMain = ref(false)
const successFinal = ref(false)

const formViewed = reactive({ hero: false, main: false, final: false })

function pushDataLayerEvent(event, extra = {}) {
  if (typeof window === 'undefined') return
  try {
    if (!Array.isArray(window.dataLayer)) {
      window.dataLayer = []
    }
    window.dataLayer.push({ event, ...extra })
  } catch (_) {}
}

function trackFormView(location) {
  if (formViewed[location]) return
  formViewed[location] = true
  pushDataLayerEvent('lead_form_viewed', { form_location: location })
}

function trackLevelSelected(location, value) {
  if (!value) return
  pushDataLayerEvent('level_selected', { form_location: location, level: value })
}

function trackDifficultySelected(location, value) {
  if (!value) return
  pushDataLayerEvent('difficulty_selected', { form_location: location, difficulty: value })
}

function trackLeadSubmitted({ location, level, difficulty, consent }) {
  pushDataLayerEvent('lead_submitted', {
    form_location: location,
    level,
    difficulty,
    consent_marketing: Boolean(consent)
  })
}

function validateEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(value).trim())
}

function validateForm(form) {
  if (!String(form.firstName || '').trim()) return 'Indique ton prénom.'
  if (!validateEmail(form.email)) return 'Indique un email valide.'
  if (!form.level) return 'Choisis ton niveau.'
  if (!form.difficulty) return 'Choisis ta principale difficulté.'
  return ''
}

function getUtmContext() {
  if (typeof window === 'undefined') return {}
  try {
    const params = new URLSearchParams(window.location.search)
    const context = {}
    const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'ttclid', 'msclkid']
    keys.forEach((key) => {
      const value = params.get(key)
      if (value) context[key] = value
    })
    if (!context.gclid) {
      const storedGclid = window.localStorage?.getItem('optitab_gclid')
      if (storedGclid) context.gclid = storedGclid
    }
    context.referrer = document?.referrer || ''
    context.landing_path = window.location.pathname
    return context
  } catch (_) {
    return {}
  }
}

function storeLeadContextForThankYou(form, location) {
  if (typeof window === 'undefined') return
  try {
    window.sessionStorage?.setItem(
      SESSION_KEY,
      JSON.stringify({
        firstName: form.firstName.trim(),
        level: form.level,
        formLocation: location,
        ts: Date.now()
      })
    )
  } catch (_) {}
}

async function handleSubmit(location, form, submittingRef, errorRef, successRef) {
  if (submittingRef.value) return

  if (form.website && form.website.trim() !== '') {
    // Honeypot : on simule un succès silencieux, sans redirection ni stockage.
    successRef.value = true
    return
  }

  const validationError = validateForm(form)
  if (validationError) {
    errorRef.value = validationError
    return
  }

  errorRef.value = ''
  submittingRef.value = true

  const payload = {
    firstName: form.firstName.trim(),
    email: form.email.trim(),
    level: form.level,
    difficulty: form.difficulty,
    consentEmailMarketing: Boolean(form.consent),
    formLocation: location,
    leadMagnet: 'diagnostic_maths',
    consentTimestamp: new Date().toISOString(),
    context: getUtmContext()
  }

  try {
    await submitDiagnosticLead(payload)
    trackLeadSubmitted({
      location,
      level: form.level,
      difficulty: form.difficulty,
      consent: form.consent
    })
    storeLeadContextForThankYou(form, location)
    router.push({ name: 'DiagnosticMerci', query: { from: location } })
  } catch (err) {
    console.error('Diagnostic lead submission failed', err)
    errorRef.value = 'Une erreur est survenue. Réessaie dans quelques secondes ou écris-nous à contact@optitab.net.'
    submittingRef.value = false
    return
  }

  submittingRef.value = false
}

function handleHeroSubmit() {
  return handleSubmit('hero', formHero, submittingHero, errorHero, successHero)
}
function handleMainSubmit() {
  return handleSubmit('main', formMain, submittingMain, errorMain, successMain)
}
function handleFinalSubmit() {
  return handleSubmit('final', formFinal, submittingFinal, errorFinal, successFinal)
}

function scrollToMainForm() {
  if (typeof document === 'undefined') return
  const node = document.getElementById('diagnostic-form')
  if (!node) return
  node.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

let mainFormObserver = null
let finalFormObserver = null

function observeFormVisibility(elementId, location) {
  if (typeof window === 'undefined' || typeof IntersectionObserver === 'undefined') return null
  const node = document.getElementById(elementId)
  if (!node) return null
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        trackFormView(location)
        observer.disconnect()
      }
    })
  }, { threshold: 0.4 })
  observer.observe(node)
  return observer
}

onMounted(() => {
  setPageSeo({
    title: 'Diagnostic maths gratuit : comprends pourquoi tu bloques | OptiTAB',
    description: 'Réponds à 6 questions et reçois ton diagnostic personnalisé en maths : tes priorités, tes erreurs, et un plan clair pour progresser. Gratuit, 2 minutes.',
    canonicalPath: '/diagnostic-maths-gratuit',
    robots: getRobotsForRoute({ route }),
    ogType: 'website'
  })

  trackFormView('hero')
  pushDataLayerEvent('diagnostic_landing_viewed', { landing_path: '/diagnostic-maths-gratuit' })

  mainFormObserver = observeFormVisibility('diagnostic-form', 'main')
  finalFormObserver = observeFormVisibility('diagnostic-final-form', 'final')
})

onUnmounted(() => {
  try { mainFormObserver?.disconnect() } catch (_) {}
  try { finalFormObserver?.disconnect() } catch (_) {}
})

const heroTrustChips = ['100 % gratuit', '2 minutes chrono', 'Sans carte bancaire']
const finalTrustChips = ['Gratuit', '2 min chrono', 'Sans carte bancaire']
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <div class="diagnostic-landing">
      <div class="landing-shell">

        <!-- HERO -->
        <section class="block hero-block">
          <div class="hero-copy">
            <p class="hero-kicker">OptiTAB — Diagnostic gratuit</p>
            <h1>Comprends enfin pourquoi tu bloques en maths.</h1>
            <p class="hero-subtitle">
              Réponds à 6 questions, reçois ton diagnostic personnalisé et ton plan pour progresser au lycée.
            </p>
            <p class="hero-result">
              Tu sauras exactement quoi travailler, dans quel ordre, et comment t'y prendre — en 2 minutes.
            </p>

            <form
              v-if="!successHero"
              class="hero-form"
              novalidate
              @submit.prevent="handleHeroSubmit"
            >
              <input
                v-show="false"
                v-model="formHero.website"
                type="text"
                name="website"
                tabindex="-1"
                autocomplete="off"
                aria-hidden="true"
              />

              <div class="field">
                <label for="hero-firstName" class="field-label">Prénom</label>
                <input
                  id="hero-firstName"
                  v-model="formHero.firstName"
                  type="text"
                  name="firstName"
                  autocomplete="given-name"
                  placeholder="Ton prénom"
                  maxlength="50"
                  required
                  aria-required="true"
                />
              </div>

              <div class="field">
                <label for="hero-email" class="field-label">Email</label>
                <input
                  id="hero-email"
                  v-model="formHero.email"
                  type="email"
                  name="email"
                  inputmode="email"
                  autocomplete="email"
                  placeholder="ton.email@exemple.fr"
                  maxlength="150"
                  required
                  aria-required="true"
                />
              </div>

              <div class="field">
                <label for="hero-level" class="field-label">Ton niveau</label>
                <select
                  id="hero-level"
                  v-model="formHero.level"
                  name="level"
                  required
                  aria-required="true"
                  @change="trackLevelSelected('hero', formHero.level)"
                >
                  <option
                    v-for="option in LEVEL_OPTIONS"
                    :key="`hero-${option.value}`"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>

              <button
                type="submit"
                class="cta-primary"
                data-cta-name="signup"
                data-cta-location="diagnostic_hero"
                :disabled="submittingHero"
              >
                {{ submittingHero ? 'Envoi…' : 'Recevoir mon diagnostic gratuit →' }}
              </button>

              <p v-if="errorHero" class="form-error" role="alert">{{ errorHero }}</p>

              <p class="hero-form-hint">
                Tu choisis ta principale difficulté après inscription.
              </p>
            </form>

            <div v-else class="form-success" role="status" aria-live="polite">
              <p class="form-success-title">✓ Diagnostic envoyé !</p>
              <p class="form-success-text">
                Vérifie ta boîte mail (et le dossier spam au cas où). Tu peux déjà découvrir un aperçu de la plateforme.
              </p>
              <a class="form-success-link" href="/plateforme-maths">Découvrir OptiTAB →</a>
            </div>

            <div class="trust-row">
              <span v-for="item in heroTrustChips" :key="item" class="trust-chip">{{ item }}</span>
            </div>
          </div>

          <aside class="hero-side" aria-hidden="true">
            <div class="diagnostic-mockup">
              <p class="mockup-header">📋 Ton diagnostic OptiTAB</p>
              <p class="mockup-level">Niveau : Terminale</p>
              <div class="mockup-block">
                <p class="mockup-block-label">🎯 Priorité n°1</p>
                <p class="mockup-block-text">Méthode de résolution d'équations</p>
              </div>
              <div class="mockup-block">
                <p class="mockup-block-label">⚠️ 2 erreurs typiques à corriger</p>
                <p class="mockup-block-text">Calcul de dérivée · Lecture d'énoncé</p>
              </div>
              <div class="mockup-block mockup-block--accent">
                <p class="mockup-block-label">📅 Plan 7 jours</p>
                <p class="mockup-block-text">Programme personnalisé jour par jour</p>
              </div>
              <p class="mockup-footer">Reçu par email · PDF · Gratuit</p>
            </div>
          </aside>
        </section>

        <!-- LEAD MAGNET -->
        <section class="block lead-magnet-block">
          <div class="section-head">
            <h2>Voilà ce que tu reçois immédiatement après inscription</h2>
            <p>Un diagnostic complet, conçu pour comprendre où ça coince et comment débloquer la situation.</p>
          </div>
          <div class="lead-magnet-grid">
            <article v-for="item in leadMagnetItems" :key="item.title" class="lead-magnet-card">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </section>

        <!-- PROBLÈMES -->
        <section class="block pains-block">
          <div class="section-head">
            <h2>Reconnais-tu un de ces blocages ?</h2>
            <p>Si oui, tu n'es pas seul·e. Et surtout : ça se règle avec la bonne méthode.</p>
          </div>
          <div class="pains-grid">
            <article v-for="(quote, idx) in painPoints" :key="`pain-${idx}`" class="pain-card">
              <span class="pain-quote-mark" aria-hidden="true">“</span>
              <p>{{ quote }}</p>
            </article>
          </div>
        </section>

        <!-- SOLUTION -->
        <section class="block solution-block">
          <div class="section-head">
            <h2>La méthode OptiTAB pour débloquer la situation</h2>
            <p>Une plateforme pensée pour comprendre, retenir et progresser, sans dépendre des cours particuliers.</p>
          </div>
          <div class="solution-grid">
            <article v-for="item in solutionCards" :key="item.title" class="solution-card">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </section>

        <!-- APERÇU -->
        <section class="block preview-block">
          <div class="section-head">
            <h2>Aperçu : voilà à quoi ressemble OptiTAB</h2>
            <p>Un aperçu honnête de ce que tu auras dans ton diagnostic et sur la plateforme.</p>
          </div>
          <div class="preview-media">
            <article class="preview-media-card">
              <p class="preview-media-label">Version desktop</p>
              <img
                src="/video/optitab-demo-exercices.gif"
                alt="Aperçu desktop d'un exercice corrigé pas à pas sur OptiTAB"
                loading="lazy"
              />
            </article>
            <article class="preview-media-card preview-media-card--mobile">
              <p class="preview-media-label">Version mobile</p>
              <img
                src="/video/optitab-demo-mobile.gif"
                alt="Aperçu mobile de la plateforme OptiTAB"
                loading="lazy"
              />
            </article>
          </div>
          <p class="preview-hook">Tu vois la méthode, tu sais comment t'y prendre.</p>
        </section>

        <!-- FORMULAIRE PRINCIPAL -->
        <section id="diagnostic-form" class="block form-block">
          <div class="section-head">
            <h2>Reçois ton diagnostic gratuit</h2>
            <p>4 informations, 2 minutes. Tu reçois ton diagnostic par email immédiatement.</p>
          </div>

          <form
            v-if="!successMain"
            class="full-form"
            novalidate
            @submit.prevent="handleMainSubmit"
          >
            <input
              v-show="false"
              v-model="formMain.website"
              type="text"
              name="website"
              tabindex="-1"
              autocomplete="off"
              aria-hidden="true"
            />

            <div class="field-grid">
              <div class="field">
                <label for="main-firstName" class="field-label">Prénom</label>
                <input
                  id="main-firstName"
                  v-model="formMain.firstName"
                  type="text"
                  name="firstName"
                  autocomplete="given-name"
                  placeholder="Ton prénom"
                  maxlength="50"
                  required
                  aria-required="true"
                />
              </div>

              <div class="field">
                <label for="main-email" class="field-label">Email</label>
                <input
                  id="main-email"
                  v-model="formMain.email"
                  type="email"
                  name="email"
                  inputmode="email"
                  autocomplete="email"
                  placeholder="ton.email@exemple.fr"
                  maxlength="150"
                  required
                  aria-required="true"
                />
              </div>

              <div class="field">
                <label for="main-level" class="field-label">Ton niveau</label>
                <select
                  id="main-level"
                  v-model="formMain.level"
                  name="level"
                  required
                  aria-required="true"
                  @change="trackLevelSelected('main', formMain.level)"
                >
                  <option
                    v-for="option in LEVEL_OPTIONS"
                    :key="`main-${option.value}`"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label for="main-difficulty" class="field-label">Ta principale difficulté</label>
                <select
                  id="main-difficulty"
                  v-model="formMain.difficulty"
                  name="difficulty"
                  required
                  aria-required="true"
                  @change="trackDifficultySelected('main', formMain.difficulty)"
                >
                  <option
                    v-for="option in DIFFICULTY_OPTIONS"
                    :key="`main-${option.value}`"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>
            </div>

            <p v-if="formMain.level === 'college'" class="field-note">
              Si tu as moins de 15 ans, demande l'accord de tes parents avant de t'inscrire.
            </p>

            <label class="consent">
              <input
                v-model="formMain.consent"
                type="checkbox"
                name="consent"
              />
              <span>
                J'accepte de recevoir par email les conseils maths, ressources et offres d'OptiTAB.
                Je peux me désinscrire à tout moment en un clic.
              </span>
            </label>

            <p class="privacy-note">
              🔒 Les données collectées (prénom, email, niveau, difficulté) sont utilisées uniquement pour vous envoyer votre diagnostic et,
              si vous y consentez, des conseils OptiTAB. Elles ne sont jamais revendues. Conformément au RGPD,
              vous disposez d'un droit d'accès, de rectification, d'opposition et de suppression que vous pouvez exercer en écrivant à
              <a href="mailto:contact@optitab.net">contact@optitab.net</a>.
              Pour en savoir plus, consultez notre <a href="/confidentialite">politique de confidentialité</a>.
            </p>

            <button
              type="submit"
              class="cta-primary cta-primary--wide"
              data-cta-name="signup"
              data-cta-location="diagnostic_main"
              :disabled="submittingMain"
            >
              {{ submittingMain ? 'Envoi…' : 'Envoyer mon diagnostic →' }}
            </button>

            <p v-if="errorMain" class="form-error" role="alert">{{ errorMain }}</p>
            <p class="form-hint">Tu reçois ton diagnostic en moins d'1 minute dans ta boîte mail.</p>
          </form>

          <div v-else class="form-success form-success--large" role="status" aria-live="polite">
            <p class="form-success-title">✓ Diagnostic envoyé !</p>
            <p class="form-success-text">
              Vérifie ta boîte mail (et le dossier spam au cas où). Tu peux déjà découvrir un aperçu de la plateforme.
            </p>
            <a class="form-success-link" href="/plateforme-maths">Découvrir OptiTAB →</a>
          </div>
        </section>

        <!-- TRUST -->
        <section class="block trust-block">
          <div class="section-head">
            <h2>Pourquoi des élèves choisissent OptiTAB</h2>
            <p>Des éléments concrets et vérifiables, pas des promesses.</p>
          </div>
          <div class="trust-grid">
            <article v-for="item in trustItems" :key="item.title" class="trust-card">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </section>

        <!-- COMPARAISON -->
        <section class="block comparison-block">
          <div class="section-head">
            <h2>OptiTAB vs les autres solutions</h2>
            <p>Un comparatif honnête pour t'aider à choisir ce qui te convient.</p>
          </div>
          <div class="comparison-table-wrapper">
            <table class="comparison-table">
              <thead>
                <tr>
                  <th scope="col"></th>
                  <th scope="col">Vidéos YouTube</th>
                  <th scope="col">Cours particuliers</th>
                  <th scope="col" class="comparison-th--highlight">OptiTAB</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in comparisonRows" :key="row.criterion">
                  <th scope="row">{{ row.criterion }}</th>
                  <td>{{ row.youtube }}</td>
                  <td>{{ row.tutor }}</td>
                  <td class="comparison-td--highlight">{{ row.optitab }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="comparison-note">
            Les cours particuliers gardent leur valeur. OptiTAB est un complément structuré,
            à un prix qui rend l'aide aux maths accessible à toutes les familles.
          </p>
        </section>

        <!-- FAQ -->
        <section class="block faq-block">
          <FaqSection
            :faq="faqItems"
            title-prefix="Questions"
            title-highlight="fréquentes"
            description="On répond aux questions qu'on nous pose le plus avant l'inscription."
          />
        </section>

        <!-- CTA FINAL -->
        <section id="diagnostic-final-form" class="block final-cta-block">
          <h2>Prêt·e à savoir exactement quoi travailler ?</h2>
          <p class="final-cta-sub">
            Reçois ton diagnostic personnalisé en moins de 2 minutes. Gratuit, sans engagement.
          </p>

          <div class="trust-row trust-row--center">
            <span v-for="item in finalTrustChips" :key="`final-${item}`" class="trust-chip">{{ item }}</span>
          </div>

          <form
            v-if="!successFinal"
            class="full-form full-form--centered"
            novalidate
            @submit.prevent="handleFinalSubmit"
          >
            <input
              v-show="false"
              v-model="formFinal.website"
              type="text"
              name="website"
              tabindex="-1"
              autocomplete="off"
              aria-hidden="true"
            />

            <div class="field-grid">
              <div class="field">
                <label for="final-firstName" class="field-label">Prénom</label>
                <input
                  id="final-firstName"
                  v-model="formFinal.firstName"
                  type="text"
                  autocomplete="given-name"
                  placeholder="Ton prénom"
                  maxlength="50"
                  required
                />
              </div>

              <div class="field">
                <label for="final-email" class="field-label">Email</label>
                <input
                  id="final-email"
                  v-model="formFinal.email"
                  type="email"
                  inputmode="email"
                  autocomplete="email"
                  placeholder="ton.email@exemple.fr"
                  maxlength="150"
                  required
                />
              </div>

              <div class="field">
                <label for="final-level" class="field-label">Ton niveau</label>
                <select
                  id="final-level"
                  v-model="formFinal.level"
                  required
                  @change="trackLevelSelected('final', formFinal.level)"
                >
                  <option
                    v-for="option in LEVEL_OPTIONS"
                    :key="`final-${option.value}`"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label for="final-difficulty" class="field-label">Ta principale difficulté</label>
                <select
                  id="final-difficulty"
                  v-model="formFinal.difficulty"
                  required
                  @change="trackDifficultySelected('final', formFinal.difficulty)"
                >
                  <option
                    v-for="option in DIFFICULTY_OPTIONS"
                    :key="`final-${option.value}`"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>
            </div>

            <label class="consent">
              <input v-model="formFinal.consent" type="checkbox" />
              <span>
                J'accepte de recevoir par email les conseils maths, ressources et offres d'OptiTAB.
                Je peux me désinscrire à tout moment.
              </span>
            </label>

            <button
              type="submit"
              class="cta-primary cta-primary--wide"
              data-cta-name="signup"
              data-cta-location="diagnostic_final"
              :disabled="submittingFinal"
            >
              {{ submittingFinal ? 'Envoi…' : 'Recevoir mon diagnostic gratuit →' }}
            </button>

            <p v-if="errorFinal" class="form-error" role="alert">{{ errorFinal }}</p>
            <p class="privacy-note privacy-note--center">
              🔒 Vos données restent confidentielles et ne seront jamais revendues.
              <a href="/confidentialite">Politique de confidentialité</a>.
            </p>
          </form>

          <div v-else class="form-success form-success--large" role="status" aria-live="polite">
            <p class="form-success-title">✓ Diagnostic envoyé !</p>
            <p class="form-success-text">À tout de suite dans ta boîte mail.</p>
            <a class="form-success-link" href="/plateforme-maths">Découvrir OptiTAB →</a>
          </div>

          <p class="final-cta-quote">
            « Enfin, je sais exactement quoi faire pour progresser en maths. »
          </p>
        </section>

      </div>

      <!-- Sticky CTA mobile -->
      <button
        type="button"
        class="sticky-mobile-cta"
        data-cta-name="signup"
        data-cta-location="diagnostic_sticky_mobile"
        @click="scrollToMainForm"
      >
        Recevoir mon diagnostic gratuit
      </button>
    </div>

    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur le diagnostic OptiTAB."
      tooltip="Une question ? WhatsApp"
    />
  </MainLayout>
</template>

<style scoped lang="scss">
.diagnostic-landing {
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

/* ===== HERO ===== */
.hero-block {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(0, 0.7fr);
  gap: 26px;
  align-items: start;
}

.hero-copy { max-width: 820px; }

.hero-kicker {
  margin: 0;
  color: #2a38b7;
  font-size: 0.82rem;
  letter-spacing: 0.02em;
  font-weight: 800;
  text-transform: uppercase;
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
  margin: 12px 0 0;
  color: #475569;
  font-size: 0.96rem;
  line-height: 1.45;
}

.hero-form {
  margin-top: 22px;
  display: grid;
  gap: 12px;
  max-width: 520px;
}

.hero-form-hint {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 0.82rem;
}

/* ===== HERO SIDE / MOCKUP ===== */
.hero-side {
  justify-self: end;
  width: 100%;
  max-width: 360px;
}

.diagnostic-mockup {
  background: linear-gradient(145deg, #ffffff 0%, #f1f5ff 100%);
  border: 1px solid #d7e2ff;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 24px 60px rgba(30, 58, 138, 0.16);
  display: grid;
  gap: 10px;
  transform: rotate(-1.5deg);
}

.mockup-header {
  margin: 0;
  font-weight: 800;
  color: #1e3a8a;
  font-size: 1rem;
}

.mockup-level {
  margin: 0;
  color: #475569;
  font-size: 0.85rem;
  font-weight: 600;
}

.mockup-block {
  border-radius: 10px;
  border: 1px solid #dbe6ff;
  background: #ffffff;
  padding: 10px 12px;
  display: grid;
  gap: 3px;
}

.mockup-block--accent {
  background: linear-gradient(135deg, #eef4ff 0%, #e1ecff 100%);
  border-color: #b9cbff;
}

.mockup-block-label {
  margin: 0;
  font-size: 0.78rem;
  font-weight: 800;
  color: #2a38b7;
}

.mockup-block-text {
  margin: 0;
  color: #1e293b;
  font-size: 0.84rem;
  font-weight: 600;
}

.mockup-footer {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 0.74rem;
  text-align: center;
  font-weight: 700;
}

/* ===== FIELDS ===== */
.field {
  display: grid;
  gap: 6px;
}

.field-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #1e293b;
}

.field input,
.field select {
  width: 100%;
  min-height: 48px;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 0 12px;
  font-size: 0.96rem;
  color: #0f172a;
  background: #ffffff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.field select {
  appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, #475569 50%),
                    linear-gradient(135deg, #475569 50%, transparent 50%);
  background-position: calc(100% - 18px) 50%, calc(100% - 13px) 50%;
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
  padding-right: 32px;
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: #6d8dff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18);
}

.field-note {
  margin: 4px 0 0;
  font-size: 0.84rem;
  color: #64748b;
}

/* ===== CTA ===== */
.cta-primary {
  margin-top: 6px;
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

.cta-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
}

.cta-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.cta-primary--wide { width: 100%; }

/* ===== TRUST CHIPS ===== */
.trust-row {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.trust-row--center {
  justify-content: center;
  margin-top: 14px;
}

.trust-chip {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: 0 12px;
  border-radius: 999px;
  background: #eef4ff;
  border: 1px solid #cfe0ff;
  color: #1e3a8a;
  font-size: 0.82rem;
  font-weight: 700;
}

/* ===== SECTION HEAD ===== */
.section-head { margin-bottom: 18px; }

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

/* ===== LEAD MAGNET ===== */
.lead-magnet-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.lead-magnet-card {
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: linear-gradient(140deg, #ffffff 0%, #f5f8ff 100%);
  padding: 16px;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}

.lead-magnet-card:hover {
  transform: translateY(-2px);
  border-color: #a8c1ff;
  box-shadow: 0 10px 24px rgba(30, 58, 138, 0.1);
}

.lead-magnet-card h3 {
  margin: 0 0 6px;
  font-size: 1rem;
  color: #0f172a;
}

.lead-magnet-card p {
  margin: 0;
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.45;
}

/* ===== PAINS ===== */
.pains-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.pain-card {
  position: relative;
  border-radius: 14px;
  border: 1px solid #dbe6ff;
  background: #f8fbff;
  border-left: 4px solid #2a38b7;
  padding: 16px 16px 16px 20px;
}

.pain-card p {
  margin: 0;
  color: #1e293b;
  font-size: 0.96rem;
  font-style: italic;
  line-height: 1.5;
}

.pain-quote-mark {
  position: absolute;
  top: 4px;
  left: 10px;
  color: #2a38b7;
  font-size: 1.4rem;
  font-weight: 800;
  opacity: 0.4;
}

/* ===== SOLUTION ===== */
.solution-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.solution-card {
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: linear-gradient(140deg, #ffffff 0%, #f5f8ff 100%);
  padding: 18px;
}

.solution-card h3 {
  margin: 0 0 8px;
  color: #0f172a;
  font-size: 1.04rem;
}

.solution-card p {
  margin: 0;
  color: #475569;
  font-size: 0.92rem;
  line-height: 1.5;
}

/* ===== PREVIEW ===== */
.preview-media {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 14px;
  margin-bottom: 14px;
}

.preview-media-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview-media-label {
  margin: 0 0 10px;
  color: #1e3a8a;
  font-size: 0.9rem;
  font-weight: 800;
  text-align: center;
}

.preview-media-card img {
  width: 100%;
  border-radius: 14px;
  display: block;
}

.preview-media-card--mobile img {
  max-width: 300px;
  margin: 0 auto;
}

.preview-media-card--mobile .preview-media-label {
  max-width: 300px;
  margin: 0 auto 10px;
}

.preview-hook {
  margin: 14px 0 0;
  color: #1e3a8a;
  font-size: 0.95rem;
  font-weight: 700;
  text-align: center;
}

/* ===== FORM BLOCK ===== */
.form-block {
  background: linear-gradient(145deg, #ffffff 0%, #eef2ff 100%);
  border-radius: 20px;
  padding: 28px 22px;
}

.form-block + .block { border-top-color: transparent; }

.full-form {
  display: grid;
  gap: 16px;
  max-width: 760px;
  margin: 0 auto;
}

.full-form--centered { margin: 18px auto 0; }

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.consent {
  display: grid;
  grid-template-columns: 22px 1fr;
  gap: 10px;
  align-items: start;
  font-size: 0.9rem;
  color: #1e293b;
  line-height: 1.5;
  cursor: pointer;
}

.consent input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin: 2px 0 0;
  accent-color: #2155d8;
  cursor: pointer;
}

.privacy-note {
  margin: 0;
  font-size: 0.82rem;
  color: #475569;
  line-height: 1.5;
}

.privacy-note a {
  color: #1e3a8a;
  font-weight: 700;
  text-decoration: underline;
}

.privacy-note--center { text-align: center; }

.form-error {
  margin: 0;
  padding: 10px 12px;
  border-radius: 10px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 0.9rem;
  font-weight: 700;
  border: 1px solid #fecaca;
}

.form-hint {
  margin: 0;
  color: #475569;
  font-size: 0.85rem;
  text-align: center;
}

/* ===== SUCCESS ===== */
.form-success {
  border-radius: 14px;
  border: 1px solid #bbf7d0;
  background: linear-gradient(140deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 18px 20px;
  display: grid;
  gap: 6px;
}

.form-success--large {
  padding: 24px;
  text-align: center;
  max-width: 520px;
  margin: 18px auto 0;
}

.form-success-title {
  margin: 0;
  font-size: 1.04rem;
  font-weight: 800;
  color: #065f46;
}

.form-success-text {
  margin: 0;
  color: #134e4a;
  font-size: 0.92rem;
}

.form-success-link {
  margin-top: 4px;
  color: #065f46;
  font-weight: 800;
  text-decoration: underline;
}

/* ===== TRUST CARDS ===== */
.trust-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
}

.trust-card {
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: #ffffff;
  padding: 14px;
}

.trust-card h3 {
  margin: 0 0 6px;
  color: #1e3a8a;
  font-size: 0.92rem;
  font-weight: 800;
}

.trust-card p {
  margin: 0;
  color: #475569;
  font-size: 0.84rem;
  line-height: 1.45;
}

/* ===== COMPARISON ===== */
.comparison-table-wrapper {
  overflow-x: auto;
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: #ffffff;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.comparison-table th,
.comparison-table td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid #eef2ff;
  color: #1e293b;
}

.comparison-table thead th {
  background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
  color: #1e3a8a;
  font-weight: 800;
  font-size: 0.88rem;
}

.comparison-table tbody th {
  color: #0f172a;
  font-weight: 700;
  background: #f8fafc;
}

.comparison-th--highlight {
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%) !important;
  color: #ffffff !important;
}

.comparison-td--highlight {
  background: #eef4ff;
  color: #1e3a8a;
  font-weight: 700;
}

.comparison-table tbody tr:last-child th,
.comparison-table tbody tr:last-child td {
  border-bottom: none;
}

.comparison-note {
  margin: 14px 0 0;
  color: #475569;
  font-size: 0.88rem;
  font-style: italic;
}

/* ===== FAQ BLOCK ===== */
.faq-block { padding-top: 16px; }
.faq-block :deep(.faq-section) {
  margin: 0 auto;
  padding-top: 16px;
}

/* ===== FINAL CTA ===== */
.final-cta-block {
  text-align: center;
  background: linear-gradient(145deg, #ffffff 0%, #eef2ff 100%);
  border-radius: 20px;
  padding: 34px 22px;
}

.final-cta-block h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.45rem, 2.6vw, 2rem);
}

.final-cta-sub {
  margin: 10px 0 0;
  color: #475569;
}

.final-cta-quote {
  margin: 18px 0 0;
  font-style: italic;
  color: #1e3a8a;
  font-size: 0.95rem;
  font-weight: 700;
}

/* ===== STICKY MOBILE CTA ===== */
.sticky-mobile-cta {
  display: none;
  position: fixed;
  bottom: 16px;
  left: 16px;
  right: 16px;
  z-index: 50;
  min-height: 52px;
  border: 1px solid #1f4ed2;
  border-radius: 14px;
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 14px 30px rgba(37, 99, 235, 0.35);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 960px) {
  .hero-block {
    grid-template-columns: 1fr;
  }
  .hero-side {
    display: none;
  }
  .lead-magnet-grid,
  .solution-grid,
  .pains-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .trust-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .preview-media {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .landing-shell {
    padding: 18px 12px 96px;
  }
  .block {
    padding: 26px 0;
  }
  .form-block,
  .final-cta-block {
    padding: 22px 16px;
    border-radius: 16px;
  }
  .lead-magnet-grid,
  .solution-grid,
  .pains-grid,
  .field-grid {
    grid-template-columns: 1fr;
  }
  .trust-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .cta-primary { width: 100%; }
  .sticky-mobile-cta { display: block; }
  .full-form { gap: 14px; }
  .pain-quote-mark { display: none; }
  .pain-card { padding-left: 16px; }
}
</style>
