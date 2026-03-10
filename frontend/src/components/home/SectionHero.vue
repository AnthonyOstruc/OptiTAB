<template>
  <section class="section-hero" :style="{ background: bg }">
    <!-- Éléments décoratifs animés -->
    <div class="hero-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
      <div class="decoration-blob blob-1"></div>
      <div class="decoration-blob blob-2"></div>
    </div>
    
    <div class="section-hero__content">
      <h1 class="section-hero__title">
        {{ titre }}<span v-if="highlight"> <span class="highlight-gradient">{{ highlight }}</span></span>
      </h1>
      <p v-if="subtitleLines.length" class="section-hero__subtitle">
        <span v-for="(line, idx) in subtitleLines" :key="idx" class="subtitle-line">{{ line }}</span>
      </p>
      <p v-if="sousTitre2" class="section-hero__subtitle2">{{ sousTitre2 }}</p>
      <div v-if="microBenefits && microBenefits.length" class="section-hero__benefits">
        <span v-for="(benefit, idx) in microBenefits" :key="idx" class="benefit-chip">
          <span class="benefit-icon">✓</span>
          {{ benefit }}
        </span>
      </div>
      <div class="section-hero__cta-group">
        <button v-if="ctaText" class="section-hero__cta main" @click="$emit('cta-main')">
          <span class="cta-text">{{ ctaText }}</span>
          <span v-if="ctaHint" class="cta-hint-main">{{ ctaHint }}</span>
        </button>
        <button v-if="ctaSecondary" class="section-hero__cta secondary" @click="$emit('cta-secondary')">
          <span class="cta-text">{{ ctaSecondary }}</span>
          <span v-if="ctaSecondaryHint" class="cta-hint">({{ ctaSecondaryHint }})</span>
        </button>
      </div>
      <div class="section-hero__reassurance">
        <GoogleReviewsCompact />
        <span v-if="reassurance" class="reassurance-text">• {{ reassurance }}</span>
      </div>
      <p v-if="miniLine" class="section-hero__mini-levels">{{ miniLine }}</p>
    </div>
    <div class="section-hero__image-wrapper" v-if="image">
      <div class="image-glow"></div>
      <img
        :src="image"
        :alt="resolvedImageAlt"
        class="section-hero__image"
        loading="eager"
        fetchpriority="high"
        decoding="async"
      />
    </div>
    
    <!-- Bouton CTA pour mobile (sous l'image) -->
    <div class="section-hero__cta-mobile">
      <button v-if="ctaText" class="section-hero__cta main" @click="$emit('cta-main')">
        <span class="cta-text">{{ ctaText }}</span>
        <span v-if="ctaHint" class="cta-hint-main">{{ ctaHint }}</span>
      </button>
      <button v-if="ctaSecondary" class="section-hero__cta secondary" @click="$emit('cta-secondary')">
        <span class="cta-text">{{ ctaSecondary }}</span>
        <span v-if="ctaSecondaryHint" class="cta-hint">({{ ctaSecondaryHint }})</span>
      </button>
      <div class="section-hero__reassurance-mobile">
        <GoogleReviewsCompact />
        <span v-if="reassurance" class="reassurance-text">• {{ reassurance }}</span>
      </div>
      <p v-if="miniLine" class="section-hero__mini-levels-mobile">{{ miniLine }}</p>
    </div>
  </section>
</template>

<script setup>
import heroDefaultImage from '@/assets/Images/HeroSection2.png'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
import { computed } from 'vue'
const props = defineProps({
  titre: { type: String, default: '' },
  description: { type: String, default: '' },
  sousTitre: { type: String, default: '' },
  sousTitre2: { type: String, default: '' },
  miniLine: { type: String, default: '' },
  image: { type: [String, Object], default: () => heroDefaultImage },
  imageAlt: { type: String, default: '' },
  showImage: { type: Boolean, default: true },
  highlight: { type: String, default: '' },
  microBenefits: { type: Array, default: () => [] },
  reassurance: { type: String, default: '' },
  ctaText: { type: String, default: "Voir la démo" },
  ctaHint: { type: String, default: '' },
  ctaSecondary: { type: String, default: "" },
  ctaSecondaryHint: { type: String, default: "" },
  bg: { type: String, default: '#ffffff' }
})

const subtitleLines = computed(() => {
  const raw = String(props.sousTitre || '').replaceAll('\r\n', '\n').trim()
  if (!raw) return []
  return raw
    .split('\n')
    .map(s => s.trim())
    .filter(Boolean)
})

const resolvedImageAlt = computed(() => {
  const explicitAlt = String(props.imageAlt || '').trim()
  if (explicitAlt) return explicitAlt

  const title = String(props.titre || '').trim()
  if (title) return `${title} - OptiTAB`

  return 'Plateforme de maths OptiTAB'
})
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.section-hero {
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  min-height: 480px;
  padding: 140px 5vw 40px 5vw;
  border-radius: 0;
  gap: 40px;
  overflow: hidden;
  width: 100%;
  margin: 0;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f1f5f9 100%);
    z-index: 1;
  }
  
  @media (max-width: 800px) {
    flex-direction: column;
    text-align: center;
    padding: 120px 4vw 32px 4vw;
    border-radius: 0;
    gap: 0px;
    min-height: auto;
    max-width: none;
  }
  
  @media (max-width: 480px) {
    padding: 100px 4vw 28px 4vw;
  }
}

