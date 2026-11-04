<template>
  <!-- Visiteur : gabarit vitrine. Élève connecté : la page s'affiche dans son espace. -->
  <component :is="isAuthenticated ? DashboardLayout : VitrineLayout">
    <div class="vt-scope cp">
      <!-- 1. Accroche -->
      <section class="vt-page-hero cp-hero">
        <div class="vt-container cp-hero__inner">
          <div class="cp-hero__copy">
            <h1 class="cp-hero__h1">
              <span class="vt-kicker cp-hero__kicker">Cours particuliers en ligne · maths, physique-chimie, informatique</span>
              <span class="vt-sr-only"> – </span>
              <span class="vt-page-hero__title cp-hero__title">Un prof qui explique, <em>jusqu’à ce que ce soit clair.</em></span>
            </h1>
            <p class="vt-page-hero__lead">
              Je m’appelle Anthony. Ingénieur diplômé de l’<span class="vt-nowrap">ISAE-SUPAERO</span>, j’accompagne depuis plus de 15 ans des élèves
              du collège à la prépa. En visio, à votre rythme, avec un suivi même entre les cours.
            </p>
            <div class="vt-page-hero__actions">
              <button type="button" class="vt-btn vt-btn--primary" data-cta-name="tutoring_contact" data-cta-location="hero" @click="scrollTo('reserver')">
                Demander un premier échange gratuit
                <ArrowRightIcon aria-hidden="true" />
              </button>
              <button type="button" class="vt-btn vt-btn--ghost" @click="scrollTo('tarifs')">Voir les tarifs</button>
            </div>
            <ul class="vt-page-hero__reassure">
              <li>Premier échange gratuit</li>
              <li>Sans engagement</li>
              <li>Réponse sous 24&nbsp;h</li>
            </ul>
          </div>

          <figure class="cp-portrait">
            <div class="cp-portrait__photo">
              <img
                src="/images/professeurs/anthony.jpg"
                alt="Anthony Tabet, professeur de mathématiques, physique-chimie et informatique"
                width="479"
                height="521"
                fetchpriority="high"
              />
            </div>
            <figcaption class="cp-portrait__card">
              <p class="cp-portrait__name">Anthony Tabet</p>
              <p class="cp-portrait__role">Fondateur d’OptiTAB · Ingénieur <span class="vt-nowrap">ISAE-SUPAERO</span></p>
              <ul class="cp-portrait__tags">
                <li>Maths</li>
                <li>Physique-chimie</li>
                <li>Informatique</li>
              </ul>
              <a :href="GOOGLE_REVIEWS_URL" target="_blank" rel="noopener noreferrer" class="cp-portrait__rating">
                <span class="cp-stars" aria-hidden="true">★★★★★</span>
                <span><strong>5/5</strong> sur Google</span>
              </a>
            </figcaption>
          </figure>
        </div>
      </section>

      <!-- 2. Chiffres -->
      <section class="cp-stats" aria-label="En quelques chiffres">
        <div class="vt-container">
          <ul class="cp-stats__list">
            <li v-for="stat in coursStats" :key="stat.libelle">
              <span class="cp-stats__value">{{ stat.valeur }}</span>
              <span class="cp-stats__label">{{ stat.libelle }}</span>
            </li>
          </ul>
        </div>
      </section>

      <!-- 3. Pour qui -->
      <section class="vt-section">
        <div class="vt-container">
          <header v-reveal class="vt-heading">
            <p class="vt-kicker">Pour qui&nbsp;?</p>
            <h2 class="vt-title">Quelle que soit la situation, on part de là où vous en êtes</h2>
            <p class="vt-lead">Du collège à la prépa et à l’université, en mathématiques, physique-chimie et informatique.</p>
          </header>
          <div class="cp-who">
            <article v-for="(item, i) in coursPourQui" :key="item.titre" v-reveal="i * 80" class="vt-card cp-who__card">
              <span class="cp-icon"><component :is="ICONES[item.icone]" aria-hidden="true" /></span>
              <h3 class="cp-who__title">{{ item.titre }}</h3>
              <p class="cp-who__text">{{ item.texte }}</p>
            </article>
          </div>
        </div>
      </section>

      <!-- 4. Le professeur -->
      <section id="professeur" class="vt-section vt-section--soft">
        <div class="vt-container cp-prof">
          <div v-reveal class="cp-prof__aside">
            <div class="cp-prof__photo">
              <img src="/images/professeurs/anthony.jpg" alt="" width="479" height="521" loading="lazy" />
            </div>
            <blockquote class="cp-prof__quote">
              «&nbsp;Ensemble, transformons vos difficultés en forces et atteignons vos objectifs avec confiance. »
            </blockquote>
          </div>

          <div v-reveal="100" class="cp-prof__copy">
            <p class="vt-kicker">Votre professeur</p>
            <h2 class="vt-title">Ingénieur avant d’être prof, et passionné par la transmission</h2>
            <p>
              Diplômé de l’<span class="vt-nowrap">ISAE-SUPAERO</span> et de l’ESIB, je suis ingénieur calculateur de structures dans un bureau d’études.
              J’utilise chaque jour les maths et la physique que j’enseigne&nbsp;: je sais à quoi elles servent, et comment les
              rendre concrètes.
            </p>
            <p>
              Depuis plus de 15 ans, je donne des cours particuliers, d’abord sur des plateformes reconnues comme Groupe
              Réussite, auprès d’élèves du collège à la prépa. J’ai ensuite créé OptiTAB pour aller plus loin&nbsp;: donner à
              chaque élève une méthode claire et les outils pour progresser durablement, même entre deux cours.
            </p>
            <ul class="vt-checks cp-prof__list">
              <li>Diplômé d’une grande école d’ingénieurs (<span class="vt-nowrap">ISAE-SUPAERO</span>)</li>
              <li>Plus de 300 élèves accompagnés, du collège à la prépa</li>
              <li>95 % de réussite aux examens</li>
              <li>Disponible 7 jours sur 7 pour les questions entre les cours</li>
            </ul>
            <p class="cp-prof__verify">
              Vérifiez mon parcours&nbsp;:
              <a href="https://www.linkedin.com/in/anthony-tabet-a34aa6192/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
              ·
              <a href="https://groupe-reussite.fr/cours-particuliers-cours-particuliers-niveaux-ligne-domicile-3452/" target="_blank" rel="noopener noreferrer">Groupe Réussite</a>
            </p>
          </div>
        </div>
      </section>

      <!-- 5. Le déroulement, étape par étape -->
      <section id="deroulement" class="vt-section">
        <div class="vt-container cp-flow">
          <header v-reveal class="cp-flow__intro">
            <p class="vt-kicker">Comment ça se passe</p>
            <h2 class="vt-title">Du premier échange aux premiers progrès</h2>
            <p class="vt-lead">
              Un accompagnement simple et suivi, étape par étape. Vous savez toujours où en est l’élève et ce qui vient
              ensuite.
            </p>
            <button type="button" class="vt-btn vt-btn--primary cp-flow__cta" @click="scrollTo('reserver')">
              Commencer par l’étape 1
              <ArrowRightIcon aria-hidden="true" />
            </button>
          </header>
          <VitrineTimeline v-reveal="100" :etapes="coursEtapes" />
        </div>
      </section>

      <!-- 6. La méthode -->
      <section class="vt-section vt-section--soft cp-method">
        <div class="vt-container">
          <header v-reveal class="vt-heading">
            <p class="vt-kicker">Ma façon d’enseigner</p>
            <h2 class="vt-title">Comprendre, s’entraîner, gagner en confiance</h2>
          </header>
          <div class="cp-method__grid">
            <article v-for="(item, i) in coursMethode" :key="item.titre" v-reveal="i * 80" class="cp-method__item">
              <span class="cp-icon cp-icon--green"><component :is="ICONES[item.icone]" aria-hidden="true" /></span>
              <h3 class="cp-method__title">{{ item.titre }}</h3>
              <p class="cp-method__text">{{ item.texte }}</p>
            </article>
          </div>
        </div>
      </section>

      <!-- 7. Tarifs -->
      <section id="tarifs" class="vt-section">
        <div class="vt-container">
          <header v-reveal class="vt-heading">
            <p class="vt-kicker">Tarifs</p>
            <h2 class="vt-title">Des tarifs clairs, selon le niveau</h2>
            <p class="vt-lead">À l’heure, ou en pack d’heures pour un tarif plus doux. Sans engagement.</p>
          </header>

          <div v-reveal class="cp-levels" role="tablist" aria-label="Niveau">
            <button
              v-for="niveau in coursTarifs"
              :key="niveau.id"
              type="button"
              role="tab"
              :aria-selected="niveau.id === niveauId ? 'true' : 'false'"
              :class="['cp-levels__tab', { 'is-active': niveau.id === niveauId }]"
              @click="niveauId = niveau.id"
            >
              {{ niveau.label }}
            </button>
          </div>

          <div v-reveal :class="['cp-prices', { 'cp-prices--3': vipPlan }]">
            <article class="vt-card cp-price">
              <p class="cp-price__name">À l’heure</p>
              <p class="cp-price__hint">Pour un besoin ponctuel</p>
              <p class="cp-price__amount"><strong>{{ tarif.heure }}&nbsp;€</strong><span>/ heure</span></p>
              <ul class="vt-checks cp-price__list">
                <li>Une séance quand vous en avez besoin</li>
                <li>Idéal pour rattraper une notion</li>
                <li>Réglée séance par séance</li>
              </ul>
              <button type="button" class="vt-btn vt-btn--ghost vt-btn--block" @click="scrollTo('reserver')">Réserver une séance</button>
            </article>

            <article class="vt-card cp-price cp-price--featured">
              <span class="cp-price__flag">Le plus avantageux</span>
              <p class="cp-price__name">Pack d’heures</p>
              <p class="cp-price__hint">Pour un suivi régulier</p>
              <p class="cp-price__amount"><span>dès</span><strong>{{ tarif.packs[20] }}&nbsp;€</strong><span>/ heure</span></p>
              <table class="cp-packs">
                <tbody>
                  <tr v-for="heures in [5, 10, 20]" :key="heures">
                    <th scope="row">{{ heures }}&nbsp;h</th>
                    <td>{{ tarif.packs[heures] }}&nbsp;€/h</td>
                    <td class="cp-packs__total">{{ heures * tarif.packs[heures] }}&nbsp;€</td>
                  </tr>
                </tbody>
              </table>
              <p class="cp-price__save">
                Soit <strong>{{ 20 * (tarif.heure - tarif.packs[20]) }}&nbsp;€ d’économie</strong> sur 20&nbsp;h par rapport à l’heure.
              </p>
              <button type="button" class="vt-btn vt-btn--primary vt-btn--block" @click="scrollTo('reserver')">Choisir un pack</button>
            </article>

            <article v-if="vipPlan" class="vt-card cp-price">
              <p class="cp-price__name">{{ vipPlan.name }}</p>
              <p class="cp-price__hint">Cours + plateforme, chaque mois</p>
              <p class="cp-price__amount"><strong>{{ formatEur(vipPlan.price) }}</strong><span>/ mois</span></p>
              <ul class="vt-checks cp-price__list">
                <li v-for="feature in vipFeatures" :key="feature">{{ feature }}</li>
              </ul>
              <router-link to="/tarifs" class="vt-btn vt-btn--ghost vt-btn--block">Voir la formule</router-link>
            </article>
          </div>

          <ul class="cp-price-notes">
            <li>Heures de pack valables 6 mois</li>
            <li>Facture fournie</li>
            <li>Remise possible pour les frères et sœurs</li>
            <li>Paiement sécurisé en ligne</li>
          </ul>
        </div>
      </section>

      <!-- 8. Avis -->
      <section v-if="shots.length" class="vt-section vt-section--soft">
        <div class="vt-container">
          <header v-reveal class="vt-heading">
            <p class="vt-kicker">Ils en parlent</p>
            <h2 class="vt-title">Des messages reçus après les résultats</h2>
          </header>
          <div v-reveal :class="['cp-shots', `cp-shots--${Math.min(shots.length, 3)}`]">
            <TestimonialShot v-for="(shot, i) in shots.slice(0, 3)" :key="shot.id" :testimonial="shot" @open="openShot(i)" />
          </div>
          <p class="cp-shots__more">
            <a :href="GOOGLE_REVIEWS_URL" target="_blank" rel="noopener noreferrer">
              <span class="cp-stars" aria-hidden="true">★★★★★</span>
              Voir tous les avis sur Google
            </a>
          </p>
        </div>
      </section>

      <!-- 9. Questions (fond gris si les avis sont masqués, pour garder l'alternance) -->
      <section :class="['vt-section', { 'vt-section--soft': !shots.length }]">
        <div class="vt-container cp-faq">
          <header v-reveal class="cp-faq__intro">
            <p class="vt-kicker">Questions fréquentes</p>
            <h2 class="vt-title">Avant de commencer</h2>
          </header>
          <VitrineFaqList v-reveal="100" :items="coursFaq" />
        </div>
      </section>

      <!-- 10. Réserver -->
      <section id="reserver" class="vt-section cp-book">
        <div class="vt-container cp-book__inner">
          <div v-reveal class="cp-book__copy">
            <p class="vt-kicker cp-book__kicker">Étape 1</p>
            <h2 class="vt-title cp-book__title">Parlons de la situation de l’élève</h2>
            <p class="cp-book__text">Le premier échange est gratuit et sans engagement. Voici ce qui se passe ensuite&nbsp;:</p>
            <ol class="cp-book__steps">
              <li><span>1</span>Vous remplissez ce formulaire (2 minutes).</li>
              <li><span>2</span>Je vous recontacte sous 24&nbsp;h.</li>
              <li><span>3</span>Nous faisons le point ensemble et fixons la première séance.</li>
            </ol>
            <div class="cp-book__alt">
              <p>Vous préférez écrire directement&nbsp;?</p>
              <a :href="whatsappUrl" target="_blank" rel="noopener noreferrer" data-cta-name="whatsapp" data-cta-location="tutoring_book">
                <img src="/icons/whatsapp.svg" alt="" width="18" height="18" />
                WhatsApp · {{ vitrineContact.whatsappAffiche }}
              </a>
              <a :href="`mailto:${vitrineContact.email}`">
                <EnvelopeIcon aria-hidden="true" />
                {{ vitrineContact.email }}
              </a>
            </div>
          </div>
          <div v-reveal="100" class="vt-card cp-book__form">
            <VitrineContactForm mode="cours" :niveau-initial="tarif.formLevel" />
          </div>
        </div>
      </section>
    </div>

    <ScreenshotLightbox
      :open="lightboxOpen"
      :items="shots"
      :index="lightboxIndex"
      @close="lightboxOpen = false"
      @update:index="lightboxIndex = $event"
    />
  </component>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  ArrowRightIcon,
  EnvelopeIcon,
  PuzzlePieceIcon,
  CalendarDaysIcon,
  RocketLaunchIcon,
  FaceSmileIcon,
  AdjustmentsHorizontalIcon,
  LightBulbIcon,
  ChatBubbleLeftRightIcon,
  FlagIcon
} from '@heroicons/vue/24/outline'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import VitrineTimeline from '@/components/vitrine/VitrineTimeline.vue'
import VitrineFaqList from '@/components/vitrine/VitrineFaqList.vue'
import VitrineContactForm from '@/components/vitrine/VitrineContactForm.vue'
import TestimonialShot from '@/components/landing/TestimonialShot.vue'
import ScreenshotLightbox from '@/components/landing/ScreenshotLightbox.vue'
import { vReveal } from '@/components/vitrine/reveal'
import { useUserStore } from '@/stores/user'
import { getPlans } from '@/api/subscriptions'
import { getPublishedTestimonials } from '@/api/testimonials'
import { vitrineContact, GOOGLE_REVIEWS_URL } from '@/config/vitrineContent'
import {
  coursStats,
  coursPourQui,
  coursEtapes,
  coursMethode,
  coursTarifs,
  coursFaq
} from '@/config/vitrineCoursParticuliers'
import '@/styles/vitrine.css'

