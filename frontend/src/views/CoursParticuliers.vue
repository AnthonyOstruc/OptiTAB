<template>
  <MainLayout>
    <div class="cours-particuliers-page">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-decoration">
          <div class="decoration-circle circle-1"></div>
          <div class="decoration-circle circle-2"></div>
        </div>
        
        <div class="hero-content">
          <div class="hero-badge">
            <span class="badge-icon">🎓</span>
            <span>Cours particuliers d'excellence</span>
          </div>
          
          <h1 class="hero-title">
            Cours Particuliers <span class="title-highlight">Experts</span>
          </h1>
          
          <p class="hero-subtitle">
            Un prof dédié, un objectif clair, une progression mesurée
          </p>
          
          <div class="hero-cta">
            <router-link to="/contact" class="btn-primary">
              Réserver un cours
            </router-link>
            <a href="#professeur" class="btn-secondary" @click.prevent="scrollToProfesseur">
              Rencontrer le professeur
            </a>
          </div>
          
          <div class="hero-reviews">
            <GoogleReviewsCompact />
          </div>
        </div>
      </section>

      <!-- Trust Indicators -->
      <section class="trust-section">
        <div class="trust-container">
          <div class="trust-item">
            <div class="trust-icon">📅</div>
            <div class="trust-content">
              <span class="trust-number">15+</span>
              <span class="trust-label">Années d'expérience</span>
            </div>
          </div>
          <div class="trust-item">
            <div class="trust-icon">🏆</div>
            <div class="trust-content">
              <span class="trust-number">95%</span>
              <span class="trust-label">Taux de réussite</span>
            </div>
          </div>
          <div class="trust-item">
            <div class="trust-icon">👥</div>
            <div class="trust-content">
              <span class="trust-number">300+</span>
              <span class="trust-label">Élèves accompagnés</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="features-section">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">Pourquoi choisir nos cours particuliers ?</h2>
            <p class="section-subtitle">
              Un accompagnement complet pour garantir votre réussite
            </p>
          </div>

          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">👨‍🏫</div>
              <h3 class="feature-title">Professeur expérimenté</h3>
              <p class="feature-desc">
                Diplômé d'une Grande École d'Ingénieur avec 15+ années d'enseignement réussies.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">🎯</div>
              <h3 class="feature-title">Méthode personnalisée</h3>
              <p class="feature-desc">
                Programme adapté à votre niveau et vos objectifs pour progresser efficacement.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">📈</div>
              <h3 class="feature-title">Résultats mesurables</h3>
              <p class="feature-desc">
                Suivi régulier de vos progrès avec évaluations et feedback personnalisés.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">⏰</div>
              <h3 class="feature-title">Horaires flexibles</h3>
              <p class="feature-desc">
                Cours adaptés à votre emploi du temps, en ligne ou en présentiel selon vos besoins.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">💡</div>
              <h3 class="feature-title">Support complet</h3>
              <p class="feature-desc">
                Accès aux ressources OptiTAB et support entre les cours pour vos questions.
              </p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">🎓</div>
              <h3 class="feature-title">Préparation aux examens</h3>
              <p class="feature-desc">
                Entraînement ciblé pour réussir vos contrôles, examens et concours avec confiance.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Professeur Section -->
      <section class="professeur-section" id="professeur">
        <div class="section-container">
          <div class="professeur-card">
            <div class="professeur-header-section">
              <div class="professeur-image-wrapper">
                <img 
                  src="/images/professeurs/anthony.jpg" 
                  alt="Anthony - Professeur de Mathématiques, Physique et Informatique"
                  class="professeur-image"
                />
              </div>
              <div class="professeur-header">
                <h2 class="professeur-name">Anthony</h2>
                <p class="professeur-role">Fondateur & Professeur Expert</p>
              </div>
              <div class="professeur-badge">Fondateur</div>
            </div>
            
            <div class="professeur-content">

              <div class="professeur-specialties">
                <span class="specialty-tag">Mathématiques</span>
                <span class="specialty-tag">Physique</span>
                <span class="specialty-tag">Informatique</span>
                <span class="specialty-tag">Chimie</span>
              </div>

              <div class="professeur-description">
                <h3 class="description-title">Présentation</h3>
                <p>
                  Diplômé de l'ISAE-SUPAERO et de l'École Supérieure d'Ingénieurs ESIB, ingénieur calculateur de structures dans un bureau d'études reconnu, 
                  je mets mon expertise et plus de 15 ans d'expérience en enseignement privé à votre service. Mon objectif ? Vous accompagner 
                  vers l'excellence et vous ouvrir les portes des meilleures écoles.
                </p>
                <p>
                  Que vous soyez en prépa ou au bac, j'adapte mon approche à votre niveau et vos objectifs pour maximiser vos chances de réussite.
                </p>
                <p>
                  Ensemble, transformons vos difficultés en forces et atteignons vos objectifs académiques avec confiance.
                </p>
              </div>

              <div class="professeur-highlights">
                <div class="highlight-item">
                  <span class="highlight-icon">🎓</span>
                  <span class="highlight-text">Diplômé Grande École d'Ingénieur</span>
                </div>
                <div class="highlight-item">
                  <span class="highlight-icon">📊</span>
                  <span class="highlight-text">300+ élèves accompagnés avec succès</span>
                </div>
                <div class="highlight-item">
                  <span class="highlight-icon">⭐</span>
                  <span class="highlight-text">95% de taux de réussite aux examens</span>
                </div>
                <div class="highlight-item">
                  <span class="highlight-icon">💼</span>
                  <span class="highlight-text">15+ années d'expérience dans l'enseignement</span>
                </div>
              </div>

              <div class="professeur-verification">
                <p class="verification-text">
                  Vérifiez mon identité et mes qualifications pour vous rassurer :
                </p>
                <div class="professeur-social-links">
                  <a href="https://www.linkedin.com/in/anthony-tabet-a34aa6192/" target="_blank" rel="noopener noreferrer" class="social-link linkedin-link">
                    <svg class="social-icon-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/>
                    </svg>
                    <span class="social-text">LinkedIn</span>
                  </a>
                  <a href="https://groupe-reussite.fr/cours-particuliers-cours-particuliers-niveaux-ligne-domicile-3452/" target="_blank" rel="noopener noreferrer" class="social-link groupe-link">
                    <span class="social-icon">👥</span>
                    <span class="social-text">Groupe Réussite</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Méthodologie Section -->
      <section class="methodologie-section">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">Méthodologie</h2>
            <p class="section-subtitle">
              Une approche pédagogique centrée sur vos besoins individuels
            </p>
          </div>

          <div class="methodologie-content">
            <p class="methodologie-intro">
              Je centre mon approche pédagogique sur les besoins individuels des élèves, en rendant les concepts de mathématiques, 
              de physique et d'informatique captivants pour tous. En combinant des méthodes innovantes, une adaptation personnalisée 
              et un engagement constant, je guide mes élèves vers une maîtrise approfondie des matières enseignées.
            </p>

            <div class="methodologie-grid">
              <div class="methodologie-card">
                <div class="methodologie-icon">🎯</div>
                <h3 class="methodologie-title">Adaptation personnalisée</h3>
                <p class="methodologie-desc">
                  J'adapte mes cours aux besoins individuels de chaque élève pour assurer une compréhension maximale.
                </p>
              </div>

              <div class="methodologie-card">
                <div class="methodologie-icon">💡</div>
                <h3 class="methodologie-title">Simplicité et clarté</h3>
                <p class="methodologie-desc">
                  Je simplifie les concepts complexes pour les rendre accessibles et faciles à comprendre.
                </p>
              </div>

              <div class="methodologie-card">
                <div class="methodologie-icon">🤝</div>
                <h3 class="methodologie-title">Engagement interactif</h3>
                <p class="methodologie-desc">
                  J'encourage la participation active des élèves pour maintenir leur intérêt et favoriser la compréhension.
                </p>
              </div>

              <div class="methodologie-card">
                <div class="methodologie-icon">📝</div>
                <h3 class="methodologie-title">Feedback régulier</h3>
                <p class="methodologie-desc">
                  Je fournis un feedback constructif pour aider les élèves à identifier leurs forces et leurs faiblesses.
                </p>
              </div>

              <div class="methodologie-card">
                <div class="methodologie-icon">🌟</div>
                <h3 class="methodologie-title">Encouragement et soutien</h3>
                <p class="methodologie-desc">
                  Je crée un environnement positif où les erreurs sont considérées comme des occasions d'apprentissage et où le soutien est toujours disponible.
                </p>
              </div>

              <div class="methodologie-card">
                <div class="methodologie-icon">🎯</div>
                <h3 class="methodologie-title">Objectifs clairs</h3>
                <p class="methodologie-desc">
                  Ensemble, nous fixons des objectifs spécifiques et mesurables pour suivre les progrès.
                </p>
              </div>

              <div class="methodologie-card methodologie-card-featured">
                <div class="methodologie-icon">⏰</div>
                <h3 class="methodologie-title">Disponibilité 7 jours sur 7</h3>
                <p class="methodologie-desc">
                  Les élèves peuvent me contacter à tout moment pour des questions ou des clarifications. Je m'engage à répondre dans les 3h pour un soutien continu en dehors des cours.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Process Section -->
      <section class="process-section">
        <div class="section-container">
          <div class="section-header">
            <h2 class="section-title">Comment ça se passe ?</h2>
            <p class="section-subtitle">
              Un processus simple en 3 étapes pour commencer vos cours
            </p>
          </div>

          <div class="process-grid">
            <div class="process-card">
              <div class="process-icon">🤝</div>
              <h3 class="process-title">Premier contact</h3>
              <p class="process-desc">
                Échange personnalisé pour comprendre vos besoins et définir vos objectifs.
              </p>
            </div>

            <div class="process-card">
              <div class="process-icon">📋</div>
              <h3 class="process-title">Programme personnalisé</h3>
              <p class="process-desc">
                Plan de cours adapté à votre rythme avec des objectifs clairs.
              </p>
            </div>

            <div class="process-card">
              <div class="process-icon">📈</div>
              <h3 class="process-title">Cours & Progression</h3>
              <p class="process-desc">
                Sessions régulières avec suivi continu et feedback personnalisé.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Final -->
      <section class="cta-final-section">
        <div class="cta-final-container">
          <p class="cta-final-subtitle">
            Contactez-nous dès maintenant pour discuter de vos besoins et découvrir notre méthode personnalisée.
          </p>
          <div class="cta-final-buttons">
            <router-link to="/contact" class="btn-cta-primary">
              Réserver un cours
            </router-link>
            <a href="https://wa.me/33764040251?text=Bonjour, j'aimerais poser une question sur les cours particuliers OptiTAB !" target="_blank" class="btn-cta-secondary">
              Poser une question
            </a>
          </div>
          <p class="cta-final-note">
            🔒 Aucune carte bancaire requise • Sans engagement
          </p>
        </div>
      </section>
    </div>
    
    <!-- Bouton WhatsApp -->
    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'aimerais en savoir plus sur les cours particuliers OptiTAB !"
      tooltip="Questions ? Contactez-nous sur WhatsApp !"
    />
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
import GoogleReviewsCompact from '@/components/home/GoogleReviewsCompact.vue'

