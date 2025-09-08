<template>
  <section class="features-section">
    <h2>{{ titre }}</h2>
    <div class="features-grid">
      <BaseCard
        v-for="feature in fonctionnalites"
        :key="feature.titre"
        :title="feature.titre"
        :description="feature.description"
        :icon="feature.icon"
      />
    </div>
    <slot />
  </section>
</template>

<script setup>
// Composant d'affichage d'une liste de fonctionnalités dynamiques
import BaseCard from '@/components/UI/BaseCard.vue'
const props = defineProps({
  titre: { type: String, required: true },
  fonctionnalites: { type: Array, required: true }
})
</script>

<style scoped>
@use '@/assets/variables.scss' as *;
.features-section {
  background-color: #f8fafc;
  padding: 40px 5vw;
  text-align: center;
}
.features-section h2 {
  font-size: 2rem;
  color: $bleu-principal;
  margin-bottom: 40px;
  font-weight: 800;
  /* Descendre le titre H2 */
  margin-top: 1.5rem;
  padding-top: 0.75rem;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  max-width: 1100px;
  margin: 0 auto;
  gap: 30px;
  justify-items: center;
}
</style> 