<script setup>
import Header from '@/components/layout/Header.vue'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { useRouter } from 'vue-router'

const { openModal } = useModalManager()
const router = useRouter()

const openRegister = () => {
  openModal(MODAL_IDS.REGISTER)
}

const goToTarifs = () => {
  router.push({ name: 'TarifsPage' })
}

const benefits = [
  {
    icon: '✏️',
    title: 'Exercices guidés',
    description: 'Des corrections pas à pas pour progresser à ton rythme.'
  },
  {
    icon: '📄',
    title: 'Fiches claires',
    description: 'Des fiches synthétiques et faciles à comprendre.'
  },
  {
    icon: '📊',
    title: 'Révisions par niveau',
    description: 'Un contenu adapté à ton niveau : Bases, 2nde, 1re et Tle.'
  },
  {
    icon: '🧮',
    title: 'Outils de calcul',
    description: 'Des outils intégrés pour calculer, vérifier et réviser plus vite.'
  }
]

const subscriptionPoints = [
  'Exercices guidés',
  'Fiches synthétiques',
  'Révisions par niveau',
  'Outils de calcul intégrés'
]
</script>

<template>
  <div class="ig-page">
    <Header />
    <main class="ig-landing">

      <!-- Section 1 — Hero -->
      <section class="ig-hero">
        <div class="ig-hero__content">
          <span class="ig-hero__badge">Bases · 2nde · 1re · Tle</span>
          <h1 class="ig-hero__title">
            Teste gratuitement la <span class="ig-hero__highlight">plateforme de maths</span>
          </h1>
          <p class="ig-hero__supporting">
            Cours, fiches, exercices guidés et outils de calcul pour réviser et progresser à ton rythme.
          </p>
          <button class="ig-cta ig-cta--primary ig-cta--hero" @click="openRegister">
            Tester gratuitement la plateforme
          </button>
          <p class="ig-hero__reassurance">Sans engagement · Accès immédiat</p>
        </div>
      </section>

      <!-- Section 2 — Ce que tu débloques gratuitement -->
      <section class="ig-unlock">
        <div class="ig-unlock__container">
          <h2 class="ig-section-title">Accède gratuitement à l’essentiel</h2>
          <p class="ig-unlock__subtitle">
            Un aperçu clair de la plateforme pour commencer à progresser en maths.
          </p>
          <div class="ig-unlock__grid">
            <article class="ig-unlock__item">
              <h3 class="ig-unlock__item-title">Cours structurés</h3>
              <p class="ig-unlock__item-desc">Des notions claires et progressives.</p>
            </article>
            <article class="ig-unlock__item">
              <h3 class="ig-unlock__item-title">Fiches de synthèse</h3>
              <p class="ig-unlock__item-desc">L’essentiel à retenir en un coup d’œil.</p>
            </article>
            <article class="ig-unlock__item">
              <h3 class="ig-unlock__item-title">Exercices guidés</h3>
              <p class="ig-unlock__item-desc">Des entraînements progressifs avec corrections.</p>
            </article>
            <article class="ig-unlock__item">
              <h3 class="ig-unlock__item-title">Outils de calcul</h3>
              <p class="ig-unlock__item-desc">Des outils intégrés pour vérifier et avancer plus vite.</p>
            </article>
          </div>
          <button class="ig-cta ig-cta--primary" @click="openRegister">Créer mon compte gratuit</button>
          <p class="ig-unlock__note">Gratuit • Sans carte bancaire</p>
        </div>
      </section>

      <!-- Section 3 — Platform preview -->
      <section class="ig-preview">
        <div class="ig-preview__container">
          <h2 class="ig-section-title">Découvre la plateforme</h2>
          <p class="ig-section-subtitle">Un espace clair pour réviser, s'entraîner et progresser à ton rythme.</p>
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

      <!-- Section 4 — Benefits -->
      <section class="ig-benefits">
        <div class="ig-benefits__container">
          <h2 class="ig-section-title">Pourquoi OptiTAB ?</h2>
          <div class="ig-benefits__grid">
            <div
              v-for="(benefit, index) in benefits"
              :key="index"
              class="ig-benefit-card"
            >
              <span class="ig-benefit-card__icon">{{ benefit.icon }}</span>
              <h3 class="ig-benefit-card__title">{{ benefit.title }}</h3>
              <p class="ig-benefit-card__desc">{{ benefit.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 5 — Transition gratuit → payant -->
      <section class="ig-transition">
        <div class="ig-transition__container">
          <div class="ig-transition__eyebrow">Déjà convaincu ?</div>
          <h2 class="ig-transition__title">Envie d'aller plus loin ?</h2>
          <p class="ig-transition__text">
            Le chapitre démo te permet de découvrir la méthode OptiTAB.<br>
            Pour accéder à tous les chapitres, fiches et exercices, passe à l'abonnement.
          </p>
        </div>
      </section>

      <!-- Section 6 — Subscription block -->
      <section class="ig-subscription">
        <div class="ig-subscription__container">
          <div class="ig-subscription__card">
            <h2 class="ig-subscription__title">Découvre l'abonnement OptiTAB</h2>
            <p class="ig-subscription__text">
              Débloque tous les chapitres, plus de fiches, plus d'exercices guidés et plus de révisions adaptées à ton niveau.
            </p>
            <ul class="ig-subscription__points">
              <li v-for="point in subscriptionPoints" :key="point">
                <span class="ig-subscription__check">✓</span> {{ point }}
              </li>
            </ul>
            <button class="ig-subscription__cta" @click="goToTarifs">
              Voir l'abonnement →
            </button>
          </div>
        </div>
      </section>

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
/* ───── Tokens (palette OptiTAB) ───── */
$primary: #667eea;
$primary-dark: #5a67d8;
$bleu: #2a38b7;
$indigo: #6366f1;
$violet: #8b5cf6;
$rose: #ec4899;
$vert: #10b981;
$text-dark: #0f172a;
$text: #475569;
$text-light: #64748b;
$white: #fff;
$bg-light: #f8fafc;
$bg-section: #f1f5f9;
$radius: 16px;
$shadow: 0 4px 24px rgba(42, 56, 183, 0.10);

/* ═══════════════════════════════════════
   Page shell
   ═══════════════════════════════════════ */
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

/* ═══════════════════════════════════════
   Main content
   ═══════════════════════════════════════ */
.ig-landing {
  flex: 1;
  width: 100%;
  overflow-x: hidden;
}

/* ───── Shared ───── */
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
  max-width: 480px;
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

  &--secondary {
    background: transparent;
    color: $white;
    border: 2px solid rgba($white, 0.5);

    &:hover {
      background: rgba($white, 0.12);
      border-color: $white;
    }
  }

  &--hero {
    padding: 16px 36px;
    font-size: 1.05rem;
    width: 100%;
    max-width: 320px;
  }
}

/* ═══════════════════════════════════════
   Section 1 — Hero
   ═══════════════════════════════════════ */
.ig-hero {
  background: linear-gradient(135deg, $white 0%, $bg-light 40%, $bg-section 80%, #e2e8f0 100%);
  padding: 2.5rem 1.25rem 2.75rem;
  text-align: center;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -30%;
    right: -15%;
    width: 380px;
    height: 380px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba($bleu, 0.04) 0%, transparent 70%);
    pointer-events: none;
  }
}

