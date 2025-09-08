<template>
  <MainLayout>
    <div class="about-page">
      <!-- Hero Section Pédagogique -->
      <div class="hero-section">
        <div class="hero-content">
          <div class="hero-badge">
            <img src="/icons/math.svg" alt="Éducation" class="badge-icon" />
            <span class="badge-text">Éducation Innovante</span>
          </div>
          <h1 class="hero-title">
            Votre enfant mérite le 
            <span class="gradient-text">meilleur accompagnement</span>
          </h1>
          <p class="hero-subtitle">
            OptiTAB révolutionne l'apprentissage des sciences avec une approche 
            pédagogique éprouvée, des outils interactifs et un suivi personnalisé 
            pour garantir la réussite de votre enfant.
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">95%</span>
              <span class="stat-label">Amélioration des notes</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">10k+</span>
              <span class="stat-label">Élèves accompagnés</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">24/7</span>
              <span class="stat-label">Support disponible</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon-bg">
              <img src="/icons/exercicesGuides.svg" alt="Cours" class="card-icon" />
            </div>
            <div class="card-content">
              <span class="card-title">Cours Interactifs</span>
              <span class="card-desc">Méthodes éprouvées</span>
            </div>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon-bg">
              <img src="/icons/fichesSynthese.svg" alt="Exercices" class="card-icon" />
            </div>
            <div class="card-content">
              <span class="card-title">Exercices Corrigés</span>
              <span class="card-desc">Progression garantie</span>
            </div>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon-bg">
              <img src="/icons/physics.svg" alt="Sciences" class="card-icon" />
            </div>
            <div class="card-content">
              <span class="card-title">Expertise Scientifique</span>
              <span class="card-desc">Contenu de qualité</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Pourquoi OptiTAB -->
      <div class="why-section">
        <div class="container">
          <div class="section-intro">
            <h2 class="section-title">Pourquoi les parents choisissent OptiTAB ?</h2>
            <p class="section-subtitle">
              Une approche pédagogique éprouvée qui transforme l'apprentissage des sciences
            </p>
          </div>
          <div class="benefits-grid">
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/math.svg" alt="Résultats" class="icon" />
              </div>
              <h3>Résultats Garantis</h3>
              <p>95% de nos élèves améliorent leurs notes de 2 points minimum en 3 mois</p>
            </div>
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/AuteursExperts.svg" alt="Experts" class="icon" />
              </div>
              <h3>Experts Pédagogues</h3>
              <p>Contenu créé par des enseignants expérimentés et des experts en sciences</p>
            </div>
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/SuiviProgression.svg" alt="Suivi" class="icon" />
              </div>
              <h3>Suivi Détaillé</h3>
              <p>Tableau de bord personnalisé pour suivre les progrès en temps réel</p>
            </div>
            <div class="benefit-card">
              <div class="benefit-icon">
                <img src="/icons/ApprentissageFlexible.svg" alt="Flexibilité" class="icon" />
              </div>
              <h3>Apprentissage Flexible</h3>
              <p>Adapté au rythme et au niveau d'apprentissage de votre enfant</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Sections -->
      <div class="content-container">
        <div v-for="(section, i) in about" :key="i" class="about-section">
          <!-- Section Header -->
          <div class="section-header">
            <div class="section-icon">
              <img :src="getSectionIcon(section.emoji)" :alt="section.title" class="icon-emoji" />
            </div>
            <h2 class="section-title">{{ section.title }}</h2>
          </div>

          <!-- Section Content -->
          <div class="section-content">
            <!-- Text Content -->
            <div v-if="section.content" class="text-content">
              <p 
                v-for="(p, j) in section.content" 
                :key="j" 
                class="content-paragraph"
                :class="{ 'highlight-text': p.includes('@') || p.includes('www') }"
              >
                {{ p }}
              </p>
            </div>

            <!-- List Content -->
            <div v-if="section.list" class="list-content">
              <ul class="feature-list">
                <li 
                  v-for="(item, k) in section.list" 
                  :key="k" 
                  class="feature-item"
                >
                  <div class="feature-bullet"></div>
                  <span class="feature-text">{{ item }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Témoignages -->
      <div class="testimonials-section">
        <div class="container">
          <h2 class="testimonials-title">Ce que disent les parents</h2>
          <div class="testimonials-grid">
            <div class="testimonial-card">
              <div class="testimonial-content">
                <p>"OptiTAB a transformé l'apprentissage des maths pour mon fils. Il a gagné 3 points en 2 mois !"</p>
              </div>
              <div class="testimonial-author">
                <div class="author-avatar">
                  <img src="/icons/math.svg" alt="Famille" class="avatar-icon" />
                </div>
                <div class="author-info">
                  <span class="author-name">Marie L.</span>
                  <span class="author-detail">Maman de Thomas, 15 ans</span>
                </div>
              </div>
            </div>
            <div class="testimonial-card">
              <div class="testimonial-content">
                <p>"L'approche pédagogique est excellente. Ma fille adore les exercices interactifs !"</p>
              </div>
              <div class="testimonial-author">
                <div class="author-avatar">
                  <img src="/icons/physics.svg" alt="Famille" class="avatar-icon" />
                </div>
                <div class="author-info">
                  <span class="author-name">Pierre D.</span>
                  <span class="author-detail">Papa de Sophie, 13 ans</span>
                </div>
              </div>
            </div>
            <div class="testimonial-card">
              <div class="testimonial-content">
                <p>"Le suivi des progrès est fantastique. Je vois exactement où ma fille progresse."</p>
              </div>
              <div class="testimonial-author">
                <div class="author-avatar">
                  <img src="/icons/SuiviProgression.svg" alt="Famille" class="avatar-icon" />
                </div>
                <div class="author-info">
                  <span class="author-name">Sophie M.</span>
                  <span class="author-detail">Maman de Lucas, 16 ans</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="cta-section">
        <div class="cta-card">
          <div class="cta-content">
            <h3 class="cta-title">Donnez à votre enfant les clés de la réussite</h3>
            <p class="cta-text">
              Rejoignez des milliers de familles qui font confiance à OptiTAB 
              pour l'avenir scolaire de leurs enfants.
            </p>
            <div class="cta-buttons">
              <router-link to="/" class="cta-button primary">
                <img src="/icons/math.svg" alt="Éducation" class="button-icon" />
                Commencer l'essai gratuit
              </router-link>
              <a href="mailto:contact@optitab.com" class="cta-button secondary">
                <img src="/icons/mail.svg" alt="Contact" class="button-icon" />
                Parler à un expert
              </a>
            </div>
            <div class="cta-guarantee">
              <img src="/icons/ApprentissageFlexible.svg" alt="Garantie" class="guarantee-icon" />
              <span class="guarantee-text">Essai gratuit de 7 jours • Résultats garantis • Support 24/7</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import about from '@/config/aboutContent.js'

// Fonction pour mapper les emojis vers les icônes SVG
const getSectionIcon = (emoji) => {
  const iconMap = {
    '🚀': '/icons/math.svg',
    '📚': '/icons/exercicesGuides.svg',
    '🎯': '/icons/fichesSynthese.svg',
    '💡': '/icons/physics.svg',
    '👥': '/icons/AuteursExperts.svg',
    '📊': '/icons/SuiviProgression.svg',
    '🔄': '/icons/ApprentissageFlexible.svg',
    '🎓': '/icons/math.svg',
    '📧': '/icons/mail.svg',
    '✅': '/icons/ApprentissageFlexible.svg'
  }
  return iconMap[emoji] || '/icons/math.svg'
}
</script>

<style scoped>
/* Page Container */
.about-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* Hero Section Pédagogique */
.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  position: relative;
  overflow: hidden;
}

