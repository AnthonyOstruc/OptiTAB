<script setup>
import Header from '@/components/layout/Header.vue'
import PricingPlans from '@/components/home/PricingPlans.vue'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

const { openModal } = useModalManager()

const openRegister = () => {
  openModal(MODAL_IDS.REGISTER)
}

const scrollToAbonnements = () => {
  const target = document.getElementById('tarifs')
  if (!target) return
  target.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const freeFeatures = [
  {
    title: 'Cours structurés',
    description: 'Des notions organisées étape par étape pour avancer sereinement.'
  },
  {
    title: 'Fiches de synthèse',
    description: 'Les formules et méthodes essentielles en version claire et rapide à relire.'
  },
  {
    title: 'Exercices guidés',
    description: 'Un entraînement progressif avec une logique de résolution facile à suivre.'
  },
  {
    title: 'Outils de calcul',
    description: 'Des outils intégrés pour vérifier, comprendre et gagner du temps.'
  }
]

const subscriptionPoints = [
  'Tous les chapitres',
  'Fiches et exercices guidés',
  'Révisions adaptées à ton niveau',
  'Outils de calcul et graphes'
]
</script>

<template>
  <div class="ig-page">
    <Header />
    <main class="ig-landing">
      <section class="ig-hero">
        <div class="ig-hero__content">
          <span class="ig-hero__badge">Bases · 2nde · 1re · Tle</span>
          <h1 class="ig-hero__title">
            Révise les maths avec une <span class="ig-hero__highlight">méthode claire et guidée</span>
          </h1>
          <p class="ig-hero__supporting">
            Une plateforme simple pour comprendre les notions, s entraîner efficacement et progresser chaque semaine.
          </p>
          <button class="ig-cta ig-cta--primary ig-cta--hero" @click="openRegister">
            Créer mon compte gratuit
          </button>
          <p class="ig-hero__reassurance">Sans engagement · Accès immédiat</p>
        </div>
      </section>

      <section class="ig-features">
        <div class="ig-features__container">
          <h2 class="ig-section-title">Accède gratuitement à l'essentiel</h2>
          <p class="ig-section-subtitle">
            Tout ce qu'il faut pour commencer et prendre de bonnes habitudes de travail.
          </p>
          <div class="ig-features__grid">
            <article v-for="feature in freeFeatures" :key="feature.title" class="ig-feature-card">
              <h3 class="ig-feature-card__title">{{ feature.title }}</h3>
              <p class="ig-feature-card__desc">{{ feature.description }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="ig-preview">
        <div class="ig-preview__container">
          <h2 class="ig-section-title">Aperçu de la plateforme</h2>
          <p class="ig-section-subtitle">Un espace clair pour réviser, s entraîner et suivre tes progrès.</p>
          <div class="ig-preview__gif-wrapper">
            <img
              src="/video/optitab-demo-exercices.gif"
              alt="Démonstration de la plateforme OptiTAB"
              class="ig-preview__gif"
              loading="lazy"
            />
          </div>
        </div>
      </section>

      <section class="ig-subscription">
        <div class="ig-subscription__container">
          <h2 class="ig-subscription__title">Débloque toute la plateforme</h2>
          <p class="ig-subscription__text">
            Après le chapitre démo, accède à plus de contenu pour réviser de façon claire et structurée.
          </p>
          <ul class="ig-subscription__points">
            <li v-for="point in subscriptionPoints" :key="point">
              <span class="ig-subscription__check">✓</span> {{ point }}
            </li>
          </ul>
          <button class="ig-cta ig-cta--primary ig-subscription__cta" @click="scrollToAbonnements">
            Voir l'abonnement
          </button>
        </div>
      </section>

      <PricingPlans />
    </main>

    <footer class="ig-footer">
      <div class="ig-footer__inner">
        <span class="ig-footer__copy">© {{ new Date().getFullYear() }} OptiTAB</span>
        <span class="ig-footer__sep">·</span>
        <router-link to="/legal" class="ig-footer__link">Mentions légales</router-link>
        <span class="ig-footer__sep">·</span>
        <router-link to="/confidentialite" class="ig-footer__link">Confidentialité</router-link>
        <span class="ig-footer__sep">·</span>
        <router-link to="/cgu" class="ig-footer__link">CGU</router-link>
        <span class="ig-footer__sep ig-footer__sep--wide">|</span>
        <a href="mailto:contact@optitab.net" class="ig-footer__link ig-footer__link--contact">contact@optitab.net</a>
      </div>
    </footer>
  </div>
</template>

<style scoped lang="scss">
$primary: #667eea;
$primary-dark: #5a67d8;
$bleu: #2a38b7;
$indigo: #6366f1;
$text-dark: #0f172a;
$text: #475569;
$text-light: #64748b;
$white: #fff;
$bg-light: #f8fafc;
$bg-section: #f1f5f9;
$radius: 16px;
$shadow: 0 4px 24px rgba(42, 56, 183, 0.1);

.ig-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-top: 64px;
}

@media (max-width: 880px) {
  .ig-page {
    padding-top: 56px;
  }
}

.ig-landing {
  flex: 1;
  width: 100%;
  overflow-x: hidden;
}

.ig-section-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: $text-dark;
  text-align: center;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.ig-section-subtitle {
  font-size: 0.95rem;
  color: $text;
  text-align: center;
  line-height: 1.55;
  margin-bottom: 1.5rem;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
}

.ig-cta {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.25s ease;
  -webkit-tap-highlight-color: transparent;

  &:active {
    transform: scale(0.97);
  }

  &--primary {
    background: $primary;
    color: $white;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.35);

    &:hover {
      background: $primary-dark;
      box-shadow: 0 6px 22px rgba(102, 126, 234, 0.45);
      transform: translateY(-1px);
    }
  }

  &--hero {
    padding: 16px 36px;
    font-size: 1.05rem;
    width: 100%;
    max-width: 320px;
  }
}

