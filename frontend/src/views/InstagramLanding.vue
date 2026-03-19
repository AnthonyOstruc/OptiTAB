<script setup>
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
import PricingPlans from '@/components/home/PricingPlans.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
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
    description: "Un entraînement progressif avec une logique de résolution facile à suivre."
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

const quickTrust = ['Sans engagement', 'Annulable à tout moment', 'Accès immédiat']
const heroStats = ['+150 chapitres', '+150 résumés', '+150 cours', '+1000 exercices']
</script>

<template>
  <div class="ig-page">
    <Header variant="landing" />
    <main class="ig-landing">
      <section class="ig-hero">
        <div class="ig-hero__content">
          <div class="ig-hero__copy">
            <p class="ig-hero__kicker">OptitTAB - Plateforme maths</p>
            <h1 class="ig-hero__title">Une plateforme maths pour progresser</h1>
            <p class="ig-hero__subtitle">Cours, fiches de synthèse et exercices corrigés pas à pas</p>
            <p class="ig-hero__supporting">
              Travaille plus efficacement, comprends mieux, progresse à ton rythme.
            </p>
            <button class="cta-primary" @click="openRegister">
              Créer mon compte gratuit
            </button>
            <div class="ig-hero__trust">
              <span v-for="item in quickTrust" :key="item" class="ig-hero__trust-chip">{{ item }}</span>
            </div>
          </div>

          <div class="ig-hero__side">
            <article class="ig-hero__offer-card">
              <p class="ig-hero__offer-title">Abonnements dès 4,99 €</p>
              <p class="ig-hero__offer-subtitle">Accès immédiat à la plateforme</p>
              <GoogleReviewsCompact />
            </article>

            <div class="ig-hero__stats">
              <article v-for="item in heroStats" :key="item" class="ig-hero__stat">
                <span class="ig-hero__stat-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.8" />
                    <path
                      d="M8.5 12.2L10.8 14.5L15.7 9.6"
                      stroke="currentColor"
                      stroke-width="1.9"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </span>
                <span class="ig-hero__stat-text">{{ item }}</span>
              </article>
            </div>
          </div>
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
          <p class="ig-section-subtitle">Un espace clair pour réviser, s'entraîner et suivre tes progrès.</p>
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

    <Footer variant="landing" />
  </div>
</template>

<style scoped lang="scss">
$primary: #667eea;
$primary-dark: #5a67d8;
$bleu: #2a38b7;
$text-dark: #0f172a;
$text: #475569;
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

.cta-primary {
  margin-top: 16px;
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

.ig-hero {
  background: linear-gradient(135deg, $white 0%, $bg-light 45%, $bg-section 100%);
  padding: 34px 16px;
}

.ig-hero__content {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  align-items: center;
  gap: 18px;
}

.ig-hero__kicker {
  margin: 0;
  color: #2a38b7;
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.ig-hero__title {
  margin: 8px 0 10px;
  font-size: clamp(1.72rem, 3.45vw, 2.72rem);
  line-height: 1.03;
  color: $text-dark;
}

.ig-hero__subtitle {
  margin: 0;
  color: #1e293b;
  font-size: 1.08rem;
  font-weight: 600;
}

.ig-hero__supporting {
  margin: 12px 0 0;
  color: #475569;
  font-size: 0.98rem;
}

.ig-hero__trust {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ig-hero__trust-chip {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid #cfe0ff;
  background: #eef4ff;
  color: #1e3a8a;
  font-size: 0.82rem;
  font-weight: 700;
}

.ig-hero__side {
  display: grid;
  align-content: start;
  gap: 10px;
}

.ig-hero__offer-card {
  width: 100%;
  background: linear-gradient(145deg, #f4f7ff 0%, #eef2ff 100%);
  border: 1px solid #cddcff;
  border-radius: 18px;
  padding: 18px;
  display: grid;
  gap: 10px;
}

.ig-hero__offer-title {
  margin: 0;
  color: #1e3a8a;
  font-size: 1.15rem;
  font-weight: 800;
}

.ig-hero__offer-subtitle {
  margin: 0;
  color: #334155;
  font-size: 0.92rem;
}

.ig-hero__stats {
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 10px;
}

.ig-hero__stat {
  min-height: 38px;
  border-radius: 10px;
  border: 1px solid #d7e3ff;
  background: linear-gradient(145deg, #f8fbff 0%, #f1f5ff 100%);
  padding: 0 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ig-hero__stat-icon {
  width: 16px;
  height: 16px;
  color: #2a38b7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ig-hero__stat-icon svg {
  width: 100%;
  height: 100%;
}

.ig-hero__stat-text {
  color: #1e293b;
  font-size: 0.85rem;
  font-weight: 700;
  line-height: 1.2;
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

@media (max-width: 960px) {
  .ig-hero__content {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 640px) {
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

@media (max-width: 640px) {
  .ig-hero__stats {
    gap: 8px;
  }

  .ig-hero__stat {
    min-height: 36px;
    padding: 0 8px;
  }

  .ig-hero__stat-text {
    font-size: 0.8rem;
  }

  .cta-primary {
    width: 100%;
  }
}
</style>