const userStore = useUserStore()
const isAuthenticated = computed(() => userStore.isAuthenticated)

const ICONES = {
  notion: PuzzlePieceIcon,
  examen: CalendarDaysIcon,
  prepa: RocketLaunchIcon,
  confiance: FaceSmileIcon,
  adapte: AdjustmentsHorizontalIcon,
  clair: LightBulbIcon,
  actif: ChatBubbleLeftRightIcon,
  objectif: FlagIcon
}

// Niveau affiché dans les tarifs ; il pré-remplit aussi le formulaire de demande.
const FORM_LEVEL = { college: 'Collège', lycee: 'Lycée', prepa: 'Prépa ou supérieur' }
const niveauId = ref('lycee')
const tarif = computed(() => {
  const t = coursTarifs.find((item) => item.id === niveauId.value) || coursTarifs[1]
  return { ...t, formLevel: FORM_LEVEL[t.id] }
})

const whatsappUrl = `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent('Bonjour Anthony, j’aimerais des informations sur les cours particuliers.')}`

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const formatEur = (value) => {
  const amount = Number(value)
  if (!Number.isFinite(amount)) return ''
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: Number.isInteger(amount) ? 0 : 2 }).format(amount)
}

// Formule « cours + plateforme » configurée dans l'admin (type « particuliers »).
const vipPlan = ref(null)
const vipFeatures = computed(() => (vipPlan.value?.features || []).slice(0, 4))

