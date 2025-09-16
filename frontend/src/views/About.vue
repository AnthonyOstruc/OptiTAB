<template>
  <MainLayout>
    <div class="about-page">
      <!-- Hero Section Pédagogique -->
      <div class="hero-section">
        <div class="hero-content">
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
                <img src="/icons/ResultatsGarantis.svg?v=2" alt="Résultats" class="icon" />
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
                :class="{ 'highlight-text': p.includes('@') || p.includes('www') || p.includes('WhatsApp') }"
                v-html="p"
              >
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

            <!-- Additional Content -->
            <div v-if="section.additionalContent" class="text-content">
              <p 
                v-for="(p, j) in section.additionalContent" 
                :key="'additional-' + j" 
                class="content-paragraph"
                v-html="p"
              >
              </p>
            </div>

            <!-- Social Media Icons -->
            <div v-if="section.socialMedia" class="social-media-section">
              <div class="social-media-row highlight-text">
                <span class="social-media-label">📱 Réseaux sociaux : @Opti.TAB</span>
                <div class="social-media-icons-inline">
                  <a href="https://instagram.com/optitabedu" target="_blank" class="social-icon-inline instagram-icon">
                    <svg class="social-icon-svg-inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.919-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" fill="currentColor"/>
                    </svg>
                  </a>
                  <a href="https://facebook.com/optitabedu" target="_blank" class="social-icon-inline facebook-icon">
                    <svg class="social-icon-svg-inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" fill="currentColor"/>
                    </svg>
                  </a>
                  <a href="https://linkedin.com/company/optitabedu" target="_blank" class="social-icon-inline linkedin-icon">
                    <svg class="social-icon-svg-inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/>
                    </svg>
                  </a>
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
              <a href="mailto:contact@optitab.net" class="cta-button secondary">
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
    '🚀': '/icons/ResultatsGarantis.svg',
    '📚': '/icons/proposeoptitab.svg',
    '🎯': '/icons/notremission.svg',
    '💡': '/icons/uniqueOpitab.svg',
    '👤': '/icons/quisommenous.svg',
    '👥': '/icons/AuteursExperts.svg',
    '📈': '/icons/visionavenir.svg',
    '📊': '/icons/SuiviProgression.svg',
    '🔄': '/icons/ApprentissageFlexible.svg',
    '🎓': '/icons/ResultatsGarantis.svg',
    '📬': '/icons/contactEchanges.svg',
    '👪': '/icons/motParent.svg',
    '📧': '/icons/mail.svg',
    '✅': '/icons/ApprentissageFlexible.svg'
  }
  return iconMap[emoji] || '/icons/ResultatsGarantis.svg'
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
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 2rem;
  margin-top: 20px;
}

.hero-content {
  width: 100%;
}


.hero-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Hero Stats */
.hero-stats {
  display: flex;
  gap: 3rem;
  justify-content: center;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2.2rem;
  font-weight: 700;
  color: #6366f1;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.95rem;
  color: #6b7280;
  font-weight: 500;
}


/* Why Section */
.why-section {
  background: transparent;
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
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
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
  transform: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: #f8fafc;
}