// Éléments décoratifs animés
.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(42, 56, 183, 0.04) 0%, transparent 70%);
  animation: floatCircle 20s ease-in-out infinite;
  
  &.circle-1 {
    width: 400px;
    height: 400px;
    top: -150px;
    left: -100px;
    animation-delay: 0s;
  }
  
  &.circle-2 {
    width: 350px;
    height: 350px;
    bottom: -100px;
    right: -80px;
    animation-delay: 7s;
  }
  
  &.circle-3 {
    width: 300px;
    height: 300px;
    top: 40%;
    right: 5%;
    animation-delay: 14s;
  }
}

.decoration-blob {
  display: none;
}

@keyframes floatCircle {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(30px, -30px) scale(1.1);
    opacity: 0.7;
  }
}
.section-hero__content {
  position: relative;
  z-index: 2;
  flex: 0 1 auto;
  max-width: 760px;
  color: #18181b;
  text-shadow: 0 2px 8px rgba(255,255,255,0.08);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  animation: fadeInUp 0.8s ease-out;
  
  @media (max-width: 800px) {
    margin: 0 auto;
    text-align: center;
    max-width: 100%;
    padding: 0 1rem;
  }
  
  @media (max-width: 480px) {
    padding: 0 0.5rem;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// Badge moderne
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(59, 130, 246, 0.08));
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 50px;
  padding: 8px 20px;
  margin-bottom: 24px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6366f1;
  backdrop-filter: blur(10px);
  animation: fadeInDown 0.6s ease-out 0.2s both;
  
  .badge-icon {
    font-size: 1rem;
    animation: sparkle 2s ease-in-out infinite;
  }
  
  .badge-text {
    letter-spacing: 0.02em;
  }
  
  @media (max-width: 800px) {
    padding: 6px 16px;
    font-size: 0.8rem;
    margin-bottom: 20px;
  }
  
  @media (max-width: 480px) {
    padding: 6px 14px;
    font-size: 0.75rem;
    margin-bottom: 16px;
    
    .badge-icon {
      font-size: 0.9rem;
    }
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes sparkle {
  0%, 100% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.2) rotate(180deg);
  }
}
.section-hero__title {
  font-size: clamp(1.82rem, 3.55vw, 2.72rem);
  font-weight: 800;
  color: #0f172a;
  margin: 0 auto 16px auto;
  max-width: 19ch;
  line-height: 1.12;
  text-shadow: 0 2px 8px rgba(0,0,0,0.06);
  letter-spacing: -0.02em;
  animation: fadeInUp 0.8s ease-out 0.3s both;
  
  .highlight-gradient {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: -4px;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
      border-radius: 2px;
      opacity: 0.3;
      animation: underlineExpand 0.8s ease-out 0.8s both;
    }
  }
  
  @media (max-width: 800px) {
    font-size: clamp(1.68rem, 5.8vw, 2.04rem);
    margin-bottom: 16px;
    line-height: 1.18;
  }
  
  @media (max-width: 600px) {
    font-size: 1.52rem;
    margin-bottom: 14px;
    max-width: 100%;
  }
  
  @media (max-width: 480px) {
    font-size: 1.42rem;
    margin-bottom: 12px;
    line-height: 1.25;
  }
  
  @media (max-width: 360px) {
    font-size: 1.28rem;
  }
}

@keyframes underlineExpand {
  from {
    width: 0;
    opacity: 0;
  }
  to {
    width: 100%;
    opacity: 0.3;
  }
}

