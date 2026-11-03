<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowRightIcon,
  CheckIcon,
  SparklesIcon,
  AcademicCapIcon,
  UserGroupIcon,
  BookOpenIcon,
  DocumentTextIcon,
  PencilSquareIcon,
  ChartBarIcon,
  ChevronDownIcon,
  EnvelopeIcon
} from '@heroicons/vue/24/outline'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import HeroMockup from '@/components/vitrine/HeroMockup.vue'
import DemoDevices from '@/components/vitrine/DemoDevices.vue'
import VitrinePricing from '@/components/vitrine/VitrinePricing.vue'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import {
  vitrineHero,
  vitrineStats,
  vitrineParcours,
  vitrineClasses,
  vitrineMethode,
  vitrineProf,
  vitrineFaq,
  vitrineContact,
  GOOGLE_REVIEWS_URL
} from '@/config/vitrineContent'

const { openModal } = useModalManager()

const parcoursIcons = { gratuit: SparklesIcon, plateforme: AcademicCapIcon, prof: UserGroupIcon }
const methodeIcons = { cours: BookOpenIcon, fiche: DocumentTextIcon, exercices: PencilSquareIcon, progression: ChartBarIcon }

const whatsappUrl = `https://wa.me/${vitrineContact.whatsapp}?text=${encodeURIComponent(vitrineContact.messageWhatsapp)}`

const openRegister = () => openModal(MODAL_IDS.REGISTER)

const scrollToId = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const classeLink = (niveau) => ({ path: '/ressources-gratuites/cours', query: { niveau } })

const CYCLE_CLES = { Primaire: 'primaire', Collège: 'college', Lycée: 'lycee' }
const classes = vitrineClasses.flatMap((cycle) =>
  cycle.classes.map((classe) => ({ ...classe, cycle: cycle.cycle, cycleCle: CYCLE_CLES[cycle.cycle] }))
)

// Apparition douce des blocs au défilement. La classe n'est posée qu'une fois
// le JavaScript chargé : sans lui, tout reste visible.
let revealObserver = null
const vReveal = {
  mounted(el, binding) {
    if (typeof window === 'undefined' || !('IntersectionObserver' in window)) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    if (!revealObserver) {
      revealObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible')
              revealObserver.unobserve(entry.target)
            }
          })
        },
        { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
      )
    }
    el.classList.add('vt-reveal')
    if (binding.value) el.style.transitionDelay = `${binding.value}ms`
    revealObserver.observe(el)
  }
}

// Arrivée par un lien « /#tarifs » depuis une autre page : la page est chargée à la
// demande, donc on descend nous-mêmes à la section une fois l'affichage posé.
const route = useRoute()
onMounted(() => {
  const id = route.hash ? route.hash.slice(1) : ''
  if (!id) return
  setTimeout(() => scrollToId(id), 350)
})

onBeforeUnmount(() => {
  revealObserver?.disconnect()
  revealObserver = null
})
</script>

