<template>
  <div class="main-layout">
    <Header :variant="headerVariant" />
    <main class="main-content">
      <slot />
    </main>
    <Footer :variant="footerVariant" />
  </div>
</template>

<script setup>
import Header from './Header.vue'
import Footer from './Footer.vue'
import '@/styles/public-document-mobile.css'

defineProps({
  headerVariant: {
    type: String,
    default: 'default'
  },
  footerVariant: {
    type: String,
    default: 'default'
  }
})
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  /* Compenser le header fixe */
  padding-top: 64px;
}
.main-content {
  flex: 1;
  min-width: 0;
  width: 100%;
  margin: 0 auto;
  padding-bottom: 0;
  /* Permettre au zoom de fonctionner - pas de max-width restrictif */
  overflow-x: hidden;
  /* Permettre le scroll vertical sur mobile */
  overflow-y: visible;
  -webkit-overflow-scrolling: touch;
}

@media (max-width: 880px) {
  .main-layout {
    padding-top: calc(60px + env(safe-area-inset-top, 0px));
  }

  .main-content :deep(:is(h1, h2, h3, p, li, a, button, label, span)) {
    -webkit-hyphens: none;
    hyphens: none;
  }

  .main-content :deep(:is(h1, h2, h3)) {
    text-wrap: balance;
    word-break: normal;
  }
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
