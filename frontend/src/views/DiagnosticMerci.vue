<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import { setPageSeo } from '@/services/seo'

const route = useRoute()
const router = useRouter()

const SESSION_KEY = 'optitab_diagnostic_lead'

function readSession() {
  if (typeof window === 'undefined') return {}
  try {
    const raw = window.sessionStorage?.getItem(SESSION_KEY)
    if (!raw) return {}
    const parsed = JSON.parse(raw)
    return parsed && typeof parsed === 'object' ? parsed : {}
  } catch (_) {
    return {}
  }
}

const leadContext = readSession()

const firstName = computed(() => {
  const fromQuery = (route.query.firstName || '').toString().trim()
  const fromSession = (leadContext.firstName || '').toString().trim()
  return fromQuery || fromSession || ''
})

const level = computed(() => leadContext.level || (route.query.level || '').toString())
const formLocation = computed(() => leadContext.formLocation || (route.query.from || '').toString())

const isDirectLanding = computed(() => !firstName.value)

const greeting = computed(() =>
  firstName.value ? `Merci ${firstName.value} !` : 'Merci pour ton inscription !'
)

const nextSteps = [
  {
    n: '01',
    title: 'Tu reçois ton diagnostic',
    text: 'Vérifie ta boîte mail dans les prochaines minutes (pense au dossier spam au cas où).'
  },
  {
    n: '02',
    title: 'Tu prends 10 minutes au calme',
    text: 'Lis ton diagnostic jusqu\'au bout. Il contient ton plan 7 jours et tes 3 priorités.'
  },
  {
    n: '03',
    title: 'Tu reçois 4 emails utiles',
    text: 'Sur 12 jours, un email court tous les 2 à 5 jours pour t\'aider à progresser concrètement.'
  }
]

const previewItems = [
  {
    title: '+150 cours clairs',
    text: 'Programme officiel collège et lycée, expliqué simplement.'
  },
  {
    title: '+150 fiches de synthèse',
    text: 'L\'essentiel à retenir, prêt à imprimer.'
  },
  {
    title: '+1000 exercices corrigés pas à pas',
    text: 'La méthode détaillée pour savoir comment faire seul·e ensuite.'
  }
]

function trackThankYouViewed() {
  if (typeof window === 'undefined') return
  try {
    if (!Array.isArray(window.dataLayer)) {
      window.dataLayer = []
    }
    window.dataLayer.push({
      event: 'diagnostic_lead_thank_you_viewed',
      form_location: formLocation.value || 'unknown',
      direct_landing: isDirectLanding.value
    })
  } catch (_) {}
}

function trackPlatformCta(location) {
  if (typeof window === 'undefined') return
  try {
    if (!Array.isArray(window.dataLayer)) {
      window.dataLayer = []
    }
    window.dataLayer.push({
      event: 'thank_you_cta_clicked',
      cta_location: location
    })
  } catch (_) {}
}

function clearLeadContext() {
  if (typeof window === 'undefined') return
  try {
    window.sessionStorage?.removeItem(SESSION_KEY)
  } catch (_) {}
}

onMounted(() => {
  setPageSeo({
    title: 'Diagnostic envoyé — Vérifie ta boîte mail | OptiTAB',
    description: 'Ton diagnostic personnalisé arrive dans ta boîte mail. Découvre la plateforme OptiTAB en attendant.',
    canonicalPath: '/diagnostic-merci',
    robots: 'noindex,nofollow',
    ogType: 'website'
  })

  trackThankYouViewed()

  // On efface le contexte session après affichage pour éviter qu'une nouvelle
  // visite directe à /diagnostic-merci ne réutilise un ancien firstName.
  setTimeout(clearLeadContext, 1500)
})
</script>

