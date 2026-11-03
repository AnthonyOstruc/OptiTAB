<template>
  <div class="vp">
    <!-- Du gratuit à l'abonnement, dans l'ordre où l'élève les découvre. -->
    <ol class="vp-ladder">
      <li
        v-for="(formule, index) in vitrineFormules"
        :key="formule.titre"
        :class="['vp-ladder__step', { 'vp-ladder__step--featured': formule.miseEnAvant }]"
      >
        <span class="vp-ladder__index">{{ index + 1 }}</span>
        <span class="vp-ladder__body">
          <span class="vp-ladder__head">
            <strong>{{ formule.titre }}</strong>
            <span class="vp-ladder__price">{{ formule.prix }}</span>
          </span>
          <span class="vp-ladder__text">{{ formule.texte }}</span>
        </span>
      </li>
    </ol>

    <!-- Bloc d'abonnement existant (paiement Stripe, choix du niveau), réutilisé
         tel quel : seules ses couleurs sont alignées sur la vitrine. -->
    <div class="vp-plans">
      <PricingPlans :show-header="false" section-id="" />
      <p class="vp-swipe" aria-hidden="true">Fais glisser pour voir les autres formules →</p>
    </div>

    <ul class="vp-trust">
      <li><CheckIcon aria-hidden="true" />Paiement sécurisé par Stripe</li>
      <li><CheckIcon aria-hidden="true" />Facture envoyée par e-mail</li>
      <li><CheckIcon aria-hidden="true" />Annulable à tout moment</li>
    </ul>
  </div>
</template>

<script setup>
import { CheckIcon } from '@heroicons/vue/24/outline'
import PricingPlans from '@/components/home/PricingPlans.vue'
import { vitrineFormules } from '@/config/vitrineContent'
</script>

<style scoped>
/* ---------- Étapes : gratuit → compte → abonnement ---------- */

.vp-ladder {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  max-width: 960px;
  margin: 0 auto 48px;
  padding: 0;
  list-style: none;
}

.vp-ladder__step {
  position: relative;
  display: flex;
  gap: 14px;
  padding: 18px 20px;
  border: 1px solid var(--vt-line);
  border-radius: 14px;
  background: #fff;
}

.vp-ladder__step + .vp-ladder__step::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -12px;
  width: 10px;
  height: 10px;
  border-top: 2px solid var(--vt-line-strong);
  border-right: 2px solid var(--vt-line-strong);
  transform: translate(-25%, -50%) rotate(45deg);
}

.vp-ladder__step--featured {
  border-color: var(--vt-navy);
  background: var(--vt-navy-50);
}

.vp-ladder__index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--vt-navy-50);
  font-size: 13px;
  font-weight: 700;
  color: var(--vt-navy);
}

.vp-ladder__step--featured .vp-ladder__index {
  background: var(--vt-navy);
  color: #fff;
}

.vp-ladder__body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.vp-ladder__head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px 10px;
  font-size: 15px;
  color: var(--vt-ink);
}

.vp-ladder__price {
  font-size: 13px;
  font-weight: 700;
  color: var(--vt-green-700);
}

.vp-ladder__text {
  font-size: 14px;
  line-height: 1.5;
  color: var(--vt-muted);
}

/* ---------- Cartes de prix ---------- */

.vp-plans :deep(.pricing-plans-section) {
  padding: 0;
  background: transparent;
}

.vp-plans :deep(.card-reviews) {
  display: none;
}

.vp-plans :deep(.pricing-tabs) {
  background: #e9edf5;
}

.vp-plans :deep(.pricing-tab) {
  font-family: var(--vt-font);
  font-weight: 700;
  white-space: nowrap;
}

.vp-plans :deep(.pricing-tab.active) {
  color: var(--vt-navy);
}

.vp-plans :deep(.pricing-card) {
  border: 1px solid var(--vt-line);
  border-radius: var(--vt-radius);
  box-shadow: var(--vt-shadow);
  font-family: var(--vt-font);
}

.vp-plans :deep(.pricing-card:hover) {
  border-color: var(--vt-navy);
  box-shadow: var(--vt-shadow-lg);
  transform: translateY(-3px);
}

.vp-plans :deep(.pricing-card.is-popular) {
  border: 2px solid var(--vt-navy);
  box-shadow: var(--vt-shadow-lg);
}

.vp-plans :deep(.badge-popular) {
  background: var(--vt-navy);
  color: #fff;
}

.vp-plans :deep(.badge-savings) {
  background: var(--vt-green-50);
  color: var(--vt-green-700);
}

.vp-plans :deep(.card-title),
.vp-plans :deep(.price-amount) {
  font-family: var(--vt-font);
  color: var(--vt-ink);
  letter-spacing: -0.02em;
}

.vp-plans :deep(.price-amount) {
  font-weight: 700;
}

.vp-plans :deep(.feature-icon) {
  color: var(--vt-green-700);
}

.vp-plans :deep(.card-button) {
  background: var(--vt-navy);
  font-family: var(--vt-font);
  font-weight: 700;
}

.vp-plans :deep(.card-button:hover:not(:disabled)) {
  background: var(--vt-navy-700);
  box-shadow: 0 8px 20px rgba(27, 60, 142, 0.28);
}

.vp-plans :deep(.level-modal-overlay) {
  z-index: 12600;
}

.vp-plans :deep(.spinner) {
  border-top-color: var(--vt-navy);
}

.vp-swipe {
  display: none;
}

.vp-trust {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 28px;
  margin: 40px 0 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  font-weight: 600;
  color: var(--vt-ink-soft);
}

.vp-trust li {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.vp-trust svg {
  width: 16px;
  height: 16px;
  stroke-width: 3;
  color: var(--vt-green-700);
}

@media (max-width: 640px) {
  .vp-ladder {
    grid-template-columns: 1fr;
    gap: 22px;
    margin-bottom: 36px;
  }

  .vp-ladder__step + .vp-ladder__step::before {
    top: -14px;
    left: 50%;
    transform: translate(-50%, -25%) rotate(135deg);
  }

  /* Formules : carrousel horizontal plutôt que quatre cartes empilées. */
  .vp-plans :deep(.pricing-grid) {
    display: flex;
    gap: 12px;
    max-width: none;
    margin: 0 calc(-1 * var(--vt-gutter));
    padding: 6px var(--vt-gutter) 18px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-padding: 0 var(--vt-gutter);
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .vp-plans :deep(.pricing-grid::-webkit-scrollbar) {
    display: none;
  }

  .vp-plans :deep(.pricing-card) {
    flex: 0 0 84%;
    height: auto;
    padding: 1.4rem 1.25rem;
    scroll-snap-align: start;
  }

  .vp-plans :deep(.pricing-card:hover) {
    transform: none;
  }

  .vp-plans :deep(.card-badge-area) {
    margin-bottom: 0.6rem;
  }

  .vp-plans :deep(.price-amount) {
    font-size: 2.3rem;
  }

  .vp-plans :deep(.pricing-tabs) {
    width: 100%;
  }

  .vp-plans :deep(.pricing-tab) {
    flex: 1;
    justify-content: center;
    padding-inline: 8px;
    font-size: 13px;
  }

  .vp-swipe {
    display: block;
    margin: 4px 0 0;
    text-align: center;
    font-size: 13px;
    font-weight: 600;
    color: var(--vt-muted);
  }

  .vp-trust {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
}
</style>
