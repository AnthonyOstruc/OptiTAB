<template>
  <section class="steps-how-section">
    <div class="steps-how-header">
      <h2 class="steps-how-title">
        {{ titre }} <span class="steps-how-highlight">{{ highlight }}</span> {{ titreFin }}
      </h2>
      <p class="steps-how-desc">{{ description }}</p>
    </div>
    <div class="steps-how-steps">
      <div v-for="(etape, idx) in etapes" :key="etape.numero" class="steps-how-step">
        <div
          class="steps-how-step-num"
          :style="{ background: getStepColor(idx), boxShadow: `0 2px 12px ${getStepShadow(idx)}` }"
        >
          {{ etape.numero }}
        </div>
        <div class="steps-how-step-icon">
          <span v-if="typeof etape.icon === 'string'" class="step-svg">{{ etape.icon }}</span>
          <component v-else :is="etape.icon" class="step-svg" />
        </div>
        <h3 class="steps-how-step-title">{{ etape.titre }}</h3>
        <p class="steps-how-step-desc">{{ etape.description }}</p>
        <div v-if="idx < etapes.length - 1" class="steps-how-arrow">→</div>
      </div>
    </div>
    <div class="steps-how-cta-top" v-if="ctaTop">{{ ctaTop }}</div>
    <div class="steps-how-bottom">
      <h4 class="steps-how-title-bas">{{ titreBas }}</h4>
      <div class="steps-how-cta-group">
        <button class="steps-how-cta-main">{{ ctaText }}</button>
        <button class="steps-how-cta-secondary">{{ ctaSecondary }}</button>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  titre: { type: String, required: true },
  highlight: { type: String, required: true },
  titreFin: { type: String, required: true },
  description: { type: String, required: true },
  etapes: { type: Array, required: true },
  ctaText: { type: String, required: true },
  ctaSecondary: { type: String, required: true },
  ctaTop: { type: String, default: '' },
  titreBas: { type: String, default: '' }
})

const bleu = '#2a38b7'
const vert = '#3ec28f'
function getStepColor(idx) {
  // Toutes les pastilles sont vertes
  return vert
}
function getStepShadow(idx) {
  return 'rgba(62,194,143,0.18)'
}
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.steps-how-section {
  background: #fff;
  padding: 56px 0 32px 0;
  text-align: center;
}
.steps-how-header {
  margin-bottom: 36px;
}
.steps-how-title {
  font-size: 2.3rem;
  font-weight: 900;
  color: $bleu-principal;
  margin-bottom: 12px;
  /* Descendre le titre H2 */
  margin-top: 1.5rem;
  padding-top: 0.75rem;
}
.steps-how-highlight {
  color: $bleu-principal;
}
.steps-how-desc {
  color: #52525b;
  font-size: 1.15rem;
  margin-bottom: 0;
}
.steps-how-steps {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 32px;
  margin: 48px auto 0 auto;
  max-width: 1200px;
  flex-wrap: wrap;
}
.steps-how-step {
  background: #fafaff;
  border-radius: 18px;
  box-shadow: 0 2px 16px rgba(30,41,59,0.06);
  padding: 38px 32px 32px 32px;
  min-width: 270px;
  max-width: 340px;
  flex: 1 1 300px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1.5px solid #f3f4f6;
}
.steps-how-step-num {
  background: $vert-logo;
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -38px auto 18px auto;
  box-shadow: 0 2px 12px rgba($vert-logo, 0.18);
  border: 4px solid #f3f4f6;
  z-index: 2;
}
.steps-how-step-icon {
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.step-svg {
  font-size: 2.5rem;
  width: 48px;
  height: 48px;
  color: #2a38b7;
  display: block;
}
.steps-how-step-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 8px;
}
.steps-how-step-desc {
  color: #52525b;
  font-size: 1rem;
  margin-bottom: 0;
}
.steps-how-arrow {
  position: absolute;
  right: -32px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2.2rem;
  color: #a78bfa;
  z-index: 1;
  pointer-events: none;
  @media (max-width: 900px) {
    display: none;
  }
}
.steps-how-cta-top {
  margin: 38px 0 0 0;
  color: #2a38b7;
  font-weight: 600;
  font-size: 1.1rem;
}
.steps-how-bottom {
  margin: 48px auto 0 auto;
  max-width: 700px;
}
.steps-how-title-bas {
  font-size: 1.25rem;
  font-weight: 800;
  color: $bleu-principal;
  margin-bottom: 22px;
}
.steps-how-cta-group {
  display: flex;
  gap: 18px;
  justify-content: center;
  flex-wrap: wrap;
}
.steps-how-cta-main {
  background: #2a38b7;
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  border-radius: 10px;
  padding: 16px 36px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(30,41,59,0.08);
  transition: background 0.2s, color 0.2s;
  &:hover {
    background: #8b5cf6;
    color: #fff;
  }
}
.steps-how-cta-secondary {
  background: #fff;
  color: #2a38b7;
  font-weight: 700;
  font-size: 1.1rem;
  border: 2px solid #e0e7ff;
  border-radius: 10px;
  padding: 16px 36px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  &:hover {
    background: #f3f4f6;
    color: #2a38b7;
  }
}
@media (max-width: 900px) {
  .steps-how-steps {
    flex-direction: column;
    gap: 28px;
  }
  .steps-how-step {
    max-width: 100%;
    min-width: 0;
  }
  .steps-how-arrow {
    display: none;
  }
}
</style> 