<template>
  <VitrineLayout>
    <!-- 1. Accroche -->
    <section class="hero">
      <div class="hero__grid-bg" aria-hidden="true"></div>
      <div class="vt-container hero__inner">
        <div class="hero__copy">
          <!-- Le H1 porte la recherche visée (« cours de maths en ligne ») puis l'accroche. -->
          <h1 class="hero__title">
            <span class="hero__eyebrow">
              <span class="hero__eyebrow-dot" aria-hidden="true"></span>
              {{ vitrineHero.eyebrow }}
            </span>
            <span class="vt-sr-only"> – </span>
            <span class="hero__headline">
              {{ vitrineHero.titre }}
              <span class="hero__accent">
                {{ vitrineHero.titreAccent }}
                <svg class="hero__swoosh" viewBox="0 0 220 18" preserveAspectRatio="none" aria-hidden="true">
                  <path d="M3 13 C 60 4, 150 2, 217 9" />
                </svg>
              </span>
            </span>
          </h1>
          <p class="hero__lead">{{ vitrineHero.sousTitre }}</p>

          <div class="hero__ctas">
            <button
              type="button"
              class="vt-btn vt-btn--primary"
              data-cta-name="signup"
              data-cta-location="hero"
              @click="openRegister"
            >
              {{ vitrineHero.ctaPrincipal }}
              <ArrowRightIcon aria-hidden="true" />
            </button>
            <router-link
              to="/ressources-gratuites"
              class="vt-btn vt-btn--ghost"
              data-cta-name="free_resources"
              data-cta-location="hero"
            >
              {{ vitrineHero.ctaSecondaire }}
            </router-link>
          </div>

          <ul class="hero__reassure">
            <li v-for="item in vitrineHero.rassurance" :key="item">
              <CheckIcon class="hero__check" aria-hidden="true" />
              {{ item }}
            </li>
          </ul>

          <a :href="GOOGLE_REVIEWS_URL" target="_blank" rel="noopener noreferrer" class="hero__rating">
            <svg class="hero__google" viewBox="0 0 256 262" aria-hidden="true">
              <path fill="#4285F4" d="M255.9 133.5c0-10.7-.9-18.5-2.9-26.6H130.6v48.2h71.9c-1.5 12-9.8 30-28.2 42.1l-.3 2.2 41 31.7 2.8.3c25.9-23.9 38.1-59.1 38.1-97.9z" />
              <path fill="#34A853" d="M130.6 261.1c34.5 0 63.4-11.3 84.5-30.8l-40.2-31.1c-10.7 7.2-25.1 12.3-44.3 12.3-33.9 0-62.7-22.9-72.9-54.5l-2.1.2-41.7 32.2-.5 2c20.9 41.6 64 69.7 117.2 69.7z" />
              <path fill="#FBBC05" d="M57.7 156.9c-2.7-8.1-4.3-16.8-4.3-25.9s1.6-17.8 4.2-25.9l-.1-2.3L15.2 70.1l-1.4.7C5.1 88.1 0 108.1 0 130.9c0 22.8 5.1 42.8 13.8 60.2l43.9-34.2z" />
              <path fill="#EA4335" d="M130.6 50.4c24 0 40.1 10.4 49.3 19.2l36-35.1C193.8 12.6 165 0 130.6 0 77.4 0 34.3 28.1 13.4 69.7l43.9 34.2c10.3-31.6 39-53.5 73.3-53.5z" />
            </svg>
            <span class="hero__stars" aria-hidden="true">★★★★★</span>
            <span><strong>5/5</strong> sur Google</span>
          </a>
        </div>

        <div class="hero__visual">
          <HeroMockup />
        </div>
      </div>
    </section>

    <!-- 2. Chiffres clés -->
    <section class="stats" aria-label="OptiTAB en chiffres">
      <div class="vt-container">
        <ul class="stats__list">
          <li v-for="stat in vitrineStats" :key="stat.libelle" class="stats__item">
            <span class="stats__value">{{ stat.valeur }}</span>
            <span class="stats__label">{{ stat.libelle }}</span>
            <span class="stats__detail">{{ stat.detail }}</span>
          </li>
        </ul>
      </div>
    </section>

    <!-- 3. Par où commencer -->
    <section class="vt-section" id="commencer">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">Par où commencer&nbsp;?</p>
          <h2 class="vt-title">Trois façons d’avancer avec OptiTAB</h2>
          <p class="vt-lead">Choisis la porte d’entrée qui te ressemble. Tu peux toujours passer de l’une à l’autre.</p>
        </header>

        <div class="paths">
          <article
            v-for="(parcours, index) in vitrineParcours"
            :key="parcours.cle"
            v-reveal="index * 90"
            :class="['path', `path--${parcours.ton}`, { 'path--featured': parcours.miseEnAvant }]"
          >
            <span v-if="parcours.miseEnAvant" class="path__flag">Recommandé</span>
            <div class="path__head">
              <span class="path__icon"><component :is="parcoursIcons[parcours.cle]" aria-hidden="true" /></span>
              <p class="path__tag">{{ parcours.etiquette }}</p>
            </div>
            <h3 class="path__title">{{ parcours.titre }}</h3>
            <p class="path__text">{{ parcours.texte }}</p>
            <ul class="path__points">
              <li v-for="point in parcours.points" :key="point">
                <CheckIcon aria-hidden="true" />
                {{ point }}
              </li>
            </ul>
            <button
              v-if="parcours.ancre"
              type="button"
              :class="['vt-btn', 'vt-btn--block', parcours.miseEnAvant ? 'vt-btn--primary' : 'vt-btn--ghost']"
              data-cta-name="pricing"
              data-cta-location="paths"
              @click="scrollToId(parcours.ancre)"
            >
              {{ parcours.cta }}
            </button>
            <router-link
              v-else
              :to="parcours.lien"
              :class="['vt-btn', 'vt-btn--block', parcours.miseEnAvant ? 'vt-btn--primary' : 'vt-btn--ghost']"
              :data-cta-name="parcours.cle === 'prof' ? 'tutoring' : 'free_resources'"
              data-cta-location="paths"
            >
              {{ parcours.cta }}
            </router-link>
          </article>
        </div>
      </div>
    </section>

    <!-- 4. Choisis ta classe -->
    <section class="vt-section vt-section--soft" id="classes">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">Tout le programme de maths</p>
          <h2 class="vt-title">Choisis ta classe</h2>
          <p class="vt-lead">Chaque chapitre du programme a son cours, sa fiche de synthèse et ses exercices corrigés. Clique sur ta classe pour voir les cours gratuits.</p>
        </header>

        <div v-reveal class="levels">
          <router-link
            v-for="classe in classes"
            :key="classe.niveau"
            :to="classeLink(classe.niveau)"
            :class="['level', `level--${classe.cycleCle}`]"
            data-cta-name="level"
            :data-cta-location="`levels_${classe.libelle}`"
          >
            <span class="level__cycle">{{ classe.cycle }}</span>
            <span class="level__name">{{ classe.libelle }}</span>
            <span class="level__count">
              {{ classe.chapitres }} chapitres
              <span v-if="classe.note" class="level__note">{{ classe.note }}</span>
            </span>
            <ArrowRightIcon class="level__arrow" aria-hidden="true" />
          </router-link>
        </div>

        <nav class="levels__links" aria-label="Ressources gratuites">
          <router-link to="/ressources-gratuites/cours">Cours de maths gratuits</router-link>
          <router-link to="/ressources-gratuites/exercices">Exercices corrigés gratuits</router-link>
          <router-link to="/ressources-gratuites/syntheses">Fiches de synthèse</router-link>
        </nav>
      </div>
    </section>

    <!-- 5. La méthode -->
    <section class="vt-section" id="methode">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">La méthode OptiTAB</p>
          <h2 class="vt-title">Chaque chapitre suit le même chemin</h2>
          <p class="vt-lead">Plus besoin de te demander quoi réviser&nbsp;: on te guide du cours jusqu’aux exercices type contrôle.</p>
        </header>

        <ol class="steps">
          <li v-for="(etape, index) in vitrineMethode" :key="etape.numero" v-reveal="index * 90" class="step">
            <span class="step__icon"><component :is="methodeIcons[etape.icone]" aria-hidden="true" /></span>
            <div class="step__body">
              <span class="step__num">Étape {{ etape.numero }}</span>
              <h3 class="step__title">{{ etape.titre }}</h3>
              <p class="step__text">{{ etape.texte }}</p>
            </div>
          </li>
        </ol>

        <div class="devices">
          <div v-reveal class="devices__copy">
            <div>
              <h3 class="devices__title">Sur ordinateur comme sur téléphone</h3>
              <p class="devices__text">
                OptiTAB s’ouvre directement dans le navigateur, sans application à installer. Tu retrouves ta progression partout, à la maison comme dans le bus.
              </p>
            </div>
            <div>
              <ul class="devices__list">
                <li><CheckIcon aria-hidden="true" />Formules et figures nettes, même sur petit écran</li>
                <li><CheckIcon aria-hidden="true" />Tableau de bord, XP et classement pour rester motivé</li>
                <li><CheckIcon aria-hidden="true" />Outils de calcul et grapheur intégrés</li>
              </ul>
              <button
                type="button"
                class="vt-btn vt-btn--primary"
                data-cta-name="signup"
                data-cta-location="devices"
                @click="openRegister"
              >
                Tester un chapitre gratuitement
                <ArrowRightIcon aria-hidden="true" />
              </button>
            </div>
          </div>
          <div v-reveal="120" class="devices__visual">
            <DemoDevices />
            <p class="devices__caption">Images réelles de la plateforme, filmées sur des chapitres de Terminale</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. Formules -->
    <section class="vt-section vt-section--soft" id="tarifs">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">Formules</p>
          <h2 class="vt-title">Commence gratuitement, <span class="vt-nowrap">abonne-toi</span> quand tu es prêt</h2>
          <p class="vt-lead">Aucun engagement&nbsp;: tu choisis la durée qui correspond à tes révisions et tu arrêtes quand tu veux.</p>
        </header>

        <VitrinePricing v-reveal />
      </div>
    </section>

    <!-- 7. Le professeur / cours particuliers -->
    <section class="vt-section prof" id="cours-particuliers">
      <div class="vt-container prof__inner">
        <div v-reveal class="prof__portrait">
          <img
            :src="vitrineProf.photo"
            :alt="vitrineProf.photoAlt"
            class="prof__photo"
            width="479"
            height="521"
            loading="lazy"
            decoding="async"
          />
          <p class="prof__name">
            <strong>Anthony</strong>
            <span>Fondateur · Ingénieur ISAE-SUPAERO</span>
          </p>
        </div>

        <div v-reveal="100" class="prof__copy">
          <p class="vt-kicker prof__kicker">{{ vitrineProf.etiquette }}</p>
          <h2 class="vt-title prof__title">{{ vitrineProf.titre }}</h2>
          <p class="prof__text">{{ vitrineProf.texte }}</p>
          <ul class="prof__list">
            <li v-for="point in vitrineProf.points" :key="point">
              <CheckIcon aria-hidden="true" />
              {{ point }}
            </li>
          </ul>
          <div class="prof__ctas">
            <router-link
              to="/cours-particuliers"
              class="vt-btn vt-btn--green"
              data-cta-name="tutoring"
              data-cta-location="prof"
            >
              {{ vitrineProf.cta }}
              <ArrowRightIcon aria-hidden="true" />
            </router-link>
            <a
              :href="whatsappUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="vt-btn vt-btn--light"
              data-cta-name="whatsapp"
              data-cta-location="prof"
            >
              {{ vitrineProf.ctaSecondaire }}
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- 8. Questions fréquentes -->
    <section class="vt-section" id="faq">
      <div class="vt-container faq">
        <header v-reveal class="faq__intro">
          <p class="vt-kicker">Questions fréquentes</p>
          <h2 class="vt-title">Tout ce qu’il faut savoir avant de commencer</h2>
          <div class="faq__contact">
            <p class="faq__contact-title">Une autre question&nbsp;?</p>
            <p class="faq__contact-text">On répond sous 24&nbsp;h, 7&nbsp;jours sur&nbsp;7.</p>
            <a :href="whatsappUrl" target="_blank" rel="noopener noreferrer" class="faq__contact-link" data-cta-name="whatsapp" data-cta-location="faq">
              <img src="/icons/whatsapp.svg" alt="" width="18" height="18" />
              WhatsApp · {{ vitrineContact.whatsappAffiche }}
            </a>
            <a :href="`mailto:${vitrineContact.email}`" class="faq__contact-link">
              <EnvelopeIcon aria-hidden="true" />
              {{ vitrineContact.email }}
            </a>
          </div>
        </header>

        <div class="faq__list">
          <details v-for="(item, index) in vitrineFaq" :key="item.question" class="faq__item" :open="index === 0">
            <summary class="faq__question">
              {{ item.question }}
              <ChevronDownIcon class="faq__chevron" aria-hidden="true" />
            </summary>
            <p class="faq__answer">{{ item.answer }}</p>
          </details>
        </div>
      </div>
    </section>

    <!-- 9. Dernier appel -->
    <section class="final">
      <div class="vt-container">
        <div v-reveal class="final__card">
          <div class="final__grid-bg" aria-hidden="true"></div>
          <h2 class="final__title">Prêt à reprendre les maths en main&nbsp;?</h2>
          <p class="final__text">Crée ton compte gratuit et débloque un chapitre complet pour tester la méthode. Sans carte bancaire.</p>
          <div class="final__ctas">
            <button
              type="button"
              class="vt-btn vt-btn--green"
              data-cta-name="signup"
              data-cta-location="final"
              @click="openRegister"
            >
              Créer mon compte gratuit
              <ArrowRightIcon aria-hidden="true" />
            </button>
            <router-link
              to="/ressources-gratuites"
              class="vt-btn vt-btn--light"
              data-cta-name="free_resources"
              data-cta-location="final"
            >
              Voir les ressources gratuites
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </VitrineLayout>
</template>

