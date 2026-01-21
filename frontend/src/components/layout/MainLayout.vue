<template>
  <div class="main-layout">
    <Header />
    <main class="main-content">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from './Header.vue'
import Footer from './Footer.vue'
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  width: 100%;
  margin: 0 auto;
  padding-bottom: 0;
  /* Permettre au zoom de fonctionner - pas de max-width restrictif */
  overflow-x: hidden;
}
</style> 