<template>
  <!-- Depuis le 2026-11-03, les pages publiques encore anciennes (ressources gratuites,
       blog, pages publicitaires et de paiement…) prennent l'en-tête et le pied de page
       de la vitrine. L'ancienne coque est conservée dans MainLayoutClassic.vue. -->
  <VitrineLayout :landing="isLanding" :show-whatsapp="false">
    <div class="main-content">
      <div v-if="sousEntete" class="ml-tabs">
        <component :is="sousEntete" />
      </div>
      <slot />
    </div>
  </VitrineLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import VitrineLayout from '@/components/vitrine/VitrineLayout.vue'
import FreeResourceTabs from '@/components/free-content/FreeResourceTabs.vue'
import CalculatorTabs from '@/components/calculator/CalculatorTabs.vue'
import '@/styles/public-document-mobile.css'

const props = defineProps({
  headerVariant: {
    type: String,
    default: 'default'
  },
  footerVariant: {
    type: String,
    default: 'default'
  }
})

const route = useRoute()

const isLanding = computed(() => props.headerVariant === 'landing')

// Onglets propres à certaines pages (auparavant dans l'ancien en-tête).
const sousEntete = computed(() => {
  if (isLanding.value) return null
  const path = route.path || ''
  if (path.startsWith('/ressources-gratuites/')) return FreeResourceTabs
  if (path === '/calculator') return CalculatorTabs
  return null
})
</script>

<style scoped>
.main-content {
  flex: 1;
  min-width: 0;
  width: 100%;
  margin: 0 auto;
  overflow-x: clip;
}

.ml-tabs {
  position: sticky;
  top: 72px;
  z-index: 20;
  display: flex;
  justify-content: center;
  padding: 10px 16px;
  border-bottom: 1px solid #e3e7ef;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: saturate(1.4) blur(10px);
}

@media (max-width: 960px) {
  .ml-tabs {
    top: 64px;
    padding: 8px 8px;
  }
}

@media (max-width: 880px) {
  .main-content :deep(:is(h1, h2, h3, p, li, a, button, label, span)) {
    -webkit-hyphens: none;
    hyphens: none;
  }

  .main-content :deep(:is(h1, h2, h3)) {
    text-wrap: balance;
    word-break: normal;
  }
}

/* Anciens boutons « Retour » fixés pour l'ancien en-tête : ils prennent place
   en haut du contenu, sous l'en-tête de la vitrine. */
.main-content :deep(:is(.back-button--top-left, .back-button--top-left-dashboard, .back-button--main-notions, .back-button--sticky)) {
  position: static !important;
  inset: auto !important;
  margin: 0 0 12px !important;
  transform: none !important;
}

@media (max-width: 768px) {
  .main-content :deep(.calc .graph-actions) {
    flex-wrap: wrap;
  }

  .main-content :deep(.calc .graph-actions > button) {
    min-width: 44px;
    min-height: 44px;
    white-space: normal;
  }

  .main-content :deep(.calc .graph-actions .reset-zoom-btn) {
    flex-basis: 100%;
  }
}
</style>