<template>
  <MainLayout header-variant="landing" footer-variant="landing">
    <div class="thank-you">
      <div class="landing-shell">

        <!-- HERO confirmation -->
        <section class="block hero-block">
          <div class="confirmation-badge" aria-hidden="true">✓</div>
          <p class="hero-kicker">Diagnostic OptiTAB · Confirmé</p>
          <h1>{{ greeting }}</h1>
          <p class="hero-subtitle">
            <template v-if="!isDirectLanding">
              Ton diagnostic personnalisé arrive dans ta boîte mail.
              Vérifie ta messagerie d'ici quelques minutes (pense au spam).
            </template>
            <template v-else>
              Si tu viens d'arriver ici sans passer par le formulaire,
              <RouterLink to="/diagnostic-maths-gratuit">commence ici</RouterLink>
              pour recevoir ton diagnostic gratuit.
            </template>
          </p>

          <div class="trust-row trust-row--center">
            <span class="trust-chip">Email en route</span>
            <span class="trust-chip">Gratuit</span>
            <span class="trust-chip">Sans engagement</span>
          </div>
        </section>

        <!-- ÉTAPES SUIVANTES -->
        <section v-if="!isDirectLanding" class="block steps-block">
          <div class="section-head">
            <h2>Ce qui se passe maintenant</h2>
            <p>Trois étapes simples pour tirer le maximum de ton diagnostic.</p>
          </div>
          <div class="steps-grid">
            <article v-for="step in nextSteps" :key="step.n" class="step-card">
              <span class="step-number" aria-hidden="true">{{ step.n }}</span>
              <h3>{{ step.title }}</h3>
              <p>{{ step.text }}</p>
            </article>
          </div>
        </section>

        <!-- APERÇU PLATEFORME -->
        <section class="block preview-block">
          <div class="section-head">
            <h2>Pendant que tu attends ton email…</h2>
            <p>Découvre concrètement à quoi ressemble la plateforme OptiTAB.</p>
          </div>

          <div class="preview-grid">
            <article v-for="item in previewItems" :key="item.title" class="preview-card">
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>

          <div class="preview-media">
            <article class="preview-media-card">
              <p class="preview-media-label">Aperçu desktop</p>
              <img
                src="/video/optitab-demo-exercices.gif"
                alt="Aperçu d'un exercice corrigé pas à pas sur OptiTAB"
                loading="lazy"
              />
            </article>
            <article class="preview-media-card preview-media-card--mobile">
              <p class="preview-media-label">Aperçu mobile</p>
              <img
                src="/video/optitab-demo-mobile.gif"
                alt="Aperçu mobile d'OptiTAB"
                loading="lazy"
              />
            </article>
          </div>

          <div class="preview-cta-wrap">
            <RouterLink
              to="/plateforme-maths"
              class="cta-primary"
              data-cta-name="pricing"
              data-cta-location="diagnostic_merci_main"
              @click="trackPlatformCta('main')"
            >
              Découvrir la plateforme OptiTAB →
            </RouterLink>
            <p class="cta-note">À partir de 4,99 €/mois · Sans engagement · Annulable à tout moment</p>
          </div>
        </section>

        <!-- AIDE / CONTACT -->
        <section class="block help-block">
          <div class="help-card">
            <h2>Tu n'as pas reçu l'email après 5 minutes ?</h2>
            <p>Vérifie ces 3 choses dans l'ordre :</p>
            <ol class="help-list">
              <li>Le dossier <strong>spam / indésirables</strong> de ta messagerie.</li>
              <li>L'onglet <strong>« Promotions »</strong> si tu utilises Gmail.</li>
              <li>Que ton email a bien été tapé sans faute de frappe.</li>
            </ol>
            <p>Si rien ne marche, écris-moi directement :</p>
            <div class="help-actions">
              <a
                href="https://wa.me/33764040251?text=Bonjour%2C%20je%20n%27ai%20pas%20re%C3%A7u%20mon%20diagnostic%20OptiTAB."
                target="_blank"
                rel="noopener noreferrer"
                class="contact-link contact-link--whatsapp"
                data-cta-name="whatsapp"
                data-cta-location="diagnostic_merci_help"
              >
                WhatsApp
              </a>
              <a
                href="mailto:contact@optitab.net?subject=Diagnostic%20non%20re%C3%A7u"
                class="contact-link"
                data-cta-name="contact"
                data-cta-location="diagnostic_merci_help"
              >
                contact@optitab.net
              </a>
            </div>
          </div>
        </section>

        <!-- FINAL CTA -->
        <section class="block final-cta-block">
          <h2>Tu peux commencer dès maintenant.</h2>
          <p>Tu n'as pas besoin d'attendre ton diagnostic pour explorer la plateforme.</p>
          <RouterLink
            to="/plateforme-maths"
            class="cta-primary"
            data-cta-name="pricing"
            data-cta-location="diagnostic_merci_final"
            @click="trackPlatformCta('final')"
          >
            Découvrir OptiTAB →
          </RouterLink>
        </section>

      </div>
    </div>

    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question après mon diagnostic OptiTAB."
      tooltip="Une question ? WhatsApp"
    />
  </MainLayout>
</template>

<style scoped lang="scss">
.thank-you {
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
  padding: 34px 0;
}

.block + .block {
  border-top: 1px solid rgba(30, 58, 138, 0.12);
}

/* ===== HERO ===== */
.hero-block {
  text-align: center;
  padding-top: 42px;
}

.confirmation-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  margin: 0 auto 18px;
  border-radius: 999px;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  font-size: 2rem;
  font-weight: 800;
  box-shadow: 0 12px 30px rgba(6, 95, 70, 0.18);
}

.hero-kicker {
  margin: 0;
  color: #2a38b7;
  font-size: 0.82rem;
  letter-spacing: 0.02em;
  font-weight: 800;
  text-transform: uppercase;
}