<style scoped>
/* ---------- 1. Accroche ---------- */

.hero {
  position: relative;
  overflow: hidden;
  padding: 40px 0 80px;
  background:
    radial-gradient(900px 480px at 85% 10%, rgba(95, 172, 96, 0.1), transparent 60%),
    radial-gradient(800px 520px at 0% 100%, rgba(27, 60, 142, 0.08), transparent 60%),
    linear-gradient(180deg, #fbfcfe 0%, #f3f6fc 100%);
}

/* Petits carreaux, comme sur un cahier de maths. */
.hero__grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(27, 60, 142, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(27, 60, 142, 0.06) 1px, transparent 1px);
  background-size: 28px 28px;
  -webkit-mask-image: radial-gradient(ellipse 70% 80% at 70% 40%, #000 20%, transparent 75%);
  mask-image: radial-gradient(ellipse 70% 80% at 70% 40%, #000 20%, transparent 75%);
  pointer-events: none;
}

.hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.12fr) minmax(0, 1fr);
  align-items: center;
  gap: 48px;
}

/* Première ligne du H1, présentée en étiquette. */
.hero__eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  max-width: 100%;
  margin: 0 0 22px;
  padding: 7px 14px;
  border: 1px solid var(--vt-navy-100);
  border-radius: 999px;
  background: #fff;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: 0;
  color: var(--vt-navy);
}

