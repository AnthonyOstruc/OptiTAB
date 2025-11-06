<template>
  <MainLayout>
    <div class="cours-particuliers-page">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">
            Cours particuliers
            <span class="gradient-text">professionnels</span>
          </h1>
          <p class="hero-subtitle">
            Enseignement individuel dispensé par des professeurs qualifiés.
            Méthodes pédagogiques structurées et évaluation continue des acquis.
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">95%</span>
              <span class="stat-label">Taux de réussite</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">15+</span>
              <span class="stat-label">Années d'expérience</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">1:1</span>
              <span class="stat-label">Ratio professeur/élève</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Professeurs Section -->
      <div class="professeurs-section">
        <div class="container">
          <div class="section-intro">
            <h2 class="section-title">Nos Professeurs Experts</h2>
            <p class="section-subtitle">
              Enseignants qualifiés et passionnés, dédiés à votre réussite
            </p>
          </div>
          <div class="professeurs-grid">
            <!-- Professeur 1 - Anthony -->
            <div class="professeur-card">
              <div class="professeur-image">
                <img src="/images/professeurs/anthony.jpg" alt="Anthony - Professeur de Mathématiques" />
                <div class="professeur-badge">Fondateur</div>
              </div>
              <div class="professeur-info">
                <h3 class="professeur-nom">Anthony</h3>
                <p class="professeur-specialite">Mathématiques, Physique & Informatique</p>
                <div class="professeur-diplomes">
                  <span class="diplome-item">🎓 Grande École d'Ingénieur</span>
                  <span class="diplome-item">📚 15+ ans d'expérience</span>
                </div>
                <p class="professeur-bio">
                  Passionné par l'enseignement des sciences, je crois que chaque élève peut réussir avec la bonne méthode et un accompagnement personnalisé.
                </p>
                <div class="professeur-stats">
                  <div class="stat">
                    <span class="stat-number">500+</span>
                    <span class="stat-label">Élèves accompagnés</span>
                  </div>
                  <div class="stat">
                    <span class="stat-number">95%</span>
                    <span class="stat-label">Taux de réussite</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Professeur 2 - Placeholder pour un autre prof -->
            <div class="professeur-card coming-soon">
              <div class="professeur-image placeholder">
                <div class="placeholder-icon">👨‍🏫</div>
              </div>
              <div class="professeur-info">
                <h3 class="professeur-nom">Bientôt disponible</h3>
                <p class="professeur-specialite">Nous agrandissons notre équipe</p>
                <p class="professeur-bio">
                  Vous êtes un enseignant passionné ? Rejoignez notre équipe et aidez des centaines d'élèves à réussir.
                </p>
                <router-link to="/contact" class="join-team-btn">
                  Rejoindre l'équipe
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- CTA Section -->
      <div class="cta-section">
        <div class="cta-card">
          <div class="cta-content">
            <h3 class="cta-title">Consultation pédagogique</h3>
            <p class="cta-text">
              Entretien d'évaluation gratuit pour définir les objectifs d'apprentissage.
              Élaboration d'un plan de formation adapté aux besoins identifiés.
            </p>
            <div class="cta-buttons">
              <router-link to="/contact" class="cta-button primary">
                Demander un entretien
              </router-link>
              <a href="mailto:contact@optitab.com" class="cta-button secondary">
                Contacter nos services
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Bouton WhatsApp flottant -->
    <WhatsappChatButton
      phone="33764040251"
      message="Bonjour, j'ai une question sur les cours particuliers OptiTAB !"
      tooltip="Une question ? Discutons sur WhatsApp !"
    />
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
import WhatsappChatButton from '@/components/home/WhatsappChatButton.vue'
</script>

<style scoped>
/* Page Container */
.cours-particuliers-page {
  min-height: 100vh;
  background: #ffffff;
}

/* Hero Section */
.hero-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 2rem;
  padding-top: calc(4rem + 60px); /* 60px pour compenser le header fixe */
  margin-top: 0;
}

.hero-content {
  width: 100%;
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
  font-size: 3rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: #475569;
  line-height: 1.7;
  margin-bottom: 3rem;
  max-width: 650px;
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
  font-size: 2.5rem;
  font-weight: 800;
  color: #2a38b7;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 600;
}


/* Professeurs Section */
.professeurs-section {
  background: #f8f9fa;
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
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 1rem;
  letter-spacing: -0.01em;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #475569;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.professeurs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.professeur-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.professeur-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.12);
  border-color: rgba(42, 56, 183, 0.2);
}

.professeur-image {
  position: relative;
  width: 100%;
  height: 350px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.professeur-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center center;
  background: #ffffff;
}

.professeur-image.placeholder {
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 350px;
  width: 100%;
}

.placeholder-icon {
  font-size: 7rem;
  opacity: 0.7;
}

.professeur-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(42, 56, 183, 0.3);
}

