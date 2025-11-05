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
      <div class="hero-badge">
        <span class="badge-icon">✨</span>
        <span class="badge-text">Plateforme d'excellence</span>
      </div>
      <h1 class="section-hero__title">
        {{ titre }}<span v-if="highlight"> <span class="highlight-gradient">{{ highlight }}</span></span>
      </h1>
      <p class="section-hero__subtitle">{{ sousTitre }}</p>
      <p v-if="messageParents" class="section-hero__parents">
        <span class="parents-icon">👨‍👩‍👧‍👦</span>
        {{ messageParents }}
      </p>
      <div class="section-hero__cta-group">
        <button v-if="ctaText" class="section-hero__cta main" @click="$emit('cta-main')">
          <span class="cta-text">{{ ctaText }}</span>
          <span class="cta-arrow">→</span>
        </button>
        <button v-if="ctaSecondary" class="section-hero__cta secondary" @click="$emit('cta-secondary')">
          {{ ctaSecondary }}
        </button>
      </div>
      <div class="section-hero__reviews">
        <GoogleReviewsCompact />
      </div>
    </div>
    <div class="section-hero__image-wrapper" v-if="image">
      <div class="image-glow"></div>
      <img
        :src="image"
        alt="Illustration OptiTAB Hero"
        class="section-hero__image"
        loading="lazy"
      />
    </div>
    
    <!-- Bouton CTA pour mobile (sous l'image) -->
    <div class="section-hero__cta-mobile">
      <button v-if="ctaText" class="section-hero__cta main" @click="$emit('cta-main')">
        <span class="cta-text">{{ ctaText }}</span>
        <span class="cta-arrow">→</span>
      </button>
      <button v-if="ctaSecondary" class="section-hero__cta secondary" @click="$emit('cta-secondary')">
        {{ ctaSecondary }}
      </button>
      <div class="section-hero__reviews-mobile">
        <GoogleReviewsCompact />
      </div>
    </div>
  </section>
</template>

<script setup>
import heroDefaultImage from '@/assets/Images/HeroSection2.png'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'
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
  flex-direction: row;
  align-items: center;
  justify-content: center;
  min-height: 580px;
  padding: 160px 5vw 48px 5vw;
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
    background: 
      radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 60%),
      radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.06) 0%, transparent 60%),
      radial-gradient(circle at 50% 50%, rgba(236, 72, 153, 0.04) 0%, transparent 70%);
    z-index: 1;
    animation: gradientShift 15s ease infinite;
  }
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%, transparent 30%, rgba(255,255,255,0.3) 70%, transparent 100%);
    z-index: 1;
  }
  
  @keyframes gradientShift {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.8;
    }
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
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(59, 130, 246, 0.08));
  filter: blur(40px);
  animation: float 20s ease-in-out infinite;
  
  &.circle-1 {
    width: 300px;
    height: 300px;
    top: -100px;
    left: -100px;
    animation-delay: 0s;
  }
  
  &.circle-2 {
    width: 250px;
    height: 250px;
    bottom: -50px;
    right: -50px;
    animation-delay: 5s;
  }
  
  &.circle-3 {
    width: 200px;
    height: 200px;
    top: 50%;
    right: 10%;
    animation-delay: 10s;
  }
}