// Témoignages publiés depuis l'admin (captures de messages).
// Section masquée pour l'instant à la demande du propriétaire : repasser à true pour la réafficher.
const AFFICHER_TEMOIGNAGES = false
const shots = ref([])
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)
const openShot = (index) => {
  lightboxIndex.value = index
  lightboxOpen.value = true
}

onMounted(async () => {
  const [plansResult, shotsResult] = await Promise.allSettled([
    getPlans(),
    AFFICHER_TEMOIGNAGES ? getPublishedTestimonials() : Promise.resolve({ data: [] })
  ])
  if (plansResult.status === 'fulfilled') {
    const plans = plansResult.value?.data?.plans || []
    vipPlan.value = plans.find((plan) => plan.plan_type === 'particuliers') || null
  }
  if (shotsResult.status === 'fulfilled') {
    const list = shotsResult.value?.data
    shots.value = Array.isArray(list) ? list : []
  }
})
</script>

<style scoped>
/* ---------- 1. Accroche ---------- */

.cp-hero__inner {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
  gap: 56px;
  align-items: center;
}

.cp-hero__h1 {
  margin: 0;
}

.cp-hero__kicker {
  display: block;
  margin-bottom: 14px;
  line-height: 1.5;
  letter-spacing: 0.08em;
}