.section-hero__description {
  font-size: 1.02rem;
  color: #475569;
  margin-bottom: 1rem;
  font-weight: 400;
  line-height: 1.7;
  animation: fadeInUp 0.8s ease-out 0.35s both;
  max-width: 680px;
  
  @media (max-width: 800px) {
    font-size: 0.95rem;
    margin-bottom: 0.85rem;
    line-height: 1.6;
    padding: 0 0.5rem;
  }
  
  @media (max-width: 480px) {
    font-size: 0.88rem;
    margin-bottom: 0.75rem;
  }
}

.section-hero__subtitle {
  font-size: 1.08rem;
  color: #334155;
  margin: 0 auto 0.7rem auto;
  max-width: 760px;
  font-weight: 500;
  line-height: 1.62;
  animation: fadeInUp 0.8s ease-out 0.4s both;
  
  @media (max-width: 800px) {
    font-size: 1rem;
    margin-bottom: 0.6rem;
    line-height: 1.55;
  }
  
  @media (max-width: 480px) {
    font-size: 0.93rem;
    margin-bottom: 0.5rem;
    padding: 0 0.5rem;
  }
}

.section-hero__subtitle2 {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 1rem;
  font-weight: 500;
  line-height: 1.6;
  animation: fadeInUp 0.8s ease-out 0.42s both;
  
  @media (max-width: 800px) {
    font-size: 0.95rem;
    margin-bottom: 0.85rem;
  }
  
  @media (max-width: 480px) {
    font-size: 0.88rem;
    margin-bottom: 0.75rem;
    padding: 0 0.5rem;
  }
}

.subtitle-line {
  display: block;
}

@media (min-width: 1024px) {
  .subtitle-line {
    white-space: nowrap;
  }
}

// Niveaux en petit en bas
.section-hero__mini-levels {
  font-size: 0.82rem;
  color: #94a3b8;
  margin: 1rem 0 0 0;
  font-weight: 500;
  line-height: 1.4;
  animation: fadeInUp 0.8s ease-out 0.8s both;

  @media (max-width: 800px) {
    display: none;
  }
}

.section-hero__mini-levels-mobile {
  font-size: 0.78rem;
  color: #94a3b8;
  margin: 0.75rem 0 0 0;
  font-weight: 500;
  text-align: center;
  
  @media (min-width: 801px) {
    display: none;
  }
}

.section-hero__mini {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
  line-height: 1.55;
  animation: fadeInUp 0.8s ease-out 0.45s both;

  @media (max-width: 800px) {
    font-size: 0.92rem;
    margin-bottom: 0.85rem;
  }

  @media (max-width: 480px) {
    font-size: 0.88rem;
    padding: 0 0.5rem;
  }
}

// Micro-bénéfices (chips)
.section-hero__benefits {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin: 1rem 0;
  animation: fadeInUp 0.8s ease-out 0.5s both;
  
  @media (max-width: 480px) {
    gap: 0.4rem;
  }
}

.benefit-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.25);
  color: #166534;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.375rem 0.75rem;
  border-radius: 999px;
  
  .benefit-icon {
    color: #22c55e;
    font-weight: 700;
  }
  
  @media (max-width: 480px) {
    font-size: 0.78rem;
    padding: 0.3rem 0.625rem;
  }
}

// Réassurance sous les boutons
.section-hero__reassurance {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1.25rem;
  animation: fadeInUp 0.8s ease-out 0.7s both;
  
  .reassurance-text {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 500;
  }
  
  @media (max-width: 800px) {
    display: none;
  }
}

.section-hero__reassurance-mobile {
  display: none;
  
  @media (max-width: 800px) {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
    
    .reassurance-text {
      font-size: 0.8rem;
      color: #64748b;
      font-weight: 500;
      text-align: center;
    }
  }
}

// Hint sur bouton secondaire
.cta-hint {
  font-size: 0.8rem;
  font-weight: 400;
  opacity: 0.8;
  margin-left: 0.25rem;
  
  @media (max-width: 480px) {
    font-size: 0.75rem;
  }
}

.cta-hint-main {
  display: block;
  font-size: 0.73rem;
  font-weight: 600;
  opacity: 0.9;
  margin-top: 0.24rem;
  letter-spacing: 0;
  
  @media (max-width: 480px) {
    font-size: 0.68rem;
  }
}

.section-hero__cta-group {
  display: flex;
  gap: 0.85rem;
  margin-top: 22px;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
  
  @media (max-width: 800px) {
    display: none; /* Masquer sur mobile */
  }
  @media (max-width: 600px) {
    flex-direction: column;
    gap: 0.7rem;
    align-items: center;
  }
}