.professeur-info {
  padding: 2rem;
}

.professeur-nom {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.professeur-specialite {
  font-size: 1rem;
  color: #2a38b7;
  font-weight: 600;
  margin-bottom: 1rem;
}

.professeur-diplomes {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

.diplome-item {
  background: #f1f5f9;
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #475569;
  font-weight: 600;
}

.professeur-bio {
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.professeur-stats {
  display: flex;
  gap: 2rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f1f5f9;
}

.professeur-stats .stat {
  text-align: center;
}

.professeur-stats .stat-number {
  display: block;
  font-size: 1.75rem;
  font-weight: 800;
  color: #2a38b7;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.professeur-stats .stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.professeur-card.coming-soon {
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 2px dashed #cbd5e1;
  background: #ffffff;
}

.professeur-card.coming-soon .professeur-info {
  text-align: center;
}

.join-team-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 700;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(42, 56, 183, 0.3);
}

.join-team-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(42, 56, 183, 0.4);
}

/* Tarifs Section */
.tarifs-section {
  background: #ffffff;
  padding: 4rem 0;
}

.tarifs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.tarif-card {
  background: #f8f9fa;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: none;
  border: 2px solid transparent;
  position: relative;
  transition: all 0.3s ease;
}

.tarif-card:hover {
  transform: translateY(-4px);
  background: #ffffff;
  border-color: rgba(42, 56, 183, 0.15);
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.1);
}

.tarif-card.featured {
  background: #ffffff;
  border: 2px solid #2a38b7;
  transform: scale(1);
  box-shadow: 0 4px 20px rgba(42, 56, 183, 0.15);
}

.tarif-header {
  text-align: center;
  margin-bottom: 2rem;
}

.tarif-header h3 {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.75rem;
}

.tarif-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.price {
  font-size: 2.75rem;
  font-weight: 900;
  color: #2a38b7;
}

.period {
  font-size: 1rem;
  color: #64748b;
  font-weight: 600;
}

.popular-badge {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 4px 12px rgba(42, 56, 183, 0.3);
}

.tarif-features {
  margin-bottom: 2rem;
}

.feature {
  display: block;
  margin-bottom: 0.75rem;
  color: #475569;
  font-weight: 500;
  font-size: 0.95rem;
  line-height: 1.5;
}

.tarif-button {
  width: 100%;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  border: 2px solid #2a38b7;
  background: transparent;
  color: #2a38b7;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tarif-button.primary {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  border-color: transparent;
}

.tarif-button.primary:hover {
  box-shadow: 0 6px 20px rgba(42, 56, 183, 0.4);
  transform: translateY(-2px);
}

.tarif-button:hover {
  background: #2a38b7;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(42, 56, 183, 0.3);
}

/* CTA Section */
.cta-section {
  background: #ffffff;
  padding: 3rem 2vw;
  margin-top: 0;
  width: 100%;
  text-align: center;
}

.cta-card {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 1rem;
  letter-spacing: -0.01em;
}

