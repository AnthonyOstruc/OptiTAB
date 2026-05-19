<script setup>
import { onMounted, reactive, ref } from 'vue'
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
  { value: 'motivation', label: 'Je manque de motivation / je me décourage' },
  { value: 'autre', label: 'Autre — je précise ci-dessous' }
]

const leadMagnetItems = [
  {
    title: 'Ton diagnostic personnalisé',
    text: 'On identifie précisément où tu bloques : cours, méthode, ou exercices.'
  },
  {
    title: 'Ton plan 7 jours',
    text: 'Une feuille de route concrète, jour par jour, adaptée à ton niveau.'
  },
  {
    title: 'La méthode à appliquer',
    text: 'Comment t\'y prendre pour débloquer durablement, sans cours particuliers.'
  }
]

const trustItems = [
  { label: 'Programme officiel', detail: 'Aligné Éducation nationale, collège & lycée.' },
  { label: 'Pas à pas', detail: 'Méthode expliquée, sans sauter d\'étapes.' },
  { label: 'Sans engagement', detail: 'Diagnostic 100 % gratuit, sans carte bancaire.' }
]

const faqItems = [
  {
    question: 'Le diagnostic est-il vraiment gratuit ?',
    answer: 'Oui, 100 % gratuit. Aucune carte bancaire, aucun engagement. Tu reçois le diagnostic par email dès que tu valides le formulaire.'
  },
  {
    question: 'Que vais-je recevoir exactement ?',
    answer: 'Un diagnostic personnalisé selon ton niveau et ta difficulté, un plan 7 jours, et la méthode à appliquer pour débloquer durablement.'
  },
  {
    question: 'Est-ce adapté à mon niveau ?',
    answer: 'Oui. Le diagnostic et les conseils sont adaptés au collège, à la Seconde, la Première, la Terminale, la prépa et le BTS.'
  },
  {
    question: 'Puis-je me désinscrire ?',
    answer: 'Oui, en un clic depuis n\'importe quel email. Pas de justification à fournir.'
  }
]

function createInitialForm() {
  return {
    firstName: '',
    email: '',
    level: '',
    difficulty: '',
    difficultyOther: '',
    consent: false,
    website: ''
  }
}

const formHero = reactive(createInitialForm())
const submittingHero = ref(false)
const errorHero = ref('')
const successHero = ref(false)
const formViewed = reactive({ hero: false })

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
  if (form.difficulty === 'autre' && !String(form.difficultyOther || '').trim()) {
    return 'Précise ta difficulté en quelques mots.'
  }
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
    difficultyOther: String(form.difficultyOther || '').trim().slice(0, 1000),
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

function scrollToHeroForm() {
  if (typeof document === 'undefined') return
  const node = document.getElementById('hero-firstName')
  if (!node) return
  node.scrollIntoView({ behavior: 'smooth', block: 'center' })
  setTimeout(() => {
    try { node.focus({ preventScroll: true }) } catch (_) {}
  }, 600)
}

onMounted(() => {
  setPageSeo({
    title: 'Diagnostic maths gratuit : comprends pourquoi tu bloques | OptiTAB',
    description: 'Réponds à 4 questions et reçois ton diagnostic personnalisé en maths : tes priorités, un plan 7 jours, la méthode à appliquer. Gratuit, 2 minutes.',
    canonicalPath: '/diagnostic-maths-gratuit',
    robots: getRobotsForRoute({ route }),
    ogType: 'website'
  })

  trackFormView('hero')
  pushDataLayerEvent('diagnostic_landing_viewed', { landing_path: '/diagnostic-maths-gratuit' })
})