.hero-content {
  flex: 1;
  max-width: 600px;
  z-index: 2;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(78, 99, 194, 0.3);
}

.badge-icon {
  width: 1.5rem;
  height: 1.5rem;
  filter: brightness(0) invert(1);
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: #1f2937;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

/* Hero Stats */
.hero-stats {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  color: #4e63c2;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

/* Hero Visual */
.hero-visual {
  flex: 1;
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-card {
  position: absolute;
  background: #fff;
  padding: 1.5rem;
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  animation: float 6s ease-in-out infinite;
  min-width: 200px;
}

.floating-card:nth-child(1) {
  top: 15%;
  left: 5%;
  animation-delay: 0s;
}

.floating-card:nth-child(2) {
  top: 45%;
  right: 10%;
  animation-delay: 2s;
}

.floating-card:nth-child(3) {
  bottom: 15%;
  left: 15%;
  animation-delay: 4s;
}

.card-icon-bg {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon {
  width: 1.5rem;
  height: 1.5rem;
  filter: brightness(0) invert(1);
}

.card-content {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-weight: 700;
  color: #1f2937;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.card-desc {
  font-size: 0.85rem;
  color: #6b7280;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Why Section */
.why-section {
  background: #fff;
  padding: 4rem 0;
  margin: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-intro {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.benefit-card {
  background: #f8fafc;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.benefit-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 25px rgba(78, 99, 194, 0.3);
}

.benefit-icon .icon {
  width: 2rem;
  height: 2rem;
  filter: brightness(0) invert(1);
}

.benefit-card h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.benefit-card p {
  color: #6b7280;
  line-height: 1.6;
}

/* Content Container */
.content-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem 4rem 2rem;
}

/* Section Styles */
.about-section {
  background: #fff;
  border-radius: 20px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.about-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.section-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(78, 99, 194, 0.3);
}

.icon-emoji {
  width: 1.8rem;
  height: 1.8rem;
  filter: brightness(0) invert(1);
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.section-content {
  color: #374151;
}

.content-paragraph {
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  color: #4b5563;
}

.highlight-text {
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border-left: 4px solid #4e63c2;
  font-weight: 500;
}

/* Feature List */
.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: #f1f5f9;
  transform: translateX(5px);
}

.feature-bullet {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  border-radius: 50%;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

.feature-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #374151;
  font-weight: 500;
}

/* Testimonials Section */
.testimonials-section {
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  padding: 4rem 0;
  color: #fff;
}

.testimonials-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.testimonial-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.testimonial-content p {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  width: 1.5rem;
  height: 1.5rem;
  filter: brightness(0) invert(1);
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
  font-size: 1rem;
}

.author-detail {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  padding: 4rem 2rem;
  margin-top: 2rem;
}

.cta-card {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 1rem;
}

.cta-text {
  font-size: 1.2rem;
  color: #d1d5db;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.cta-button.primary {
  background: linear-gradient(135deg, #4e63c2 0%, #6b46c1 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(78, 99, 194, 0.4);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(78, 99, 194, 0.6);
}

.cta-button.secondary {
  background: transparent;
  color: #fff;
  border-color: #fff;
}

.cta-button.secondary:hover {
  background: #fff;
  color: #1f2937;
  transform: translateY(-2px);
}

.button-icon {
  width: 1.2rem;
  height: 1.2rem;
  filter: brightness(0) invert(1);
}

.cta-guarantee {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #9ca3af;
  font-size: 0.95rem;
}

.guarantee-icon {
  width: 1.1rem;
  height: 1.1rem;
  filter: brightness(0) invert(1);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 3rem 1.5rem;
  }
  
  .hero-title {
    font-size: 2.8rem;
  }
  
  .hero-visual {
    height: 300px;
    margin-top: 2rem;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .floating-card {
    padding: 1rem;
    min-width: 180px;
  }
  
  .benefits-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .content-container {
    padding: 0 1rem 3rem 1rem;
  }
  
  .about-section {
    padding: 2rem;
  }
  
  .section-title {
    font-size: 1.6rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .cta-button {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
  
  .testimonials-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.8rem;
  }
  
  .hero-badge {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }
  
  .about-section {
    padding: 1.5rem;
  }
  
  .section-header {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .section-icon {
    width: 50px;
    height: 50px;
  }
  
  .icon-emoji {
    width: 1.5rem;
    height: 1.5rem;
  }
  
  .feature-item {
    padding: 0.75rem;
  }
  
  .feature-text {
    font-size: 1rem;
  }
  
  .floating-card {
    min-width: 150px;
    padding: 0.75rem;
  }
  
  .card-title {
    font-size: 0.9rem;
  }
  
  .card-desc {
    font-size: 0.8rem;
  }
}
</style> 