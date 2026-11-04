<template>
  <VitrineLayout>
    <!-- 1. Accroche -->
    <section class="vt-page-hero">
      <div class="vt-container ab-hero">
        <div>
          <h1 class="ab-hero__h1">
            <span class="vt-kicker ab-hero__kicker">À propos d’OptiTAB</span>
            <span class="vt-sr-only"> – </span>
            <span class="vt-page-hero__title">Rendre les maths claires, <em>pour chaque élève.</em></span>
          </h1>
          <p class="vt-page-hero__lead">
            OptiTAB est né de plus de 15 ans de cours particuliers, et d’une conviction&nbsp;: chaque élève peut progresser
            quand on lui explique clairement, avec méthode, et qu’il peut s’entraîner sur des exercices bien corrigés.
          </p>
          <div class="vt-page-hero__actions">
            <button type="button" class="vt-btn vt-btn--primary" @click="scrollTo('histoire')">
              Lire notre histoire
              <ArrowDownIcon aria-hidden="true" />
            </button>
            <router-link to="/cours-particuliers" class="vt-btn vt-btn--ghost">Rencontrer Anthony</router-link>
          </div>
        </div>

        <ul class="vt-card ab-figures" aria-label="OptiTAB aujourd’hui">
          <li v-for="stat in vitrineStats" :key="stat.libelle">
            <span class="ab-figures__value">{{ stat.valeur }}</span>
            <span class="ab-figures__label">{{ stat.libelle }}</span>
            <span class="ab-figures__detail">{{ stat.detail }}</span>
          </li>
        </ul>
      </div>
    </section>

    <!-- 2. L'histoire, dans l'ordre -->
    <section id="histoire" class="vt-section">
      <div class="vt-container ab-story">
        <header v-reveal class="ab-story__intro">
          <p class="vt-kicker">Notre histoire</p>
          <h2 class="vt-title">D’une salle de cours à une plateforme pour tous</h2>
          <figure class="ab-founder">
            <img src="/images/professeurs/anthony.jpg" alt="Anthony Tabet, fondateur d’OptiTAB" width="479" height="521" loading="lazy" />
            <figcaption>
              <strong>Anthony Tabet</strong>
              <span>Fondateur · Ingénieur <span class="vt-nowrap">ISAE-SUPAERO</span></span>
            </figcaption>
          </figure>
        </header>
        <VitrineTimeline v-reveal="100" :etapes="HISTOIRE" />
      </div>
    </section>

    <!-- 3. Nos engagements -->
    <section class="vt-section vt-section--soft">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">Nos engagements</p>
          <h2 class="vt-title">Ce qui guide chaque cours et chaque exercice</h2>
        </header>
        <div class="ab-values">
          <article v-for="(valeur, i) in VALEURS" :key="valeur.titre" v-reveal="i * 80" class="vt-card ab-values__card">
            <span class="ab-values__icon"><component :is="valeur.icone" aria-hidden="true" /></span>
            <h3 class="ab-values__title">{{ valeur.titre }}</h3>
            <p class="ab-values__text">{{ valeur.texte }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- 4. Pour les parents -->
    <section class="vt-section">
      <div class="vt-container ab-parents">
        <div v-reveal class="ab-parents__copy">
          <p class="vt-kicker">Un mot pour les parents</p>
          <h2 class="vt-title">Vous voulez le meilleur pour votre enfant. Nous aussi.</h2>
          <p class="ab-parents__text">
            Des cours clairs et structurés, un suivi de ses progrès, des résultats concrets&nbsp;: OptiTAB a été pensé pour
            répondre à ces attentes, sans remplacer l’école mais en l’accompagnant.
          </p>
          <ul class="vt-checks ab-parents__list">
            <li>Des contenus conformes au programme officiel, du CE2 à la Terminale</li>
            <li>Un tableau de bord pour voir où en est votre enfant</li>
            <li>Une équipe joignable 7 jours sur 7, par WhatsApp ou e-mail</li>
            <li>Sans engagement&nbsp;: vous arrêtez quand vous voulez</li>
          </ul>
        </div>
        <aside v-reveal="100" class="ab-vision">
          <p class="ab-vision__label">Notre ambition</p>
          <p class="ab-vision__quote">
            Devenir la référence francophone du soutien scientifique en ligne, avec de nouvelles ressources chaque mois.
          </p>
          <div class="ab-vision__links">
            <a href="https://instagram.com/opti.tab" target="_blank" rel="noopener noreferrer" aria-label="OptiTAB sur Instagram">
              <img src="/icons/instagram.svg" alt="" width="20" height="20" />
            </a>
            <a href="https://tiktok.com/@optitab" target="_blank" rel="noopener noreferrer" aria-label="OptiTAB sur TikTok">
              <img src="/icons/tiktok.svg" alt="" width="20" height="20" />
            </a>
            <a href="https://facebook.com/optitab" target="_blank" rel="noopener noreferrer" aria-label="OptiTAB sur Facebook">
              <img src="/icons/facebook.svg" alt="" width="20" height="20" />
            </a>
            <span>@opti.tab</span>
          </div>
        </aside>
      </div>
    </section>

    <!-- 5. Dernier appel -->
    <VitrineFinalCta
      titre="Envie d’essayer la méthode ?"
      texte="Crée un compte gratuit pour tester un chapitre complet, ou parle directement avec Anthony."
    >
      <button type="button" class="vt-btn vt-btn--green" data-cta-name="signup" data-cta-location="about_final" @click="openRegister">
        Créer mon compte gratuit
        <ArrowRightIcon aria-hidden="true" />
      </button>
      <router-link to="/contact" class="vt-btn vt-btn--light">Nous contacter</router-link>
    </VitrineFinalCta>
  </VitrineLayout>
</template>

<script setup>
import {
  ArrowDownIcon,
  ArrowRightIcon,
  AcademicCapIcon,
  UserGroupIcon,
  MagnifyingGlassIcon,
  RocketLaunchIcon,
  SparklesIcon,
  LightBulbIcon,
  BookOpenIcon,
  PencilSquareIcon,
  HeartIcon
} from '@heroicons/vue/24/outline'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import VitrineTimeline from '@/components/vitrine/VitrineTimeline.vue'
import VitrineFinalCta from '@/components/vitrine/VitrineFinalCta.vue'
import { vReveal } from '@/components/vitrine/reveal'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { vitrineStats } from '@/config/vitrineContent'

const { openModal } = useModalManager()
const openRegister = () => openModal(MODAL_IDS.REGISTER)

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const HISTOIRE = [
  {
    etiquette: 'Au départ',
    icone: AcademicCapIcon,
    titre: 'Ingénieur avant d’être prof',
    texte: 'Anthony Tabet, diplômé de l’ISAE-SUPAERO et de l’ESIB, devient ingénieur calculateur de structures. Les maths et la physique sont ses outils de tous les jours.'
  },
  {
    etiquette: '15 ans d’enseignement',
    icone: UserGroupIcon,
    titre: 'Des centaines d’élèves accompagnés',
    texte: 'En parallèle, il donne des cours particuliers, notamment via Groupe Réussite, du collège à la prépa, en maths et en physique-chimie : plus de 300 élèves suivis.'
  },
  {
    etiquette: 'Le constat',
    icone: MagnifyingGlassIcon,
    titre: 'Les sciences paraissent difficiles, sans bons outils',
    texte: 'Une notion mal comprise, une méthode qui manque, trop peu d’exercices bien corrigés pour s’entraîner seul : c’est souvent là que tout se joue.'
  },
  {
    etiquette: 'La création',
    icone: RocketLaunchIcon,
    titre: 'OptiTAB voit le jour',
    texte: 'Une plateforme pour avoir, à chaque chapitre, un cours clair, une fiche de synthèse et des exercices corrigés pas à pas, avec un suivi de progression.'
  },
  {
    etiquette: 'Aujourd’hui',
    icone: SparklesIcon,
    titre: 'Tout le programme de maths, du CE2 à la Terminale',
    texte: '211 chapitres et plus de 3 300 exercices corrigés, enrichis chaque mois, et des cours particuliers pour les élèves qui ont besoin d’un professeur.'
  }
]

const VALEURS = [
  { icone: LightBulbIcon, titre: 'La clarté avant tout', texte: 'Des explications simples, des exemples concrets et des figures soignées.' },
  { icone: BookOpenIcon, titre: 'Le programme officiel', texte: 'Des contenus écrits par des enseignants, au plus près de ce qui est demandé en classe.' },
  { icone: PencilSquareIcon, titre: 'S’entraîner pour de vrai', texte: 'Chaque exercice est corrigé étape par étape, pour comprendre ses erreurs.' },
  { icone: HeartIcon, titre: 'Un humain derrière', texte: 'Un professeur joignable, des réponses rapides, et de la bienveillance.' }
]
</script>

<style scoped>
/* ---------- Accroche ---------- */

.ab-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 0.75fr);
  gap: 56px;
  align-items: center;
}