.hero__headline {
  display: block;
}

.hero__eyebrow-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--vt-green);
  box-shadow: 0 0 0 4px rgba(95, 172, 96, 0.18);
}

.hero__title {
  font-size: clamp(42px, 5.6vw, 68px);
  line-height: 1.04;
  letter-spacing: -0.035em;
}

.hero__accent {
  position: relative;
  display: inline-block;
  color: var(--vt-navy);
  white-space: nowrap;
}

.hero__swoosh {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -0.12em;
  width: 100%;
  height: 0.28em;
  overflow: visible;
}

.hero__swoosh path {
  fill: none;
  stroke: var(--vt-green);
  stroke-width: 6;
  stroke-linecap: round;
}

.hero__lead {
  max-width: 540px;
  margin: 28px 0 0;
  font-size: 19px;
  line-height: 1.65;
  color: var(--vt-muted);
}

.hero__ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 36px;
}

.hero__ctas .vt-btn {
  padding: 0 22px;
}

.hero__reassure {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
  margin: 24px 0 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-ink-soft);
}

.hero__reassure li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.hero__check {
  width: 16px;
  height: 16px;
  stroke-width: 3;
  color: var(--vt-green-700);
}

.hero__rating {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--vt-line);
  font-size: 14px;
  color: var(--vt-ink-soft);
  text-decoration: none;
}