.benefit-icon {
  width: 120px;
  height: 120px;
  background: transparent;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.benefit-icon .icon {
  width: 6rem;
  height: 6rem;
  filter: none;
  color: #6366f1;
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
  padding: 0 2rem 0 2rem;
}

/* Section Styles */
.about-section {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  backdrop-filter: blur(10px);
}

.about-section:hover {
  transform: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.section-icon {
  width: 120px;
  height: 120px;
  background: transparent;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-emoji {
  width: 5.4rem;
  height: 5.4rem;
  filter: none;
  color: #2a38b7;
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
  border-left: 4px solid #6366f1;
  font-weight: 500;
}

.contact-link {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.contact-link:hover {
  color: #4f46e5;
  text-decoration: underline;
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
  background: #f8fafc;
  transform: none;
}

.feature-bullet {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
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

/* Social Media Section */
.social-media-section {
  margin-top: 1.5rem;
}

.social-media-row {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
}

.social-media-label {
  font-size: 1.05rem;
  color: #374151;
  font-weight: 500;
  margin: 0;
}

.social-media-icons-inline {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-left: 0.5rem;
}

.social-media-icons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: #fff;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.social-icon:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.social-icon:nth-child(1):hover {
  border-color: #E4405F;
  background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
}

.social-icon:nth-child(2):hover {
  border-color: #1877F2;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.social-icon:nth-child(3):hover {
  border-color: #0A66C2;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.social-icon-svg {
  width: 32px;
  height: 32px;
}

/* Couleurs spécifiques pour chaque réseau social */
.instagram-icon .social-icon-svg {
  color: #E4405F;
}

.facebook-icon .social-icon-svg {
  color: #1877F2;
}

.linkedin-icon .social-icon-svg {
  color: #0A66C2;
}

/* Effets de survol avec couleurs */
.instagram-icon:hover .social-icon-svg {
  color: #C13584;
}

.facebook-icon:hover .social-icon-svg {
  color: #166FE5;
}

.linkedin-icon:hover .social-icon-svg {
  color: #004182;
}

/* Icônes en ligne */
.social-icon-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border-radius: 6px;
  border: none;
  transition: all 0.3s ease;
  text-decoration: none;
  box-shadow: none;
}

.social-icon-inline:hover {
  transform: none;
  box-shadow: none;
}

.instagram-icon:hover {
  border: none;
  background: transparent;
}

.facebook-icon:hover {
  border: none;
  background: transparent;
}

.linkedin-icon:hover {
  border: none;
  background: transparent;
}

.social-icon-svg-inline {
  width: 20px;
  height: 20px;
}

/* Couleurs spécifiques pour les icônes en ligne */
.instagram-icon .social-icon-svg-inline {
  color: #E4405F;
}

.facebook-icon .social-icon-svg-inline {
  color: #1877F2;
}

.linkedin-icon .social-icon-svg-inline {
  color: #0A66C2;
}

/* Effets de survol avec couleurs pour les icônes en ligne */
.instagram-icon:hover .social-icon-svg-inline {
  color: #C13584;
}

.facebook-icon:hover .social-icon-svg-inline {
  color: #166FE5;
}

.linkedin-icon:hover .social-icon-svg-inline {
  color: #004182;
}


/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 4rem 2rem;
  margin-top: 0;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
}

.cta-card {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.cta-text {
  font-size: 1.2rem;
  color: #6b7280;
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
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.cta-button.primary:hover {
  transform: none;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.cta-button.secondary {
  background: transparent;
  color: #6366f1;
  border-color: #6366f1;
}

.cta-button.secondary:hover {
  background: #6366f1;
  color: #fff;
  transform: none;
}

.button-icon {
  width: 1.2rem;
  height: 1.2rem;
  filter: none;
}

.cta-guarantee {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.95rem;
}

.guarantee-icon {
  width: 1.1rem;
  height: 1.1rem;
  filter: none;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    padding: 3rem 1.5rem;
  }
  
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-stats {
    gap: 2rem;
  }
  
  .benefits-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 600px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-stats {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .content-container {
    padding: 0 1rem 0 1rem;
  }
  
  .about-section {
    padding: 2rem;
  }
  
  .section-title {
    font-size: 1.6rem;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
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
    width: 100px;
    height: 100px;
  }
  
  .icon-emoji {
    width: 4.5rem;
    height: 4.5rem;
  }
  
  .feature-item {
    padding: 0.75rem;
  }
  
  .feature-text {
    font-size: 1rem;
  }
  
  .hero-badge-visual {
    font-size: 0.9rem;
    padding: 0.6rem 1.2rem;
  }
  
  .hero-badge-secondary {
    font-size: 0.8rem;
    padding: 0.5rem 1rem;
  }
}
</style> 