.cp-hero__title {
  display: block;
}

.cp-portrait {
  position: relative;
  max-width: 400px;
  margin: 0 auto;
}

.cp-portrait__photo {
  overflow: hidden;
  padding: 24px 24px 0;
  border-radius: 28px;
  background: linear-gradient(180deg, #fff 0%, #eef2fa 100%);
  border: 1px solid var(--vt-line);
  box-shadow: var(--vt-shadow-lg);
}

.cp-portrait__photo img {
  display: block;
  width: 100%;
  height: auto;
}

.cp-portrait__card {
  position: relative;
  margin: -64px 20px 0;
  padding: 18px 20px;
  border: 1px solid var(--vt-line);
  border-radius: 18px;
  background: #fff;
  box-shadow: var(--vt-shadow-lg);
  text-align: center;
}

.cp-portrait__name {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--vt-ink);
}

.cp-portrait__role {
  margin: 2px 0 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--vt-muted);
}

.cp-portrait__tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin: 0 0 12px;
  padding: 0;
  list-style: none;
}

.cp-portrait__tags li {
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--vt-navy-50);
  font-size: 12px;
  font-weight: 700;
  color: var(--vt-navy);
}

.cp-portrait__rating {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--vt-ink-soft);
  text-decoration: none;
}

.cp-portrait__rating:hover strong {
  text-decoration: underline;
}