.hero__rating:hover strong {
  text-decoration: underline;
}

.hero__google {
  width: 18px;
  height: 18px;
}

.hero__stars {
  color: #f5b400;
  letter-spacing: 1px;
}

/* ---------- 2. Chiffres ---------- */

.stats {
  border-bottom: 1px solid var(--vt-line);
  background: #fff;
}

.stats__list {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin: 0;
  padding: 0;
  list-style: none;
}

.stats__item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 36px 28px;
}

.stats__item + .stats__item {
  border-left: 1px solid var(--vt-line);
}

.stats__value {
  font-size: 36px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--vt-navy);
}

.stats__label {
  margin-top: 6px;
  font-size: 15px;
  font-weight: 700;
  color: var(--vt-ink);
}

.stats__detail {
  font-size: 14px;
  color: var(--vt-muted);
}

/* ---------- 3. Parcours ---------- */

.paths {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
  align-items: stretch;
}

.path {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 32px 28px 28px;
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  background: #fff;
  box-shadow: var(--vt-shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.path:hover {
  transform: translateY(-3px);
  box-shadow: var(--vt-shadow-lg);
}

.path--featured {
  border: 2px solid var(--vt-navy);
}

.path__flag {
  position: absolute;
  top: -13px;
  left: 28px;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--vt-navy);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.path__head {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.path__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 14px;
}

.path__icon svg {
  width: 24px;
  height: 24px;
}

.path--green .path__icon {
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.path--navy .path__icon {
  background: var(--vt-navy-50);
  color: var(--vt-navy);
}

.path--orange .path__icon {
  background: var(--vt-orange-50);
  color: var(--vt-orange-700);
}

.path__tag {
  margin: 0;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--vt-muted);
}

.path__title {
  font-size: 23px;
}

.path__text {
  margin: 12px 0 0;
  font-size: 16px;
  color: var(--vt-muted);
}

.path__points {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 20px 0 28px;
  padding: 18px 0 0;
  border-top: 1px solid var(--vt-line);
  list-style: none;
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-ink-soft);
}

.path__points li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.path__points svg {
  width: 18px;
  height: 18px;
  margin-top: 3px;
  flex-shrink: 0;
  stroke-width: 2.6;
  color: var(--vt-green-700);
}

.path .vt-btn {
  margin-top: auto;
}

/* ---------- 4. Classes ---------- */

.levels {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
}

.level {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 18px 18px 16px;
  border: 1px solid var(--vt-line);
  border-radius: 14px;
  background: #fff;
  color: var(--vt-ink);
  text-decoration: none;
  box-shadow: 0 1px 2px rgba(16, 32, 79, 0.04);
  transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.level:hover {
  border-color: var(--vt-navy);
  box-shadow: var(--vt-shadow);
  transform: translateY(-2px);
}

.level__cycle {
  align-self: flex-start;
  margin-bottom: 6px;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.level--primaire .level__cycle {
  background: var(--vt-orange-50);
  color: var(--vt-orange-700);
}

.level--college .level__cycle {
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.level--lycee .level__cycle {
  background: var(--vt-navy-50);
  color: var(--vt-navy);
}

.level__name {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--vt-ink);
}

.level__count {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--vt-muted);
}

.level__note {
  padding: 1px 7px;
  border: 1px solid var(--vt-line-strong);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  color: var(--vt-ink-soft);
}

.level__arrow {
  position: absolute;
  top: 18px;
  right: 16px;
  width: 16px;
  height: 16px;
  color: var(--vt-navy);
  opacity: 0;
  transform: translateX(-4px);
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.level:hover .level__arrow {
  opacity: 1;
  transform: none;
}

.levels__links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 12px;
  margin-top: 36px;
}

.levels__links a {
  padding: 9px 16px;
  border: 1px solid var(--vt-line-strong);
  border-radius: 999px;
  background: #fff;
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-navy);
  text-decoration: none;
}

.levels__links a:hover {
  border-color: var(--vt-navy);
}

/* ---------- 5. Méthode ---------- */

.steps {
  position: relative;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.step {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 26px 24px;
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  background: #fff;
}

.step__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 14px;
  background: var(--vt-navy);
  color: #fff;
}

.step__icon svg {
  width: 24px;
  height: 24px;
}

.step__num {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--vt-green-700);
}

