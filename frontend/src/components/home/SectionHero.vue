<template>
  <section class="section-hero" :style="{ background: bg }">
    <div class="section-hero__content">
      <h1 class="section-hero__title">
        {{ titre }}<span v-if="highlight"> <span>{{ highlight }}</span></span>
      </h1>
      <p class="section-hero__subtitle">{{ sousTitre }}</p>
      <p v-if="messageParents" class="section-hero__parents">{{ messageParents }}</p>
      <div class="section-hero__cta-group">
        <button v-if="ctaText" class="section-hero__cta main" @click="$emit('cta-main')">{{ ctaText }}</button>
        <button v-if="ctaSecondary" class="section-hero__cta secondary" @click="$emit('cta-secondary')">{{ ctaSecondary }}</button>
      </div>
    </div>
    <div class="section-hero__image-wrapper" v-if="image">
      <img
        :src="image"
        alt="Illustration OptiTAB Hero"
        class="section-hero__image"
        loading="lazy"
      />
    </div>
  </section>
</template>

<script setup>
import heroDefaultImage from '@/assets/Images/HeroSection2.png'
const props = defineProps({
  titre: { type: String, default: '' },
  sousTitre: { type: String, default: '' },
  image: { type: [String, Object], default: () => heroDefaultImage },
  highlight: { type: String, default: '' },
  messageParents: { type: String, default: "Un accompagnement sur-mesure pour la réussite de votre enfant. Rejoignez la communauté de parents qui font confiance à OptiTAB !" },
  ctaText: { type: String, default: "Découvrir OptiTAB" },
  ctaSecondary: { type: String, default: "" },
  bg: { type: String, default: 'linear-gradient(90deg, #e0f2fe 60%, #d1fae5 100%)' }
})
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.section-hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 480px;
  padding: 160px 5vw 48px 5vw;
  border-radius: 0;
  box-shadow: 0 2px 16px rgba(30,41,59,0.04);
  gap: 40px;
  overflow: hidden;
  @media (max-width: 900px) {
    flex-direction: column;
    text-align: center;
    padding: 130px 2vw 24px 2vw;
    border-radius: 0;
    gap: 24px;
    min-height: 420px;
  }
}
.section-hero__content {
  position: relative;
  z-index: 2;
  flex: 1 1 350px;
  max-width: 520px;
  color: #18181b;
  text-shadow: 0 2px 8px rgba(255,255,255,0.08);
  @media (max-width: 900px) {
    margin: 0 auto;
  }
}
.section-hero__title {
  font-size: 2.7rem;
  font-weight: 800;
  color: $bleu-principal;
  margin-bottom: 18px;
  line-height: 1.15;
  span {
    color: $bleu-principal;
    font-weight: 900;
  }
}
.section-hero__subtitle {
  font-size: 1.25rem;
  color: #475569;
  margin-bottom: 0.5rem;
}
.section-hero__parents {
  font-size: 1.1rem;
  color: #22c55e;
  margin: 18px 0 24px 0;
  font-weight: 600;
}
.section-hero__cta-group {
  display: flex;
  gap: 1.1rem;
  margin-top: 18px;
  @media (max-width: 600px) {
    flex-direction: column;
    gap: 0.7rem;
    align-items: center;
  }
}
.section-hero__cta {
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  border-radius: 10px;
  padding: 16px 36px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(30,41,59,0.08);
  transition: background 0.2s, color 0.2s;
  &.main {
    background: $bleu-principal;
    color: #fff;
    &:hover {
      background: #1e40af;
      color: #fff;
    }
  }
  &.secondary {
    background: #e0f2fe;
    color: $bleu-principal;
    &:hover {
      background: #bae6fd;
      color: #1e40af;
    }
  }
}
.section-hero__image-wrapper {
  position: relative;
  z-index: 2;
  flex: 1 1 320px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 220px;
  @media (max-width: 900px) {
    margin-top: 24px;
  }
}
.section-hero__image {
  max-width: 380px;
  width: 100%;
  height: auto;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(99,102,241,0.08);
  background: #fff;
  object-fit: cover;
}
</style> 