.cp-stars {
  color: #f5b400;
  letter-spacing: 1px;
}

/* ---------- 2. Chiffres ---------- */

.cp-stats {
  border-bottom: 1px solid var(--vt-line);
}

.cp-stats__list {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin: 0;
  padding: 0;
  list-style: none;
}

.cp-stats__list li {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 30px 24px;
}

.cp-stats__list li + li {
  border-left: 1px solid var(--vt-line);
}

.cp-stats__value {
  font-size: 34px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--vt-navy);
}

.cp-stats__label {
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-muted);
}

/* ---------- Icônes ---------- */

.cp-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: var(--vt-navy-50);
  color: var(--vt-navy);
}

.cp-icon--green {
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.cp-icon :deep(svg) {
  width: 24px;
  height: 24px;
}

/* ---------- 3. Pour qui ---------- */

.cp-who {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.cp-who__card {
  padding: 26px 22px;
}

.cp-who__title {
  margin-top: 18px;
  font-size: 18px;
}

.cp-who__text {
  margin: 10px 0 0;
  font-size: 15px;
  color: var(--vt-muted);
}

/* ---------- 4. Professeur ---------- */

.cp-prof {
  display: grid;
  grid-template-columns: minmax(0, 0.75fr) minmax(0, 1.25fr);
  gap: 64px;
  align-items: center;
}

.cp-prof__photo {
  overflow: hidden;
  padding: 20px 20px 0;
  border-radius: 24px;
  background: #fff;
  border: 1px solid var(--vt-line);
}

.cp-prof__photo img {
  display: block;
  width: 100%;
  height: auto;
}

.cp-prof__quote {
  margin: 18px 0 0;
  padding: 16px 20px;
  border-left: 3px solid var(--vt-green);
  border-radius: 0 14px 14px 0;
  background: #fff;
  font-size: 16px;
  font-weight: 600;
  font-style: italic;
  line-height: 1.6;
  color: var(--vt-ink-soft);
}

.cp-prof__copy > p:not(.vt-kicker) {
  margin: 16px 0 0;
  font-size: 16px;
  line-height: 1.75;
  color: var(--vt-ink-soft);
}

.cp-prof__copy .vt-title {
  margin-top: 0;
}

.cp-prof__list {
  margin-top: 22px;
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-ink);
}

.cp-prof__copy > .cp-prof__verify {
  margin-top: 22px;
  font-size: 14px;
  color: var(--vt-muted);
}

.cp-prof__verify a {
  color: var(--vt-navy);
  font-weight: 700;
}

/* ---------- 5. Déroulement ---------- */

.cp-flow {
  display: grid;
  grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr);
  gap: 64px;
  align-items: start;
}