function scrollToProfesseur(e) {
  e.preventDefault()
  const element = document.getElementById('professeur')
  if (element) {
    const offset = 100 // Offset pour le header fixe
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
    const offsetPosition = elementPosition - offset
    
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
  }
}
</script>

<style scoped>
/* Variables - mêmes couleurs que le home */
:root {
  --primary: #2a38b7;
  --primary-light: #667eea;
  --dark: #0f172a;
  --gray-dark: #475569;
  --gray: #64748b;
  --gray-light: #cbd5e1;
  --gray-lighter: #f1f5f9;
  --white: #ffffff;
}

/* Page Container */
.cours-particuliers-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f1f5f9 100%);
}

/* Hero Section - Style comme le home */
.hero-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 120px 2rem 80px 2rem;
  text-align: center;
  position: relative;
}

.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.8;
}

.circle-1 {
  width: 500px;
  height: 500px;
  top: -150px;
  right: -150px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
}

.circle-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  background: radial-gradient(circle, rgba(42, 56, 183, 0.06) 0%, transparent 70%);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, rgba(42, 56, 183, 0.1), rgba(102, 126, 234, 0.08));
  border: 1px solid rgba(42, 56, 183, 0.2);
  border-radius: 50px;
  padding: 0.6rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #2a38b7;
  margin-bottom: 1.5rem;
  backdrop-filter: blur(10px);
}

