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
    
    <!-- Bouton CTA pour mobile (sous l'image) -->
    <div class="section-hero__cta-mobile">
      <button v-if="ctaText" class="section-hero__cta main" @click="$emit('cta-main')">{{ ctaText }}</button>
      <button v-if="ctaSecondary" class="section-hero__cta secondary" @click="$emit('cta-secondary')">{{ ctaSecondary }}</button>
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
  bg: { type: String, default: '#ffffff' }
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
  gap: 40px;
  overflow: hidden;
  max-width: 1200px;
  margin: 0 auto;
  @media (max-width: 800px) {
    flex-direction: column;
    text-align: center;
    padding: 130px 2vw 24px 2vw;
    border-radius: 0;
    gap: 0px;
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
  @media (max-width: 800px) {
    margin: 0 auto;
  }
}
.section-hero__title {
  font-size: 2.7rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 18px;
  line-height: 1.15;
  text-shadow: 0 2px 4px rgba(0,0,0,0.08);
  span {
    color: #2563eb;
    font-weight: 900;
  }
}
.section-hero__subtitle {
  font-size: 1.25rem;
  color: #475569;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
.section-hero__parents {
  font-size: 1.1rem;
  color: #059669;
  margin: 18px 0 24px 0;
  font-weight: 600;
  background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
  padding: 12px 16px;
  border-radius: 12px;
  border-left: 4px solid #10b981;
  
  @media (max-width: 800px) {
    margin: 18px 0 0px 0; /* Supprimer l'espace en bas sur mobile */
  }
}
.section-hero__cta-group {
  display: flex;
  gap: 1.1rem;
  margin-top: 18px;
  @media (max-width: 800px) {
    display: none; /* Masquer sur mobile */
  }
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
  padding: 20px;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    border-radius: 24px;
    backdrop-filter: blur(1px);
  }
  
  @media (max-width: 800px) {
    margin-top: -12px; /* Supprimer complètement l'espace en haut sur mobile */
    padding: 16px;
  }
}

.section-hero__cta-mobile {
  display: none; /* Masqué par défaut sur desktop */
  
  @media (max-width: 800px) {
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
    align-items: center;
    margin-top: 3px; /* Juste 3px d'espace entre l'image et le bouton */
    width: 100%;
  }
}

.section-hero__image {
  max-width: 320px;
  width: 100%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.08);
  background: #fff;
  object-fit: cover;
  filter: brightness(1.05) contrast(1.1) saturate(0.9) blur(0.5px);
  transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
  
}
</style> 