.cp-flow__intro {
  position: sticky;
  top: 104px;
}

.cp-flow__cta {
  margin-top: 28px;
}

/* ---------- 6. Méthode ---------- */

.cp-method__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 28px;
}

.cp-method__title {
  margin-top: 16px;
  font-size: 17px;
}

.cp-method__text {
  margin: 8px 0 0;
  font-size: 15px;
  color: var(--vt-muted);
}

/* ---------- 7. Tarifs ---------- */

.cp-levels {
  display: flex;
  justify-content: center;
  gap: 4px;
  width: fit-content;
  max-width: 100%;
  margin: 0 auto 32px;
  padding: 5px;
  border-radius: 14px;
  background: #e9edf5;
}

.cp-levels__tab {
  padding: 10px 18px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  font-family: var(--vt-font);
  font-size: 15px;
  font-weight: 700;
  color: var(--vt-muted);
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.cp-levels__tab:hover {
  color: var(--vt-ink);
}

.cp-levels__tab.is-active {
  background: #fff;
  color: var(--vt-navy);
  box-shadow: 0 2px 8px rgba(16, 32, 79, 0.1);
}

.cp-prices {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px;
  max-width: 820px;
  margin: 0 auto;
  align-items: stretch;
}

.cp-prices--3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  max-width: none;
}