.step__title {
  font-size: 19px;
}

.step__text {
  margin: 10px 0 0;
  font-size: 15px;
  color: var(--vt-muted);
}

/* Texte au-dessus, appareils sur toute la largeur : les vidéos restent lisibles. */
.devices {
  margin-top: 96px;
}

.devices__copy {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  align-items: end;
  gap: 24px 64px;
}

.devices__visual {
  max-width: 1080px;
  margin: 56px auto 0;
}

.devices__title {
  font-size: clamp(26px, 2.6vw, 34px);
}

.devices__text {
  margin: 16px 0 0;
  font-size: 17px;
  color: var(--vt-muted);
}

.devices__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0 0 28px;
  padding: 0;
  list-style: none;
  font-size: 15px;
  font-weight: 600;
  color: var(--vt-ink-soft);
}

.devices__list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.devices__list svg {
  width: 18px;
  height: 18px;
  margin-top: 3px;
  flex-shrink: 0;
  stroke-width: 2.6;
  color: var(--vt-green-700);
}

.devices__caption {
  margin: 22px 0 0;
  text-align: center;
  font-size: 13px;
  font-weight: 500;
  color: var(--vt-muted);
}

/* ---------- 7. Professeur ---------- */

.prof {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(700px 400px at 100% 0%, rgba(95, 172, 96, 0.18), transparent 60%),
    var(--vt-navy);
  color: rgba(255, 255, 255, 0.82);
}