.cta-text {
  font-size: 1.05rem;
  color: #475569;
  line-height: 1.7;
  margin-bottom: 2rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
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
  font-size: 1.05rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.cta-button.primary {
  background: linear-gradient(135deg, #2a38b7 0%, #667eea 100%);
  color: #fff;
  box-shadow: 0 4px 16px rgba(42, 56, 183, 0.3);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(42, 56, 183, 0.4);
}

.cta-button.secondary {
  background: transparent;
  color: #2a38b7;
  border-color: #2a38b7;
}

.cta-button.secondary:hover {
  background: #2a38b7;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(42, 56, 183, 0.3);
}

.button-icon {
  width: 1.2rem;
  height: 1.2rem;
  filter: none;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-section {
    padding: 3rem 1.5rem;
    padding-top: calc(3rem + 60px); /* 60px pour compenser le header fixe */
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .hero-stats {
    gap: 2rem;
  }

  .avantages-section {
    padding: 3rem 0;
    margin: 1.5rem 0;
  }

  .container {
    padding: 0 1.5rem;
  }

  .section-intro {
    margin-bottom: 2.5rem;
  }

  .section-title {
    font-size: 2.2rem;
  }

  .section-subtitle {
    font-size: 1.1rem;
  }

  .avantages-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    max-width: 600px;
  }

  .tarifs-section {
    padding: 3rem 0;
  }

  .tarifs-grid {
    gap: 1.5rem;
    margin-top: 2.5rem;
  }

  .cta-section {
    padding: 2.5rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 1.25rem;
    padding-top: calc(2rem + 60px); /* 60px pour compenser le header fixe */
  }

  .hero-title {
    font-size: 1.75rem;
    line-height: 1.3;
    margin-bottom: 1rem;
  }

  .hero-subtitle {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 2rem;
    padding: 0 0.5rem;
  }

  .hero-stats {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 1.5rem;
  }

  .stat-item {
    flex: 0 1 calc(33.333% - 1rem);
    min-width: 80px;
  }

  .stat-number {
    font-size: 1.8rem;
    margin-bottom: 0.25rem;
  }

  .stat-label {
    font-size: 0.85rem;
    line-height: 1.3;
  }

  .avantages-section {
    padding: 2.5rem 0;
    margin: 1.5rem 0;
  }

  .container {
    padding: 0 1.25rem;
  }

  .section-intro {
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
    margin-bottom: 0.875rem;
  }

  .section-subtitle {
    font-size: 1.05rem;
    padding: 0 0.5rem;
  }

  .avantages-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
    max-width: 100%;
  }

  .avantage-card {
    padding: 1.5rem;
    border-radius: 12px;
  }

  .avantage-icon {
    width: 70px;
    height: 70px;
    margin-bottom: 1rem;
  }

  .avantage-icon .icon {
    width: 4rem;
    height: 4rem;
  }

  .avantage-card h3 {
    font-size: 1.15rem;
    margin-bottom: 0.75rem;
  }

  .avantage-card p {
    font-size: 0.95rem;
    line-height: 1.5;
  }

  .tarifs-section {
    padding: 2.5rem 0;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .tarifs-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
    margin-top: 2rem;
  }

  .tarif-card {
    padding: 1.5rem;
    border-radius: 16px;
  }

  .tarif-card.featured {
    transform: none;
    border-width: 2px;
  }

  .tarif-header h3 {
    font-size: 1.3rem;
    margin-bottom: 0.875rem;
  }

  .price {
    font-size: 2rem;
  }

  .period {
    font-size: 0.9rem;
  }

  .popular-badge {
    font-size: 0.75rem;
    padding: 0.2rem 0.625rem;
  }

  .tarif-features {
    margin-bottom: 1.5rem;
  }

  .feature {
    font-size: 0.9rem;
    margin-bottom: 0.625rem;
  }

  .tarif-button {
    padding: 0.875rem;
    font-size: 0.95rem;
  }

  .cta-section {
    padding: 2.5rem 1.25rem;
    border-radius: 10px;
    margin: 2rem auto 0;
    max-width: 800px;
  }

  .cta-title {
    font-size: 1.75rem;
    line-height: 1.3;
    margin-bottom: 0.875rem;
  }

  .cta-text {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 2rem;
    padding: 0 0.5rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
    gap: 0.875rem;
    margin-bottom: 0;
  }

  .cta-button {
    width: 100%;
    max-width: 100%;
    padding: 0.875rem 1.5rem;
    font-size: 1rem;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 1.5rem 1rem;
    padding-top: calc(1.5rem + 60px); /* 60px pour compenser le header fixe */
  }

  .hero-title {
    font-size: 1.5rem;
    margin-bottom: 0.875rem;
  }

  .hero-subtitle {
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    padding: 0;
  }

  .hero-stats {
    gap: 1rem;
    margin-top: 1.25rem;
  }

  .stat-item {
    flex: 1;
    min-width: 70px;
  }

  .stat-number {
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
  }

  .stat-label {
    font-size: 0.8rem;
  }

  .avantages-section {
    padding: 2rem 0;
    margin: 1rem 0;
  }

  .container {
    padding: 0 1rem;
  }

  .section-intro {
    margin-bottom: 1.5rem;
  }

  .section-title {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
  }

  .section-subtitle {
    font-size: 1rem;
    padding: 0;
  }

  .avantages-grid {
    gap: 1rem;
  }

  .avantage-card {
    padding: 1.25rem;
    border-radius: 10px;
  }

  .avantage-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 0.875rem;
  }

  .avantage-icon .icon {
    width: 3.5rem;
    height: 3.5rem;
  }

  .avantage-card h3 {
    font-size: 1.1rem;
    margin-bottom: 0.625rem;
  }

  .avantage-card p {
    font-size: 0.9rem;
  }

  .tarifs-section {
    padding: 2rem 0;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .tarifs-grid {
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .tarif-card {
    padding: 1.25rem;
    border-radius: 12px;
  }

  .tarif-header h3 {
    font-size: 1.2rem;
    margin-bottom: 0.75rem;
  }

  .price {
    font-size: 1.75rem;
  }

  .period {
    font-size: 0.85rem;
  }

  .popular-badge {
    font-size: 0.7rem;
    padding: 0.15rem 0.5rem;
  }

  .tarif-features {
    margin-bottom: 1.25rem;
  }

  .feature {
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
  }

  .tarif-button {
    padding: 0.75rem;
    font-size: 0.9rem;
  }

  .cta-section {
    padding: 2rem 1rem;
    border-radius: 8px;
  }

  .cta-title {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
  }

  .cta-text {
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    padding: 0;
  }

  .cta-button {
    padding: 0.875rem 1.25rem;
    font-size: 0.95rem;
  }
}
</style>
