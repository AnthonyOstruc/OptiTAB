<template>
  <section class="intro-features-section">
    <div class="intro-features-header">
      <h2 class="intro-features-title">
        {{ titre }} <span class="highlight">{{ highlight }}</span>
      </h2>
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
  background: #ffffff;
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
  color: #0f172a;
  margin-bottom: 18px;
  line-height: 1.1;
  letter-spacing: -1px;
}
.highlight {
  color: #2563eb;
  font-weight: 800;
  background: none;
  -webkit-background-clip: initial;
  -webkit-text-fill-color: initial;
  background-clip: initial;
}
.intro-features-desc {
  font-size: 1.18rem;
  color: #475569;
  margin-bottom: 0;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
.intro-features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 36px;
  max-width: 1200px;
  margin: 48px auto 0 auto;
  padding: 0 2vw;
}
.intro-feature-card {
  background: #fff;
  border-radius: 32px;
  box-shadow: 0 4px 32px rgba($bleu-principal, 0.13);
  padding: 42px 36px 36px 36px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  border: none;
  min-height: 180px;
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
  margin-right: 32px;
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
  font-size: 1.25rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 14px;
  text-align: left;
  letter-spacing: -0.5px;
  line-height: 1.3;
}
.intro-feature-desc {
  color: #475569;
  font-size: 1.05rem;
  margin-bottom: 0;
  text-align: left;
  line-height: 1.7;
}
@media (max-width: 800px) {
  .intro-features-section {
    padding: 56px 24px 40px;
  }
  .intro-features-header {
    max-width: 620px;
    margin-bottom: 32px;
  }
  .intro-features-title {
    font-size: clamp(1.65rem, 5.5vw, 2.1rem);
    line-height: 1.25;
    letter-spacing: -0.03em;
    text-wrap: balance;
  }
  .intro-features-desc {
    font-size: 1rem;
    line-height: 1.65;
  }
  .intro-features-grid {
    grid-template-columns: minmax(0, 1fr);
    max-width: 620px;
    gap: 20px;
    margin-top: 32px;
    padding: 0;
  }
  .intro-feature-card {
    min-width: 0;
    padding: 24px;
    flex-direction: column;
    align-items: center;
    border-radius: 20px;
    min-height: 0;
    box-shadow: 0 4px 24px rgba($bleu-principal, 0.08);
    border: 1px solid #e8edf5;

    &:hover {
      transform: none;
    }
  }
  .intro-feature-icon.left {
    min-width: 56px;
    margin-right: 0;
    margin-bottom: 16px;
    align-items: center;
    justify-content: center;
  }
  .feature-svg {
    width: 56px;
    height: 56px;
    font-size: 2.5rem;
  }
  .intro-feature-content {
    min-width: 0;
    width: 100%;
  }
  .intro-feature-title {
    font-size: 1.15rem;
    margin-bottom: 10px;
    text-align: center;
    text-wrap: balance;
  }
  .intro-feature-desc {
    font-size: 1rem;
    text-align: center;
    line-height: 1.6;
  }
}

@media (max-width: 600px) {
  .intro-features-section {
    padding: 48px 16px 32px;
  }
  .intro-feature-card {
    padding: 24px 20px;
  }
}
</style> 