.cp-price {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 28px 24px 24px;
}

.cp-price--featured {
  border: 2px solid var(--vt-navy);
  box-shadow: var(--vt-shadow-lg);
}

.cp-price__flag {
  position: absolute;
  top: -13px;
  left: 24px;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--vt-navy);
  font-size: 12px;
  font-weight: 700;
  color: #fff;
}

.cp-price__name {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--vt-ink);
}

.cp-price__hint {
  margin: 2px 0 0;
  font-size: 14px;
  color: var(--vt-muted);
}

.cp-price__amount {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin: 18px 0 16px;
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-muted);
}

.cp-price__amount strong {
  font-size: 42px;
  line-height: 1;
  letter-spacing: -0.03em;
  color: var(--vt-ink);
}

.cp-price__list {
  margin-bottom: 24px;
  font-size: 15px;
  color: var(--vt-ink-soft);
}

.cp-price .vt-btn {
  margin-top: auto;
}

.cp-packs {
  width: 100%;
  margin: 0 0 12px;
  border-collapse: collapse;
  font-size: 15px;
}

.cp-packs th,
.cp-packs td {
  padding: 9px 4px;
  border-top: 1px solid var(--vt-line);
  text-align: left;
  color: var(--vt-ink-soft);
}

.cp-packs tr:first-child th,
.cp-packs tr:first-child td {
  border-top: 0;
}

.cp-packs th {
  font-weight: 700;
  color: var(--vt-ink);
}

.cp-packs__total {
  text-align: right !important;
  font-weight: 700;
  color: var(--vt-ink) !important;
}

.cp-price__save {
  margin: 0 0 22px;
  padding: 10px 12px;
  border-radius: 10px;
  background: var(--vt-green-50);
  font-size: 14px;
  color: var(--vt-green-700);
}

.cp-price-notes {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 26px;
  margin: 32px 0 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-muted);
}

.cp-price-notes li::before {
  content: '·';
  margin-right: 8px;
  color: var(--vt-green);
  font-weight: 700;
}

/* ---------- 8. Avis ---------- */

.cp-shots {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
  margin: 0 auto;
}

.cp-shots--1 {
  grid-template-columns: minmax(0, 340px);
  justify-content: center;
}

.cp-shots--2 {
  grid-template-columns: repeat(2, minmax(0, 340px));
  justify-content: center;
}

.cp-shots__more {
  margin: 28px 0 0;
  text-align: center;
}

.cp-shots__more a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 700;
  color: var(--vt-navy);
  text-decoration: none;
}

.cp-shots__more a:hover {
  text-decoration: underline;
}

/* ---------- 9. Questions ---------- */