.ab-hero__h1 {
  margin: 0;
}

.ab-hero__kicker {
  display: block;
  margin-bottom: 14px;
}

.ab-figures {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin: 0;
  padding: 0;
  list-style: none;
  box-shadow: var(--vt-shadow-lg);
}

.ab-figures li {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 24px 22px;
}

.ab-figures li:nth-child(even) {
  border-left: 1px solid var(--vt-line);
}

.ab-figures li:nth-child(n + 3) {
  border-top: 1px solid var(--vt-line);
}

.ab-figures__value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--vt-navy);
}

.ab-figures__label {
  margin-top: 4px;
  font-size: 14px;
  font-weight: 700;
  color: var(--vt-ink);
}

.ab-figures__detail {
  font-size: 13px;
  color: var(--vt-muted);
}

/* ---------- Histoire ---------- */

.ab-story {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 64px;
  align-items: start;
}

.ab-story__intro {
  position: sticky;
  top: 104px;
}

.ab-founder {
  position: relative;
  max-width: 300px;
  margin: 32px 0 0;
}

.ab-founder img {
  display: block;
  width: 100%;
  height: auto;
  padding: 18px 18px 0;
  border: 1px solid var(--vt-line);
  border-radius: 22px;
  background: linear-gradient(180deg, #fff 0%, #eef2fa 100%);
}

.ab-founder figcaption {
  display: flex;
  flex-direction: column;
  margin: -40px 16px 0;
  padding: 12px 16px;
  position: relative;
  border: 1px solid var(--vt-line);
  border-radius: 14px;
  background: #fff;
  box-shadow: var(--vt-shadow);
  text-align: center;
}

.ab-founder strong {
  font-size: 16px;
  color: var(--vt-ink);
}

.ab-founder span {
  font-size: 12px;
  font-weight: 600;
  color: var(--vt-muted);
}

/* ---------- Engagements ---------- */

.ab-values {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.ab-values__card {
  padding: 26px 22px;
}

.ab-values__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.ab-values__icon :deep(svg) {
  width: 24px;
  height: 24px;
}

.ab-values__title {
  margin-top: 18px;
  font-size: 18px;
}

.ab-values__text {
  margin: 10px 0 0;
  font-size: 15px;
  color: var(--vt-muted);
}

/* ---------- Parents ---------- */

.ab-parents {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
  gap: 56px;
  align-items: center;
}

.ab-parents__text {
  margin: 18px 0 0;
  font-size: 17px;
  line-height: 1.7;
  color: var(--vt-muted);
}

.ab-parents__list {
  margin-top: 24px;
  font-size: 16px;
  font-weight: 600;
  color: var(--vt-ink-soft);
}

.ab-vision {
  padding: 32px 30px;
  border-radius: 24px;
  background:
    radial-gradient(400px 220px at 100% 0%, rgba(95, 172, 96, 0.25), transparent 60%),
    var(--vt-navy);
  color: #fff;
}

.ab-vision__label {
  margin: 0;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--vt-green-300);
}

.ab-vision__quote {
  margin: 14px 0 0;
  font-size: 21px;
  font-weight: 700;
  line-height: 1.45;
}

.ab-vision__links {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 26px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}

.ab-vision__links a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  transition: background-color 0.15s ease;
}

