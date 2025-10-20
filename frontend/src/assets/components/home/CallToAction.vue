<template>
  <section class="cta">
    <h2 class="cta__title">{{ titre }}</h2>
    <button class="cta__btn cta__btn--large">{{ bouton }}</button>
  </section>
</template>

<script setup>
const props = defineProps({
  titre: { type: String, default: '' },
  bouton: { type: String, default: '' }
})
// CallToAction: simple CTA section for homepage or landing
</script>

<style scoped lang="scss">
.cta {
  background: linear-gradient(90deg, #fc6805 0%, #818cf8 100%);
  color: #fff;
  text-align: center;
  padding: 48px 5vw 48px 5vw;
}
.cta__title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 24px;
  /* Descendre le titre H2 */
  margin-top: 1rem;
  padding-top: 0.5rem;
}
.cta__btn--large {
  font-size: 1.2rem;
  padding: 18px 40px;
  border-radius: 10px;
  background: #fff;
  color: #2a38b7;
  font-weight: 700;
  border: none;
  transition: background 0.2s, color 0.2s;
  cursor: pointer;
  &:hover {
    background: #2a38b7;
    color: #fff;
  }
}
</style> 