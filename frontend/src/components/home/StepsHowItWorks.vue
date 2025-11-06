<template>
  <section class="steps-how-section">
    <!-- Éléments décoratifs animés -->
    <div class="steps-decoration">
      <div class="decoration-wave wave-1"></div>
      <div class="decoration-wave wave-2"></div>
    </div>
    
    <div class="steps-how-header">
      <div class="header-badge">
        <span class="badge-icon">🚀</span>
        <span class="badge-text">Parcours simplifié</span>
      </div>
      <h2 class="steps-how-title">
        {{ titre }} <span class="steps-how-highlight">{{ highlight }}</span> {{ titreFin }}
      </h2>
      <p class="steps-how-desc">{{ description }}</p>
    </div>
    
    <!-- Ligne de connexion pour desktop -->
    <div class="steps-connection-line" v-if="etapes.length > 1">
      <div class="connection-line"></div>
    </div>
    
    <div class="steps-how-steps">
      <div 
        v-for="(etape, idx) in etapes" 
        :key="etape.numero" 
        class="steps-how-step"
        :class="{ 'step-animated': true }"
        :style="{ '--step-index': idx }"
      >
        <!-- Glow effect -->
        <div class="step-glow"></div>
        
        <div
          class="steps-how-step-num"
          :style="{ background: getStepColor(idx), boxShadow: `0 4px 20px ${getStepShadow(idx)}` }"
        >
          <span class="num-text">{{ etape.numero }}</span>
          <div class="num-pulse"></div>
        </div>
        
        <div class="steps-how-step-icon">
          <div class="icon-wrapper">
            <span v-if="typeof etape.icon === 'string'" class="step-svg step-emoji">{{ etape.icon }}</span>
            <component v-else :is="etape.icon" class="step-svg" />
          </div>
        </div>
        
        <h3 class="steps-how-step-title">{{ etape.titre }}</h3>
        <p class="steps-how-step-desc">{{ etape.description }}</p>
        
        <!-- Flèche animée pour desktop -->
        <div v-if="idx < etapes.length - 1" class="steps-how-arrow">
          <div class="arrow-path">
            <svg width="40" height="40" viewBox="0 0 40 40">
              <path d="M 10 20 L 30 20 M 25 15 L 30 20 L 25 25" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
    
    <div class="steps-how-cta-section" v-if="ctaTop || titreBas">
      <div class="steps-how-cta-container">
        <div class="steps-how-cta-top" v-if="ctaTop">{{ ctaTop }}</div>
        <h4 class="steps-how-title-bas">{{ titreBas }}</h4>
        <div class="steps-how-cta-group">
          <button class="steps-how-cta-main" @click="$emit('cta-main')">
            <span class="cta-text">{{ ctaText }}</span>
            <span class="cta-icon">→</span>
          </button>
          <button class="steps-how-cta-secondary" @click="$emit('cta-secondary')">
            {{ ctaSecondary }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

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

const emit = defineEmits(['cta-main', 'cta-secondary'])

const bleu = '#2a38b7'
const vert = '#3ec28f'

function getStepColor(idx) {
  // Dégradé de couleurs pour chaque étape
  const colors = [
    'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'
  ]
  return colors[idx % colors.length] || vert
}

function getStepShadow(idx) {
  const shadows = [
    'rgba(16, 185, 129, 0.3)',
    'rgba(59, 130, 246, 0.3)',
    'rgba(139, 92, 246, 0.3)'
  ]
  return shadows[idx % shadows.length] || 'rgba(62,194,143,0.18)'
}

// Animation au scroll
onMounted(() => {
  const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('step-visible')
      }
    })
  }, observerOptions)
  
  const steps = document.querySelectorAll('.steps-how-step')
  steps.forEach(step => observer.observe(step))
})
</script>

<style scoped lang="scss">
@use '@/assets/variables.scss' as *;
.steps-how-section {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #ffffff 100%);
  padding: 80px 0 64px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

// Éléments décoratifs
.steps-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.decoration-wave {
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, transparent 70%);
  animation: waveFloat 20s ease-in-out infinite;
  
  &.wave-1 {
    top: -50%;
    left: -50%;
    animation-delay: 0s;
  }
  
  &.wave-2 {
    bottom: -50%;
    right: -50%;
    animation-delay: 10s;
  }
}