.prof__inner {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  align-items: center;
  gap: 72px;
}

.prof__portrait {
  position: relative;
  max-width: 420px;
  margin: 0 auto;
  padding: 24px 24px 0;
  border-radius: 28px;
  background: #fff;
  box-shadow: 0 30px 60px rgba(5, 14, 40, 0.35);
  overflow: hidden;
}

.prof__photo {
  display: block;
  width: 100%;
  height: auto;
}

.prof__name {
  position: absolute;
  left: 50%;
  bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: max-content;
  max-width: calc(100% - 32px);
  margin: 0;
  padding: 10px 18px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: var(--vt-shadow);
  transform: translateX(-50%);
  text-align: center;
  line-height: 1.35;
}

.prof__name strong {
  font-size: 16px;
  color: var(--vt-ink);
}

.prof__name span {
  font-size: 12px;
  font-weight: 600;
  color: var(--vt-muted);
}

.prof__kicker {
  color: var(--vt-green-300);
}

.prof .prof__title {
  color: #fff;
}

.prof__text {
  margin: 20px 0 0;
  font-size: 17px;
  line-height: 1.7;
}

.prof__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 26px 0 36px;
  padding: 0;
  list-style: none;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.prof__list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.prof__list svg {
  width: 20px;
  height: 20px;
  margin-top: 2px;
  flex-shrink: 0;
  stroke-width: 2.6;
  color: var(--vt-green-300);
}

.prof__ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

/* ---------- 8. FAQ ---------- */

.faq {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 64px;
  align-items: start;
}

.faq__contact {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 32px;
  padding: 22px;
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  background: var(--vt-bg-soft);
}

.faq__contact-title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--vt-ink);
}

.faq__contact-text {
  margin: 0 0 6px;
  font-size: 15px;
  color: var(--vt-muted);
}

.faq__contact-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  font-size: 15px;
  font-weight: 700;
  color: var(--vt-navy);
  text-decoration: none;
}

.faq__contact-link:hover {
  text-decoration: underline;
}

.faq__contact-link svg {
  width: 18px;
  height: 18px;
}

.faq__list {
  border-top: 1px solid var(--vt-line);
}

.faq__item {
  border-bottom: 1px solid var(--vt-line);
}

.faq__question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 22px 4px;
  font-size: 17px;
  font-weight: 700;
  color: var(--vt-ink);
  cursor: pointer;
  list-style: none;
}

.faq__question::-webkit-details-marker {
  display: none;
}

.faq__question:hover {
  color: var(--vt-navy);
}

.faq__chevron {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--vt-muted);
  transition: transform 0.2s ease;
}

.faq__item[open] .faq__chevron {
  transform: rotate(180deg);
  color: var(--vt-navy);
}

.faq__answer {
  margin: -6px 0 0;
  padding: 0 40px 24px 4px;
  font-size: 16px;
  line-height: 1.7;
  color: var(--vt-muted);
}

/* ---------- 9. Dernier appel ---------- */

.final {
  padding: 0 0 104px;
}

.final__card {
  position: relative;
  overflow: hidden;
  padding: 72px 40px;
  border-radius: 28px;
  background:
    radial-gradient(600px 300px at 15% 0%, rgba(95, 172, 96, 0.25), transparent 60%),
    linear-gradient(135deg, var(--vt-navy) 0%, var(--vt-navy-900) 100%);
  text-align: center;
}