.hero-block h1 {
  margin: 12px auto 0;
  max-width: 22ch;
  font-size: clamp(1.7rem, 3vw, 2.4rem);
  line-height: 1.1;
  color: #0f172a;
  text-wrap: balance;
}

.hero-subtitle {
  margin: 16px auto 0;
  max-width: 56ch;
  color: #1e293b;
  font-size: 1.04rem;
  font-weight: 500;
  line-height: 1.5;
}

.hero-subtitle a {
  color: #1e3a8a;
  font-weight: 700;
  text-decoration: underline;
}

/* ===== TRUST CHIPS ===== */
.trust-row {
  margin-top: 20px;
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
  padding: 0 12px;
  border-radius: 999px;
  background: #eef4ff;
  border: 1px solid #cfe0ff;
  color: #1e3a8a;
  font-size: 0.82rem;
  font-weight: 700;
}

/* ===== SECTION HEAD ===== */
.section-head {
  text-align: center;
  margin-bottom: 22px;
}

.section-head h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.4rem, 2.4vw, 1.9rem);
}

.section-head p {
  margin: 8px auto 0;
  max-width: 60ch;
  color: #475569;
  font-size: 0.96rem;
}

/* ===== STEPS ===== */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.step-card {
  position: relative;
  border-radius: 16px;
  border: 1px solid #d6e1ff;
  background: linear-gradient(140deg, #ffffff 0%, #f5f8ff 100%);
  padding: 22px 18px 18px;
  text-align: center;
}

.step-number {
  display: inline-block;
  font-size: 1.4rem;
  font-weight: 900;
  color: #2a38b7;
  letter-spacing: 0.02em;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.step-card h3 {
  margin: 10px 0 8px;
  color: #0f172a;
  font-size: 1.04rem;
}

.step-card p {
  margin: 0;
  color: #475569;
  font-size: 0.92rem;
  line-height: 1.5;
}

/* ===== PREVIEW ===== */
.preview-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.preview-card {
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: #ffffff;
  padding: 16px;
  text-align: center;
}

.preview-card h3 {
  margin: 0 0 6px;
  color: #1e3a8a;
  font-size: 1rem;
  font-weight: 800;
}

.preview-card p {
  margin: 0;
  color: #475569;
  font-size: 0.88rem;
  line-height: 1.45;
}

.preview-media {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 14px;
  margin-bottom: 24px;
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

.preview-cta-wrap {
  text-align: center;
  margin-top: 8px;
}

/* ===== CTA ===== */
.cta-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  border: 1px solid #1f4ed2;
  border-radius: 14px;
  padding: 0 24px;
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
  font-size: 1rem;
  font-weight: 800;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cta-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 32px rgba(37, 99, 235, 0.35);
}

.cta-note {
  margin: 12px 0 0;
  color: #64748b;
  font-size: 0.82rem;
}

/* ===== HELP ===== */
.help-block { padding: 28px 0; }

.help-card {
  border-radius: 18px;
  border: 1px solid #cfe0ff;
  background: linear-gradient(145deg, #f8fbff 0%, #eef3ff 100%);
  padding: 24px;
}

.help-card h2 {
  margin: 0 0 8px;
  color: #0f172a;
  font-size: 1.2rem;
}

.help-card p {
  margin: 8px 0 0;
  color: #475569;
  font-size: 0.94rem;
  line-height: 1.5;
}

.help-list {
  margin: 10px 0 0;
  padding-left: 22px;
  color: #1e293b;
  font-size: 0.94rem;
  line-height: 1.7;
}

.help-list strong { color: #0f172a; }

.help-actions {
  margin-top: 14px;
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

/* ===== FINAL CTA ===== */
.final-cta-block {
  text-align: center;
  background: linear-gradient(145deg, #ffffff 0%, #eef2ff 100%);
  border-radius: 20px;
  padding: 32px 22px;
}

.final-cta-block h2 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(1.35rem, 2.3vw, 1.8rem);
}

.final-cta-block p {
  margin: 10px 0 18px;
  color: #475569;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 960px) {
  .steps-grid,
  .preview-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .preview-media {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .landing-shell {
    padding: 18px 12px 88px;
  }
  .block {
    padding: 24px 0;
  }
  .hero-block {
    padding-top: 24px;
  }
  .confirmation-badge {
    width: 60px;
    height: 60px;
    font-size: 1.6rem;
  }
  .steps-grid,
  .preview-grid {
    grid-template-columns: 1fr;
  }
  .help-card {
    padding: 18px;
  }
  .final-cta-block {
    padding: 22px 16px;
    border-radius: 16px;
  }
  .cta-primary {
    width: 100%;
  }
}
</style>