.ab-vision__links a:hover {
  background: rgba(255, 255, 255, 0.2);
}

.ab-vision__links img {
  filter: brightness(0) invert(1);
}

.ab-vision__links span {
  margin-left: 6px;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
}

/* ---------- Tablette et téléphone ---------- */

@media (max-width: 1080px) {
  .ab-hero,
  .ab-story,
  .ab-parents {
    grid-template-columns: minmax(0, 1fr);
    gap: 40px;
  }

  .ab-story__intro {
    position: static;
  }

  .ab-figures {
    max-width: 560px;
  }

  .ab-values {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .ab-figures li {
    padding: 18px 14px;
  }

  .ab-figures__value {
    font-size: 26px;
  }

  .ab-founder {
    display: none;
  }

  .ab-values {
    grid-template-columns: minmax(0, 1fr);
  }

  .ab-values__card {
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr);
    column-gap: 14px;
    align-items: center;
    padding: 18px 16px;
  }

  .ab-values__icon {
    width: 44px;
    height: 44px;
  }

  .ab-values__title {
    margin-top: 0;
  }

  .ab-values__text {
    grid-column: 1 / -1;
  }

  .ab-vision {
    padding: 26px 22px;
  }

  .ab-vision__quote {
    font-size: 19px;
  }
}
</style>