.section-hero__reviews {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeInUp 0.8s ease-out 0.7s both;
  
  @media (max-width: 800px) {
    display: none; /* Masqué sur mobile, visible dans le CTA mobile */
  }
}
.section-hero__cta {
  font-weight: 650;
  font-size: 1.02rem;
  border: 1px solid transparent;
  border-radius: 14px;
  padding: 12px 24px;
  cursor: pointer;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  min-width: 252px;
  min-height: 72px;
  transition: transform 0.2s ease, box-shadow 0.25s ease, background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
  animation: fadeInUp 0.8s ease-out 0.6s both;
  
  .cta-text {
    font-weight: 700;
    display: block;
    line-height: 1.2;
    letter-spacing: -0.01em;
  }
  
  &.main {
    background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
    color: #fff;
    border-color: #1f4ed2;
    box-shadow: 0 10px 22px rgba(37, 99, 235, 0.24);
    
    &:hover {
      background: linear-gradient(180deg, #2a64e6 0%, #1d4ed8 100%);
      transform: translateY(-1px);
      box-shadow: 0 14px 28px rgba(29, 78, 216, 0.33);
    }
    
    &:active {
      transform: translateY(0);
      box-shadow: 0 6px 14px rgba(37, 99, 235, 0.24);
    }

    &:focus-visible {
      outline: none;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.24), 0 12px 24px rgba(29, 78, 216, 0.28);
    }
  }
  
  &.secondary {
    background: rgba(255, 255, 255, 0.88);
    color: #1f2937;
    border: 1px solid #c5d1e2;
    min-width: 236px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    
    &:hover {
      background: #ffffff;
      color: #0f172a;
      border-color: #9fb2cf;
      transform: translateY(-1px);
      box-shadow: 0 8px 18px rgba(15, 23, 42, 0.12);
    }
    
    &:active {
      transform: translateY(0);
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    }

    &:focus-visible {
      outline: none;
      border-color: #90a7c6;
      box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.22), 0 8px 18px rgba(15, 23, 42, 0.12);
    }
  }
  
  @media (max-width: 800px) {
    width: 100%;
    max-width: 360px;
    justify-content: center;
    padding: 11px 18px;
    font-size: 0.95rem;
    min-height: 64px;
    white-space: nowrap;
  }
  
  @media (max-width: 480px) {
    max-width: 100%;
    padding: 10px 16px;
    font-size: 0.88rem;
    border-radius: 10px;
    white-space: nowrap;
  }
  
  @media (max-width: 360px) {
    max-width: 100%;
    padding: 10px 14px;
    font-size: 0.82rem;
    white-space: nowrap;
  }
}
.section-hero__image-wrapper {
  position: relative;
  z-index: 2;
  flex: 0 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeInRight 1s ease-out 0.4s both;
  
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
    margin-top: 24px;
    padding: 12px;
    animation: fadeInUp 0.8s ease-out 0.6s both;
  }
  
  @media (max-width: 600px) {
    padding: 10px;
    margin-top: 20px;
  }
  
  @media (max-width: 480px) {
    padding: 8px;
    margin-top: 18px;
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.image-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
  filter: blur(40px);
  z-index: -1;
  animation: pulse 3s ease-in-out infinite;
  
  @media (max-width: 800px) {
    filter: blur(30px);
    opacity: 0.7;
  }
  
  @media (max-width: 480px) {
    filter: blur(25px);
    opacity: 0.6;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

.section-hero__cta-mobile {
  display: none; /* Masqué par défaut sur desktop */
  
  @media (max-width: 800px) {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    align-items: center;
    margin-top: 24px;
    width: 100%;
    padding: 0 4vw;
    z-index: 2;
    position: relative;
  }
  
  @media (max-width: 480px) {
    margin-top: 20px;
    gap: 0.625rem;
    padding: 0 4vw;
  }
}

.section-hero__reviews-mobile {
  margin-top: 1rem;
  
  @media (min-width: 801px) {
    display: none;
  }
}

.section-hero__image {
  max-width: 380px;
  max-height: 280px;
  width: 100%;
  height: auto;
  border-radius: 20px;
  background: #fff;
  object-fit: cover;
  filter: brightness(1.08) contrast(1.15) saturate(1.05);
  position: relative;
  z-index: 1;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  
  @media (max-width: 800px) {
    max-width: 100%;
    max-height: 320px;
    width: 98%;
    border-radius: 16px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 600px) {
    max-height: 300px;
    width: 96%;
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  }
  
  @media (max-width: 480px) {
    max-height: 280px;
    width: 98%;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  }
  
  @media (max-width: 360px) {
    max-height: 260px;
    width: 100%;
  }
}
</style> 