@keyframes waveFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(30px, -30px) scale(1.1);
    opacity: 0.7;
  }
}
.steps-how-header {
  margin-bottom: 56px;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s ease-out;
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

.header-badge {
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
  
  .badge-icon {
    font-size: 1rem;
    animation: bounce 2s ease-in-out infinite;
  }
  
  .badge-text {
    letter-spacing: 0.02em;
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

.steps-how-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 16px;
  margin-top: 0;
  padding-top: 0;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.steps-how-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}

.steps-how-desc {
  color: #475569;
  font-size: 1.2rem;
  margin-bottom: 0;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

// Ligne de connexion pour desktop
.steps-connection-line {
  position: relative;
  max-width: 1200px;
  margin: 0 auto -48px;
  height: 2px;
  z-index: 0;
  
  .connection-line {
    position: absolute;
    top: 50%;
    left: 15%;
    right: 15%;
    height: 2px;
    background: linear-gradient(90deg, 
      rgba(16, 185, 129, 0.3) 0%,
      rgba(59, 130, 246, 0.3) 50%,
      rgba(139, 92, 246, 0.3) 100%
    );
    border-radius: 2px;
    animation: lineFlow 3s ease-in-out infinite;
  }
  
  @media (max-width: 900px) {
    display: none;
  }
}

@keyframes lineFlow {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

.steps-how-steps {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 40px;
  margin: 48px auto 0 auto;
  max-width: 1200px;
  padding: 0 2vw;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.steps-how-step {
  background: linear-gradient(135deg, #ffffff 0%, #fafaff 100%);
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  padding: 48px 32px 36px 32px;
  min-width: 280px;
  max-width: 360px;
  flex: 1 1 320px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 2px solid transparent;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateY(40px);
  
  &.step-visible {
    opacity: 1;
    transform: translateY(0);
    animation: stepReveal 0.6s ease-out forwards;
    animation-delay: calc(var(--step-index) * 0.2s);
  }
  
  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    border-color: rgba(99, 102, 241, 0.2);
    
    .step-glow {
      opacity: 1;
    }
    
    .steps-how-step-num {
      transform: scale(1.1) rotate(5deg);
    }
    
    .icon-wrapper {
      transform: scale(1.1) rotate(-5deg);
    }
  }
}

@keyframes stepReveal {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.step-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
  border-radius: 24px;
  filter: blur(30px);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
}
.steps-how-step-num {
  color: #fff;
  font-weight: 800;
  font-size: 1.2rem;
  border-radius: 50%;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -48px auto 24px auto;
  border: 4px solid #ffffff;
  z-index: 2;
  position: relative;
  transition: transform 0.3s ease;
  
  .num-text {
    position: relative;
    z-index: 2;
  }
  
  .num-pulse {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: inherit;
    opacity: 0.5;
    animation: pulse 2s ease-in-out infinite;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0;
  }
}
.steps-how-step-icon {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(59, 130, 246, 0.08) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, transparent 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover::before {
    opacity: 1;
  }
}

.step-svg {
  font-size: 3rem;
  width: 48px;
  height: 48px;
  display: block;
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
  line-height: 1;
  
  // Pour les emojis, on les affiche normalement
  &.step-emoji {
    background: none !important;
    -webkit-background-clip: initial !important;
    -webkit-text-fill-color: initial !important;
    background-clip: initial !important;
    color: initial !important;
    font-size: 3.5rem;
    font-style: normal;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  
  // Pour les composants SVG (si utilisé plus tard)
  &:not(.step-emoji) svg {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  &:hover {
    transform: scale(1.1);
  }
}
.steps-how-step-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 12px;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.steps-how-step-desc {
  color: #475569;
  font-size: 1.05rem;
  margin-bottom: 0;
  line-height: 1.6;
}

.steps-how-arrow {
  position: absolute;
  right: -50px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  pointer-events: none;
  color: #a78bfa;
  
  .arrow-path {
    animation: arrowMove 2s ease-in-out infinite;
    
    svg {
      filter: drop-shadow(0 2px 4px rgba(167, 139, 250, 0.3));
    }
  }
  
  @media (max-width: 900px) {
    display: none;
  }
}

@keyframes arrowMove {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(8px);
  }
}
.steps-how-cta-section {
  margin-top: 80px;
  padding: 80px 0;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f0f9ff 100%);
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 50%, rgba(42, 56, 183, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(102, 126, 234, 0.05) 0%, transparent 50%);
    pointer-events: none;
  }
}

.steps-how-cta-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2vw;
  text-align: center;
  position: relative;
  z-index: 1;
}

.steps-how-cta-top {
  margin: 0 0 16px 0;
  color: #2a38b7;
  font-weight: 600;
  font-size: 1.15rem;
  letter-spacing: 0.02em;
}

.steps-how-title-bas {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 32px;
  line-height: 1.3;
  letter-spacing: -0.01em;
}
.steps-how-cta-group {
  display: flex;
  gap: 18px;
  justify-content: center;
  flex-wrap: wrap;
}
.steps-how-cta-main {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  font-weight: 700;
  font-size: 1.15rem;
  border: none;
  border-radius: 14px;
  padding: 20px 48px;
  cursor: pointer;
  box-shadow: 0 6px 24px rgba(42, 56, 183, 0.25);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
  }
  
  &:hover {
    background: linear-gradient(135deg, #1e2a9a 0%, #5a67d8 100%);
    transform: translateY(-3px);
    box-shadow: 0 10px 32px rgba(42, 56, 183, 0.35);
    
    &::before {
      width: 300px;
      height: 300px;
    }
    
    .cta-icon {
      transform: translateX(5px);
    }
  }
  
  .cta-text {
    position: relative;
    z-index: 1;
  }
  
  .cta-icon {
    position: relative;
    z-index: 1;
    transition: transform 0.3s ease;
    font-size: 1.2rem;
  }
  
  &:active {
    transform: translateY(-1px);
  }
}

.steps-how-cta-secondary {
  background: #ffffff;
  color: #2a38b7;
  font-weight: 600;
  font-size: 1.1rem;
  border: 2px solid rgba(42, 56, 183, 0.2);
  border-radius: 14px;
  padding: 20px 40px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  
  &:hover {
    background: #f8fafc;
    border-color: rgba(42, 56, 183, 0.4);
    color: #1e2a9a;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(42, 56, 183, 0.15);
  }
  
  &:active {
    transform: translateY(0);
  }
}
@media (max-width: 900px) {
  .steps-how-steps {
    flex-direction: column;
    gap: 32px;
    padding: 0 4vw;
  }
  .steps-how-step {
    max-width: 100%;
    min-width: 0;
    padding: 40px 28px 32px 28px;
  }
  .steps-how-arrow {
    display: none;
  }
  
  .steps-how-cta-section {
    padding: 60px 0;
  }
  
  .steps-how-title-bas {
    font-size: 1.75rem;
  }
}

@media (max-width: 600px) {
  .steps-how-title {
    font-size: 2rem;
  }
  
  .steps-how-desc {
    font-size: 1.05rem;
  }
  
  .steps-how-cta-section {
    margin-top: 60px;
    padding: 60px 0;
  }
  
  .steps-how-title-bas {
    font-size: 1.5rem;
    margin-bottom: 28px;
  }
  
  .steps-how-cta-main,
  .steps-how-cta-secondary {
    width: 100%;
    max-width: 320px;
    padding: 18px 36px;
    font-size: 1.05rem;
  }
  
  .steps-how-step {
    padding: 36px 24px 28px 24px;
    border-radius: 20px;
  }
  
  .steps-how-step-num {
    width: 52px;
    height: 52px;
    font-size: 1.1rem;
  }
  
  .icon-wrapper {
    width: 72px;
    height: 72px;
  }
  
  .step-svg {
    font-size: 2.5rem;
  }
  
  .steps-how-step-title {
    font-size: 1.2rem;
  }
  
  .steps-how-step-desc {
    font-size: 1rem;
  }
  
  .steps-how-cta-main,
  .steps-how-cta-secondary {
    width: 100%;
    max-width: 320px;
    padding: 16px 32px;
  }
}

@media (max-width: 480px) {
  .steps-how-section {
    padding: 60px 0 48px 0;
  }
  
  .steps-how-title {
    font-size: 1.75rem;
  }
  
  .header-badge {
    padding: 6px 16px;
    font-size: 0.8rem;
    margin-bottom: 20px;
  }
  
  .steps-how-cta-section {
    margin-top: 48px;
    padding: 48px 0;
  }
  
  .steps-how-title-bas {
    font-size: 1.35rem;
    margin-bottom: 24px;
  }
  
  .steps-how-cta-top {
    font-size: 1rem;
    margin-bottom: 12px;
  }
  
  .steps-how-cta-main,
  .steps-how-cta-secondary {
    padding: 16px 32px;
    font-size: 1rem;
  }
  
  .steps-how-step {
    padding: 32px 20px 24px 20px;
  }
}
</style> 