.ig-hero__content {
  max-width: 520px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
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
  font-weight: 900;
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
  letter-spacing: 0.01em;
}

/* ═══════════════════════════════════════
   Section 2 — Ce que tu débloques
   ═══════════════════════════════════════ */
.ig-unlock {
  padding: 2.5rem 1.25rem;
  background: $white;
  text-align: center;
}

.ig-unlock__container {
  max-width: 860px;
  margin: 0 auto;
}

.ig-unlock__subtitle {
  max-width: 560px;
  margin: 0 auto 1.2rem;
  font-size: 0.96rem;
  color: $text;
  line-height: 1.55;
}

.ig-unlock__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.85rem;
  margin: 1.2rem 0 1.7rem;
}

.ig-unlock__item {
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

.ig-unlock__item-title {
  margin: 0 0 0.35rem;
  font-size: 1.02rem;
  font-weight: 750;
  color: $text-dark;
  letter-spacing: -0.01em;
}

.ig-unlock__item-desc {
  margin: 0;
  font-size: 0.86rem;
  color: $text;
  line-height: 1.45;
}

.ig-unlock__note {
  margin-top: 0.7rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: $text-light;
}

/* ═══════════════════════════════════════
   Section 3 — Preview
   ═══════════════════════════════════════ */
.ig-preview {
  padding: 2.5rem 1.25rem;
  background: $white;
}

.ig-preview__container {
  max-width: 560px;
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

/* ═══════════════════════════════════════
   Section 4 — Benefits
   ═══════════════════════════════════════ */
.ig-benefits {
  padding: 2.5rem 1.25rem;
  background: $bg-light;
}

.ig-benefits__container {
  max-width: 800px;
  margin: 0 auto;
}

.ig-benefits__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.ig-benefit-card {
  background: $white;
  border-radius: 14px;
  padding: 1rem 1.15rem;
  text-align: center;
  box-shadow: 0 2px 16px rgba(42, 56, 183, 0.07);
  border: 1px solid rgba($indigo, 0.06);
}

.ig-benefit-card__icon {
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  margin: 0 auto 0.4rem;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba($indigo, 0.08), rgba(59, 130, 246, 0.06));
}

.ig-benefit-card__title {
  font-size: 0.95rem;
  font-weight: 700;
  color: $text-dark;
  margin-bottom: 0.2rem;
}

.ig-benefit-card__desc {
  font-size: 0.84rem;
  color: $text;
  line-height: 1.45;
}

/* ═══════════════════════════════════════
   Section 5 — Transition
   ═══════════════════════════════════════ */
.ig-transition {
  padding: 2.5rem 1.25rem;
  background: $white;
  text-align: center;
}

.ig-transition__container {
  max-width: 500px;
  margin: 0 auto;
}

.ig-transition__title {
  font-size: 1.15rem;
  font-weight: 800;
  color: $text-dark;
  margin-bottom: 0.75rem;
}

.ig-transition__text {
  font-size: 1rem;
  color: $text;
  line-height: 1.6;
  margin-bottom: 0;
}

/* ═══════════════════════════════════════
   Section 6 — Subscription
   ═══════════════════════════════════════ */
.ig-subscription {
  padding: 3rem 1.25rem 4rem;
  background: $bg-section;
  text-align: center;
}

.ig-subscription__container {
  max-width: 540px;
  margin: 0 auto;
}

.ig-subscription__card {
  background: linear-gradient(160deg, #1a2580 0%, $bleu 40%, #3a4fd4 100%);
  border: none;
  border-radius: 20px;
  padding: 2.25rem 1.5rem;
}

.ig-subscription__title {
  font-size: 1.55rem;
  font-weight: 900;
  color: #fff;
  margin-bottom: 0.85rem;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.ig-subscription__text {
  font-size: 1.05rem;
  color: rgba(255,255,255,0.82);
  line-height: 1.65;
  margin-bottom: 1.5rem;
}

.ig-subscription__points {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem;
  display: flex;
  justify-content: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.ig-subscription__points li {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  white-space: nowrap;
}

.ig-subscription__check {
  color: #6ee7b7;
  font-weight: 700;
  margin-right: 4px;
}

.ig-subscription__cta {
  display: inline-block;
  padding: 16px 40px;
  background: #fff;
  color: $bleu;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 6px 24px rgba(0,0,0,0.18);
  -webkit-tap-highlight-color: transparent;
  letter-spacing: 0.01em;

  &:hover {
    background: #f1f5ff;
    transform: translateY(-2px);
    box-shadow: 0 10px 32px rgba(0,0,0,0.22);
  }

  &:active {
    transform: scale(0.97);
  }
}

/* ═══════════════════════════════════════
   Footer (minimal, light)
   ═══════════════════════════════════════ */
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
  color: rgba(255,255,255,0.55);
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #fff;
  }

  &--contact {
    font-weight: 500;
    color: rgba(255,255,255,0.75);
  }
}

.ig-footer__copy {
  font-weight: 600;
  color: rgba(255,255,255,0.75);
}

/* ═══════════════════════════════════════
   Responsive — tablet + desktop
   ═══════════════════════════════════════ */
@media (min-width: 640px) {
  .ig-hero {
    padding: 4rem 2rem 3.5rem;
  }

  .ig-hero__title {
    font-size: 2rem;
  }

  .ig-hero__badge {
    font-size: 0.85rem;
    padding: 8px 22px;
  }

  .ig-cta--hero {
    width: auto;
    max-width: none;
  }

  .ig-section-title {
    font-size: 1.6rem;
  }

  .ig-preview,
  .ig-unlock,
  .ig-benefits,
  .ig-transition,
  .ig-subscription {
    padding: 3.5rem 2rem;
  }

  .ig-unlock__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }

  .ig-unlock__item {
    text-align: center;
    padding: 1.1rem 1rem;
    min-height: 130px;
  }

  .ig-transition__title {
    font-size: 1.65rem;
  }

  .ig-subscription__title {
    font-size: 1.8rem;
  }

  .ig-subscription__card {
    padding: 2.75rem 2.5rem;
  }
}

@media (max-width: 639px) {
  .ig-benefits__grid {
    grid-template-columns: 1fr;
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
