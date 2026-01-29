<template>
  <section class="offers-section" itemscope itemtype="https://schema.org/WebPage">
    <div class="offers-section__inner">
      <!-- Header avec H1 -->
      <header class="offers-section__header">
        <h1 class="offers-section__title">Plateforme de maths en ligne et cours particuliers</h1>
      </header>

      <!-- Deux offres principales -->
      <div class="offers-section__grid">
        <article class="offer-card" itemscope itemtype="https://schema.org/Product">
          <meta itemprop="name" content="Abonnement plateforme de maths OptiTAB" />
          <span class="offer-card__badge">Abonnement</span>
          <h2 class="offer-card__title">Plateforme de maths en ligne</h2>
          <ul class="offer-card__list">
            <li>Cours structurés et fiches de synthèse</li>
            <li>Exercices corrigés progressifs</li>
            <li>Suivi de progression en autonomie</li>
            <li>Programme Première et Terminale + bases</li>
          </ul>
          <a href="#tarifs" class="offer-card__cta" itemprop="url">Découvrir l'abonnement</a>
          <span class="offer-card__hint">Première • Terminale • Spé maths • Bases</span>
        </article>

        <article class="offer-card" itemscope itemtype="https://schema.org/Service">
          <meta itemprop="name" content="Cours particuliers en ligne OptiTAB" />
          <span class="offer-card__badge">Cours particuliers</span>
          <h2 class="offer-card__title">Cours particuliers en visio</h2>
          <ul class="offer-card__list">
            <li>Maths, physique-chimie, informatique</li>
            <li>Préparation brevet, bac et concours</li>
            <li>Aide aux devoirs et méthode de travail</li>
            <li>Tous niveaux : collège à prépa</li>
          </ul>
          <router-link to="/cours-particuliers" class="offer-card__cta" itemprop="url">Réserver un cours</router-link>
          <span class="offer-card__hint">Collège • Lycée • Prépa • Réponse sous 24h</span>
        </article>
      </div>

      <!-- Liens internes optimisés -->
      <nav class="offers-section__nav" aria-label="Ressources gratuites">
        <router-link to="/ressources-gratuites/cours" class="offers-section__link">Cours gratuits de maths</router-link>
        <span class="offers-section__separator">•</span>
        <router-link to="/ressources-gratuites/exercices" class="offers-section__link">Exercices corrigés gratuits</router-link>
        <span class="offers-section__separator">•</span>
        <router-link to="/ressources-gratuites/syntheses" class="offers-section__link">Fiches de synthèse maths</router-link>
        <span class="offers-section__separator">•</span>
        <router-link to="/cours-particuliers" class="offers-section__link">Cours particuliers en visio</router-link>
      </nav>
    </div>

    <ContactModal
      :isOpen="isContactModalOpen"
      :initialSubject="contactModalSubject"
      @close="closeContactModal"
      @success="handleContactSuccess"
    />
  </section>
</template>

<script setup>
import { ref } from 'vue'
import ContactModal from '@/components/common/ContactModal.vue'

const isContactModalOpen = ref(false)
const contactModalSubject = ref('')

const openContactModal = (subject = '') => {
  contactModalSubject.value = subject
  isContactModalOpen.value = true
}

const closeContactModal = () => {
  isContactModalOpen.value = false
  contactModalSubject.value = ''
}

const handleContactSuccess = (message) => {
  alert(message)
}
</script>

<style scoped>
.offers-section {
  background: #f8fafc;
  padding: 72px 0;
}

.offers-section__inner {
  max-width: 920px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
.offers-section__header {
  text-align: center;
  margin-bottom: 56px;
}

.offers-section__title {
  font-size: 2.1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  line-height: 1.25;
  letter-spacing: -0.02em;
}

/* Offres */
.offers-section__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
  margin-bottom: 40px;
}

.offer-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: box-shadow 0.25s ease, transform 0.25s ease, border-color 0.25s ease;
}

.offer-card:hover {
  box-shadow: 0 12px 40px rgba(42, 56, 183, 0.1);
  transform: translateY(-4px);
  border-color: rgba(42, 56, 183, 0.2);
}

.offer-card__badge {
  display: inline-block;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #2a38b7;
  background: rgba(42, 56, 183, 0.1);
  margin-bottom: 20px;
}

.offer-card__title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

.offer-card__list {
  list-style: none;
  padding: 0;
  margin: 0 0 28px 0;
  flex-grow: 1;
}

.offer-card__list li {
  position: relative;
  padding-left: 24px;
  font-size: 0.95rem;
  color: #475569;
  line-height: 1.7;
  margin-bottom: 10px;
}

.offer-card__list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
}

.offer-card__list li:last-child {
  margin-bottom: 0;
}

.offer-card__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 16px 28px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  font-family: inherit;
  text-decoration: none;
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, #2a38b7 0%, #3d4cc9 100%);
  color: #ffffff;
  box-shadow: 0 4px 16px rgba(42, 56, 183, 0.25);
  transition: all 0.2s ease;
  margin-bottom: 16px;
}

.offer-card__cta:hover {
  background: linear-gradient(135deg, #232fa0 0%, #3541b5 100%);
  box-shadow: 0 6px 24px rgba(42, 56, 183, 0.35);
  transform: translateY(-2px);
}

.offer-card__hint {
  font-size: 0.85rem;
  color: #94a3b8;
  text-align: center;
  width: 100%;
  font-weight: 500;
}

/* Navigation liens */
.offers-section__nav {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 56px;
}

.offers-section__link {
  font-size: 0.95rem;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s ease;
  padding: 8px 4px;
}

.offers-section__link:hover {
  color: #2a38b7;
}

.offers-section__separator {
  color: #cbd5e1;
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .offers-section {
    padding: 48px 0;
  }

  .offers-section__inner {
    padding: 0 20px;
  }

  .offers-section__header {
    margin-bottom: 36px;
  }

  .offers-section__title {
    font-size: 1.6rem;
  }

  .offers-section__intro {
    font-size: 0.95rem;
  }

  .offers-section__grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 32px;
  }

  .offer-card {
    padding: 28px 24px;
    border-radius: 16px;
  }

  .offer-card__badge {
    padding: 6px 12px;
    font-size: 0.7rem;
    margin-bottom: 16px;
  }

  .offer-card__title {
    font-size: 1.2rem;
    margin-bottom: 16px;
  }

  .offer-card__list {
    margin-bottom: 24px;
  }

  .offer-card__list li {
    font-size: 0.9rem;
    margin-bottom: 8px;
    padding-left: 20px;
  }

  .offer-card__list li::before {
    width: 6px;
    height: 6px;
    top: 9px;
  }

  .offer-card__cta {
    padding: 14px 24px;
    font-size: 0.95rem;
    border-radius: 10px;
  }

  .offer-card__hint {
    font-size: 0.8rem;
  }

  .offers-section__nav {
    margin-bottom: 40px;
    gap: 8px;
  }

  .offers-section__link {
    font-size: 0.85rem;
  }
}
</style>
