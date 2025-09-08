<template>
  <section class="subjects-section">
    <h2>{{ titre }}</h2>
    <div class="subjects-grid">
      <BaseCard
        v-for="sujet in sujets"
        :key="sujet.id || sujet.nom"
        :title="sujet.nom"
        :icon="sujet.svg_icon"
        :description="sujet.description || ''"
        @click="onSubjectClick(sujet)"
      />
    </div>
    <slot />
  </section>
</template>

<script setup>
import BaseCard from '@/components/UI/BaseCard.vue'

const props = defineProps({
  titre: { type: String, required: true },
  sujets: { type: Array, required: true }
})

const emit = defineEmits(['subject-selected'])

function onSubjectClick(subject) {
  console.log(`Subject clicked: ${subject.nom}`)
  emit('subject-selected', subject)
}
</script>

<style scoped>
.subjects-section {
  background-color: #fff;
  padding: 40px 5vw;
  text-align: center;
}

.subjects-section h2 {
  font-size: 2rem;
  color: #193e8e;
  margin-bottom: 40px;
  font-weight: 800;
  /* Descendre le titre H2 */
  margin-top: 1.5rem;
  padding-top: 0.75rem;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  max-width: 1100px;
  margin: 0 auto;
  gap: 30px;
  justify-items: center;
}
</style> 