.cp-faq {
  display: grid;
  grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr);
  gap: 56px;
  align-items: start;
}

/* ---------- 10. Réserver ---------- */

.cp-book {
  background:
    radial-gradient(700px 400px at 100% 0%, rgba(95, 172, 96, 0.18), transparent 60%),
    var(--vt-navy);
}

.cp-book__inner {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 56px;
  align-items: start;
}

.cp-book__kicker {
  color: var(--vt-green-300);
}

.cp .cp-book__title {
  color: #fff;
}

.cp-book__text {
  margin: 16px 0 0;
  font-size: 17px;
  color: rgba(255, 255, 255, 0.82);
}

.cp-book__steps {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: 24px 0 0;
  padding: 0;
  list-style: none;
}

.cp-book__steps li {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.cp-book__steps span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.12);
  font-size: 14px;
  font-weight: 700;
  color: var(--vt-green-300);
}

.cp-book__alt {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}

.cp-book__alt p {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.cp-book__alt a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  text-decoration: none;
}

.cp-book__alt a:hover {
  color: var(--vt-green-300);
}

.cp-book__alt img {
  filter: brightness(0) invert(1);
}

.cp-book__alt svg {
  width: 18px;
  height: 18px;
}

.cp-book__form {
  padding: 28px;
  box-shadow: 0 30px 60px rgba(5, 14, 40, 0.3);
}

/* ---------- Tablette ---------- */

@media (max-width: 1080px) {
  .cp-hero__inner,
  .cp-prof,
  .cp-flow,
  .cp-faq,
  .cp-book__inner {
    grid-template-columns: minmax(0, 1fr);
    gap: 40px;
  }

  .cp-portrait {
    max-width: 340px;
  }

  .cp-flow__intro {
    position: static;
  }

  .cp-prof__aside {
    max-width: 380px;
  }

  .cp-who,
  .cp-method__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cp-prices--3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    max-width: 820px;
  }

  .cp-stats__list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cp-stats__list li:nth-child(3) {
    border-left: 0;
  }

  .cp-stats__list li:nth-child(n + 3) {
    border-top: 1px solid var(--vt-line);
  }
}

/* ---------- Téléphone ---------- */

@media (max-width: 640px) {
  .cp-hero__kicker {
    font-size: 12px;
  }

  .cp-portrait {
    max-width: 300px;
  }

  .cp-stats__list li {
    padding: 20px 14px 20px 0;
  }

  .cp-stats__list li:nth-child(even) {
    padding-left: 16px;
  }

  .cp-stats__value {
    font-size: 28px;
  }

  .cp-who,
  .cp-method__grid,
  .cp-prices,
  .cp-prices--3,
  .cp-shots,
  .cp-shots--2 {
    grid-template-columns: minmax(0, 1fr);
  }

  .cp-shots--1 {
    grid-template-columns: minmax(0, 1fr);
  }

  /* Icône à côté du titre : cartes plus compactes. */
  .cp-who__card,
  .cp-method__item {
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr);
    column-gap: 14px;
    align-items: center;
  }

  .cp-who__card {
    padding: 18px 16px;
  }

  .cp-who__card .cp-icon,
  .cp-method__item .cp-icon {
    width: 44px;
    height: 44px;
  }

  .cp-who__title,
  .cp-method__title {
    margin-top: 0;
  }

  .cp-who__text,
  .cp-method__text {
    grid-column: 1 / -1;
  }

  .cp-method__grid {
    gap: 22px;
  }

  .cp-levels {
    width: 100%;
  }

  .cp-levels__tab {
    flex: 1;
    padding: 10px 8px;
    font-size: 13px;
    white-space: normal;
  }

  .cp-price {
    padding: 26px 18px 20px;
  }

  .cp-price-notes {
    flex-direction: column;
    align-items: center;
  }

  .cp-book__form {
    padding: 20px 16px;
  }
}
</style>