.decoration-blob {
  position: absolute;
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.06), rgba(99, 102, 241, 0.04));
  filter: blur(60px);
  animation: blob 25s ease-in-out infinite;
  
  &.blob-1 {
    width: 400px;
    height: 400px;
    top: 20%;
    right: -100px;
    animation-delay: 0s;
  }
  
  &.blob-2 {
    width: 350px;
    height: 350px;
    bottom: 10%;
    left: -150px;
    animation-delay: 12s;
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

@keyframes blob {
  0%, 100% {
    border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
    transform: translate(0, 0) scale(1);
  }
  25% {
    border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%;
    transform: translate(20px, -30px) scale(1.1);
  }
  50% {
    border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%;
    transform: translate(-20px, 20px) scale(0.9);
  }
  75% {
    border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%;
    transform: translate(30px, 10px) scale(1.05);
  }
}
.section-hero__content {
  position: relative;
  z-index: 2;
  flex: 0 1 auto;
  max-width: 560px;
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
  font-size: 3rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 20px;
  line-height: 1.1;
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
    font-size: 2rem;
    margin-bottom: 16px;
    line-height: 1.2;
  }
  
  @media (max-width: 600px) {
    font-size: 1.65rem;
    margin-bottom: 14px;
  }
  
  @media (max-width: 480px) {
    font-size: 1.5rem;
    margin-bottom: 12px;
    line-height: 1.25;
  }
  
  @media (max-width: 360px) {
    font-size: 1.35rem;
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
.section-hero__subtitle {
  font-size: 1.3rem;
  color: #475569;
  margin-bottom: 0.5rem;
  font-weight: 500;
  line-height: 1.6;
  animation: fadeInUp 0.8s ease-out 0.4s both;
  
  @media (max-width: 800px) {
    font-size: 1.05rem;
    margin-bottom: 0.75rem;
    line-height: 1.5;
  }
  
  @media (max-width: 480px) {
    font-size: 0.95rem;
    margin-bottom: 0.625rem;
    padding: 0 0.5rem;
  }
}
.section-hero__parents {
  font-size: 1.05rem;
  color: #047857;
  margin: 24px 0 28px 0;
  font-weight: 600;
  background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
  padding: 16px 20px;
  border-radius: 16px;
  border: 2px solid #10b981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.8s ease-out 0.5s both;
  transition: all 0.3s ease;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.5s ease;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.2);
    
    &::before {
      left: 100%;
    }
  }
  
  .parents-icon {
    margin-right: 8px;
    font-size: 1.2rem;
    display: inline-block;
    animation: bounce 2s ease-in-out infinite;
  }
  
  @media (max-width: 800px) {
    margin: 20px auto 0 auto;
    padding: 14px 16px;
    font-size: 0.9rem;
    max-width: 95%;
    line-height: 1.5;
    
    .parents-icon {
      font-size: 1.1rem;
      margin-right: 6px;
    }
  }
  
  @media (max-width: 480px) {
    margin: 16px auto 0 auto;
    padding: 12px 14px;
    font-size: 0.85rem;
    line-height: 1.4;
    border-radius: 14px;
    
    .parents-icon {
      font-size: 1rem;
      margin-right: 5px;
    }
  }
  
  @media (max-width: 360px) {
    font-size: 0.8rem;
    padding: 10px 12px;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
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

.section-hero__reviews {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeInUp 0.8s ease-out 0.7s both;
  
  @media (max-width: 800px) {
    display: none; /* Masqué sur mobile, visible dans le CTA mobile */
  }
}
.section-hero__cta {
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  border-radius: 12px;
  padding: 18px 40px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 0.8s ease-out 0.6s both;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
  }
  
  &:hover::before {
    width: 300px;
    height: 300px;
  }
  
  .cta-text {
    position: relative;
    z-index: 1;
  }
  
  .cta-arrow {
    position: relative;
    z-index: 1;
    transition: transform 0.3s ease;
  }
  
  &:hover .cta-arrow {
    transform: translateX(4px);
  }
  
  &.main {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: #fff;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    
    &:hover {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
  
  &.secondary {
    background: rgba(224, 242, 254, 0.8);
    color: $bleu-principal;
    border: 2px solid rgba(99, 102, 241, 0.2);
    backdrop-filter: blur(10px);
    
    &:hover {
      background: rgba(186, 230, 253, 0.9);
      color: #1e40af;
      border-color: rgba(99, 102, 241, 0.3);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
  }
  
  @media (max-width: 800px) {
    width: 100%;
    max-width: 320px;
    padding: 16px 32px;
    font-size: 1rem;
  }
  
  @media (max-width: 480px) {
    max-width: 100%;
    padding: 14px 28px;
    font-size: 0.95rem;
    border-radius: 10px;
  }
  
  @media (max-width: 360px) {
    padding: 12px 24px;
    font-size: 0.9rem;
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
  max-width: 500px;
  width: 100%;
  height: auto;
  border-radius: 24px;
  background: #fff;
  object-fit: cover;
  filter: brightness(1.08) contrast(1.15) saturate(1.05);
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  
  &:hover {
    transform: translateY(-8px) scale(1.02);
  }
  
  @media (max-width: 800px) {
    max-width: 100%;
    width: 90%;
    border-radius: 20px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 600px) {
    width: 85%;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 480px) {
    width: 90%;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 360px) {
    width: 95%;
    border-radius: 14px;
  }
}
</style> 