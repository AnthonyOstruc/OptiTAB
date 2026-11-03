<template>
  <VitrineLayout>
    <!-- 1. Accroche -->
    <section class="vt-page-hero">
      <div class="vt-container tf-hero">
        <h1 class="tf-hero__h1">
          <span class="vt-kicker tf-hero__kicker">Tarifs</span>
          <span class="vt-sr-only"> – </span>
          <span class="vt-page-hero__title">Des formules simples, <em>sans engagement.</em></span>
        </h1>
        <p class="vt-page-hero__lead">
          Commence gratuitement, puis choisis la durée qui correspond à tes révisions&nbsp;: une journée, une semaine, un mois
          ou toute l’année.
        </p>
        <div class="vt-page-hero__actions">
          <button type="button" class="vt-btn vt-btn--primary" @click="scrollTo('formules')">
            Voir les formules
            <ArrowDownIcon aria-hidden="true" />
          </button>
          <router-link to="/ressources-gratuites" class="vt-btn vt-btn--ghost" data-cta-name="free_resources" data-cta-location="tarifs_hero">
            Essayer gratuitement
          </router-link>
        </div>
        <ul class="vt-page-hero__reassure">
          <li>Dès 3,99&nbsp;€</li>
          <li>Annulable à tout moment</li>
          <li>Paiement sécurisé</li>
        </ul>
      </div>
    </section>

    <!-- 2. Les formules, du gratuit à l'abonnement -->
    <section id="formules" class="vt-section vt-section--soft">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">Les formules</p>
          <h2 class="vt-title">Trois étapes, à ton rythme</h2>
          <p class="vt-lead">Tu découvres sans payer, puis tu débloques ta classe en entier quand tu es prêt.</p>
        </header>
        <VitrinePricing v-reveal />
      </div>
    </section>

    <!-- 3. Ce que débloque l'abonnement -->
    <section class="vt-section">
      <div class="vt-container">
        <header v-reveal class="vt-heading">
          <p class="vt-kicker">Comparer</p>
          <h2 class="vt-title">Ce que débloque l’abonnement</h2>
          <p class="vt-lead">Chaque abonnement ou pass donne accès à toute une classe, choisie au moment du paiement.</p>
        </header>
        <div v-reveal class="vt-card tf-compare">
          <table class="tf-table">
            <thead>
              <tr>
                <th scope="col"><span class="vt-sr-only">Contenu</span></th>
                <th scope="col">Sans inscription</th>
                <th scope="col">Compte gratuit</th>
                <th scope="col" class="tf-table__featured">Abonnement</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ligne in COMPARATIF" :key="ligne.label">
                <th scope="row">{{ ligne.label }}</th>
                <td v-for="(valeur, i) in ligne.valeurs" :key="i" :class="{ 'tf-table__featured': i === 2 }">
                  <CheckCircleIcon v-if="valeur === true" class="tf-yes" aria-label="Inclus" />
                  <MinusIcon v-else-if="valeur === false" class="tf-no" aria-label="Non inclus" />
                  <span v-else>{{ valeur }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 4. Avec un professeur -->
    <section class="vt-section vt-section--soft">
      <div class="vt-container">
        <article v-reveal class="vt-card tf-prof">
          <img src="/images/professeurs/anthony.jpg" alt="" class="tf-prof__photo" width="479" height="521" loading="lazy" />
          <div class="tf-prof__copy">
            <p class="vt-kicker">Besoin d’un professeur&nbsp;?</p>
            <h2 class="tf-prof__title">Des cours particuliers en visio, dès 30&nbsp;€ de l’heure</h2>
            <p class="tf-prof__text">
              Maths, physique-chimie et informatique, du collège à la prépa, avec Anthony, ingénieur <span class="vt-nowrap">ISAE-SUPAERO</span> et
              professeur depuis plus de 15 ans. Premier échange gratuit et sans engagement.
            </p>
            <router-link to="/cours-particuliers" class="vt-btn vt-btn--primary" data-cta-name="tutoring" data-cta-location="tarifs">
              Découvrir les cours particuliers
              <ArrowRightIcon aria-hidden="true" />
            </router-link>
          </div>
        </article>
      </div>
    </section>

    <!-- 5. Questions -->
    <section class="vt-section">
      <div class="vt-container tf-faq">
        <header v-reveal class="tf-faq__intro">
          <p class="vt-kicker">Questions fréquentes</p>
          <h2 class="vt-title">Paiement, résiliation, accès</h2>
          <p class="tf-faq__more">
            Une autre question&nbsp;? <router-link to="/contact">Écris-nous</router-link>, on répond sous 24&nbsp;h.
          </p>
        </header>
        <VitrineFaqList v-reveal="100" :items="FAQ" />
      </div>
    </section>

    <!-- 6. Dernier appel -->
    <VitrineFinalCta
      titre="Prêt à t’y mettre ?"
      texte="Crée ton compte gratuit et débloque un chapitre complet pour tester la méthode. Sans carte bancaire."
    >
      <button type="button" class="vt-btn vt-btn--green" data-cta-name="signup" data-cta-location="tarifs_final" @click="openRegister">
        Créer mon compte gratuit
        <ArrowRightIcon aria-hidden="true" />
      </button>
      <router-link to="/ressources-gratuites" class="vt-btn vt-btn--light">Voir les ressources gratuites</router-link>
    </VitrineFinalCta>
  </VitrineLayout>
</template>

<script setup>
import { ArrowDownIcon, ArrowRightIcon, MinusIcon } from '@heroicons/vue/24/outline'
import { CheckCircleIcon } from '@heroicons/vue/24/solid'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import VitrinePricing from '@/components/vitrine/VitrinePricing.vue'
import VitrineFaqList from '@/components/vitrine/VitrineFaqList.vue'
import VitrineFinalCta from '@/components/vitrine/VitrineFinalCta.vue'
import { vReveal } from '@/components/vitrine/reveal'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'
import { vitrineFaq } from '@/config/vitrineContent'

const { openModal } = useModalManager()
const openRegister = () => openModal(MODAL_IDS.REGISTER)

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Valeurs : true = inclus, false = non inclus, texte = accès partiel.
const COMPARATIF = [
  { label: 'Cours', valeurs: ['Une sélection', '1 chapitre complet', true] },
  { label: 'Fiches de synthèse', valeurs: ['Une sélection', '1 chapitre complet', true] },
  { label: 'Exercices corrigés pas à pas', valeurs: ['Une sélection', '1 chapitre complet', true] },
  { label: 'Suivi de progression et XP', valeurs: [false, false, true] },
  { label: 'Ordinateur, tablette et téléphone', valeurs: [true, true, true] }
]

// Questions de l'accueil liées au paiement, complétées par deux questions propres aux tarifs.
const QUESTIONS_ACCUEIL = [
  'Quelle formule choisir ?',
  'Est-ce que je peux essayer gratuitement ?',
  'Puis-je annuler à tout moment ?',
  'Le paiement est-il sécurisé ?'
]
const normalize = (s) => s.replace(/\s/g, ' ').replace(/ ([?:!;])/g, '$1')
const FAQ = [
  ...QUESTIONS_ACCUEIL.map((q) => vitrineFaq.find((item) => normalize(item.question) === normalize(q))).filter(Boolean),
  {
    question: 'Un abonnement donne accès à quelle classe ?',
    answer: 'À une classe, que tu choisis au moment du paiement : tous ses chapitres, fiches et exercices corrigés sont débloqués. Pour une autre classe, il faut une autre souscription.'
  },
  {
    question: 'Faut-il créer un compte avant de payer ?',
    answer: 'Non. Si tu n’as pas encore de compte, il est créé automatiquement avec l’adresse e-mail utilisée lors du paiement.'
  }
]
</script>

<style scoped>
/* ---------- Accroche ---------- */

.tf-hero__h1 {
  margin: 0;
}

.tf-hero__kicker {
  display: block;
  margin-bottom: 14px;
}

/* ---------- Comparatif ---------- */

.tf-compare {
  max-width: 920px;
  margin: 0 auto;
  overflow: hidden;
}

.tf-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
}