.ig-hero {
  background: linear-gradient(135deg, $white 0%, $bg-light 45%, $bg-section 100%);
  padding: 2.8rem 1.25rem 3rem;
  text-align: center;
}

.ig-hero__content {
  max-width: 560px;
  margin: 0 auto;
}

.ig-hero__badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba($indigo, 0.1), rgba(59, 130, 246, 0.08));
  border: 1px solid rgba($indigo, 0.2);
  border-radius: 50px;
  padding: 6px 18px;
  font-size: 0.8rem;
  font-weight: 600;
  color: $indigo;
  margin-bottom: 1.25rem;
  letter-spacing: 0.02em;
}

.ig-hero__title {
  font-size: 1.5rem;
  font-weight: 900;
  line-height: 1.3;
  margin-bottom: 0.85rem;
  color: $text-dark;
  letter-spacing: -0.02em;
}

.ig-hero__highlight {
  background: linear-gradient(135deg, $bleu 0%, $primary 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.ig-hero__supporting {
  font-size: 0.95rem;
  color: $text;
  margin-bottom: 1.75rem;
  line-height: 1.55;
}

.ig-hero__reassurance {
  margin-top: 0.75rem;
  font-size: 0.78rem;
  color: $text-light;
}

.ig-features {
  padding: 2.5rem 1.25rem;
  background: $white;
}

.ig-features__container {
  max-width: 860px;
  margin: 0 auto;
}

.ig-features__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.85rem;
  margin-top: 1.1rem;
}

.ig-feature-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1rem 1.05rem;
  text-align: center;
  box-shadow: 0 1px 10px rgba(15, 23, 42, 0.04);
  min-height: 118px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.ig-feature-card__title {
  margin: 0 0 0.35rem;
  font-size: 1.02rem;
  font-weight: 750;
  color: $text-dark;
  letter-spacing: -0.01em;
}

.ig-feature-card__desc {
  margin: 0;
  font-size: 0.86rem;
  color: $text;
  line-height: 1.45;
}

.ig-preview {
  padding: 2.5rem 1.25rem;
  background: $white;
}

.ig-preview__container {
  max-width: 620px;
  margin: 0 auto;
}

.ig-preview__gif-wrapper {
  border-radius: $radius;
  overflow: hidden;
  box-shadow: $shadow;
  border: 1px solid rgba($bleu, 0.06);
}

.ig-preview__gif {
  display: block;
  width: 100%;
  height: auto;
}

.ig-subscription {
  padding: 2.5rem 1.25rem 3rem;
  background: $white;
  text-align: center;
}

.ig-subscription__container {
  max-width: 760px;
  margin: 0 auto;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
  padding: 1.5rem 1.2rem;
}

.ig-subscription__title {
  font-size: 1.25rem;
  font-weight: 800;
  color: $text-dark;
  margin-bottom: 0.55rem;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.ig-subscription__text {
  max-width: 620px;
  margin: 0 auto 1rem;
  font-size: 0.92rem;
  color: $text;
  line-height: 1.5;
}

.ig-subscription__points {
  list-style: none;
  padding: 0;
  margin: 0 0 1.15rem;
  display: grid;
  gap: 0.55rem;
  text-align: left;
}

.ig-subscription__points li {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: $text-dark;
  line-height: 1.35;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.6rem 0.75rem;
}

.ig-subscription__check {
  color: #2563eb;
  font-weight: 700;
  line-height: 1;
}

.ig-subscription__cta {
  margin-top: 0.25rem;
}

.ig-footer {
  background: #13205e;
  padding: 1.25rem 1rem;
}

.ig-footer__inner {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  color: $text-light;
}

.ig-footer__sep {
  color: #cbd5e1;
  user-select: none;

  &--wide {
    margin-left: 0.25rem;
    margin-right: 0.25rem;
  }
}

.ig-footer__link {
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #fff;
  }

  &--contact {
    font-weight: 500;
    color: rgba(255, 255, 255, 0.75);
  }
}

.ig-footer__copy {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
}

@media (min-width: 640px) {
  .ig-hero {
    padding: 4rem 2rem 3.6rem;
  }

  .ig-hero__title {
    font-size: 2rem;
  }

  .ig-cta--hero {
    width: auto;
    max-width: none;
  }

  .ig-section-title {
    font-size: 1.6rem;
  }

  .ig-features,
  .ig-preview,
  .ig-subscription {
    padding: 3.5rem 2rem;
  }

  .ig-features__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }

  .ig-feature-card {
    padding: 1.1rem 1rem;
    min-height: 130px;
  }

  .ig-subscription__container {
    padding: 2rem 1.8rem;
  }

  .ig-subscription__title {
    font-size: 1.55rem;
  }

  .ig-subscription__points {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.7rem 0.9rem;
  }
}

@media (min-width: 1024px) {
  .ig-hero {
    padding: 5rem 2rem 4.5rem;
  }

  .ig-hero__title {
    font-size: 2.35rem;
  }
}
</style>
