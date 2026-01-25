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
  
  @media (max-width: 700px) {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 0 4vw;
  }
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
  
  @media (max-width: 700px) {
    width: 64px;
    height: 64px;
    font-size: 2.8rem;
  }
  
  @media (max-width: 350px) {
    width: 48px;
    height: 48px;
    font-size: 2rem;
  }
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
@media (max-width: 700px) {
  .intro-features-title {
    font-size: 2rem;
  }
  .intro-feature-card {
    padding: 28px 20px 24px 20px;
    flex-direction: column;
    align-items: center;
    border-radius: 22px;
    min-height: 200px;
  }
  .intro-feature-icon.left {
    margin-right: 0;
    margin-bottom: 16px;
    align-items: center;
    justify-content: center;
  }
  .intro-feature-title {
    margin-bottom: 12px;
    text-align: center;
  }
  .intro-feature-desc {
    text-align: center;
    line-height: 1.6;
  }
}

@media (max-width: 350px) {
  .intro-features-title {
    font-size: 1.75rem;
  }
  .intro-features-desc {
    font-size: 1rem;
  }
  .intro-feature-card {
    padding: 24px 16px 20px 16px;
    border-radius: 18px;
    min-height: 160px;
  }
  .intro-feature-icon.left {
    min-width: 48px;
    margin-bottom: 12px;
  }
  .intro-feature-title {
    font-size: 1.05rem;
    margin-bottom: 10px;
    line-height: 1.3;
  }
  .intro-feature-desc {
    font-size: 0.9rem;
    line-height: 1.6;
  }
}
</style> 