const heroTrustChips = ['100 % gratuit', '2 minutes chrono', 'Sans carte bancaire']
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <div class="diagnostic-landing">
      <div class="landing-shell">

        <!-- HERO -->
        <section class="block hero-block">
          <div class="hero-copy">
            <p class="hero-kicker">Diagnostic gratuit</p>
            <h1>Identifie ce qui freine ta progression en maths.</h1>
            <p class="hero-subtitle">
              Réponds à 4 questions. Reçois ton diagnostic personnalisé et un plan clair pour progresser.
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

              <div class="field">
                <label for="hero-difficulty" class="field-label">Ta principale difficulté</label>
                <select
                  id="hero-difficulty"
                  v-model="formHero.difficulty"
                  name="difficulty"
                  required
                  aria-required="true"
                  @change="trackDifficultySelected('hero', formHero.difficulty)"
                >
                  <option
                    v-for="option in DIFFICULTY_OPTIONS"
                    :key="`hero-${option.value}`"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label for="hero-difficulty-other" class="field-label">
                  {{ formHero.difficulty === 'autre'
                    ? 'Précise ta difficulté'
                    : 'Tu veux ajouter un détail ?' }}
                  <span v-if="formHero.difficulty !== 'autre'" class="field-optional">(optionnel)</span>
                </label>
                <textarea
                  id="hero-difficulty-other"
                  v-model="formHero.difficultyOther"
                  name="difficultyOther"
                  rows="3"
                  maxlength="1000"
                  :placeholder="formHero.difficulty === 'autre'
                    ? 'Explique en quelques mots où tu (ou ton enfant) bloques le plus.'
                    : 'Donne-nous plus de contexte si tu le souhaites — sinon laisse vide.'"
                  :required="formHero.difficulty === 'autre'"
                  :aria-required="formHero.difficulty === 'autre' ? 'true' : 'false'"
                ></textarea>
              </div>

              <label class="consent">
                <input v-model="formHero.consent" type="checkbox" name="consent" />
                <span>
                  J'accepte de recevoir des conseils maths et ressources d'OptiTAB. Désinscription en un clic.
                </span>
              </label>

              <button
                type="submit"
                class="cta-primary"
                data-cta-name="signup"
                data-cta-location="diagnostic_hero"
                :disabled="submittingHero"
              >
                {{ submittingHero ? 'Envoi…' : 'Recevoir mon diagnostic gratuit' }}
              </button>

              <p v-if="errorHero" class="form-error" role="alert">{{ errorHero }}</p>

              <p class="hero-form-hint">
                Reçu par email en moins d'1 minute. Nous ne revendons jamais tes données.
              </p>
            </form>

            <div v-else class="form-success" role="status" aria-live="polite">
              <p class="form-success-title">✓ Diagnostic envoyé</p>
              <p class="form-success-text">
                Vérifie ta boîte mail (et les spams au cas où). Tu peux déjà découvrir un aperçu de la plateforme.
              </p>
              <a class="form-success-link" href="/plateforme-maths">Découvrir OptiTAB →</a>
            </div>

            <div class="trust-row">
              <span v-for="item in heroTrustChips" :key="item" class="trust-chip">{{ item }}</span>
            </div>
          </div>

          <aside class="hero-side" aria-hidden="true">
            <div class="diagnostic-mockup">
              <p class="mockup-header">Ton diagnostic OptiTAB</p>
              <p class="mockup-level">Niveau · Terminale</p>
              <div class="mockup-block">
                <p class="mockup-block-label">Priorité n°1</p>
                <p class="mockup-block-text">Méthode de résolution d'équations</p>
              </div>
              <div class="mockup-block">
                <p class="mockup-block-label">Erreurs à corriger</p>
                <p class="mockup-block-text">Calcul de dérivée · Lecture d'énoncé</p>
              </div>
              <div class="mockup-block mockup-block--accent">
                <p class="mockup-block-label">Plan 7 jours</p>
                <p class="mockup-block-text">Programme jour par jour</p>
              </div>
              <p class="mockup-footer">Reçu par email · PDF · Gratuit</p>
            </div>
          </aside>
        </section>

        <!-- VALEUR -->
        <section class="block value-block">
          <div class="section-head">
            <h2>Ce que tu reçois</h2>
          </div>
          <div class="value-grid">
            <article
              v-for="(item, idx) in leadMagnetItems"
              :key="item.title"
              class="value-card"
            >
              <span class="value-num">{{ String(idx + 1).padStart(2, '0') }}</span>
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </section>

        <!-- TRUST -->
        <section class="block trust-block">
          <ul class="trust-list">
            <li v-for="item in trustItems" :key="item.label">
              <span class="trust-check" aria-hidden="true">✓</span>
              <div>
                <p class="trust-label">{{ item.label }}</p>
                <p class="trust-detail">{{ item.detail }}</p>
              </div>
            </li>
          </ul>
        </section>

        <!-- FAQ -->
        <section class="block faq-block">
          <FaqSection
            :faq="faqItems"
            title-prefix="Questions"
            title-highlight="fréquentes"
            description=""
          />
        </section>

        <!-- FINAL CTA -->
        <section class="block final-cta-block">
          <h2>Prêt·e à savoir exactement quoi travailler ?</h2>
          <p class="final-cta-sub">
            Reçois ton diagnostic personnalisé. Gratuit, sans engagement, en moins de 2 minutes.
          </p>
          <button
            type="button"
            class="cta-primary cta-primary--inline"
            data-cta-name="signup"
            data-cta-location="diagnostic_final"
            @click="scrollToHeroForm"
          >
            Recevoir mon diagnostic gratuit
          </button>
        </section>

      </div>

      <!-- Sticky CTA mobile -->
      <button
        type="button"
        class="sticky-mobile-cta"
        data-cta-name="signup"
        data-cta-location="diagnostic_sticky_mobile"
        @click="scrollToHeroForm"
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
$ink-900: #0f172a;
$ink-700: #1e293b;
$ink-500: #475569;
$ink-400: #64748b;
$brand-900: #1e3a8a;
$brand-700: #2a38b7;
$brand-600: #2155d8;
$brand-500: #2f6df4;
$brand-50: #eef4ff;
$brand-25: #f5f8ff;
$line: #e6ecf5;
$line-strong: #d6e1ff;