.badge-icon {
  font-size: 1.1rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--dark);
  line-height: 1.15;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.title-highlight {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: var(--gray-dark);
  line-height: 1.7;
  margin-bottom: 2.5rem;
  max-width: 750px;
  margin-left: auto;
  margin-right: auto;
}

.hero-cta {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.btn-primary,
.btn-cta-primary {
  display: inline-block;
  padding: 12px 24px;
  background: #2563eb;
  color: #ffffff;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.05rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.15);
}

.btn-primary:hover,
.btn-cta-primary:hover {
  background: #1e40af;
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(37, 99, 235, 0.25);
}

.btn-secondary,
.btn-cta-secondary {
  display: inline-block;
  padding: 12px 24px;
  background: #ffffff;
  color: #1e293b;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.05rem;
  border: 2px solid #cbd5e1;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover,
.btn-cta-secondary:hover {
  background: #f8fafc;
  border-color: #94a3b8;
  color: #0f172a;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.hero-reviews {
  margin-top: 2rem;
}

/* Trust Section */
.trust-section {
  background: linear-gradient(135deg, #f0f4ff 0%, #f8f9ff 50%, #ffffff 100%);
  padding: 3rem 2rem;
  margin-bottom: 0;
  position: relative;
  overflow: hidden;
}

.trust-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

.trust-section::after {
  content: '';
  position: absolute;
  bottom: -50%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(42, 56, 183, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.trust-container {
  max-width: 900px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
  border-radius: 12px;
  border: 1px solid rgba(42, 56, 183, 0.1);
}

.trust-icon {
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 1;
}

.trust-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.trust-number {
  font-size: 1.75rem;
  font-weight: 800;
  color: #2a38b7;
  line-height: 1;
  margin-bottom: 0.25rem;
  text-align: center;
  width: 100%;
}

.trust-label {
  font-size: 0.875rem;
  color: var(--gray);
  font-weight: 600;
  text-align: center;
  width: 100%;
}

/* Section commune */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 1.25rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--dark);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -0.75rem;
  left: 0;
  right: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #2a38b7 0%, #667eea 100%);
  border-radius: 2px;
}

.section-subtitle {
  font-size: 1.15rem;
  color: var(--gray-dark);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Features Section */
.features-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 50%, #f0f4ff 100%);
  position: relative;
}

.features-section::before {
  content: '';
  position: absolute;
  top: 20%;
  right: 5%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.features-section::after {
  content: '';
  position: absolute;
  bottom: 20%;
  left: 5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(42, 56, 183, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.feature-card {
  background: var(--white);
  border: 1px solid rgba(42, 56, 183, 0.1);
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #2a38b7 0%, #667eea 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  border-color: rgba(42, 56, 183, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.12);
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.25rem;
  display: block;
  transition: transform 0.3s ease;
}

.feature-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 0.75rem;
}

.feature-desc {
  font-size: 1rem;
  color: var(--gray);
  line-height: 1.7;
}

/* Professeur Section */
.professeur-section {
  background: linear-gradient(180deg, #ffffff 0%, #f0f4ff 50%, #e0e7ff 100%);
  position: relative;
}

.professeur-section::before {
  content: '';
  position: absolute;
  top: 10%;
  left: 10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(42, 56, 183, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.professeur-section::after {
  content: '';
  position: absolute;
  bottom: 10%;
  right: 10%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.professeur-card {
  background: var(--white);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
  padding: 2.5rem;
}

.professeur-header-section {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(42, 56, 183, 0.1);
  position: relative;
}

.professeur-image-wrapper {
  position: relative;
  flex-shrink: 0;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.professeur-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: #ffffff;
  padding: 0.45rem 0.9rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.4);
  z-index: 2;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.professeur-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.professeur-content {
  display: flex;
  flex-direction: column;
}

.professeur-header {
  flex: 1;
  margin-bottom: 0;
}

.professeur-name {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--dark);
  margin-bottom: 0.5rem;
}

.professeur-role {
  font-size: 1.1rem;
  color: #2a38b7;
  font-weight: 600;
}

.professeur-specialties {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.specialty-tag {
  background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
  color: #2a38b7;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  border: 1px solid rgba(42, 56, 183, 0.15);
}

.professeur-description {
  font-size: 1.05rem;
  color: var(--gray);
  line-height: 1.8;
  margin-bottom: 2rem;
  text-align: justify;
}

.description-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 1rem;
  margin-top: 0;
}

.professeur-description p {
  margin-bottom: 1rem;
}

.professeur-description p:last-child {
  margin-bottom: 0;
}

.professeur-highlights {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
  border-radius: 10px;
  border: 1px solid rgba(42, 56, 183, 0.1);
}

.highlight-icon {
  font-size: 1.5rem;
}

.highlight-text {
  font-size: 0.9rem;
  color: #2a38b7;
  font-weight: 600;
  line-height: 1.4;
}

/* Social Links */
.professeur-verification {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(42, 56, 183, 0.1);
}

.verification-text {
  font-size: 0.95rem;
  color: var(--gray-dark);
  margin-bottom: 1rem;
  font-style: italic;
  line-height: 1.6;
  text-align: center;
}

.professeur-social-links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.social-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f4ff 100%);
  border: 1px solid rgba(42, 56, 183, 0.15);
  border-radius: 10px;
  text-decoration: none;
  color: #2a38b7;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  min-height: 44px;
  box-sizing: border-box;
}

.social-link:hover {
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  border-color: rgba(42, 56, 183, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(42, 56, 183, 0.15);
}

.social-link .social-icon {
  font-size: 1.25rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.social-link .social-icon-svg {
  width: 20px;
  height: 20px;
  color: #0A66C2;
  flex-shrink: 0;
}

.social-link.linkedin-link:hover .social-icon-svg {
  color: #004182;
}

.social-link .social-text {
  color: #2a38b7;
}

/* Méthodologie Section */
.methodologie-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 50%, #f0f4ff 100%);
  position: relative;
}

.methodologie-section::before {
  content: '';
  position: absolute;
  top: 20%;
  right: 5%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.methodologie-section::after {
  content: '';
  position: absolute;
  bottom: 20%;
  left: 5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(42, 56, 183, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.methodologie-content {
  position: relative;
  z-index: 1;
}

.methodologie-intro {
  font-size: 1.2rem;
  color: var(--gray-dark);
  line-height: 2;
  max-width: 900px;
  margin: 0 auto 3rem;
  text-align: justify;
  font-weight: 400;
  letter-spacing: 0.01em;
}

.methodologie-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 1024px) {
  .methodologie-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .methodologie-card-featured {
    grid-column: span 2;
  }
}

.methodologie-card {
  background: var(--white);
  border: 1px solid rgba(42, 56, 183, 0.1);
  border-radius: 16px;
  padding: 2rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.methodologie-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #2a38b7 0%, #667eea 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.methodologie-card:hover {
  border-color: rgba(42, 56, 183, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.12);
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
}

.methodologie-card:hover::before {
  transform: scaleX(1);
}

.methodologie-card-featured {
  grid-column: span 2;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-color: rgba(42, 56, 183, 0.2);
}

.methodologie-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: block;
  transition: transform 0.3s ease;
}

.methodologie-card:hover .methodologie-icon {
  transform: scale(1.1);
}

.methodologie-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 0.75rem;
}

.methodologie-desc {
  font-size: 1rem;
  color: var(--gray);
  line-height: 1.7;
}

/* Process Section */
.process-section {
  background: #ffffff;
  position: relative;
}

.process-section .section-container {
  padding-bottom: 0;
}

.process-section::before {
  content: none;
  width: 0;
  height: 0;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  position: relative;
  z-index: 1;
}

.process-card {
  text-align: center;
  padding: 1.5rem;
  background: var(--white);
  border: 1px solid rgba(42, 56, 183, 0.1);
  border-radius: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.process-card:hover {
  border-color: rgba(42, 56, 183, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.12);
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
}

.process-card:hover .process-icon {
  transform: scale(1.1);
}

.process-icon {
  font-size: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem auto;
  transition: transform 0.3s ease;
  line-height: 1;
}

.process-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 0.75rem;
}

.process-desc {
  font-size: 1rem;
  color: var(--gray);
  line-height: 1.7;
}

/* CTA Final Section */
.cta-final-section {
  background: #ffffff;
  position: relative;
  padding-top: 0;
  margin-top: 0;
}

.cta-final-section::before,
.cta-final-section::after {
  content: none;
  width: 0;
  height: 0;
}

.cta-final-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 2rem 3rem 2rem;
  text-align: center;
  position: relative;
  z-index: 1;
}

.cta-final-subtitle {
  font-size: 1.15rem;
  color: var(--gray-dark);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.cta-final-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.cta-final-note {
  font-size: 0.95rem;
  color: var(--gray);
  font-weight: 500;
  margin-top: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .professeur-card {
    padding: 2rem;
  }

  .professeur-header-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1.5rem;
  }

  .professeur-image-wrapper {
    width: 120px;
    height: 120px;
  }

  .professeur-content {
    padding: 0;
  }

  .professeur-highlights {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 80px 1rem 40px 1rem;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .hero-subtitle {
    font-size: 0.95rem;
  }

  .hero-cta {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    max-width: 280px;
    text-align: center;
    margin: 0 auto;
    padding: 10px 20px;
    font-size: 0.95rem;
  }

  .trust-section {
    padding: 1.5rem 0.5rem;
  }

  .trust-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    max-width: 100%;
  }

  .trust-item {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem 0.5rem;
  }

  .trust-icon {
    font-size: 1.5rem;
  }

  .trust-number {
    font-size: 1.25rem;
  }

  .trust-label {
    font-size: 0.7rem;
    text-align: center;
  }

  .section-container {
    padding: 1.5rem 1rem;
  }

  .section-title {
    font-size: 1.35rem;
  }

  .section-subtitle {
    font-size: 0.9rem;
  }
  
  .section-header {
    margin-bottom: 1rem;
  }

  .feature-card,
  .methodologie-card,
  .process-card {
    padding: 1.25rem;
  }

  .feature-icon,
  .methodologie-icon,
  .process-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
  }

  .feature-title,
  .methodologie-title,
  .process-title {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }

  .feature-desc,
  .methodologie-desc,
  .process-desc {
    font-size: 0.85rem;
    line-height: 1.5;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .methodologie-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .methodologie-card-featured {
    grid-column: span 1;
  }

  .methodologie-intro {
    font-size: 0.95rem;
    margin-bottom: 1.25rem;
    line-height: 1.6;
  }

  .process-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .professeur-card {
    padding: 1.25rem;
  }

  .professeur-header-section {
    flex-direction: row;
    align-items: flex-start;
    text-align: left;
    gap: 1rem;
    padding-bottom: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .professeur-image-wrapper {
    width: 80px;
    height: 80px;
    flex-shrink: 0;
  }

  .professeur-header {
    flex: 1;
    text-align: left;
  }

  .professeur-name {
    font-size: 1.35rem;
    margin-bottom: 0.25rem;
  }

  .professeur-role {
    font-size: 0.85rem;
  }

  .professeur-badge {
    top: 0;
    right: 0;
    font-size: 0.65rem;
    padding: 0.3rem 0.6rem;
  }

  .professeur-specialties {
    justify-content: flex-start;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .specialty-tag {
    font-size: 0.75rem;
    padding: 0.35rem 0.7rem;
  }

  .professeur-description {
    font-size: 0.9rem;
    text-align: left;
    margin-bottom: 1.25rem;
  }

  .description-title {
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
  }

  .professeur-highlights {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
  }

  .highlight-item {
    padding: 0.6rem;
    gap: 0.5rem;
  }

  .highlight-icon {
    font-size: 1.2rem;
  }

  .highlight-text {
    font-size: 0.75rem;
  }

  .professeur-verification {
    margin-top: 1.25rem;
    padding-top: 1.25rem;
  }

  .verification-text {
    font-size: 0.8rem;
    text-align: left;
    margin-bottom: 0.75rem;
  }

  .professeur-social-links {
    justify-content: flex-start;
    gap: 0.75rem;
  }

  .social-link {
    font-size: 0.8rem;
    padding: 0.55rem 0.95rem;
  }

  .cta-final-container {
    padding: 1rem 1rem;
  }

  .cta-final-subtitle {
    font-size: 0.95rem;
  }

  .cta-final-buttons {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .btn-cta-primary,
  .btn-cta-secondary {
    width: 100%;
    max-width: 280px;
    text-align: center;
    padding: 10px 20px;
    font-size: 0.95rem;
  }

  .cta-final-note {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 70px 0.75rem 30px 0.75rem;
  }

  .hero-title {
    font-size: 1.5rem;
  }

  .hero-subtitle {
    font-size: 0.85rem;
  }

  .hero-badge {
    font-size: 0.75rem;
    padding: 0.4rem 0.8rem;
  }

  .btn-primary,
  .btn-secondary {
    padding: 8px 16px;
    font-size: 0.85rem;
  }

  .trust-section {
    padding: 1rem 0.5rem;
  }

  .trust-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.4rem;
  }

  .trust-item {
    flex-direction: column;
    gap: 0.4rem;
    padding: 0.6rem 0.4rem;
  }

  .trust-icon {
    font-size: 1.25rem;
  }

  .trust-number {
    font-size: 1rem;
  }

  .trust-label {
    font-size: 0.65rem;
    text-align: center;
    line-height: 1.2;
  }

  .section-container {
    padding: 1.25rem 0.75rem;
  }

  .section-title {
    font-size: 1.2rem;
  }

  .section-subtitle {
    font-size: 0.8rem;
  }

  .feature-card,
  .methodologie-card,
  .process-card {
    padding: 1rem;
  }

  .feature-icon,
  .methodologie-icon,
  .process-icon {
    font-size: 1.75rem;
    margin-bottom: 0.6rem;
  }

  .feature-title,
  .methodologie-title,
  .process-title {
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
  }

  .feature-desc,
  .methodologie-desc,
  .process-desc {
    font-size: 0.8rem;
    line-height: 1.5;
  }

  .methodologie-intro {
    font-size: 0.9rem;
    margin-bottom: 1.25rem;
    line-height: 1.6;
  }

  .professeur-card {
    padding: 1rem;
  }

  .professeur-header-section {
    gap: 0.75rem;
    padding-bottom: 1.25rem;
    margin-bottom: 1.25rem;
  }

  .professeur-image-wrapper {
    width: 70px;
    height: 70px;
  }

  .professeur-name {
    font-size: 1.2rem;
    margin-bottom: 0.2rem;
  }

  .professeur-role {
    font-size: 0.8rem;
  }

  .professeur-badge {
    font-size: 0.6rem;
    padding: 0.25rem 0.5rem;
  }

  .professeur-specialties {
    gap: 0.4rem;
    margin-bottom: 0.9rem;
  }

  .specialty-tag {
    font-size: 0.7rem;
    padding: 0.3rem 0.6rem;
  }

  .professeur-description {
    font-size: 0.8rem;
    margin-bottom: 1rem;
  }

  .description-title {
    font-size: 1rem;
    margin-bottom: 0.6rem;
  }

  .professeur-highlights {
    gap: 0.6rem;
    margin-bottom: 1rem;
  }

  .highlight-item {
    padding: 0.5rem;
    gap: 0.4rem;
  }

  .highlight-icon {
    font-size: 1.1rem;
  }

  .highlight-text {
    font-size: 0.7rem;
  }

  .professeur-verification {
    margin-top: 1rem;
    padding-top: 1rem;
  }

  .verification-text {
    font-size: 0.75rem;
    margin-bottom: 0.65rem;
  }

  .professeur-social-links {
    gap: 0.65rem;
  }

  .social-link {
    font-size: 0.75rem;
    padding: 0.5rem 0.8rem;
  }

  .cta-final-container {
    padding: 0.75rem 0.75rem;
  }

  .cta-final-subtitle {
    font-size: 0.85rem;
  }

  .btn-cta-primary,
  .btn-cta-secondary {
    padding: 8px 16px;
    font-size: 0.85rem;
  }

  .cta-final-note {
    font-size: 0.8rem;
  }
}
</style>
