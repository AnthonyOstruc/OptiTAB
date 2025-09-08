<template>
  <section class="intro-features-section">
    <div class="intro-features-header">
      <h1 class="intro-features-title">
        {{ titre }} <span class="highlight">{{ highlight }}</span>
      </h1>
      <p class="intro-features-desc">{{ description }}</p>
    </div>
    <div v-if="features && features.length" class="intro-features-grid">
      <div v-for="feature in features" :key="feature.titre" class="intro-feature-card">
        <div class="intro-feature-icon left">
          <img v-if="typeof feature.icon === 'string'" :src="`/icons/${feature.icon}.svg`" class="feature-svg" alt="Icône" />
          <span v-else-if="typeof feature.icon === 'string'" class="feature-svg">{{ feature.icon }}</span>
          <component v-else :is="feature.icon" class="feature-svg" />
        </div>
        <div class="intro-feature-content">
          <h3 class="intro-feature-title">{{ feature.titre }}</h3>
          <p class="intro-feature-desc">{{ feature.description }}</p>
        </div>
      </div>
    </div>
    <div v-else class="intro-features-debug">
      <p>Aucune fonctionnalité à afficher (vérifiez la config ou les icônes).</p>
    </div>
  </section>
</template>

<script setup>
// Section d'avantages/atouts, style familial/éducatif
const props = defineProps({
  titre: { type: String, required: true },
  highlight: { type: String, required: true },
  description: { type: String, required: true },
  features: { type: Array, required: true }
})
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
@use "sass:color";
.intro-features-section {
  padding: 56px 0 32px 0;
  background: color.adjust($bleu-principal, $lightness: 50%);
  font-family: 'Poppins', 'Nunito', Arial, sans-serif;
}
.intro-features-header {
  max-width: 900px;
  margin: 0 auto 40px auto;
  text-align: center;
}
.intro-features-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #2563eb;
  margin-bottom: 18px;
  line-height: 1.1;
  letter-spacing: -1px;
}
.highlight {
  color: #22c55e;
  font-weight: 800;
  background: none;
  -webkit-background-clip: initial;
  -webkit-text-fill-color: initial;
  background-clip: initial;
}
.intro-features-desc {
  font-size: 1.18rem;
  color: color.adjust($bleu-principal, $lightness: -30%);
  margin-bottom: 0;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
.intro-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 36px;
  max-width: 1200px;
  margin: 48px auto 0 auto;
  padding: 0 2vw;
}
.intro-feature-card {
  background: #fff;
  border-radius: 32px;
  box-shadow: 0 4px 32px rgba($bleu-principal, 0.13);
  padding: 38px 32px 32px 32px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  border: none;
  min-height: 160px;
  transition: box-shadow 0.2s, transform 0.2s;
  &:hover {
    box-shadow: 0 8px 40px rgba($bleu-principal, 0.18);
    transform: translateY(-4px) scale(1.03);
  }
}
.intro-feature-icon.left {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  margin-right: 28px;
  min-width: 72px;
}
.feature-svg {
  width: 72px;
  height: 72px;
  font-size: 3.2rem;
  color: $bleu-principal;
  display: block;
  background: none !important;
  border-radius: 50%;
  box-shadow: none;
}
.intro-feature-content {
  flex: 1 1 0%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.intro-feature-title {
  font-size: 1.22rem;
  font-weight: 700;
  color: $bleu-principal;
  margin-bottom: 8px;
  text-align: left;
  letter-spacing: -0.5px;
}
.intro-feature-desc {
  color: color.adjust($bleu-principal, $lightness: -30%);
  font-size: 1.04rem;
  margin-bottom: 0;
  text-align: left;
}
@media (max-width: 700px) {
  .intro-features-title {
    font-size: 2rem;
  }
  .intro-features-grid {
    gap: 18px;
  }
  .intro-feature-card {
    padding: 22px 12px 18px 12px;
    flex-direction: column;
    align-items: center;
    border-radius: 22px;
  }
  .intro-feature-icon.left {
    margin-right: 0;
    margin-bottom: 12px;
    align-items: center;
    justify-content: center;
  }
  .intro-feature-title, .intro-feature-desc {
    text-align: center;
  }
}
</style> 