.diagnostic-landing {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 35%, #f6f8ff 100%);
  min-height: 100%;
}

.landing-shell {
  max-width: 1080px;
  margin: 0 auto;
  padding: 48px 24px 96px;
  display: grid;
  gap: 0;
}

.block {
  padding: 56px 0;
}

.block + .block {
  border-top: 1px solid $line;
}

/* ===== SECTION HEAD ===== */
.section-head {
  margin-bottom: 28px;
  max-width: 640px;
}

.section-head h2 {
  margin: 0;
  color: $brand-900;
  font-size: clamp(1.6rem, 2.8vw, 2.1rem);
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1.15;
}

/* ===== HERO ===== */
.hero-block {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 0.75fr);
  gap: 48px;
  align-items: start;
  padding-top: 24px;
  padding-bottom: 64px;
  border-top: none;
}

.hero-copy { max-width: 560px; }

.hero-kicker {
  margin: 0 0 14px;
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: $brand-50;
  color: $brand-700;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
  font-weight: 800;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 2.85rem);
  line-height: 1.08;
  letter-spacing: -0.025em;
  color: $brand-900;
  font-weight: 800;
  text-wrap: balance;
}

.hero-subtitle {
  margin: 18px 0 0;
  color: $ink-500;
  font-size: 1.08rem;
  line-height: 1.5;
  max-width: 52ch;
}

.hero-form {
  margin-top: 28px;
  display: grid;
  gap: 14px;
  max-width: 480px;
}

.hero-form-hint {
  margin: 4px 0 0;
  color: $ink-400;
  font-size: 0.82rem;
  line-height: 1.5;
}

/* ===== HERO SIDE / MOCKUP ===== */
.hero-side {
  justify-self: end;
  width: 100%;
  max-width: 340px;
  position: sticky;
  top: 32px;
}

