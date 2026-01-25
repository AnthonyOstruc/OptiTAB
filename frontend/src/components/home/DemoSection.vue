<template>
  <section class="demo-section" id="demo">
    <div class="demo-container">
      <!-- Titre accrocheur -->
      <div class="demo-header">
        <div class="header-badge">
          <span class="badge-icon">✨</span>
          <span class="badge-text">Découvrez OptiTAB en action</span>
        </div>
        <h2 class="demo-title">
          Voyez comment <span class="demo-highlight">OptiTAB</span> transforme l'apprentissage
        </h2>
        <p class="demo-desc">
          Des exercices interactifs, des corrections détaillées, un suivi personnalisé et des synthèses pour progresser rapidement
        </p>
      </div>

      <!-- Conteneur des GIFs côte à côte -->
      <div class="demo-gifs-container">
        <!-- GIF Desktop -->
        <div class="demo-gif-card demo-gif-card-desktop">
          <div class="demo-gif-label">
            <span class="label-icon">💻</span>
            <span class="label-text">Version Desktop</span>
          </div>
          <div class="demo-gif-wrapper demo-gif-wrapper-desktop">
            <img 
              src="/video/optitab-demo-exercices.gif" 
              alt="Démonstration OptiTAB version desktop" 
              class="demo-gif"
            />
          </div>
          <p class="demo-gif-caption">Interface complète pour travailler confortablement</p>
        </div>

        <!-- GIF Mobile -->
        <div class="demo-gif-card demo-gif-card-mobile">
          <div class="demo-gif-label">
            <span class="label-icon">📱</span>
            <span class="label-text">Version Mobile</span>
          </div>
          <div class="demo-gif-wrapper demo-gif-wrapper-mobile">
            <img 
              src="/video/optitab-demo-mobile.gif" 
              alt="Démonstration OptiTAB version mobile" 
              class="demo-gif"
            />
          </div>
          <p class="demo-gif-caption">Étudiez partout, à tout moment</p>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="demo-cta-container">
        <h3 class="demo-cta-title">Rejoignez OptiTAB dès maintenant</h3>
        <p class="demo-cta-desc">Accédez à des milliers d'exercices et progressez à votre rythme</p>
        <div class="demo-cta-buttons">
          <button class="demo-cta-primary" @click="$emit('cta-subscribe')">
            Commencer gratuitement
          </button>
          <button class="demo-cta-secondary" @click="$emit('cta-pricing')">
            Voir les tarifs
          </button>
        </div>
      </div>
    </div>

    <!-- Éléments décoratifs -->
    <div class="demo-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

defineEmits(['cta-subscribe', 'cta-pricing'])

// Animation au scroll
onMounted(() => {
  const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
      }
    })
  }, observerOptions)
  
  const elements = document.querySelectorAll('.demo-gif-card, .demo-header, .demo-cta-container')
  elements.forEach(el => observer.observe(el))
})
</script>

<style scoped lang="scss">
.demo-section {
  background: #ffffff;
  padding: 100px 0;
  position: relative;
  overflow: hidden;
  scroll-margin-top: 80px;
}

.demo-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2vw;
  position: relative;
  z-index: 1;
}