.tf-table th,
.tf-table td {
  padding: 16px 18px;
  border-top: 1px solid var(--vt-line);
  text-align: center;
  vertical-align: middle;
  color: var(--vt-ink-soft);
}

.tf-table thead th {
  border-top: 0;
  font-size: 14px;
  font-weight: 700;
  color: var(--vt-ink);
}

.tf-table tbody th {
  text-align: left;
  font-weight: 700;
  color: var(--vt-ink);
}

.tf-table td span {
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-muted);
}

.tf-table__featured {
  background: var(--vt-navy-50);
}

.tf-table thead .tf-table__featured {
  color: var(--vt-navy);
}

.tf-yes {
  width: 24px;
  height: 24px;
  color: var(--vt-green-700);
  vertical-align: middle;
}

.tf-no {
  width: 20px;
  height: 20px;
  color: #b6bdcc;
  vertical-align: middle;
}

/* ---------- Avec un professeur ---------- */

.tf-prof {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 40px;
  align-items: center;
  max-width: 980px;
  margin: 0 auto;
  padding: 28px 40px 0 28px;
  overflow: hidden;
}

.tf-prof__photo {
  display: block;
  width: 100%;
  height: auto;
  align-self: end;
}

.tf-prof__copy {
  padding-bottom: 28px;
}