.diagnostic-mockup {
  background: linear-gradient(145deg, #ffffff 0%, $brand-25 100%);
  border: 1px solid $line-strong;
  border-radius: 16px;
  padding: 20px;
  box-shadow:
    0 1px 2px rgba(15, 23, 42, 0.04),
    0 18px 40px rgba(42, 56, 183, 0.12);
  display: grid;
  gap: 10px;
}

.mockup-header {
  margin: 0;
  font-weight: 800;
  color: $ink-900;
  font-size: 0.95rem;
}

.mockup-level {
  margin: 0 0 4px;
  color: $ink-400;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.mockup-block {
  border-radius: 10px;
  border: 1px solid $line;
  background: #fbfcfe;
  padding: 10px 12px;
  display: grid;
  gap: 3px;
}

.mockup-block--accent {
  background: $brand-50;
  border-color: $line-strong;
}

.mockup-block-label {
  margin: 0;
  font-size: 0.72rem;
  font-weight: 800;
  color: $brand-700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.mockup-block-text {
  margin: 0;
  color: $ink-700;
  font-size: 0.84rem;
  font-weight: 600;
}

.mockup-footer {
  margin: 4px 0 0;
  color: $ink-400;
  font-size: 0.72rem;
  text-align: center;
  font-weight: 600;
  letter-spacing: 0.02em;
}

/* ===== FIELDS ===== */
.field {
  display: grid;
  gap: 6px;
}

.field-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: $ink-700;
}

.field-optional {
  margin-left: 6px;
  font-size: 0.78rem;
  font-weight: 500;
  color: $ink-400;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  min-height: 48px;
  border: 1px solid #d4dbe6;
  border-radius: 10px;
  padding: 0 14px;
  font-size: 0.95rem;
  color: $ink-900;
  background: #ffffff;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  font-family: inherit;
}

.field textarea {
  min-height: 96px;
  padding: 12px 14px;
  line-height: 1.5;
  resize: vertical;
}

.field select {
  appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, #64748b 50%),
                    linear-gradient(135deg, #64748b 50%, transparent 50%);
  background-position: calc(100% - 18px) 50%, calc(100% - 13px) 50%;
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
  padding-right: 36px;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: $brand-600;
  box-shadow: 0 0 0 3px rgba(33, 85, 216, 0.15);
}

/* ===== CONSENT ===== */
.consent {
  display: grid;
  grid-template-columns: 20px 1fr;
  gap: 10px;
  align-items: start;
  font-size: 0.85rem;
  color: $ink-500;
  line-height: 1.5;
  cursor: pointer;
}

.consent input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin: 2px 0 0;
  accent-color: $brand-600;
  cursor: pointer;
}

/* ===== CTA ===== */
.cta-primary {
  margin-top: 4px;
  min-height: 52px;
  border: 1px solid $brand-700;
  border-radius: 12px;
  padding: 0 22px;
  background: linear-gradient(180deg, $brand-500 0%, $brand-600 100%);
  color: #ffffff;
  font-size: 0.98rem;
  font-weight: 700;
  letter-spacing: -0.005em;
  cursor: pointer;
  transition: box-shadow 0.18s ease, transform 0.1s ease, filter 0.15s ease;
  -webkit-tap-highlight-color: transparent;
  box-shadow: 0 1px 2px rgba(33, 85, 216, 0.18);
}

.cta-primary:hover:not(:disabled) {
  box-shadow: 0 10px 24px rgba(33, 85, 216, 0.28);
  filter: brightness(1.04);
}

.cta-primary:active:not(:disabled) {
  transform: translateY(1px);
  box-shadow: 0 4px 10px rgba(33, 85, 216, 0.22);
}

.cta-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cta-primary--inline {
  margin-top: 0;
  padding: 0 28px;
}

/* ===== TRUST CHIPS (hero) ===== */
.trust-row {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.trust-chip {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 12px;
  border-radius: 999px;
  background: transparent;
  border: 1px solid $line;
  color: $ink-500;
  font-size: 0.8rem;
  font-weight: 600;
}

/* ===== VALUE (Ce que tu reçois) ===== */
.value-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.value-card {
  display: grid;
  gap: 8px;
  padding: 0;
}

.value-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: $brand-50;
  color: $brand-700;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  margin-bottom: 4px;
  border: 1px solid $line-strong;
}

.value-card h3 {
  margin: 0;
  color: $ink-900;
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.3;
}

.value-card p {
  margin: 0;
  color: $ink-500;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* ===== TRUST ===== */
.trust-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.trust-list li {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 10px;
  align-items: start;
}

.trust-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(180deg, $brand-500 0%, $brand-600 100%);
  color: #ffffff;
  font-size: 0.78rem;
  font-weight: 800;
  margin-top: 2px;
  box-shadow: 0 2px 4px rgba(33, 85, 216, 0.25);
}

.trust-label {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: $ink-900;
}

.trust-detail {
  margin: 2px 0 0;
  font-size: 0.88rem;
  color: $ink-500;
  line-height: 1.5;
}

/* ===== FAQ ===== */
.faq-block {
  padding-top: 56px;
  padding-bottom: 56px;
}

.faq-block :deep(.faq-section) {
  margin: 0;
  padding: 0;
}

/* ===== FORM ERROR / SUCCESS ===== */
.form-error {
  margin: 0;
  padding: 10px 14px;
  border-radius: 10px;
  background: #fef2f2;
  color: #b42318;
  font-size: 0.88rem;
  font-weight: 600;
  border: 1px solid #fecdca;
}

.form-success {
  border-radius: 12px;
  border: 1px solid #a7f3d0;
  background: #f0fdf4;
  padding: 18px 20px;
  display: grid;
  gap: 6px;
}

.form-success-title {
  margin: 0;
  font-size: 1.02rem;
  font-weight: 800;
  color: #065f46;
}

.form-success-text {
  margin: 0;
  color: #134e4a;
  font-size: 0.9rem;
}

.form-success-link {
  margin-top: 6px;
  color: #065f46;
  font-weight: 700;
  text-decoration: underline;
}

/* ===== FINAL CTA ===== */
.final-cta-block {
  text-align: center;
  padding: 64px 0 32px;
  border-top: 1px solid $line;
}

.final-cta-block h2 {
  margin: 0;
  color: $brand-900;
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 800;
  letter-spacing: -0.015em;
  line-height: 1.2;
}

.final-cta-sub {
  margin: 14px 0 24px;
  color: $ink-500;
  font-size: 1rem;
  max-width: 480px;
  margin-left: auto;
  margin-right: auto;
}

/* ===== STICKY MOBILE CTA ===== */
.sticky-mobile-cta {
  display: none;
  position: fixed;
  bottom: calc(12px + env(safe-area-inset-bottom, 0px));
  left: 12px;
  right: 12px;
  z-index: 50;
  min-height: 54px;
  border: 1px solid $brand-700;
  border-radius: 12px;
  background: linear-gradient(180deg, $brand-500 0%, $brand-600 100%);
  color: #ffffff;
  font-size: 0.98rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 14px 30px rgba(33, 85, 216, 0.35);
  -webkit-tap-highlight-color: transparent;
}

.sticky-mobile-cta:active {
  transform: translateY(1px);
  filter: brightness(0.96);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 960px) {
  .hero-block {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  .hero-side {
    display: none;
  }
  .value-grid,
  .trust-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .landing-shell {
    padding: 32px 20px 88px;
  }
  .block {
    padding: 44px 0;
  }
  .hero-block {
    padding-top: 16px;
    padding-bottom: 48px;
  }
  .section-head { margin-bottom: 22px; }
  .section-head h2 {
    font-size: clamp(1.45rem, 5vw, 1.85rem);
  }
}

@media (max-width: 640px) {
  .landing-shell {
    padding: 24px 16px calc(96px + env(safe-area-inset-bottom, 0px));
  }
  .block { padding: 36px 0; }

  .hero-copy h1 {
    font-size: clamp(1.85rem, 7vw, 2.3rem);
  }
  .hero-subtitle { font-size: 1rem; }
  .hero-form { margin-top: 22px; gap: 12px; max-width: 100%; }

  .value-grid,
  .trust-list {
    grid-template-columns: 1fr;
    gap: 18px;
  }

  /* Inputs : 16px pour empêcher le zoom iOS */
  .field input,
  .field select,
  .field textarea {
    font-size: 16px;
    min-height: 50px;
  }
  .field textarea { min-height: 110px; }

  .cta-primary {
    width: 100%;
    min-height: 52px;
  }

  .sticky-mobile-cta { display: block; }

  .final-cta-block {
    padding: 44px 0 16px;
  }
  .final-cta-block h2 {
    font-size: clamp(1.4rem, 5.6vw, 1.7rem);
  }
  .final-cta-sub { font-size: 0.95rem; margin-bottom: 20px; }
}

@media (max-width: 400px) {
  .landing-shell {
    padding: 20px 14px calc(96px + env(safe-area-inset-bottom, 0px));
  }
  .block { padding: 32px 0; }
  .hero-copy h1 {
    font-size: clamp(1.7rem, 7.4vw, 2rem);
  }
  .trust-chip {
    font-size: 0.76rem;
    min-height: 26px;
    padding: 0 10px;
  }
  .sticky-mobile-cta {
    left: 10px;
    right: 10px;
    font-size: 0.94rem;
  }
}
</style>