.final__grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 28px 28px;
  -webkit-mask-image: radial-gradient(ellipse 60% 90% at 50% 50%, #000 10%, transparent 75%);
  mask-image: radial-gradient(ellipse 60% 90% at 50% 50%, #000 10%, transparent 75%);
  pointer-events: none;
}

.final .final__title {
  position: relative;
  max-width: 720px;
  margin: 0 auto;
  font-size: clamp(30px, 3.8vw, 46px);
  color: #fff;
}

.final__text {
  position: relative;
  max-width: 560px;
  margin: 18px auto 0;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
}

.final__ctas {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 36px;
}

/* ---------- Tablette ---------- */

@media (max-width: 1080px) {
  /* minmax(0, …) : la largeur des formules ne doit jamais élargir la colonne. */
  .hero__inner {
    grid-template-columns: minmax(0, 1fr);
    gap: 40px;
  }

  .hero__copy {
    max-width: 680px;
  }

  .hero__visual {
    max-width: 620px;
    width: 100%;
    margin: 0 auto;
  }

  .stats__list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .stats__item:nth-child(3) {
    border-left: 0;
  }

  .stats__item:nth-child(n + 3) {
    border-top: 1px solid var(--vt-line);
  }

  .paths {
    grid-template-columns: 1fr;
    max-width: 640px;
    margin: 0 auto;
    gap: 28px;
  }

  .levels {
    gap: 10px;
  }

  .level {
    padding: 14px 14px 12px;
  }

  .level__name {
    font-size: 19px;
  }

  .level__arrow {
    display: none;
  }

  .steps {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .devices {
    margin-top: 72px;
  }

  .devices__copy {
    grid-template-columns: 1fr;
    max-width: 640px;
  }

  .devices__list {
    margin-top: 4px;
  }

  .devices__visual {
    margin-top: 40px;
  }

  .prof__inner {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .prof__portrait {
    max-width: 360px;
  }

  .faq {
    grid-template-columns: 1fr;
    gap: 36px;
  }
}

/* ---------- Mobile ---------- */

@media (max-width: 760px) {
  .levels {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .level__arrow {
    display: block;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 36px 0 56px;
  }

  .hero__eyebrow {
    margin-bottom: 18px;
    padding: 6px 12px;
    font-size: 12px;
    line-height: 1.4;
  }

  .hero__title {
    font-size: clamp(38px, 11vw, 46px);
  }

  .hero__lead {
    margin-top: 20px;
    font-size: 17px;
  }

  .hero__ctas {
    flex-direction: column;
    margin-top: 28px;
  }

  .hero__ctas .vt-btn {
    width: 100%;
  }

  .hero__reassure {
    gap: 8px 16px;
    font-size: 13px;
  }

  .hero__rating {
    margin-top: 22px;
    padding-top: 18px;
  }

  .stats__item {
    padding: 22px 14px 22px 0;
  }

  .stats__item:nth-child(even) {
    padding-left: 16px;
  }

  .stats__value {
    font-size: 28px;
  }

  .stats__label {
    font-size: 14px;
  }

  .stats__detail {
    font-size: 13px;
  }

  .path {
    padding: 26px 20px 20px;
  }

  .path__icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
  }

  .path__points {
    margin: 16px 0 22px;
    padding-top: 16px;
  }

  .path__title {
    font-size: 21px;
  }

  .levels {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  .level {
    padding: 14px 14px 12px;
  }

  .level__name {
    font-size: 20px;
  }

  .level__arrow {
    opacity: 1;
    transform: none;
  }

  .levels__links {
    flex-direction: column;
    align-items: stretch;
  }

  .levels__links a {
    text-align: center;
  }

  .steps {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .step {
    flex-direction: row;
    align-items: flex-start;
    gap: 16px;
    padding: 20px 18px;
  }

  .step__icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
  }

  .step__num {
    margin-bottom: 2px;
  }

  .step__title {
    font-size: 18px;
  }

  .step__text {
    margin-top: 6px;
  }

  .devices__copy .vt-btn {
    width: 100%;
  }

  .devices__caption {
    margin-top: 16px;
    padding: 0 12px;
  }

  .prof__portrait {
    max-width: 300px;
    padding: 18px 18px 0;
  }

  .prof__text {
    font-size: 16px;
  }

  .prof__list {
    font-size: 15px;
  }

  .prof__ctas {
    flex-direction: column;
  }

  .prof__ctas .vt-btn {
    width: 100%;
  }

  .faq__question {
    padding: 18px 2px;
    font-size: 16px;
  }

  .faq__answer {
    padding: 0 8px 20px 2px;
    font-size: 15px;
  }

  .final {
    padding-bottom: 72px;
  }

  .final__card {
    padding: 48px 20px;
    border-radius: 22px;
  }

  .final__text {
    font-size: 16px;
  }

  .final__ctas {
    flex-direction: column;
  }

  .final__ctas .vt-btn {
    width: 100%;
  }
}
</style>