.tf-prof__title {
  font-size: clamp(24px, 2.6vw, 32px);
}

.tf-prof__text {
  margin: 14px 0 24px;
  font-size: 16px;
  color: var(--vt-muted);
}

/* ---------- Questions ---------- */

.tf-faq {
  display: grid;
  grid-template-columns: minmax(0, 0.75fr) minmax(0, 1.25fr);
  gap: 56px;
  align-items: start;
}

.tf-faq__more {
  margin: 20px 0 0;
  font-size: 15px;
  color: var(--vt-muted);
}

.tf-faq__more a {
  color: var(--vt-navy);
  font-weight: 700;
}

@media (max-width: 1080px) {
  .tf-faq {
    grid-template-columns: minmax(0, 1fr);
    gap: 32px;
  }
}

@media (max-width: 760px) {
  .tf-prof {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
    padding: 28px 22px 0;
    text-align: center;
  }

  .tf-prof__photo {
    order: 2;
    max-width: 220px;
    margin: 0 auto;
  }

  .tf-prof__copy {
    padding-bottom: 24px;
  }
}

@media (max-width: 640px) {
  .tf-table th,
  .tf-table td {
    padding: 12px 6px;
  }

  .tf-table thead th {
    font-size: 12px;
    line-height: 1.3;
  }

  .tf-table tbody th {
    padding-left: 12px;
    font-size: 13px;
    line-height: 1.35;
  }

  .tf-table td span {
    display: block;
    font-size: 12px;
    line-height: 1.3;
  }

  .tf-prof .vt-btn {
    width: 100%;
  }
}

/* Petits écrans : colonnes fixes calées sur le mot le plus long de chacune
   (« progression », « inscription », « chapitre », « Abonnement ») */
@media (max-width: 400px) {
  .tf-table {
    table-layout: fixed;
  }

  .tf-table thead th:nth-child(1) {
    width: 30%;
  }

  .tf-table thead th:nth-child(2) {
    width: 24%;
  }

  .tf-table thead th:nth-child(3) {
    width: 20%;
  }

  .tf-table th,
  .tf-table td {
    padding: 10px 3px;
  }

  .tf-table thead th {
    font-size: 11px;
  }

  .tf-table tbody th {
    padding-left: 10px;
    font-size: 12px;
  }

  .tf-table td span {
    font-size: 11px;
  }

  .tf-yes {
    width: 20px;
    height: 20px;
  }

  .tf-no {
    width: 16px;
    height: 16px;
  }
}

@media (max-width: 350px) {
  .tf-table thead th {
    font-size: 10px;
  }

  .tf-table thead th:nth-child(1) {
    width: 31%;
  }

  .tf-table thead th:nth-child(2) {
    width: 22%;
  }

  .tf-table thead th:nth-child(3) {
    width: 19%;
  }
}
</style>
