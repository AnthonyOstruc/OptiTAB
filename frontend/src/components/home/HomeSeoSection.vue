<template>
  <section class="home-seo">
    <div class="home-seo__inner">
      <h2 class="home-seo__title">Deux solutions pour réussir</h2>
      <p class="home-seo__text">
        <span class="home-seo__text-line">
          Cours particuliers en ligne (maths, physique‑chimie, informatique) et plateforme de maths par abonnement.
        </span>
        <span class="home-seo__text-line">Cours, fiches de synthèse, exercices corrigés — du collège à l’université.</span>
      </p>
      <div class="home-seo__links" aria-label="Accès rapide">
        <router-link to="/cours-particuliers" class="home-seo__link">Cours particuliers</router-link>
        <router-link to="/ressources-gratuites/cours" class="home-seo__link">Cours gratuits</router-link>
        <router-link to="/ressources-gratuites/exercices" class="home-seo__link">Exercices gratuits</router-link>
        <router-link to="/ressources-gratuites/syntheses" class="home-seo__link">Synthèses gratuites</router-link>
        <button type="button" class="home-seo__link" @click="openContactModal('Demande d\'information')">Contact</button>
      </div>
      <div class="home-seo__trust" aria-label="Informations clés">
        <span class="trust-pill">Collège • Lycée • Prépa • Université</span>
        <span class="trust-pill">Cours en ligne, méthode &amp; corrections</span>
        <span class="trust-pill">Réponse sous 24h</span>
      </div>
      <h3 class="home-seo__offers-title">Deux offres</h3>
      <div class="home-seo__offers" aria-label="Deux offres OptiTAB">
        <article class="offer-card offer-card--subscription">
          <div class="offer-badge">📘 Abonnement</div>
          <h4 class="offer-title">Plateforme de maths (abonnement)</h4>
          <ul class="offer-list">
            <li>Cours structurés et fiches de synthèse</li>
            <li>Exercices corrigés (progressifs)</li>
            <li>Suivi de progression</li>
            <li>Accès immédiat, en autonomie</li>
          </ul>
          <a href="#tarifs" class="offer-cta primary">Voir les formules (Maths)</a>
          <p class="offer-note">Abonnement = maths uniquement.</p>
        </article>
        <article class="offer-card offer-card--tutoring">
          <div class="offer-badge">👨‍🏫 Cours particuliers</div>
          <h4 class="offer-title">Cours particuliers en ligne</h4>
          <ul class="offer-list">
            <li>Maths, physique‑chimie, informatique</li>
            <li>Aide aux devoirs / DM + méthode</li>
            <li>Préparation DS, bac, examens/concours</li>
            <li>Suivi personnalisé</li>
          </ul>
          <button type="button" class="offer-cta secondary" @click="openContactModal('Réserver un cours')">Réserver une séance</button>
          <p class="offer-note">Réponse sous 24h.</p>
        </article>
      </div>
      <p class="home-seo__note">Objectif&nbsp;: comprendre, s’entraîner et progresser avec une méthode claire.</p>
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

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;

.home-seo {
  background: #fff;
  padding: 18px 0 56px 0;
}

.home-seo__inner {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2vw;
  text-align: center;
}

.home-seo__title {
  font-size: 2.05rem;
  font-weight: 900;
  color: $bleu-principal;
  margin: 0 0 12px 0;
  line-height: 1.15;
}

.home-seo__text {
  color: #475569;
  font-size: 1.06rem;
  line-height: 1.7;
  margin: 0 auto 18px auto;
  max-width: 860px;
}

.home-seo__text-line {
  display: block;
}

.home-seo__links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin: 0 auto 14px auto;
}

.home-seo__trust {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin: 0 auto 18px auto;
}

.trust-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 0.92rem;
  color: #334155;
  background: rgba(15, 23, 42, 0.04);
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.home-seo__offers-title {
  margin: 18px 0 12px 0;
  font-size: 1.25rem;
  font-weight: 900;
  color: #0f172a;
}

.home-seo__offers {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  max-width: 980px;
  margin: 0 auto 12px auto;
}

.offer-card {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid rgba(42, 56, 183, 0.12);
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
  padding: 16px 16px 14px 16px;
  text-align: left;
}

.offer-card--subscription {
  background: linear-gradient(135deg, rgba(42, 56, 183, 0.06) 0%, #ffffff 60%);
}

.offer-card--tutoring {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, #ffffff 60%);
}

.offer-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 900;
  font-size: 0.9rem;
  color: $bleu-principal;
  background: rgba(42, 56, 183, 0.09);
  margin-bottom: 10px;
}

.offer-title {
  margin: 0 0 10px 0;
  font-size: 1.18rem;
  font-weight: 900;
  color: #0f172a;
}

.offer-list {
  margin: 0 0 12px 0;
  padding-left: 1.2rem;
  color: #334155;
  line-height: 1.6;
  font-weight: 600;
}

.offer-list li {
  margin: 0.15rem 0;
}

.offer-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 12px;
  border-radius: 12px;
  font-weight: 900;
  border: none;
  cursor: pointer;
  font-family: inherit;
  text-decoration: none;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}

.offer-cta.primary {
  background: $bleu-principal;
  color: #fff;
  box-shadow: 0 10px 22px rgba(42, 56, 183, 0.22);
}

.offer-cta.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 26px rgba(42, 56, 183, 0.28);
}

.offer-cta.secondary {
  background: rgba(42, 56, 183, 0.08);
  color: $bleu-principal;
}

.offer-cta.secondary:hover {
  background: rgba(42, 56, 183, 0.14);
  transform: translateY(-1px);
}

.offer-note {
  margin: 10px 0 0 0;
  color: #64748b;
  font-size: 0.92rem;
  font-weight: 600;
}

.home-seo__link {
  background: rgba(42, 56, 183, 0.08);
  color: $bleu-principal;
  text-decoration: none;
  border: none;
  padding: 10px 14px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.98rem;
  transition: background 0.15s ease, transform 0.15s ease;
  cursor: pointer;
  font-family: inherit;
}

.home-seo__link:hover {
  background: rgba(42, 56, 183, 0.14);
  transform: translateY(-1px);
}

.home-seo__note {
  color: #64748b;
  font-size: 0.98rem;
  margin: 0;
}

@media (max-width: 700px) {
  .home-seo {
    padding: 10px 0 26px 0;
  }

  .home-seo__inner {
    padding: 0 4vw;
  }

  .home-seo__title {
    font-size: 1.3rem;
  }

  .home-seo__text {
    font-size: 0.95rem;
    margin-bottom: 14px;
  }

  .home-seo__link {
    font-size: 0.9rem;
    padding: 9px 12px;
  }

  .home-seo__note {
    font-size: 0.92rem;
  }

  .home-seo__offers-title {
    font-size: 1.05rem;
    margin-top: 14px;
  }

  .home-seo__offers {
    grid-template-columns: repeat(2, minmax(280px, 1fr));
    gap: 12px;
    overflow-x: auto;
    overscroll-behavior-x: contain;
    -webkit-overflow-scrolling: touch;
    scroll-snap-type: x mandatory;
    padding: 0 4vw 8px 4vw;
    margin: 0 -4vw 12px -4vw;
    justify-content: start;
    scrollbar-width: none;
  }

  .home-seo__offers::-webkit-scrollbar {
    display: none;
  }

  .offer-card {
    scroll-snap-align: start;
  }

  .offer-title {
    font-size: 1.05rem;
  }

  .offer-list {
    font-size: 0.95rem;
  }

  .offer-note {
    font-size: 0.88rem;
  }
}
</style>