// Header
.demo-header {
  text-align: center;
  margin-bottom: 40px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
  
  &.animate-in {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.08));
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 50px;
  padding: 10px 24px;
  margin-bottom: 24px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #6366f1;
  
  .badge-icon {
    font-size: 1.1rem;
    animation: sparkle 2s ease-in-out infinite;
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

.demo-title {
  font-size: 3rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 20px;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.demo-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}

.demo-desc {
  font-size: 1.25rem;
  color: #475569;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
}

// Conteneur des GIFs
.demo-gifs-container {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 40px;
  margin-bottom: 80px;
  align-items: start;
}

.demo-gif-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 24px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateY(40px);
  
  &.animate-in {
    opacity: 1;
    transform: translateY(0);
    
    &:nth-child(1) {
      animation: slideInLeft 0.8s ease-out forwards;
    }
    
    &:nth-child(2) {
      animation: slideInRight 0.8s ease-out forwards;
      animation-delay: 0.2s;
    }
  }
  
  &:hover {
    transform: translateY(-8px);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.demo-gif-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 8px 16px;
  margin-bottom: 16px;
  font-weight: 700;
  font-size: 0.9rem;
  color: #0369a1;
  width: 100%;
  
  .label-icon {
    font-size: 1.2rem;
  }
}

.demo-gif-wrapper {
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-gif-wrapper-desktop {
  width: 100%;
}

.demo-gif-wrapper-mobile {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.demo-gif {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

.demo-gif-caption {
  text-align: center;
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
}

// Call to Action
.demo-cta-container {
  text-align: center;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  border-radius: 24px;
  padding: 60px 40px;
  box-shadow: 0 10px 40px rgba(42, 56, 183, 0.2);
  position: relative;
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s ease-out;
  
  &.animate-in {
    opacity: 1;
    transform: translateY(0);
  }
}

.demo-cta-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
  position: relative;
  z-index: 1;
}

.demo-cta-desc {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 36px;
  position: relative;
  z-index: 1;
}

.demo-cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.demo-cta-primary {
  background: #ffffff;
  color: #2a38b7;
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  border-radius: 12px;
  padding: 16px 40px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    background: #f8f9fa;
  }
  
  &:active {
    transform: translateY(0);
  }
}

.demo-cta-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 16px 36px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }
  
  &:active {
    transform: translateY(0);
  }
}

// Décorations
.demo-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
  animation: floatCircle 20s ease-in-out infinite;
  
  &.circle-1 {
    width: 400px;
    height: 400px;
    top: -200px;
    left: -100px;
    animation-delay: 0s;
  }
  
  &.circle-2 {
    width: 300px;
    height: 300px;
    top: 50%;
    right: -150px;
    animation-delay: 7s;
  }
  
  &.circle-3 {
    width: 500px;
    height: 500px;
    bottom: -250px;
    left: 50%;
    animation-delay: 14s;
  }
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

// Responsive
@media (max-width: 1024px) {
  .demo-gifs-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .demo-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .demo-section {
    padding: 70px 0;
  }
  
  .demo-title {
    font-size: 2rem;
  }
  
  .demo-desc {
    font-size: 1.1rem;
  }
  
  .demo-gifs-container {
    grid-template-columns: 1fr;
    gap: 28px;
  }
  
  .demo-gif-wrapper-mobile {
    max-width: 280px;
  }
  
  .demo-cta-container {
    padding: 48px 32px;
    border-radius: 24px;
  }
  
  .demo-cta-title {
    font-size: 2rem;
  }
  
  .demo-cta-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .demo-cta-primary,
  .demo-cta-secondary {
    width: 100%;
    max-width: 350px;
    margin: 0 auto;
  }
}

@media (max-width: 600px) {
  .demo-section {
    padding: 60px 0;
  }
  
  .demo-header {
    margin-bottom: 36px;
  }
  
  .demo-title {
    font-size: 1.75rem;
  }
  
  .demo-desc {
    font-size: 1rem;
  }
  
  .demo-gif-card {
    padding: 20px;
    border-radius: 20px;
  }
  
  .demo-gifs-container {
    margin-bottom: 60px;
  }
  
  .demo-gif-wrapper-mobile {
    max-width: 250px;
  }
  
  .demo-cta-container {
    padding: 40px 24px;
  }
  
  .demo-cta-title {
    font-size: 1.75rem;
  }
  
  .demo-cta-desc {
    font-size: 1.05rem;
  }
  
  .demo-cta-primary {
    padding: 18px 36px;
    font-size: 1.1rem;
  }
  
  .demo-cta-secondary {
    padding: 16px 32px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .header-badge {
    padding: 8px 18px;
    font-size: 0.85rem;
  }
  
  .demo-title {
    font-size: 1.5rem;
  }
  
  .demo-gif-wrapper-mobile {
    max-width: 220px;
  }
  
  .demo-cta-title {
    font-size: 1.5rem;
  }
}
</style>
